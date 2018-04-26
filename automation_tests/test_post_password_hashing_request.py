#!/usr/bin/env python3

"""
Created on April 22nd, 2018
@author: andres.fernandez

"""

import sys
import os
import subprocess
import time
import logging
import requests
import json
import junit_xml
import hashlib
import pytest
import base64
import codecs
import multiprocessing
from multiprocessing.dummy import Pool

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, "../lib"))

import testlogging
import testinghelper

HASH_APP_PROCESS = 0
PORT = "8088"


def setup_module():
    logging.info("* Running setup_module module in test_post_password... *")
    testlogging.get_logger(script_dir + '/../logs/test-hash-app.log', logging.INFO, True)
    logging.info("Platform: " + sys.platform)
    logging.info("* Exiting setup_module method in test_post_password... *")


def teardown_module():
    logging.info("* Running teardown_module method *")
    logging.info("* Exiting teardown_module method *")


def setup_function():
    logging.info("** Running setup_function method **")
    global HASH_APP_PROCESS
    os.environ["PORT"] = PORT
    logging.info("Current working directory: " + os.getcwd())
    os_extension_name = ""
    if "darwin" == sys.platform:
        os_extension_name = "darwin"
    elif "win32" == sys.platform:
        os_extension_name = "_win.exe"

    try:
        testinghelper.post_request_shutdown_helper_no_validation()
    except:
        logging.info("Got exception trying to shutdown")

    try:
        logging.info("Running application")
        HASH_APP_PROCESS = subprocess.Popen([".//resources//broken-hashserve_" + os_extension_name, ""])
    except subprocess.CalledProcessError:
        logging.info("There was an error starting the process")
    logging.info("** Exiting setup_function method **")


def teardown_function():
    logging.info("** Running teardown_function method **")
    global HASH_APP_PROCESS
    try:
        HASH_APP_PROCESS.terminate()
    except subprocess.CalledProcessError:
        logging.info("Couldn't stop process")
    logging.info("** Exiting teardown_function method **")


@pytest.mark.skip(reason="no way of currently testing this")
def test_concurrent_post_password_hash_calls():
    logging.info("*** Starting concurrent test calls ***")
    password_argument = "concurrent"
    pooled_calls = Pool(10)
    callback_pool = []
    for x in range(10):
        json_value = {"password": password_argument + str(x)}
        callback_pool.append(pooled_calls.apply_async(testinghelper.post_request_hash_helper, [json_value, 200]))
    for callback_response in callback_pool:
        logging.info("GET REST call concurrent response: " + str(callback_response.get()))
    testinghelper.get_request_stats_helper()
    logging.info("*** Finished concurrent test calls ***")


@pytest.mark.parametrize("key,value,code", [
    ("password", "", 400),
    ("password", "a", 200),
    ("password", "!@#$%&*()", 200),
    ("boguskey", "password1", 400),
    ("", "password1", 400),
    ("", "", 400)
])
@pytest.mark.skip(reason="no way of currently testing this")
def test_parameterized_post_password_hash_calls(key, value, code):
    logging.info("*** Starting parameterized test calls ***")
    json_value = {key: value}
    testinghelper.post_request_hash_helper(json_value, code)
    testinghelper.get_request_stats_helper()
    logging.info("*** Finished parameterized test calls ***")


@pytest.mark.skip(reason="no way of currently testing this")
def test_post_single_password_hash_call():
    logging.info("*** Starting single test call ***")
    password_argument = "angrymonkey"
    json_value = {"password": password_argument}
    response = testinghelper.post_request_hash_helper(json_value, 200)
    assert(str(response).isdigit())
    testinghelper.get_request_stats_helper()
    logging.info("*** Finished single test call ***")


#@pytest.mark.skip(reason="no way of currently testing this")
def test_sequential_post_password_hash_calls():
    logging.info("*** Starting sequential test calls ***")
    password_argument = "password"
    number_of_tries = 5
    incremented_set_of_integers = set()

    for i in range(number_of_tries):
        json_value = {"password": password_argument + str(i)}
        response = testinghelper.post_request_hash_helper(json_value, 200)
        assert (str(response).isdigit())
        try:
            incremented_set_of_integers.add(str(response))
        except:
            logging.info("Added a duplicate number, each hash call should return a unique number")
            pytest.raises(RuntimeError, "Duplicate hash number added")

    assert (len(incremented_set_of_integers) == number_of_tries)
    testinghelper.get_request_stats_helper()
    logging.info("*** Finished sequential test calls ***")


def main():
    logging.info("In main function")
    test_post_single_password_hash_call()
    test_sequential_post_password_hash_calls()


if __name__ == "__main__":
    testlogging.get_logger(script_dir + '/../logs/test-hash-app.log', logging.INFO, True)
    logging.info("Platform: " + sys.platform)
    if "darwin" == sys.platform:
        logging.info("Mac platform!")
    elif "win32" == sys.platform:
        logging.info("Windows platform!")
    main()
