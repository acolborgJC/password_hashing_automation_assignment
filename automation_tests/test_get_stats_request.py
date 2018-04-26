#!/usr/bin/env python3

"""
Created on April 25th, 2018
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

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, "../lib"))

import testlogging
import testinghelper

HASH_APP_PROCESS = 0
PORT = "8088"


def setup_module():
    testlogging.get_logger(script_dir + '/../logs/test-hash-app.log', logging.INFO, True)
    logging.info("Running setup_module module in test_get_password...")
    logging.info("Platform: " + sys.platform)
    logging.info("Exiting setup_module method in test_get_password...")


def teardown_module():
    logging.info("Running teardown_module method")
    logging.info("Exiting teardown_module method")


def setup_function():
    logging.info("Running setup_function method")
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


def teardown_function():
    logging.info("Running teardown_function method")
    global HASH_APP_PROCESS
    try:
        HASH_APP_PROCESS.terminate()
    except subprocess.CalledProcessError:
        logging.info("Couldn't stop process")


@pytest.mark.skip(reason="no way of currently testing this")
def test_get_stats_no_data():
    logging.info("*** Starting stats call ***")
    response = testinghelper.get_request_stats_helper(200)
    assert("0" in response)
    logging.info("*** Finished stats call ***")


def main():
    logging.info("In main function")
    test_get_stats_no_data()


if __name__ == "__main__":
    testlogging.get_logger(script_dir + '/../logs/test-hash-app.log', logging.INFO, True)
    logging.info("Platform: " + sys.platform)
    if "darwin" == sys.platform:
        logging.info("Mac platform!")
    elif "win32" == sys.platform:
        logging.info("Windows platform!")
    main()
