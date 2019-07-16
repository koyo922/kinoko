#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
n 皇后问题研究的是如何将 n 个皇后放置在 n×n 的棋盘上，并且使皇后彼此之间不能相互攻击。

给定一个整数 n，返回 n 皇后不同的解决方案的数量。

示例:

输入: 4
输出: 2
解释: 4 皇后问题存在如下两个不同的解法。
[
 [".Q..",  // 解法 1
  "...Q",
  "Q...",
  "..Q."],

 ["..Q.",  // 解法 2
  "Q...",
  "...Q",
  ".Q.."]
]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/n-queens-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/16 下午10:30
"""


class Solution(object):
    def _dfs(self, row, col, pie, na):
        if row >= self.N:
            self.cnt += 1
            return
        # 注意 pie 是当前所有的"撇"在本行的阴影
        bits = ~(col | pie | na) & self.LOWER_N_BITS  # 得到所有的有效位
        while bits:
            b = bits & -bits  # 最低有效位
            # pie是阴影，在下一行会左移一格
            self._dfs(row + 1, col | b, (pie | b) << 1, (na | b) >> 1)
            bits &= (bits - 1)  # 干掉最低有效位

    def totalNQueens(self, n):
        """
        DFS + 位运算
        """
        self.cnt, self.N, self.LOWER_N_BITS = 0, n, (1 << n) - 1
        self._dfs(0, 0, 0, 0)
        return self.cnt
