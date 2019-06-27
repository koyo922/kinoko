#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
使用参考文件，对 csv/tsv 文件进行修补
e.g.

<reference.txt>内容如下:
jiaose 角色 juese
xxx 色情词 <DEL>

<file_to_patch>内容如下:
field1 field2 角色 jiaose field4
field1 field2 色情词 xxx field4

<result直接写到stdout>,内容如下:
field1 field2 角色 juese field4

命令行用法举例
patchtsv -r input/ref1.txt input/ref2.txt \
    -i ./input/infile.txt \
    -o ./input/outfile.txt \
    -k 0 1 -v 0


Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/6/27 下午11:20
"""
from __future__ import unicode_literals, print_function

import sys
from typing import Text

import argparse

from ..func import strip_fields
from ..text.io import file_wrapper


def main(console_args=sys.argv[1:], key_fmt_fn=strip_fields):
    """
    入口
    :param console_args:
    :param key_fmt_fn: 对key的格式化函数；默认为 simeji_nlp_py.func.strip_fields
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--ref', required=True, nargs='+', type=Text, help='path to reference file(s)')
    parser.add_argument('-d', '--delimeter', default='\t')
    parser.add_argument('-i', '--input', type=Text, default='/dev/stdin', help='path to the file being patched')
    parser.add_argument('-o', '--output', type=Text, default='/dev/stdout')
    parser.add_argument('-k', nargs='+', type=int, default=[0])
    parser.add_argument('-v', type=int, default=-1)
    args = parser.parse_args(console_args)

    # 参考文件 读取成 规则
    rules = dict()
    for ref_path in args.ref:  # 遍历多个参考文件（可以是一个）
        for line in file_wrapper(ref_path):
            sp = line.rstrip('\n').split(args.delimeter)
            rules[tuple(sp[:-1])] = sp[-1]

    fout = file_wrapper(args.output, mode='wt')
    for line in file_wrapper(args.input):
        segs = line.rstrip('\n').split(args.delimeter)
        key = key_fmt_fn(tuple(segs[i] for i in args.k))
        tgt_value = rules.get(key)
        if tgt_value is None:
            pass
        elif tgt_value == '<DEL>':
            continue
        else:
            # 注意，不是直接整体代换，而是replace掉非空格部分
            old_tgt_val = segs[args.v]  # 旧值有空格 ' いまか'
            # 替换新值也要保留空格
            segs[args.v] = old_tgt_val.replace(old_tgt_val.strip(), tgt_value)

        try:
            fout.write(args.delimeter.join(segs) + '\n')
        except IOError as ex:
            if ex.errno == 32:  # broken pipe by downstream `head`
                break
            else:
                raise


if __name__ == '__main__':
    main()
