#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
辅助debug leetcode样例输出的工具

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/8 下午11:07
"""
from __future__ import unicode_literals

import six

import json


# Definition for a binary tree node.
@six.python_2_unicode_compatible
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

    @classmethod
    def from_json(cls, json_line):
        """
        解析leetcode官网给出的，用完全数组格式描述的二叉树

        >>> root = TreeNode.from_json("[3,9,20,null,null,15,7]")
        >>> root.to_json()
        '[3, 9, 20, null, null, 15, 7]'

        :param json_line: 可能含有 "null" 的json串
        :return: 构造出来的二叉树的根节点
        """
        node_vals = json.loads(json_line)
        if not node_vals:
            return None
        nodes = [(None if v is None else TreeNode(v)) for v in node_vals]
        for i, n in enumerate(nodes[1:], start=1):
            parent = nodes[(i - 1) // 2]
            if i % 2 == 0:
                parent.right = n
            else:
                parent.left = n
        return nodes[0]

    @staticmethod
    def max_depth(root):
        if not root:
            return 0
        if root == 'self':
            return TreeNode.max_depth(root)
        return 1 + max(TreeNode.max_depth(root.left), TreeNode.max_depth(root.right))

    def fill_to_complete(self, idx, node, nodes):
        nodes[idx] = node
        if node.left:
            self.fill_to_complete(idx * 2 + 1, node.left, nodes)
        if node.right:
            self.fill_to_complete(idx * 2 + 2, node.right, nodes)

    def to_complete(self):
        complete_size = 1
        for d in range(TreeNode.max_depth(self) - 1):
            complete_size = (complete_size << 1) + 1
        nodes = [None] * complete_size
        self.fill_to_complete(0, self, nodes)
        return nodes

    def to_json(self):
        return json.dumps([(n.val if n else None) for n in self.to_complete()])

    def __str__(self):
        return '({} -> {}, {})'.format(self.val, (self.left.val if self.left else None),
                                     (self.right.val if self.right else None))

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    "[3, 9, 20, null, null, 15, 7]"
