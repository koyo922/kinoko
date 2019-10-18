#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/10/17 下午4:02
"""
from __future__ import unicode_literals, division

import pandas as pd
import numpy as np
import pytest

from kinoko.time_series.dtw import UCR_DTW, square_dist_fn

ucr_dtw = UCR_DTW(dist_cb=square_dist_fn)

x = np.linspace(0, 50, 100)
ts1 = pd.Series(3.1 * np.sin(x / 1.5) + 3.5)
ts2 = pd.Series(2.2 * np.sin(x / 3.5 + 2.4) + 3.2)
ts3 = pd.Series(0.04 * x + 3.0)


def _FastDTWDistance(s1, s2, w):
    """ 用作测试标准的 参考实现 https://github.com/JozeeLin/ucr-suite-python/blob/master/DTW.ipynb """
    DTW = {}

    w = max(w, abs(len(s1) - len(s2)))  # window

    for i in range(-1, len(s1)):
        for j in range(-1, len(s2)):
            DTW[(i, j)] = float('inf')
    DTW[(-1, -1)] = 0

    for i in range(len(s1)):
        for j in range(max(0, i - w), min(len(s2), i + w + 1)):  # 注意 range()是右开区间，要用 w+1
            dist = (s1[i] - s2[j]) ** 2
            DTW[(i, j)] = dist + min(DTW[(i - 1, j)], DTW[(i, j - 1)], DTW[(i - 1, j - 1)])

    return np.sqrt(DTW[len(s1) - 1, len(s2) - 1])


@pytest.mark.parametrize("content, query", [(ts1, ts2), (ts1, ts3)])
def test_dtw_distance(content, query):
    assert (pytest.approx(_FastDTWDistance(content, query, 10) ** 2) ==
            ucr_dtw.dtw_distance(content, query, max_stray=10, rolling_level=0) ==
            ucr_dtw.dtw_distance(content, query, max_stray=10, rolling_level=1) ==
            ucr_dtw.dtw_distance(content, query, max_stray=10, rolling_level=2)
            )


def _LB_Keogh(s1, s2, r):
    LB_sum = 0
    for ind, i in enumerate(s1):
        # 注意右开区间
        lower_bound = min(s2[(ind - r if ind - r >= 0 else 0):(ind + r + 1 if ind + r < len(s2) else len(s2))])
        upper_bound = max(s2[(ind - r if ind - r >= 0 else 0):(ind + r + 1 if ind + r < len(s2) else len(s2))])

        if i > upper_bound:
            LB_sum = LB_sum + (i - upper_bound) ** 2
        elif i < lower_bound:
            LB_sum = LB_sum + (i - lower_bound) ** 2

    return np.sqrt(LB_sum)


@pytest.mark.parametrize("content, query", [(ts1, ts2), (ts1, ts3)])
def test_lb_keogh(content, query):
    assert _LB_Keogh(content, query, 20) == ucr_dtw.lb_keogh_ec(content, query, window_size=20)
