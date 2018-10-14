#! /usr/bin/env python3
import time
# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, MoveTargetOutOfBoundsException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Util imports
from util import assert_url_contains, change_dropdown_selection, return_when_visible, setup, test_passed

def test_selectbox(select_name, select_option, url_param):
    '''Changes the selectbox value and ensures that it was applied to the search
    
    Parameters:
        select_name: The id of the select element (string)
        select_option: The text of the option to select (string)
        url_param: The URL query string that should be applied (string)
    '''

    # Make sure this test is from a clean state
    setup("Ensuring that the search applies the parameter {}".format(url_param))

    # Change the dropdown option
    change_dropdown_selection(select_name, select_option)

    # Allow time for search options to update in JS
    time.sleep(1)

    # Press search
    search_button = return_when_visible(By.XPATH, "//button[@type='submit']")
    search_button.click()

    # Slight delay to see search results screen
    time.sleep(1)

    # Check if the url query string matches the search options
    test_passed(assert_url_contains(url_param))

def main():
    '''The function that runs all tests within this file'''

    # Run tests
    test_selectbox("year_min", "1980", "search?year_min=1980")
    test_selectbox("year_max", "2017", "search?year_max=2017")
    test_selectbox("price_min", "$3k", "search?price_min=3000")
    test_selectbox("price_max", "$50k", "search?price_max=50000")
