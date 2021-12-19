from Const import *
import time
from os.path import isdir
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

getGecko_installed = True
try:
    from get_gecko_driver import GetGeckoDriver
except BaseException:
    getGecko_installed = False


class Scraper:

    def __init__(self, DEBUG: bool):
        self.MB_URL = "https://www.moonboard.com"
        self.DEBUG = DEBUG

        # use getGecko to get the driver
        if getGecko_installed:
            print("Getting GeckoDriver")
            get_driver = GetGeckoDriver()
            get_driver.install()

    MONTH_MAP = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "Mai": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
    }

    def fetch_data(self, USERNAME: str, PASSWORD: str) -> dict:

        # use the installed GeckoDriver with Selenium
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.headless = not self.DEBUG
        driver = webdriver.Firefox(options=fireFoxOptions)

        driver.get(self.MB_URL)

        # login
        driver.find_element_by_id("loginDropdown").click()
        driver.find_element_by_id("Login_Username").send_keys(USERNAME)
        driver.find_element_by_id("Login_Password").send_keys(PASSWORD)
        driver.find_element_by_id("navlogin").click()

        time.sleep(10)  # TODO: await properly

        # navigate to logbook
        driver.find_element_by_id("llogbook").click()
        driver.find_element_by_link_text("VIEW").click()

        time.sleep(10)  # TODO: await properly

        # select version
        select = Select(driver.find_element_by_id("Holdsetup"))
        select.select_by_index(1)  # 2019 version TODO : more stable

        time.sleep(1)  # TODO: await properly

        main_section = driver.find_element_by_id("main-section")

        # get headers for rows
        headers = main_section.find_elements_by_class_name(
            "logbook-grid-header")

        # get a tag expanders for the various days
        expanders = driver.find_elements_by_xpath(
            "//a[@class='k-icon k-i-expand']")

        # create list of elements
        res = []
        def any_nested(list, key): return any([k == key for k, _ in list])
        for a_tag, header in zip(expanders, headers):
            a_tag.click()  # expand information

            # get all entries for that day
            entries = main_section.find_elements_by_class_name("entry")

            for entry in entries:
                # get data
                if not any_nested(res, entry.text):
                    res_entry = (entry.text, header.text)  # (route info, date)
                    res.append(res_entry)

        # process data
        formatted_data = []
        for (data, date) in res:
            data_arr = data.split('\n')
            day, month, year = date.split('\n')[0].split(' ')
            day, month, year = int(day), self.MONTH_MAP[month], int(year)

            formatted = {
                'Name': data_arr[0],
                'Setter': data_arr[1],
                'Grade': data_arr[2].split('.')[0],
                'Date': (day, month, year)
            }

            formatted_data.append(formatted)

        # cleanup
        driver.quit()

        return formatted_data
