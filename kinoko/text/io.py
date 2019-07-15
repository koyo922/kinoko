#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
IO related utils

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/6/27 下午11:20
"""
from __future__ import absolute_import, unicode_literals

import json
import subprocess
from io import open
import sys

import six
import tqdm

try:
    from pathlib2 import Path
except ImportError:
    from pathlib import Path


def ensure_text(s, encoding='utf8'):
    """ 确保进来的 str/unicode 全部转成 Text类型 """
    if isinstance(s, six.binary_type):
        return s.decode(encoding)
    elif isinstance(s, six.text_type):
        return s
    else:
        raise NotImplementedError('Unsupported argument s: {}'.format(repr(s)))


def ensure_binary(s, encoding='utf8'):
    """ 确保进来的 str/unicode 全部转成 Binary类型 """
    if isinstance(s, six.binary_type):
        return s
    elif isinstance(s, six.text_type):
        return s.encode(encoding)
    else:
        raise NotImplementedError('Unsupported argument s: {}'.format(repr(s)))


def as_lines(f, total=None, desc=None, with_lineno=False):
    """
    将文件对象包裹成 行的迭代器
    :param f: 文件对象
    :param total: 总行数(用于进度条)，默认None
    :param desc: 描述串(用于进度条)，默认None
    :param with_lineno: 是否一起返回行号，默认False
    :return:
    """
    items = enumerate(f) if with_lineno else f
    for e in tqdm.tqdm(items, total=total, desc=desc):
        yield e


def file_wrapper(path='/dev/stdin', mode=None, with_lineno=False, desc=None, **open_kwargs):
    """
    对文件读写器的包裹
    :param path: 文件路径，默认 /dev/stdin
    :param mode: open() 的参数
    :param with_lineno: 是否带上行号(仅对可读的文本文件有意义)
    :param desc: 描述串(用于进度条)，默认为文件路径最后两层
    :param open_kwargs: 传给io.open()函数的参数
    :return:
    """
    # 调节默认参数
    open_kwargs.setdefault('encoding', 'utf8')
    if path in ('/dev/stdout', '/dev/stderr'):
        mode = mode or 'wt'
        if 'pytest' in sys.modules:  # py.test框架会patch & 捕获 stdout/stderr
            f = sys.stdout if path.endswith('stdout') else sys.stderr
        else:
            fd = sys.stdout.fileno() if path.endswith('stdout') else sys.stderr.fileno()
            f = open(fd, mode=mode, **open_kwargs)
    else:
        mode = mode or 'rt'
        f = open(path, mode=mode, **open_kwargs)

    if 'w' in mode or 'a' in mode:  # 写文件: 直接返回可写的文件对象
        return f
    else:  # 读文件: 返回行迭代器
        return as_lines(f, with_lineno=with_lineno, total=n_lines(path),
                        desc=(desc or '/'.join(Path(path).parts[-2:])))


def n_lines(file_path):
    """ 数文件的行数 """
    if file_path == '/dev/stdin' or file_path.startswith('/dev/fd/'):  # 不要对管道统计行数（否则会耗尽内容）
        return None
    num = subprocess.check_output(['wc', '-l', file_path]).decode('utf8')
    return int(num.strip().split(' ')[0])


def dump_utf8(obj, indent=None):
    """ json dump without ensure_ascii """
    return json.dumps(obj, ensure_ascii=False, indent=indent)
