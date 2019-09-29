#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
- 函数式有关工具
- 各种容器

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/6/27 下午11:20
"""
from typing import Any, Iterable, Union, TypeVar
from functional.pipeline import Sequence
from functional import seq

T = TypeVar('T')


def strip_fields(tup):
    """ 对tuple中的每个域做 strip """
    return tuple(f.strip().replace(' ', '') for f in tup)


def sliding(sequence, size, step=1, skip_non_full=False):
    # type: (Union[Sequence, Iterable], int, int, bool) -> Iterable[Any]
    """
    滑动窗口
    封装 pyfunctional提供的 seq.sliding() 函数； 支持跳过不完整元组
    :param sequence: 待滑动的序列
    :param size: 滑动窗口序列
    :param step: 滑动步长
    :param skip_non_full: 跳过结尾可能遇到的不完整元组
    :return:
    """
    s = sequence if isinstance(sequence, Sequence) else seq(sequence)
    for tup in s.sliding(size=size, step=step):
        if skip_non_full and tup.len() < size:
            break
        yield tuple(tup)


def static_vars(**kwargs):
    """
    为函数提供静态变量的装饰器, 参考:
    https://stackoverflow.com/questions/279561/what-is-the-python-equivalent-of-static-variables-inside-a-function
    """

    def decorate(func):
        """ 装饰后的函数 """
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


def try_flatten(sequence):
    # type: (Sequence[T]) -> Union[T, Sequence[T]]
    """
    trying to flatten a sequence;
    - if it is none or empty, return none
    - if len(it)==1, return it's only element(FLATTEN)
    - if len(it)>1, return itself untouched
    :param sequence:
    :return:
    """
    if sequence is None or len(sequence) == 0:
        return None
    if len(sequence) == 1:
        return tuple(sequence)[0]
    return sequence


def try_tuple(obj):
    # type: (Union[T, Tuple[T]]) -> Tuple[T]
    """ try to wrap a object into len==1 tuple """
    if isinstance(obj, tuple):
        return obj

    return obj,  # NOTE the comma, made into tuple
