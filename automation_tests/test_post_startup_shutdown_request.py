#!/usr/bin/env python3

"""
Created on April 26th, 2018
@author: andres.fernandez

"""

import sys
import os
import logging
import pytest
from multiprocessing.dummy import Pool

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, "../lib"))

import testlogging
import testinghelper
import setup_teardown_helper

HASH_APP_PROCESS = 0


def setup_module():
    setup_teardown_helper.setup_module_helper("test_post_startup_shutdown...")


def teardown_module():
    setup_teardown_helper.teardown_module_helper("test_post_startup_shutdown...")


def setup_function():
    global HASH_APP_PROCESS
    HASH_APP_PROCESS = setup_teardown_helper.setup_function_helper()


def teardown_function():
    setup_teardown_helper.teardown_function_helper(HASH_APP_PROCESS)


@pytest.mark.skip(reason="not working the way I want. ")
def test_post_startup_called_twice():
    #TODO Need to investigate why this isn't failing properly
    logging.info("*** Starting startup called twice ***")
    return_code = setup_teardown_helper.startup_call(setup_teardown_helper.get_os_extension())
    assert (return_code == -1)
    logging.info("*** Finished startup called twice ***")


def test_post_concurrent_password_hash_calls_with_shutdown_call():
    logging.info("*** Starting concurrent test calls with shutdown call ***")
    password_argument = "concurrent"
    pooled_calls = Pool(10)
    callback_pool = []
    for x in range(10):
        if x == 4:
            logging.info("Calling shutdown in the middle of the concurrent requests")
            callback_pool.append(pooled_calls.apply_async(testinghelper.post_request_shutdown_helper, []))
        else:
            json_value = {"password": password_argument + str(x)}
            callback_pool.append(pooled_calls.apply_async(testinghelper.post_request_hash_helper, [json_value, 200, 10]))
    for callback_response in callback_pool:
        logging.info("GET REST call concurrent response (or shutdown response): " + str(callback_response.get()))
    logging.info("*** Finished concurrent test calls with shutdown call ***")


def main():
    logging.info("In test_post_password_hashing_request main function")
    test_post_concurrent_password_hash_calls_with_shutdown_call()


if __name__ == "__main__":
    testlogging.get_logger(script_dir + '/../logs/test-hash-app.log', logging.INFO, True)
    main()
