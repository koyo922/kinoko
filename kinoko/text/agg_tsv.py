#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
聚合tsv文件的某些列

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/6/27 下午11:20
"""
from __future__ import unicode_literals, print_function, division

import argparse
import sys
from collections import OrderedDict

import six
import tqdm
from typing import Text

from ..misc.log_writer import init_log
from ..text.io import file_wrapper

logger = init_log(__name__)


def main(console_args=None, agg_func=None):
    """ 逻辑入口 """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', type=Text, default='/dev/stdin')
    parser.add_argument('-o', '--outfile', type=Text, default='/dev/stdout')
    parser.add_argument('--sep', type=Text, default='\t')
    parser.add_argument('-k', '--keep_cols', type=int, nargs='+')
    parser.add_argument('-r', '--reduce_col', type=int)
    parser.add_argument('-t', '--output_template', type=Text, default=None)
    parser.add_argument('-a', '--agg_func', type=Text, choices=('sum', 'mean', 'first', 'last', 'callback'),
                        default='sum')
    args = parser.parse_args(console_args or sys.argv[1:])
    if args.agg_func == 'sum':
        args.agg_func = lambda x: sum((float(v) if '.' in v else int(v)) for v in x)
    elif args.agg_func == 'mean':  # pragma: no cover
        args.agg_func = lambda x: sum(x) / len(x)
    elif args.agg_func == 'first':  # pragma: no cover
        args.agg_func = lambda x: x[0]
    elif args.agg_func == 'last':  # pragma: no cover
        args.agg_func = lambda x: x[-1]
    else:  # pragma: no cover
        assert args.agg_func is not None
        args.agg_func = agg_func

    logger.info('loading file: %s', args.infile)
    cache = OrderedDict()
    for line in file_wrapper(args.infile):
        fields = line.rstrip('\n').split(args.sep)
        k = tuple(fields[i] for i in args.keep_cols)
        v = fields[args.reduce_col]
        cache.setdefault(k, []).append(v)

    all_fields = set(args.keep_cols) | {args.reduce_col, }
    if args.output_template is None:
        template = args.sep.join('{{${}}}'.format(f) for f in sorted(all_fields))
    else:  # pragma: no cover
        template = args.output_template

    logger.info('aggregate and dumping')
    fout = file_wrapper(args.outfile, 'wt')
    for k, v in tqdm.tqdm(six.iteritems(cache), desc='aggregating', total=len(cache)):
        col_mapping = {'${}'.format(idx): val for idx, val in zip(args.keep_cols, k)}
        col_mapping['${}'.format(args.reduce_col)] = Text(args.agg_func(v))
        fout.write(template.format(**col_mapping) + '\n')
    fout.flush()
    if 'pytest' not in sys.modules:  # pragma: no cover
        fout.close()


if __name__ == '__main__':
    main()  # pragma: no cover
