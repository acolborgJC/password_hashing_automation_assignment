#!/usr/bin/env python3

"""
Created on April 22nd, 2018
@author: andres.fernandez

"""

import sys
import os
import logging
import junit_xml
import hashlib
import pytest
import codecs

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, "../lib"))

import testlogging
import testinghelper
import setup_teardown_helper

HASH_APP_PROCESS = 0


def setup_module():
    setup_teardown_helper.setup_module_helper("test_get_password_base64_encoded...")


def teardown_module():
    setup_teardown_helper.teardown_module_helper("test_get_password_base64_encoded...")


def setup_function():
    global HASH_APP_PROCESS
    HASH_APP_PROCESS = setup_teardown_helper.setup_function_helper()


def teardown_function():
    setup_teardown_helper.teardown_function_helper(HASH_APP_PROCESS)


@pytest.mark.skip(reason="no way of currently testing this")
def test_get_password_hash_call():
    password_argument = "angrymonkey"
    json_value = {"password": password_argument}
    response = testinghelper.post_request_hash_helper(json_value, 200)
    logging.info("Returned Value from POST request: " + str(response))
    returned_base64_encoding = testinghelper.get_request_hash_helper(response, 200)
    message = hashlib.sha512(password_argument.encode()).hexdigest()
    logging.info("Sha512 hex digest: " + message)
    b64 = codecs.encode(codecs.decode(message, 'hex'), 'base64').decode()
    b64 = b64.replace('\n', '')
    logging.info("Base64 expected string: " + b64)
    assert (str(returned_base64_encoding) == b64)
    assert (len(str(returned_base64_encoding)) == 88)


def test_get_password_hash_with_invalid_number():
    logging.info("*** Starting get base64 encoded hash call with invalid number ***")
    password_argument = "testpassword@1234"
    json_value = {"password": password_argument}
    response = testinghelper.post_request_hash_helper(json_value, 200, 10)
    assert (str(response).isdigit())
    response = testinghelper.get_request_hash_helper(99, 400)
    assert ("Hash not found" in str(response))
    logging.info("*** Finished get base64 encoded hash call with invalid number ***")

def test_get_password_hash_with_ascii_character():
    logging.info("*** Starting get base64 encoded hash call with ascii character ***")
    password_argument = "testpassword@1234"
    json_value = {"password": password_argument}
    response = testinghelper.post_request_hash_helper(json_value, 200, 10)
    response = testinghelper.get_request_hash_helper('a', 400)
    assert ("strconv.Atoi:" in str(response))
    assert ("invalid syntax" in str(response))
    logging.info("*** Finished get base64 encoded hash call with ascii character ***")



def main():
    logging.info("In test_get_password_base64_encoded_request main function")
    test_get_password_hash_call()


if __name__ == "__main__":
    testlogging.get_logger(script_dir + '/../logs/test-hash-app.log', logging.INFO, True)
    main()
