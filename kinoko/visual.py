#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
for better formatting / displaying

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/10/10 上午7:08
"""
import pandas as pd
from contextlib import contextmanager


@contextmanager
def pd_showing_detail(max_cols=10, max_colwidth=800):
    with pd.option_context('display.max_columns', max_cols, 'max_colwidth', max_colwidth):
        yield
