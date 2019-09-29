#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/6/27 下午11:20
"""
from __future__ import unicode_literals

import os
from typing import Text

import pytest
import requests
import six

from kinoko.misc.network.chase_redirection import (chase_url_cli, chase_redirection, ChaseError,
                                                   UnexpectedHttpStatus, DepthOverflow)
from kinoko.misc.network.proxy import proxing, DEFAULT_HTTP_PROXY
from kinoko.text.io import file_wrapper

if six.PY3:
    from unittest.mock import Mock
else:
    # noinspection PyPackageRequirements
    from mock import Mock

url_jumps = [
    ('http://www.cyberciti.biz/tips/', ['http://www.cyberciti.biz/tips/', 'https://www.cyberciti.biz/tips/']),
    ('http://apollo.auto/index_cn.html', ['http://apollo.auto/index_cn.html']),
    ('http://nonexist.site', [])
]


# noinspection PyUnusedLocal
def mock_head(url, timeout=None):
    if url == 'http://www.cyberciti.biz/tips/':
        return Mock(status_code=requests.codes.found, headers={'location': 'https://www.cyberciti.biz/tips/'})
    elif url == 'https://www.cyberciti.biz/tips/':
        return Mock(status_code=requests.codes.ok)
    elif url == 'http://apollo.auto/index_cn.html':
        return Mock(status_code=requests.codes.ok)
    elif url == 'http://nonexist.site':
        raise requests.exceptions.ConnectionError('mocked unreachable url')
    else:
        raise ValueError('unexpected url: ' + url)


@pytest.mark.parametrize("url, jumps", url_jumps)
def test_chase_redirection(url, jumps, mocker):
    """ 测试chase_redirection的逻辑，包括异常 """
    mocker.patch.object(requests, 'head', mock_head)

    try:
        all_jumps = chase_redirection(url, max_depth=3)
    except ChaseError:
        all_jumps = []
    assert jumps == all_jumps


def test_chase_redirection_exceptions(mocker):
    mocker.patch.object(requests, 'head', return_value=Mock(status_code=911))
    with pytest.raises(UnexpectedHttpStatus) as ex:
        chase_redirection('dummy_url', max_depth=3)
        assert ex.http_status == 911

    # noinspection PyUnusedLocal
    def mock_head_10(url, timeout=None):
        back_url = int(url) + 1 if int(url) < 10 else 10
        return Mock(status_code=requests.codes.found, headers={'location': Text(back_url)})

    mocker.patch.object(requests, 'head', side_effect=mock_head_10)
    with pytest.raises(DepthOverflow) as ex:
        chase_redirection('1', max_depth=5)
        assert ex.url == '5'


def test_chase_url_cli(tmp_path):
    """ 测试命令行工具 """
    in_path = (tmp_path / 'urllist').as_posix()
    with file_wrapper(in_path, 'wt') as f:
        f.writelines([u + '\n' for u, t in url_jumps])

    out_path = (tmp_path / 'out').as_posix()
    chase_url_cli(['-i', in_path, '-o', out_path, '--template', '{n_jumps}\t{url}\t{tgt_url}'])
    expected_lines = ['{n_jumps}\t{url}\t{tgt_url}\n'.format(n_jumps=-1 if not j else len(j), url=u,
                                                             tgt_url=None if len(j) == 0 else j[-1])
                      for u, j in url_jumps]
    assert expected_lines == list(file_wrapper(out_path))


def test_proxing():
    old_http, old_https = 'http://old', 'https://old'
    os.environ['HTTP_PROXY'], os.environ['HTTPS_PROXY'] = old_http, old_https
    with proxing():  # default
        assert os.environ['HTTP_PROXY'] == os.environ['HTTPS_PROXY'] == DEFAULT_HTTP_PROXY
    with proxing('http://dummy'):
        assert os.environ['HTTP_PROXY'] == os.environ['HTTPS_PROXY'] == 'http://dummy'
    assert (os.environ['HTTP_PROXY'], os.environ['HTTPS_PROXY']) == (old_http, old_https)
