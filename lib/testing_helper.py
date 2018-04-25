#!/usr/bin/env python3

"""
Created on April 22nd, 2018
@author: andres.fernandez

"""

import json
import requests
import logging

PORT = "8088"


def post_hash_request_helper(json_parameter):
    json_payload = json.dumps(json_parameter)
    url = 'http://localhost:' + PORT + '/hash'
    r = requests.post(url, json_payload)
    logging.info("Status Code from POST: " + str(r.status_code))
    logging.info("JSON response: " + str(r.json()))
    assert (r.status_code == 200)
    assert (str(r.json()).isdigit())

    return str(r.json())


def get_hash_request_helper(hash_parameter):
    url = 'http://localhost:' + PORT + '/hash/' + str(hash_parameter)
    r = requests.get(url)
    logging.info("Status Code from GET: " + str(r.status_code))
    logging.info("JSON response: " + str(r.text))
    assert (r.status_code == 200)
    return r.text