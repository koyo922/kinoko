#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/9/29 下午8:25
"""
import os
from distutils.sysconfig import EXEC_PREFIX

from kinoko.misc.setup_utils import get_setuptools_script_dir


def test_script_dir():
    assert os.path.join(EXEC_PREFIX, 'bin') == get_setuptools_script_dir()
