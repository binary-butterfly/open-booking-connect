# encoding: utf-8

"""
open booking connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

import os
import logging
from logging.handlers import WatchedFileHandler
from ..config import Config


class Logger:
    registered_logs = {}

    def get_log(self, log_name):
        if log_name in self.registered_logs:
            return self.registered_logs[log_name]

        logger = logging.getLogger(log_name)
        logger.handlers.clear()
        logger.setLevel(logging.INFO)

        # Init File Handler
        file_name = os.path.join(Config.LOG_DIR, '%s.log' % log_name)
        file_handler = WatchedFileHandler(file_name)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s ')
        )
        logger.addHandler(file_handler)

        file_name = os.path.join(Config.LOG_DIR, '%s.err' % log_name)
        file_handler = WatchedFileHandler(file_name)
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s ')
        )
        logger.addHandler(file_handler)

        if Config.DEBUG:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_format = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
            console_handler.setFormatter(console_format)
            logger.addHandler(console_handler)

        self.registered_logs[log_name] = logger

        return logger

    def debug(self, log_name, message):
        self.get_log(log_name).debug(message)

    def info(self, log_name, message):
        self.get_log(log_name).info(message)

    def warn(self, log_name, message):
        self.get_log(log_name).warning(message)

    def error(self, log_name, message, details=None):
        self.get_log(log_name).error(message + (("\n" + details) if details else ""))

    def exception(self, log_name, message, details=None):
        self.get_log(log_name).exception(message + (("\n" + details) if details else ""))

    def critical(self, log_name, message, details=None):
        self.get_log(log_name).critical(message + (("\n" + details) if details else ""))
