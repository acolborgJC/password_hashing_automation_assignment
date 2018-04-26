#!/usr/bin/env python3

"""
Created on April 25th, 2018
@author: andres.fernandez

"""

import os
import sys
import logging
import yaml
import subprocess

script_dir = os.path.dirname(__file__)

import testlogging
import testinghelper

YAMLFILE = './/properties//test_params.yaml'


def setup_module_helper(qualifier):
    logging.info("* Running setup_module method in " + qualifier + " *")
    testlogging.get_logger(script_dir + get_property_value("logfile"), logging.INFO, True)
    logging.info("Platform: " + sys.platform)
    logging.info("* Exiting setup_module method in " + qualifier + " *")


def teardown_module_helper(qualifier):
    logging.info("* Running teardown_module method in " + qualifier + " *")
    logging.info("* Exiting teardown_module method in " + qualifier + " *")


def get_os_extension():
    os_extension_name = ""
    if "darwin" == sys.platform:
        os_extension_name = "darwin"
    elif "win32" == sys.platform:
        os_extension_name = "_win.exe"
    return os_extension_name


def startup_call(os_extension_name):
    try:
        logging.info("Running application")
        hash_app_process = subprocess.Popen([".//resources//broken-hashserve_" + os_extension_name, ""])
        logging.info("Launching application success")
        return hash_app_process
    except subprocess.CalledProcessError:
        logging.info("There was an error starting the process")
        return -1


def setup_function_helper():
    logging.info("** Running setup_function method **")
    os.environ["PORT"] = get_property_value("port")
    logging.info("Current working directory: " + os.getcwd())
    os_extension_name = get_os_extension()

    #try:
    #    testinghelper.post_request_shutdown_helper_no_validation()
    #except:
    #    logging.info("Got exception trying to shutdown")

    hash_app_process = startup_call(os_extension_name)
    logging.info("** Exiting setup_function method **")
    return hash_app_process


def teardown_function_helper(hash_app_process):
    logging.info("** Running teardown_function method **")
    try:
        hash_app_process.terminate()
    except subprocess.CalledProcessError:
        logging.info("Couldn't stop process")
    logging.info("** Exiting teardown_function method **")


def get_property_value(requested_key_value):
    logging.info("Opening yaml file")
    try:
        params = yaml.load(open(YAMLFILE))
        return str(params[requested_key_value])
    except:
        logging.info("Couldn't load YAML file: " + YAMLFILE)




