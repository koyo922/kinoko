#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
提供logger对象的模块

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/6/27 下午11:20
"""

import os
import sys
import logging
import logging.handlers


class _BelowWarningFilter(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.WARNING


# noinspection PyIncorrectDocstring
def init_log(logger_name=None, log_path=None, level=None, when="MIDNIGHT", backup=365,
             is_writing_console=True, is_show_logger_src=False, is_propagate=False,
             fmt="%(levelname)s: %(asctime)s.%(msecs)03d: %(filename)s:%(lineno)d %(message)s",
             datefmt="%m-%d %H:%M:%S"):
    """
    init_log - initialize log module;
    WARNING: IT IS NOT SAFE FOR MULTI-PROCESSING APPS. LOGS MAY BE LOST OR PRINT INTO A RANDOM FILE.

    Args:
      logger_name   - name of the logger to get, if None, return root logger
                      default value: None
                      Any non-exist parent directories will be created automatically
      log_path      - Log file path prefix.
                      Log data will go to two files: log_path.log and log_path.log.wf
                      Any non-exist parent directories will be created automatically
                      the default value is None, meaning no files needed
      level         - msg above the level will be displayed in *.log(always WARN for *.log.wf, DEBUG for stdout)
                      DEBUG < INFO < WARNING < ERROR < CRITICAL
                      the default value is `os.environ.get('LOGLEVEL', 'INFO')`
      when          - how to split the log file by time interval
                      'S' : Seconds
                      'M' : Minutes
                      'H' : Hours
                      'D' : Days
                      'W' : Week day
                      default value: 'MIDNIGHT'; 'D' causes BUG in py2; see https://www.jianshu.com/p/25f70905ae9d
      backup        - how many backup file to keep
                      default value: 365
      to_console    - whether always write to console
                      default value: True
      is_show_logger_src
                    - show name and path for all loggers, including 3rd-party library,
                      used for debugging and silence those unwanted
                      default value: False
      is_propagate  - whether propagate to parent logger
                      default value: False
      fmt           - format of the log
                      default format:
                      %(levelname)s: %(asctime)s.%(msecs)03d: %(filename)s:%(lineno)d %(message)s
                      > INFO: 12-09 18:02:42.025: log.py:40 HELLO WORLD
      datefmt       - format for the datetime part in ``fmt``

    Return:
        logging.Logger: the logger object

    Raises:
        OSError: fail to create log directories
        IOError: fail to open log file
    """
    # check params
    is_writing_files = not (log_path is None or log_path == '')
    assert is_writing_files or is_writing_console, 'Neither writing to files or console, useless logger'
    level = level or os.environ.get('LOGLEVEL', 'INFO').upper()

    # config the logger
    if is_show_logger_src:
        fmt = fmt.replace('%(filename)s:%(lineno)d', '[%(name)s@%(pathname)s]%(filename)s:%(lineno)d')
    formatter = logging.Formatter(fmt, datefmt)
    logger = logging.getLogger(logger_name)
    logger.propagate = is_propagate
    logger.setLevel(logging.DEBUG)

    # config handlers for files
    if is_writing_files:
        log_dir = os.path.dirname(log_path)
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)

        handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log.debug",
                                                            when=when,
                                                            encoding='utf8',
                                                            backupCount=backup)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log",
                                                            when=when,
                                                            encoding='utf8',
                                                            backupCount=backup)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log.wf",
                                                            when=when,
                                                            encoding='utf8',
                                                            backupCount=backup)
        handler.setLevel(logging.WARNING)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # config handlers for console
    if is_writing_console:
        handler_stdout = logging.StreamHandler(sys.stdout)
        handler_stdout.setLevel(level)
        handler_stdout.addFilter(_BelowWarningFilter())  # 低于WARNING的打到 stdout
        handler_stdout.setFormatter(formatter)
        logger.addHandler(handler_stdout)

        handler_stderr = logging.StreamHandler(sys.stderr)
        handler_stderr.setLevel(logging.WARNING)  # >= WARNING的打到 stderr
        handler_stderr.setFormatter(formatter)
        logger.addHandler(handler_stderr)

    # return the logger
    return logger
