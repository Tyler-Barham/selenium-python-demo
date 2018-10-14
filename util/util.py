#! /usr/bin/env python3

import sys
import time
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, MoveTargetOutOfBoundsException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

#Global varibles
_browser = webdriver.Firefox() # Instance of the firefox driver
_timeout = 10 # How long to wait for an element before timeouts
_test_pass_count = 0 # Counter for the number of passed tests
_test_fail_count = 0 # Counter for the number of failed tests
_start_time = time.time() # To keep track of how long the tests took

def assert_url_contains(text):
    '''Checks if the given text is contained within the URL

    Parameters:
        text: The URL substring to check for (string)
    
    Return:
        If the text was within the URL (boolean)
    '''

    try:
        global _timeout
        wait = WebDriverWait(_browser, _timeout)
        wait.until(EC.url_contains(text))
        return True
    except Exception:
        return False

def change_dropdown_selection(dropdown_id, option):
    '''Select the option for a given dropdown

    Parameters:
        dropdown_id: The id of the dropdown (string)
        option: The option within the dropdown to select (string)
    '''

    # Get item
    select_elem = return_when_visible(By.NAME, dropdown_id)

    # Move to it and click (to expand it)
    actions = ActionChains(_browser)
    actions.move_to_element(select_elem).click().perform()

    # Cast to a select
    select = Select(select_elem)

    # When options can be seen, select the correct one
    return_when_visible(By.XPATH, "//option[contains(text(), '{}')]".format(option))
    for opt in select.options:
        if option in opt.text:
            opt.click()
            break

def finish_executing():
    '''Called when finished running all tests'''

    # Output relevant test data
    print()
    print("Passed: {}".format(_test_pass_count))
    print("Failed: {}".format(_test_fail_count))
    print()
    print("{} tests took {}s".format(_test_pass_count + _test_fail_count, time.time() - _start_time))

    # Close the browser
    _browser.quit()

def return_when_visible(search_type, search_value, text=None):
    '''Searches for the element and returns it once found
    
    Parameters:
        search_type: How to search for the element (selenium.webdriver.common.By)
        search_value: The value of the search (string)
        text(optional): Text to be contained within the searched element (string)
    
    Return:
        The found element (WebElement)
    
    Raises:
        TimeoutException: If the element could not be found
    '''

    try:
        # Get the element if it's present
        element_present = EC.visibility_of_any_elements_located((search_type, search_value))

        # Checks if we should be waiting to text to appear in the element (only works for single items such as ID searches, not classes)
        if text is not None:
            element_present = EC.text_to_be_present_in_element((search_type, search_value), text)

        # Wait until element/text is present
        global _timeout
        WebDriverWait(_browser, _timeout).until(element_present)

        # Return the searched for element
        elem = _browser.find_element(by=search_type, value=search_value)
        actions = ActionChains(_browser)
        actions.move_to_element(elem).perform()
        return elem

    except TimeoutException:
        # if the element cannot be found within a given time, pass the exception to main
        if text is None:
            raise Exception("Timed out while waiting for {}={}".format(search_type, search_value)) from TimeoutException
        else:
            raise Exception("Timed out while waiting for {}={} to contain {}".format(search_type, search_value, text)) from TimeoutException

    except MoveTargetOutOfBoundsException:
        # If the target was out of the view, scroll to it then return it
        scroll_to(elem)
        return elem

def scroll_through_list(ul_id):
    '''Will scroll through every li element in a ul list
    
    Parameters:
        ul_id: The id of the ul element (string)
    '''

    # Find the ul list
    list_elem = return_when_visible(By.ID, ul_id)
    # Get all li items within the ul
    list_items = list_elem.find_elements_by_tag_name("li")

    # Scroll to each item
    for item in list_items:
        scroll_to(item)

def scroll_to(elem):
    '''A helper function to scroll the element into view
    
    Parameters:
        elem: The element to scroll to (WebElement)
    '''

    coordinates = elem.location_once_scrolled_into_view
    _browser.execute_script('window.scrollTo({}, {});'.format(coordinates['x'], coordinates['y']))

def set_display_size(size):
    '''Helper function that changes the window size
    
    Parameters:
        size: Possible values - xs, sm, md, lg, xl (string)
    
    Raises:
        ValueError: If size was an incorrect option
    '''

    # For a given size, set the window
    if size == "xs":
        _browser.set_window_size(375, 1000)
    elif size == "sm":
        _browser.set_window_size(512, 1000)
    elif size == "md":
        _browser.set_window_size(768, 1000)
    elif size == "lg":
        _browser.set_window_size(1024, 1000)
    elif size == "xl":
        _browser.set_window_size(1366, 1000)
    else:
        raise ValueError("Did not select a valid size. Attempted to use {}".format(size))

    print("==================Testing {} window size===================".format(size))

def setup(test_desc):
    '''Called before running each test to ensure a clean state
    
    Parameters:
        test_desc: A description of the test that will be printed (string)
    '''

    print(test_desc)
    # Go to the trademe home page
    _browser.get("https://preview.trademe.co.nz")

    # Click on trademe motors
    motors_tab = return_when_visible(By.XPATH, "//a[@href='/motors']")
    motors_tab.click()

def signal_handler(sig, frame):
    '''A hanlder for capturing signals'''
    print
    sys.exit(0)

def test_passed(is_pass):
    '''A helper function for test results

    Parameters:
        is_pass: Whether or not the test passed (boolean)
    '''

    # Check if the test passed or not
    if is_pass:
        global _test_pass_count
        _test_pass_count += 1
        print("Test result: Passed")
    else:
        global _test_fail_count
        _test_fail_count += 1
        print("Test result: Failed")

    print("")
