from __future__ import annotations

import re
from typing import TYPE_CHECKING, List

from bs4 import BeautifulSoup as Soup

from .book import Book

if TYPE_CHECKING:
    from bs4.element import Tag
    from requests import Session

    from config import Config


def field_value(field_tag: Tag) -> str:
    """Returns cleaned string value of field."""
    return field_tag.find("div").text.strip().split("\n")[0]


class ShelfPage(Soup):
    """
    Represents the current webpage shown for the shelf.
    """

    def __init__(self, session: Session, base_url: str, page_num: int):
        url = base_url if page_num == 1 else f"{base_url}&page={page_num}"
        response = session.get(url)
        super().__init__(response.content, "html.parser")

        self.__session = session
        self.__base_url = base_url
        self.__page_num = page_num

        self.titles = list(
            map(field_value, self.find_all("td", {"class": "field title"}))
        )
        self.authors = list(
            map(field_value, self.find_all("td", {"class": "field author"}))
        )

    @staticmethod
    def from_session(session: Session, base_url: str, page_num: int = 1) -> ShelfPage:
        """Generates response and soup of current page."""
        return ShelfPage(session, base_url, page_num)

    def next(self) -> ShelfPage:
        """Returns the next ShelfPage."""
        new_page_num = self.__page_num + 1
        return ShelfPage.from_session(
            self.__session, self.__base_url, page_num=new_page_num
        )

    @property
    def total_books(self) -> int:
        page_title = self.find("title").text
        return int(re.search(r"(\d+) books", page_title).group(1))


class Shelf:
    """Collection of Books."""

    def __init__(self, config: Config):
        self._name: str = config.shelf
        self._url: str = (
            f"https://www.goodreads.com/review/list/{config.user_id}?shelf={self._name}&per_page=100"
        )

        self._books: List[Book] = []

    def __iter__(self) -> Book:
        for book in self._books:
            yield book

    def __len__(self) -> int:
        return len(self._books)

    def populate(self, session: Session):
        """Populates the shelf with books."""
        current_page = ShelfPage.from_session(session, self._url)
        total_books = current_page.total_books
        self._add(current_page.titles, current_page.authors)

        while len(self) < total_books:
            current_page = current_page.next()
            self._add(current_page.titles, current_page.authors)

    def _add(self, *args) -> None:
        if len(args) == 1:
            self._books.append(args[0])
        elif len(args) == 2:
            self._add_titles_and_authors(*args)
        else:
            raise TypeError

    def _add_titles_and_authors(self, titles: List[str], authors: List[str]) -> None:
        for title, author in zip(titles, authors):
            self._books.append(Book(title, author))

    def _remove(self, book: Book) -> None:
        self._books.remove(book)
