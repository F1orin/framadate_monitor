import logging

from enum import StrEnum
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

log = logging.getLogger(__name__)


class Vote(StrEnum):
    """Represents possible responses/votes to a Framadate poll."""
    YES = "Yes"
    NO = "No"
    IF_NEEDED = "If needed"


class PlayerNotFoundError(LookupError):
    """Raised when the player's response row is not found in the Framadate table."""


class PollInterfaceError(RuntimeError):
    """Raised when the Framadate interface cannot be loaded or interpreted."""


def check_player_has_unmarked_days(framadate_url, player_name) -> bool:
    """
    Check whether a player has any unanswered dates in a Framadate poll.

    Returns:
        True when at least one answer cell is empty, otherwise False.

    Uses Selenium WebDriver to interact with the Framadate web interface and analyze poll results.
    """
    log.debug('check_player_has_unmarked_days called')

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    try:
        with webdriver.Chrome(options=opts) as driver:
            driver.get(framadate_url)
            wait = WebDriverWait(driver, 10)

            table = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#poll table.proposals-table")
            ))
            log.debug("Table found")

            rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")

            target_row = None
            for row in rows:
                author = row.find_element(
                    By.CSS_SELECTOR,
                    "th[scope='row'] .proposals-table__author",
                ).text.strip()
                log.debug("Player found: %s", author)

                if author == player_name:
                    target_row = row
                    break

            if not target_row:
                raise PlayerNotFoundError(
                    f"Player '{player_name}' not found")

            cells = target_row.find_elements(By.CSS_SELECTOR, "td")
            for cell in cells:
                votes = cell.find_elements(By.CSS_SELECTOR, ".vote")
                if not votes:
                    log.debug("Unanswered date found")
                    return True

                value = votes[0].find_element(
                    By.CSS_SELECTOR, ".sr-only"
                ).get_attribute("textContent").strip()
                try:
                    vote = Vote(value)
                except ValueError as error:
                    raise PollInterfaceError(
                        f"Unexpected vote label in Framadate poll: '{value}'"
                    ) from error
                log.debug("Answer found: %s", vote)
    except (PlayerNotFoundError, PollInterfaceError):
        raise
    except TimeoutException as error:
        raise PollInterfaceError(
            "Timed out waiting for the Framadate poll interface"
        ) from error
    except WebDriverException as error:
        raise PollInterfaceError(
            "Could not read the Framadate poll interface"
        ) from error

    return False
