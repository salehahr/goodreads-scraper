from __future__ import annotations

import re
from typing import TYPE_CHECKING

from requests.adapters import HTTPAdapter, Retry
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from .browser import get_cookies, load_browser

if TYPE_CHECKING:
    from pathlib import Path

    from requests import Session
    from selenium import webdriver

    from config import Config


def get_auth(filepath: Path) -> dict:
    """Obtains login data from local csv file."""
    with open(filepath, "r") as file:
        text = file.read().strip()
        username, password = text.split(",")
    return {
        "email": username,
        "password": password,
    }


def sign_in(config: Config, session: Session) -> None:
    """
    Logs in to Goodreads using Selenium.
    Initialises session and updates user id in config.
    """
    browser = load_browser(config)
    init_session(session, browser)

    # find login page
    browser.get(f"https://www.goodreads.com/user/sign_in?source=home")
    browser.find_element(By.CLASS_NAME, "authPortalSignInButton").click()

    # fill in form
    for k, v in config.login.dict().items():
        element = browser.find_element(By.NAME, k)
        element.send_keys(v)
    browser.find_element(By.ID, "signInSubmit").click()

    try:
        shelf_link = browser.find_element(By.LINK_TEXT, "My Books").get_attribute(
            "href"
        )
    except NoSuchElementException as e:
        print("CAPTCHA request.")
        raise e

    config.user_id = int(re.search(f"\d+", shelf_link).group(0))

    session.cookies.update(get_cookies(browser))


def init_session(session: Session, browser: webdriver) -> None:
    """Sets retry param and agent for the current session."""
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount("http://", HTTPAdapter(max_retries=retries))

    agent = browser.execute_script("return navigator.userAgent;")
    session.headers.update({"user-agent": agent})
