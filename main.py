#! /usr/bin/env python3

import signal
import time
import traceback

# Util imports
from util import finish_executing, set_display_size, signal_handler

# Test imports
from tests.test_motors_search_fields.test_selectbox import main as run_selectbox_tests

def main():
    '''The main function'''
    # Wrap in a try for exception handling
    try:
        # Capture and quit on Ctrl+C
        signal.signal(signal.SIGINT, signal_handler)

        # Run tests for different breakpoints
        set_display_size("xs")
        run_selectbox_tests()
        time.sleep(1)

        set_display_size("sm")
        run_selectbox_tests()
        time.sleep(1)

        set_display_size("md")
        run_selectbox_tests()
        time.sleep(1)

        set_display_size("lg")
        run_selectbox_tests()
        time.sleep(1)

        set_display_size("xl")
        run_selectbox_tests()
        time.sleep(1)

    except Exception:
        print(traceback.format_exc())

    finally:
        print("===========================================================")
        finish_executing()


if __name__ == '__main__':
    main()
