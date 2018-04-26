#!/usr/bin/env python3

"""
Created on April 25th, 2018
@author: andres.fernandez

Currently not implemented

"""

import pytest
import logging


@pytest.fixture(scope="session")
def my_setup(request):
    logging.info("Doing setup")


def fin():
    logging.info("\nDoing teardown")
