from __future__ import annotations

from typing import TYPE_CHECKING

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

if TYPE_CHECKING:
    from config import Config


def load_browser(config: Config) -> webdriver:
    """Loads headless Chrome driver."""
    options = Options()
    options.page_load_strategy = "normal"
    options.add_argument("--headless=new")

    if config.chromedriver_path:
        s = Service(str(config.chromedriver_path))
        return webdriver.Chrome(service=s, options=options)
    else:
        return webdriver.Chrome(options=options)


def get_cookies(browser_: webdriver) -> dict:
    """Returns session cookies."""
    cookies = browser_.get_cookies()
    return {c["name"]: c["value"] for c in cookies}
