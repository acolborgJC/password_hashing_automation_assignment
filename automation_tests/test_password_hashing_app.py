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

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, "../lib"))

import testlogging
import testing_helper

HASH_APP_PROCESS = 0
PORT = "8088"


def setup_module():

    testlogging.get_logger(script_dir + '/../logs/test-hash-app.log', logging.INFO, True)

    logging.info("Platform: " + sys.platform)

    global HASH_APP_PROCESS
    os.environ["PORT"] = PORT
    print("Current working directory: " + os.getcwd())
    os_extension_name = "darwin"

    try:
        HASH_APP_PROCESS = subprocess.Popen([".//resources//broken-hashserve_" + os_extension_name, ""])
    except subprocess.CalledProcessError:
        print("There was an error starting the process")


def teardown_module():
    global HASH_APP_PROCESS
    try:
        HASH_APP_PROCESS.terminate()
    except subprocess.CalledProcessError:
        print("Couldn't stop process")


def test_get_password_hash_call():
    password_argument = "angrymonkey"
    json_value = {"password": password_argument}
    returned_value = post_hash_request_helper(json_value)
    logging.info("Returned Value from POST request: " + str(returned_value))
    returned_base64_encoding = get_hash_request_helper(returned_value)
    message = hashlib.sha512(b"angrymonkey").hexdigest()
    logging.info("Sha512 hex digest: " + message)
    b64 = codecs.encode(codecs.decode(message, 'hex'), 'base64').decode()
    b64 = b64.replace('\n', '')
    logging.info("Base64 expected string: " + b64)
    assert(str(returned_base64_encoding) == b64)


#@pytest.mark.skip(reason="no way of currently testing this")
def test_post_password_hash_call():
    password_argument = "angrymonkey"
    json_value = {"password": password_argument}
    returned_value = post_hash_request_helper(json_value)
    return set(str(returned_value))


#@pytest.mark.skip(reason="no way of currently testing this")
def test_multiple_post_password_hash_calls():
    password_argument = "password"
    number_of_tries = 5
    incremented_set_of_integers = set()

    for i in range(number_of_tries):
        json_value = {"password": password_argument+str(i)}
        returned_value = post_hash_request_helper(json_value)
        try:
            incremented_set_of_integers.add(str(returned_value))
        except:
            logging.info("Added a duplicate number, each hash call should return a unique number")
            pytest.raises(RuntimeError, "Duplicate hash number added")

    assert(len(incremented_set_of_integers) == number_of_tries)
    return incremented_set_of_integers


def main():
    print("In main")
    test_post_password_hash_call()
    test_multiple_post_password_hash_calls()


if __name__ == "__main__":
    testlogging.get_logger(script_dir + '/../logs/test-hash-app.log', logging.INFO, True)

    logging.info("Platform: " + sys.platform)

    if "darwin" == sys.platform:
        logging.info("Mac platform!")

    elif "win32" == sys.platform:
        logging.info("Windows platform!")

    main()

