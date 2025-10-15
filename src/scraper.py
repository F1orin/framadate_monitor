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
    """Represents possible responses/votes to a Framadate poll."""
    YES = "Yes"
    NO = "No"
    UNDER_RESERVE = "Under reserve"
    I_DONT_KNOW = "I don’t know"  # curly apostrophe on purpose


class PlayerNotFoundError(LookupError):
    """Raised when the player's response row is not found in the Framadate table."""


def check_player_has_unmarked_days() -> bool:
    """
    Checks the Framadate poll to determine if a player has any unmarked (i.e., "I don't know") days.

    Returns:
        VoteStatus: See `VoteStatus` class documentation for descriptions of the returned values.

    Reads environment variables:
        FRAMADATE_URL: URL of the Framadate poll.
        PLAYER_NAME: Name of the player to search for.

    Uses Selenium WebDriver to interact with the Framadate web interface and analyze poll results.
    """
    log.debug('check_player_has_unmarked_days called')

    framadate_url = os.environ["FRAMADATE_URL"]
    player_name = os.environ["PLAYER_NAME"]
    if not framadate_url or not player_name:
        raise ValueError("FRAMADATE_URL and PLAYER_NAME must be set in .env")

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
            raise PlayerNotFoundError(
                f"Player '{player_name}' not found")

        cells = target_row.find_elements(By.CSS_SELECTOR, "td")
        for c in cells:
            span = c.find_element(By.CSS_SELECTOR, "span.sr-only")
            value = span.get_attribute("textContent")
            log.debug(f"Answer found: {value}")

            if value == Vote.I_DONT_KNOW:
                return True

    return False
