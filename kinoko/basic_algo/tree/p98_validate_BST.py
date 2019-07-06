#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给定一个二叉树，判断其是否是一个有效的二叉搜索树。

假设一个二叉搜索树具有如下特征：

节点的左子树只包含小于当前节点的数。
节点的右子树只包含大于当前节点的数。
所有左子树和右子树自身必须也是二叉搜索树。
示例 1:

输入:
    2
   / \
  1   3
输出: true

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/validate-binary-search-tree
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/6 上午11:08
"""


class Solution(object):
    def inorder(self, node):
        if node:
            for n in self.inorder(node.left):
                yield n
            yield node
            for n in self.inorder(node.right):  # 拷代码时记得改成right
                yield n

    def recursion(self, node, lower, upper):
        if node is None:
            return True
        if not (lower < node.val < upper):
            return False
        return self.recursion(node.left, lower, node.val) and self.recursion(node.right, node.val, upper)

    def isValidBST(self, root):
        # # 中序遍历必须升序
        # pre = float('-inf')
        # for n in self.inorder(root):
        #     if n.val <= pre:
        #         return False
        #     pre = n.val
        # return True

        # 递归判断
        return self.recursion(root, float('-inf'), float('inf'))
