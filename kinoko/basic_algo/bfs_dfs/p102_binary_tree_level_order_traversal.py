#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给定一个二叉树，返回其按层次遍历的节点值。 （即逐层地，从左到右访问所有节点）。

例如:
给定二叉树: [3,9,20,null,null,15,7],

    3
   / \
  9  20
    /  \
   15   7
返回其层次遍历结果：

[
  [3],
  [9,20],
  [15,7]
]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/binary-tree-level-order-traversal
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/7 下午9:55
"""


class Solution(object):
    def bfs(self, root):
        res = []
        row = [root] if root else None  # 注意 根节点为None情况
        while row:
            res.append([n.val for n in row])  # 注意写法，先加有效行；避免事后append一个[]
            row = [k for n in row for k in (n.left, n.right) if k]
        return res

    def pseudo_dfs(self, level, root):
        if root is None:
            return
        if level + 1 > len(self.layers):  # 必要时拓展层深
            self.layers.append([])
        self.layers[level].append(root.val)
        self.pseudo_dfs(level + 1, root.left)
        self.pseudo_dfs(level + 1, root.right)

    def levelOrder(self, root):
        # sol1: BFS
        return self.bfs(root)

        # sol2: 伪DFS, 沿途记下来层深度，放入相应的层
        self.layers = []
        self.pseudo_dfs(0, root)
        return self.layers
