#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给定一个二叉搜索树, 找到该树中两个指定节点的最近公共祖先。

百度百科中最近公共祖先的定义为：“对于有根树 T 的两个结点 p、q，最近公共祖先表示为一个结点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（一个节点也可以是它自己的祖先）。”

例如，给定如下二叉搜索树:  root = [6,2,8,0,4,7,9,null,null,3,5]

示例 1:

输入: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8
输出: 6
解释: 节点 2 和节点 8 的最近公共祖先是 6。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/lowest-common-ancestor-of-a-binary-search-tree
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/6 下午12:44
"""


class Solution(object):
    def recursion(self, root, p, q):
        if p.val < root.val > q.val:  # 如果root比两边都大，说明要往左子树搜索
            return self.recursion(root.left, p, q)
        if p.val > root.val < q.val:
            return self.recursion(root.right, p, q)
        return root

    def iteration(self, root, p, q):
        while root:  # 上述递归算法的 TCO版本
            if p.val < root.val > q.val:
                root = root.left
            elif p.val > root.val < q.val:
                root = root.right
            else:
                return root

    def lowestCommonAncestor(self, root, p, q):
        # return self.recursion(root, p, q)
        return self.iteration(root, p, q)
