#!/usr/bin/env python3

"""

Created April 20th, 2018
@author, Andres Fernandez

Logger for test modules which prints to stdout and to a specified log file.

Call like this:

  import testlogging
  logger = testlogging.getLogger(script_dir + '/../logs/my-module.log', logging.INFO)
  logger.info("my-module starting")

"""

__author__ = 'Andres.Fernandez'

import logging
import logging.config


def get_logger(filename, level, stdout=False):
    format_str = '%(asctime)s %(levelname)-8s - %(message)s'
    if stdout:
        logging.basicConfig(level=level, format=format_str)
    formatter = logging.Formatter(format_str)

    file_handler = logging.handlers.RotatingFileHandler(filename, maxBytes=10485760, backupCount=5)
    file_handler.setFormatter(formatter)
    logging.getLogger('').addHandler(file_handler)
    logging.getLogger('').setLevel(level)


