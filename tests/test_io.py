#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/9/29 下午9:48
"""
import pytest

from kinoko.text.io import ensure_text, ensure_binary


def test_ensure_text():
    assert (u'中文'
            == ensure_text(u'中文', encoding='utf8')  # intact
            == ensure_text(u'中文'.encode('utf8'), encoding='utf8')  # bytes supported
            == ensure_text(u'中文'.encode('utf8'))  # default encoding to utf8
            )
    with pytest.raises(NotImplementedError):
        ensure_text(911)


def test_ensure_binary():
    assert (u'中文'.encode('utf8')
            == ensure_binary(u'中文'.encode('utf8'))  # intact
            == ensure_binary(u'中文', encoding='utf8')  # text supported
            == ensure_binary(u'中文')  # default encoding to utf8
            )
    with pytest.raises(NotImplementedError):
        ensure_binary(911)
