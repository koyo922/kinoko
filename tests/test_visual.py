#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/10/10 上午7:19
"""
from __future__ import unicode_literals

import pandas as pd
from typing import Text

from kinoko.visual import pd_showing_detail


def test_pd_showing_detail():
    df = pd.DataFrame.from_records(data=[
        ('zhangsan', 18, 'bio_zhang', 'story_zhang~' * 20),
        ('lisi', 19, 'bio_li', 'story_li~' * 20),
    ], columns=['name', 'age', 'bio', 'story'])

    with pd_showing_detail(max_cols=3, max_colwidth=5):
        assert r"""   name  ...    story
0  z...  ...    s... 
1  lisi  ...    s... 

[2 rows x 4 columns]""".replace(' ', '') == Text(df).replace(' ', '')
