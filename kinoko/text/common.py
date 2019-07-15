#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
一些基础通用的文本工具

Authors: qianweishuo<qianweishuo@baidu.com>
Date:    2019/7/9 上午10:00
"""
from __future__ import unicode_literals, print_function

import six
import typing

from ..misc.log_writer import init_log
from ..text.io import ensure_text

logger = init_log(__name__)

TAB_OR_NEWLINE = {'\t', '\n', '\r'}


def is_none_or_empty(s):
    """
    判断指定的 字符串或者容器 是否为 None或者空
    :param s: 字符串 或者 set/list 等容器
    """
    return s is None or len(s) == 0


def no_special_chars(text, special_chars=TAB_OR_NEWLINE):
    """
    判断 指定的字符串中是否不含有 特殊字符
    :param text: 字符串
    :param special_chars: 特殊字符集合，支持 str/unicode/container
    """
    if is_none_or_empty(text):
        return True
    text = ensure_text(text)  # 确保转成 Text类型

    if isinstance(special_chars, typing.Container):
        special_chars = set(special_chars)  # 最好的情况，直接把原来的容器换成set
    elif isinstance(special_chars, six.string_types):
        special_chars = {c for c in ensure_text(special_chars)}  # 原来的字符串做成 字符set
    else:
        raise ValueError('unsupported argument %s, please use type of `set/str/unicode`', repr(special_chars))
    return all(c not in text for c in special_chars)
