#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
测试tsv有关 工具

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/6/27 下午11:20
"""
from __future__ import absolute_import, unicode_literals

try:
    from pathlib2 import Path
except ImportError:
    from pathlib import Path

from kinoko.text import patch_tsv, agg_tsv
from kinoko.text.io import file_wrapper


def test_patch_tsv(tmp_path):
    """ 用简单用例测试 patch_tsv """
    # type: (Path) -> None
    ref_path = (tmp_path / 'ref').as_posix()
    with file_wrapper(ref_path, mode='wt') as f:
        f.writelines(['jiaose\t角色\tjuese\n',
                      'xxx\t色情词\t<DEL>\n'])

    input_path = (tmp_path / 'in').as_posix()
    with file_wrapper(input_path, mode='wt') as f:
        f.writelines(['field1\tfield2\t角色\tjiaose\tfield4\n',
                      'field1\t field2\t角色\tjiaose\tfield4\n',  # field2 开头多一个空格，替换后要保留
                      'field1\tfield2\t色情词\txxx\tfield4\n'])

    out_path = (tmp_path / 'out').as_posix()
    patch_tsv.main(['-r', ref_path,
                    '-d', '\t',
                    '-i', input_path, '-o', out_path,
                    '-k', '3', '2', '-v', '3'
                    ])
    assert tuple(file_wrapper(out_path)) == ('field1\tfield2\t角色\tjuese\tfield4\n',
                                             'field1\t field2\t角色\tjuese\tfield4\n',)


def test_agg_tsv(tmp_path, capsys):
    """ 测试tsv的聚合工具 """
    # type: (Path) -> None
    # 准备样例tsv文件
    path = (tmp_path / 'evalset').as_posix()
    with file_wrapper(path, 'wt') as f:
        f.write(r"""
わ      わ      笑      14614975
わら      わ      笑      1000
で      で      で      11270299
で      で      で      1000
が      が      が      11097238
""".lstrip('\n'))

    # 1. 按照前三列聚合，sum最后一列
    agg_tsv.main(['--infile', path, '--sep', r'      ',
                  '-k', '0', '1', '2', '-r', '3',
                  '-a', 'sum'])
    captured = capsys.readouterr()
    assert r"""
わ      わ      笑      14614975
わら      わ      笑      1000
で      で      で      11271299
が      が      が      11097238
""".lstrip('\n') == captured.out

    # 2. 按照2~3列聚合，sum最后一列
    agg_tsv.main(['--infile', path, '--sep', r'      ',
                  '-k', '1', '2', '-r', '3',
                  '-a', 'sum'])
    captured = capsys.readouterr()
    assert r"""
わ      笑      14615975
で      で      11271299
が      が      11097238
""".lstrip('\n') == captured.out
