#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
测试基础的文本工具

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/9 上午10:31
"""
from __future__ import unicode_literals

import pytest

from kinoko.text.common import is_none_or_empty, no_special_chars


@pytest.mark.parametrize("ele, tgt", [
    # None 或者 空串 或者 空容器 都是True
    (None, True),
    ('', True),
    (tuple(), True),
    ([], True),
    ({}, True),
    # 只要非空，就返回False；不考虑元素是否为 None或者whitespace
    (u'abc', False),
    (b'abc', False),
    (u'   ', False),
    (u'中文', False),
    (u'中文'.encode('utf8'), False),
    ([None], False),
    (['abc'], False),
])
def test_is_none_or_empty(ele, tgt):
    """ test """
    assert tgt == is_none_or_empty(ele)


@pytest.mark.parametrize("args, tgt", [
    # None "里面"不含有特殊字符
    ((None,), True),
    # 默认special_chars是 TAB_OR_NEWLINE
    ((b'abc',), True),
    ((u'abc',), True),
    ((u'中文',), True),
    ((u'中文',), True),
    # 空串或者空容器里面不含 特殊字符
    (('',), True),
    (('', '\t\n\r'), True),
    ((tuple(),), True),
    (([],), True),
    (({},), True),
    # 不含 特殊字符的容器/字符串
    ((u'abc',), True),
    ((b'abc',), True),
    ((u'中文',), True),
    ((u'中文'.encode('utf8'),), True),
    # 含有 特殊字符的容器/字符串
    ((u'中\t文',), False),
    ((u'中\t文', '\t\n\r'), False),
])
def test_no_special_chars(args, tgt):
    """ test """
    assert tgt == no_special_chars(*args)
