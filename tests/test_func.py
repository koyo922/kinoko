#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/6/27 下午11:20
"""
from __future__ import unicode_literals, absolute_import, print_function

from kinoko.func import static_vars


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
