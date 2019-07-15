#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给出 n 代表生成括号的对数，请你写出一个函数，使其能够生成所有可能的并且有效的括号组合。

例如，给出 n = 3，生成结果为：

[
  "((()))",
  "(()())",
  "(())()",
  "()(())",
  "()()()"
]


来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/generate-parentheses
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/9 下午10:33
"""


class Solution(object):
    def generateParenthesis(self, n):
        self.solutions = []  # 定义成field，减少传参
        self._gen(n, n, '')  # 过程式
        return self.solutions

    def _gen(self, left, right, cur):
        # 定义成"remaining"可以直接减到零，避免传n进来; 如果定义成"used"就需要上界
        if left == right == 0:  # 剩余的左右括号都为零
            self.solutions.append(cur)
            return
        if left > 0:  # 如果尚有左括号可用；直接拼接在尾部，必然合法
            self._gen(left - 1, right, cur + '(')
        if left < right > 0:  # 注意方向 尚余右括号可用，且remaining左括号比右括号少（即, used左括号比较多）才合法
            self._gen(left, right - 1, cur + ')')
