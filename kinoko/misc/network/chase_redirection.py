#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
跟踪URL重定向

Usage:
    chase_url [options]

Options:
    -i INPUT --input=INPUT               input file [default: /dev/stdin]
                                         BETTER TO USE FILE THAN PIPE, for a meaningful progressbar
    -o OUTPUT --output=OUTPUT            output file [default: /dev/stdout]
    -m MAX_DEPTH --max_depth=MAX_DEPTH   max depth of redirection [default: 5]
    -t TEMPLATE --template=TEMPLATE      output template [default: {n_jumps}\t{url}\t{tgt_url}]
                                         supported elements: (n_jumps, url, tgt_url, all_jumps, exception)
                                         NOTE: curly braces are needed, <tab> need to be bash-escaped via $'\\t'

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/6/27 下午11:12
"""
from __future__ import unicode_literals, print_function

import json
import sys
from docopt import docopt
import redo as redo
import requests
from typing import Text

from pathlib import Path

from kinoko.func import profile, dummy_fn
from kinoko.text.io import file_wrapper
from kinoko.misc.log_writer import init_log

logger = init_log(__name__)


class ChaseError(ValueError):
    """ chase_redirects有关的异常基类 """

    def jsonify(self):
        """ return json represention of self """
        return json.dumps(self.__dict__, ensure_ascii=False, default=Text)


class UnexpectedHttpStatus(ChaseError):
    """ 追踪URL重定向时遇到了 除了 202 和 300~400 以外的http状态码 """

    def __init__(self, http_status, jumps):
        """ constructor """
        super(UnexpectedHttpStatus, self).__init__()
        self.http_status = http_status
        self.jumps = jumps


class DepthOverflow(ChaseError):
    """ URL重定向过深 """

    def __init__(self, url, jumps):
        """ constructor """
        super(DepthOverflow, self).__init__()
        self.url = url
        self.jumps = jumps


class NetworkError(ChaseError):
    """ 网络访问有关的异常 """

    def __init__(self, cause, jumps):
        """ constructor """
        super(NetworkError, self).__init__()
        self.cause = cause
        self.jumps = jumps


@redo.retriable(attempts=3, sleeptime=3, jitter=1)
def chase(url, max_depth):
    """
    追踪url重定向，返回最终的原始url和跳转层数
    :param url: 可能包含重定向的url
    :param max_depth: 最多允许max_depth层深度的跳转
    :return: 跳转历史
    :raises: NetworkError, UnexpectedHttpStatus, DepthOverflow
    """
    jumps = [url]
    while len(jumps) <= max_depth:
        try:
            resp = requests.head(url, timeout=0.5)  # 注意这里是head()，比get()快
        except Exception as ex:
            raise NetworkError(cause=ex, jumps=jumps)
        if 300 <= resp.status_code < 400:  # 重定向
            url = resp.headers['location']
            jumps.append(url)
        elif resp.status_code == requests.codes.ok:  # 正确地址
            return jumps
        else:  # 其他http状态码
            raise UnexpectedHttpStatus(resp.status_code, jumps)
    else:
        raise DepthOverflow(url, jumps)


def chase_url_cli(argv=None):
    """ 追踪URL重定向的命令行接口 """
    args = docopt(__doc__, argv or sys.argv[1:])
    template = args['--template'] + '\n'
    max_depth = int(args['--max_depth'])
    with file_wrapper(args['--output'], 'wt') as fout:
        for url in file_wrapper(args['--input']):
            try:
                url = url.rstrip('\n')
                all_jumps = chase(url, max_depth)
                exception = None
            except (NetworkError, UnexpectedHttpStatus, DepthOverflow) as ex:
                all_jumps = ex.jumps
                exception = ex.jsonify()
            n_jumps = len(all_jumps) if exception is None else -1
            tgt_url = all_jumps[-1] if exception is None else None
            fout.write(template.format(**locals()))
