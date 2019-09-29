#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/6/27 下午11:20
"""
from __future__ import unicode_literals, absolute_import, print_function

from kinoko.func import static_vars, sliding, try_flatten, try_tuple


def test_static_vars(capsys):
    """ 测试函数的静态变量 """

    @static_vars(counter=0)
    def foo():
        """ 待装饰的原函数 """
        foo.counter += 1
        print(foo.counter * 10)

    foo()
    foo()
    foo()
    captured = capsys.readouterr()
    assert '10\n20\n30\n' == captured.out


def test_sliding():
    assert ((0, 1, 2), (2, 3, 4), (4, 5)) == tuple(sliding(range(6), size=3, step=2))
    assert ((0, 1, 2), (2, 3, 4)) == tuple(sliding(range(6), size=3, step=2, skip_non_full=True))


def test_flatten():
    assert None is try_flatten(None)
    assert None is try_flatten([])

    assert 1 == try_flatten([1])
    assert [1, 2] == try_flatten([1, 2])


def test_tuple():
    assert (1,) == try_tuple(1)
    assert (1, 2) == try_tuple((1, 2))
    assert ([1, 2],) == try_tuple([1, 2])  # CAUTION
