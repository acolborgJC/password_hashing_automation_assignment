#!/usr/bin/env python3

"""
Created on April 25th, 2018
@author: andres.fernandez

"""

import sys
import os
import logging
import junit_xml
import re

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, "../lib"))

import testlogging
import testinghelper
import setup_teardown_helper

HASH_APP_PROCESS = 0


def setup_module():
    setup_teardown_helper.setup_module_helper("test_get_stats_request...")


def teardown_module():
    setup_teardown_helper.teardown_module_helper("test_get_stats_request...")


def setup_function():
    global HASH_APP_PROCESS
    HASH_APP_PROCESS = setup_teardown_helper.setup_function_helper()


def teardown_function():
    setup_teardown_helper.teardown_function_helper(HASH_APP_PROCESS)


def test_get_stats_no_data():
    logging.info("*** Starting no stats call ***")
    response = testinghelper.get_request_stats_helper(200)
    assert("0" in response)
    pattern = re.compile('^\{.*:0,.*:0\}$')
    match = pattern.match(response)
    if match:
        logging.info("matched 0 stats result")
        assert match
    else:
        logging.info("No match for no stats call!")
    logging.info("*** Finished no stats call ***")


def test_get_stats_one_request():
    logging.info("*** Starting stats call for one request ***")
    password_argument = "statsRequestForOneRequest1"
    json_value = {"password": password_argument}
    response = testinghelper.post_request_hash_helper(json_value, 200, 10)
    assert (str(response).isdigit())
    response = testinghelper.get_request_stats_helper(200)
    pattern = re.compile('^\{.*:1,.*:[0-9]{4,7}\}$')
    match = pattern.match(response)
    if match:
        logging.info("matched stats result for one hash request")
        assert match
    else:
        logging.info("No match for stats results for one hash request!")
    logging.info("*** Finished stats call for one request ***")


def main():
    logging.info("In test_get_stats_request main function")
    test_get_stats_no_data()
    test_get_stats_one_request()


if __name__ == "__main__":
    testlogging.get_logger(script_dir + '/../logs/test-hash-app.log', logging.INFO, True)
    main()
