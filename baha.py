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
        logger.info(page.text_content("#signin-btn")[9:])
        page.click("#signin-btn")
        logger.info(page.text_content(".popup-dailybox__subtitle > p:nth-child(1)"))
        page.goto("https://fuli.gamer.com.tw/")
        logger.info(
            page.locator("//html/body/div[6]/div/div[3]/h5[1]").text_content()
            + page.text_content("#forum-lastBoard").strip()
        )
        browser.close()


if __name__ == "__main__":
    username, password = getenv(BAHA_USERNAME_ENV), getenv(BAHA_PASSWORD_ENV)
    login(username, password)
