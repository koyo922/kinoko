#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
A context manager for using HTTP_PROXY in jupyter notebook

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/9/27 下午10:10
"""
import os
from contextlib import contextmanager

PROXY_ENABLED = True
DEFAULT_HTTP_PROXY = 'http://172.17.0.1:1082'


@contextmanager
def proxing(url=DEFAULT_HTTP_PROXY):  # 默认的docker宿主机IP
    try:
        old_proxies = os.environ.get('HTTP_PROXY', ''), os.environ.get('HTTPS_PROXY', '')
        if PROXY_ENABLED:
            os.environ['HTTP_PROXY'] = os.environ['HTTPS_PROXY'] = url
        yield
    finally:
        os.environ['HTTP_PROXY'], os.environ['HTTPS_PROXY'] = old_proxies
