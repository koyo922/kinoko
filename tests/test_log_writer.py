#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/9/29 下午6:17
"""
import os
import re
import sys

import six

from kinoko.misc.log_writer import init_log


def test_writing_files(mocker):
    mocker.spy(os.path, 'dirname')
    mocker.patch('os.path.isdir', return_value=True)
    mocker.patch('os.makedirs')
    mocker.patch('sys.stdout')
    mocker.patch('sys.stderr')
    # don't use `wraps=open`, or the files will get really created
    mocker.patch('logging.open' if six.PY3 else '__builtin__.open')

    logger = init_log(__name__, is_show_logger_src=True, log_path='./tmp/')
    assert len(logger.handlers) == 3 + 2  # file + stream

    logger.info('myinfo中文')
    assert re.match(r'^INFO:[-\d:\. ]+\[\S+@\S+.py\]\S+.py:\d+ myinfo中文\n?$',
                    sys.stdout.write.call_args_list[0][0][0])  # first call, args, first arg
    if six.PY3:
        assert os.linesep == sys.stdout.write.call_args_list[1][0][0]

    mocker.patch('os.path.isdir', return_value=False)
    init_log(log_path='./tmp')
    os.makedirs.assert_called_once()
