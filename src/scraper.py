import logging
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

log = logging.getLogger(__name__)


def check_user_has_unmarked_days():
    log.debug('user_has_unmarked_days called')

    framadate_url = os.environ["FRAMADATE_URL"]

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    with webdriver.Chrome(options=opts) as driver:
        driver.get(framadate_url)
        wait = WebDriverWait(driver, 10)

        table = wait.until(EC.presence_of_element_located((By.ID, "results2")))
        log.debug('table found')

    return False
