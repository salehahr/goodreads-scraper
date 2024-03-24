from __future__ import annotations

import re
from typing import TYPE_CHECKING, List

from .browser import get_soup

from .book import Book

if TYPE_CHECKING:
    from bs4 import BeautifulSoup
    from bs4.element import Tag
    from config import Config
    from requests import Session


def clean_field_value(field_tag: Tag) -> str:
    """Returns cleaned string value of field."""
    field_value = field_tag.find("a").text.strip()
    field_value = field_value.split("\n")[0]
    return field_value


class Shelf(object):
    """Collection of Books."""

    def __init__(self, config: Config):
        self._user_id: int = config.user_id
        self._name: str = config.shelf
        self._url: str = f"https://www.goodreads.com/review/list/{self._user_id}?shelf={self._name}&per_page=100"

        self._books: List[Book] = []

    def __iter__(self) -> Book:
        for book in self._books:
            yield book

    def __len__(self) -> int:
        return len(self._books)

    def populate(self, session: Session):
        """Populates the shelf with books."""
        soup = get_soup(self._url, session)
        num_books = int(re.search(f"(\d+) books", soup.find("title").text).group(1))

        page = 0
        while len(self) < num_books:
            page += 1
            if page > 1:
                soup = get_soup(self._next_url(page), session)

            titles = [
                clean_field_value(title)
                for title in soup.find_all("td", {"class": "field title"})
            ]
            authors = [
                clean_field_value(author)
                for author in soup.find_all("td", {"class": "field author"})
            ]
            self._add(titles, authors)

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

    def _next_url(self, page) -> str:
        return f"{self._url}&page={page}"
