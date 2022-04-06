from os import getenv

from loguru import logger
from playwright.sync_api import sync_playwright

BAHA_USERNAME_ENV = "BAHA_USERNAME"
BAHA_PASSWORD_ENV = "BAHA_PASSWORD"


def login(username: str, password: str):
    if not username or not password:
        raise ValueError("BAHA_USERNAME or BAHA_PASSWORD is empty")

    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()
        page.goto("https://user.gamer.com.tw/login.php")
        page.fill("#form-login > input:nth-child(1)", username)
        page.fill(".password-box > input:nth-child(1)", password)
        page.click("#btn-login")
        page.wait_for_selector("#signin-btn > i:nth-child(1)")
        logger.info(page.text_content("#signin-btn"))
        browser.close()


if __name__ == "__main__":
    username, password = getenv(BAHA_USERNAME_ENV), getenv(BAHA_PASSWORD_ENV)
    login(username, password)
