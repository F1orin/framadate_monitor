"""Interface and scraper regressions; no live poll or email needed."""

import unittest
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from src.scraper import PlayerNotFoundError, check_player_has_unmarked_days


POLL_URL = (Path(__file__).parent / "fixtures" / "new_poll.html").resolve().as_uri()


class NewInterfaceStructureTests(unittest.TestCase):
    """Document the DOM contract observed in the new interface.

    These characterize the fixture. The regression tests below exercise the
    production scraper against it.
    """

    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(options=options)
        cls.addClassCleanup(cls.driver.quit)
        cls.driver.get(POLL_URL)

    def test_poll_has_date_headers(self):
        tables = self.driver.find_elements(By.CSS_SELECTOR, "#poll table.proposals-table")
        self.assertEqual(len(tables), 1)
        headers = tables[0].find_elements(By.CSS_SELECTOR, "thead th[scope='col']")
        self.assertEqual(
            [header.get_attribute("title") for header in headers],
            [
                "Sun 27 Sept 2026 : 12h30",
                "Sun 4 Oct 2026 : 12h30",
                "Sun 11 Oct 2026 : 12h30",
                "Sun 18 Oct 2026 : 12h30",
            ],
        )
        self.assertEqual(
            [
                header.find_element(
                    By.CSS_SELECTOR, ".proposal__label"
                ).get_attribute("textContent").strip()
                for header in headers
            ],
            ["12h30"] * 4,
        )

    def test_fixture_has_no_links_forms_or_external_identifiers(self):
        unsafe_elements = self.driver.find_elements(
            By.CSS_SELECTOR,
            "a, form, input, button, [href], [src], [action], "
            "[data-url], [data-proposal-id]",
        )
        self.assertEqual(unsafe_elements, [])

    def test_participant_names_are_in_row_headers(self):
        authors = self.driver.find_elements(
            By.CSS_SELECTOR, "table.proposals-table tbody th[scope='row'] .proposals-table__author"
        )
        self.assertEqual([author.text.strip() for author in authors],
                         ["Unanswered Player", "Answered Player"])

    def test_each_participant_has_one_answer_cell_per_date(self):
        rows = self.driver.find_elements(By.CSS_SELECTOR, "table.proposals-table tbody tr")
        self.assertEqual(len(rows), 2)
        for row in rows:
            with self.subTest(participant=row.text):
                self.assertEqual(len(row.find_elements(By.CSS_SELECTOR, "td")), 4)

    def test_answered_votes_have_labels_and_unanswered_cells_are_empty(self):
        rows = self.driver.find_elements(By.CSS_SELECTOR, "table.proposals-table tbody tr")
        labels = rows[1].find_elements(By.CSS_SELECTOR, "td .vote .sr-only")
        self.assertEqual([label.get_attribute("textContent").strip() for label in labels],
                         ["No", "Yes", "If needed", "Yes"])
        for cell in rows[0].find_elements(By.CSS_SELECTOR, "td")[1:]:
            self.assertEqual(cell.get_attribute("textContent").strip(), "")
            self.assertEqual(cell.find_elements(By.CSS_SELECTOR, ".vote"), [])


class NewInterfaceScraperTests(unittest.TestCase):
    def test_all_three_vote_choices_count_as_answered(self):
        self.assertIs(check_player_has_unmarked_days(POLL_URL, "Answered Player"), False)

    def test_empty_answer_cell_counts_as_unanswered(self):
        self.assertIs(check_player_has_unmarked_days(POLL_URL, "Unanswered Player"), True)

    def test_missing_participant_raises_player_not_found(self):
        with self.assertRaises(PlayerNotFoundError):
            check_player_has_unmarked_days(POLL_URL, "Missing Player")


if __name__ == "__main__":
    unittest.main()
