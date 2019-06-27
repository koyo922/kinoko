#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/6/27 下午11:20
"""
from __future__ import unicode_literals

import pytest

from kinoko.misc.network.reachability import JINGDONG_REACHABLE
from kinoko.text.io import file_wrapper

from kinoko.misc.network.chase_redirection import chase_url_cli, chase_redirection, ChaseError

url_jumps = [
    ('http://www.jingdong.com', ['http://www.jingdong.com', 'https://www.jd.com/']),
    ('http://apollo.auto/index_cn.html', ['http://apollo.auto/index_cn.html']),
    ('http://nonexist.site', [])
]

pytestmark = pytest.mark.skipif(not JINGDONG_REACHABLE, reason='not internet available')


@pytest.mark.parametrize("url, jumps", url_jumps)
def test_chase_redirection(url, jumps):
    """ 测试chase_redirection的逻辑，包括异常 """
    try:
        all_jumps = chase_redirection(url, max_depth=3)
    except ChaseError:
        all_jumps = []
    assert jumps == all_jumps


def test_chase_url_cli(tmp_path):
    """ 测试命令行工具 """
    in_path = (tmp_path / 'urllist').as_posix()
    with file_wrapper(in_path, 'wt') as f:
        f.writelines([u + '\n' for u, t in url_jumps])

    out_path = (tmp_path / 'out').as_posix()
    chase_url_cli(['-i', in_path, '-o', out_path, '--template', '{n_jumps}\t{url}\t{tgt_url}'])
    expected_lines = ['2\thttp://www.jingdong.com\thttps://www.jd.com/\n',
                      '1\thttp://apollo.auto/index_cn.html\thttp://apollo.auto/index_cn.html\n',
                      '-1\thttp://nonexist.site\tNone\n']
    assert expected_lines == list(file_wrapper(out_path))
