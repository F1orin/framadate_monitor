import logging
import os

from enum import IntEnum
from enum import StrEnum
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

log = logging.getLogger(__name__)


class Vote(StrEnum):
    YES = "Yes"
    NO = "No"
    UNDER_RESERVE = "Under reserve"
    I_DONT_KNOW = "I don’t know"  # curly apostrophe on purpose


class VoteStatus(IntEnum):
    HAS_UNMARKED = 1
    ALL_MARKED = 0
    PLAYER_NOT_FOUND = -1


def check_player_has_unmarked_days():
    log.debug('user_has_unmarked_days called')

    framadate_url = os.environ["FRAMADATE_URL"]
    player_name = os.environ["PLAYER_NAME"]

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    with webdriver.Chrome(options=opts) as driver:
        driver.get(framadate_url)
        wait = WebDriverWait(driver, 10)

        table = wait.until(EC.presence_of_element_located((By.ID, "results2")))
        log.debug("Table found")

        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")

        target_row = None
        for r in rows:
            title = r.get_attribute("title")
            log.debug(f"Title found: {title}")

            if title == player_name:
                target_row = r
                break

        if not target_row:
            return VoteStatus.PLAYER_NOT_FOUND

        cells = target_row.find_elements(By.CSS_SELECTOR, "td")
        for c in cells:
            span = c.find_element(By.CSS_SELECTOR, "span.sr-only")
            value = span.get_attribute("textContent")
            log.debug(f"Answer found: {value}")

            if value == Vote.I_DONT_KNOW:
                return VoteStatus.HAS_UNMARKED

    return VoteStatus.ALL_MARKED
