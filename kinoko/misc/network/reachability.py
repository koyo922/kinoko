#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
检测网络可达性

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/6/27 下午11:12
"""

import os

JINGDONG_REACHABLE = os.system("ping -c 1 jd.com") == 0
GOOGLE_REACHABLE = os.system("ping -c 1 google.com") == 0
