#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给定一个二叉树，找出其最小深度。

最小深度是从根节点到最近叶子节点的最短路径上的节点数量。

说明: 叶子节点是指没有子节点的节点。

示例:

给定二叉树 [3,9,20,null,null,15,7],

    3
   / \
  9  20
    /  \
   15   7
返回它的最小深度  2.

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/minimum-depth-of-binary-tree
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/8 下午10:34
"""
from __future__ import unicode_literals, print_function

from kinoko.basic_algo.definitions import TreeNode


class Solution(object):
    def bfs(self, root):
        if not root:
            return 0
        row, depth = [root], 1
        while row:
            nrow = []
            for n in row:
                kids = tuple(e for e in (n.left, n.right) if e)
                if not kids:  # 上一层的某个节点是叶子节点
                    return depth
                nrow += kids
            row, depth = nrow, depth + 1
        assert False

    def dfs(self, root):
        if not root:
            return 0
        l, r = self.dfs(root.left), self.dfs(root.right)
        # 如果两边都非零，就取min+1 ； 否则取较深那边+1
        return (1 + min(l, r)) if (l and r) else (l + r + 1)

    def minDepth(self, root):
        return self.bfs(root)
        # return self.dfs(root)


if __name__ == '__main__':
    root = TreeNode.from_json('[3,9,20,null,null,15,7]')
    print(Solution().bfs(root))
