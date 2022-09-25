from __future__ import annotations

from typing import TYPE_CHECKING

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

if TYPE_CHECKING:
    from requests import Session


def load_browser() -> webdriver:
    """Loads headless Chrome driver."""
    options = Options()
    options.page_load_strategy = "normal"
    options.headless = True
    return webdriver.Chrome(options=options)


def get_cookies(browser_: webdriver) -> dict:
    """Returns session cookies."""
    cookies = browser_.get_cookies()
    return {c["name"]: c["value"] for c in cookies}


def get_soup(url: str, session: Session) -> BeautifulSoup:
    """Generates response and soup of current page."""
    response = session.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    return soup
