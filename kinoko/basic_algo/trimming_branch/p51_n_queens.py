#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
n 皇后问题研究的是如何将 n 个皇后放置在 n×n 的棋盘上，并且使皇后彼此之间不能相互攻击。

给定一个整数 n，返回所有不同的 n 皇后问题的解决方案。

每一种解法包含一个明确的 n 皇后问题的棋子放置方案，该方案中 'Q' 和 '.' 分别代表了皇后和空位。

示例:

输入: 4
输出: [
 [".Q..",  // 解法 1
  "...Q",
  "Q...",
  "..Q."],

 ["..Q.",  // 解法 2
  "Q...",
  "...Q",
  ".Q.."]
]
解释: 4 皇后问题存在两个不同的解法。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/n-queens
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/9 下午10:58
"""


class Solution(object):
    def solveNQueens(self, n):
        self.solutions, self.n = [], n  # 如果把 _dfs()做成闭包，可以省略这两个参数
        self._dfs(cols=[], pie=set(), na=set())
        # 注意两层写法
        return [['.' * c + 'Q' + '.' * (n - 1 - c) for c in cols] for cols in self.solutions]

    def _dfs(self, cols, pie, na):
        r = len(cols)  # 第几行
        if r == self.n:
            self.solutions.append(cols)
            return
        for c in range(self.n):
            if c not in cols and r + c not in pie and r - c not in na:
                # 注意并集写法，不能用加号
                self._dfs(cols + [c], pie | {r + c}, na | {r - c})
