#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
编写一个程序，通过已填充的空格来解决数独问题。

一个数独的解法需遵循如下规则：

数字 1-9 在每一行只能出现一次。
数字 1-9 在每一列只能出现一次。
数字 1-9 在每一个以粗实线分隔的 3x3 宫内只能出现一次。
空白格用 '.' 表示。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/sudoku-solver
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/9 下午11:27
"""


class Solution(object):
    default_hint = set(map(str, range(1, 10)))

    def possible_candidates(self, board, i, j, hint=default_hint):
        cell_x, cell_y = (i // 3) * 3, (j // 3) * 3
        used = set(board[i]) | {board[I][j] for I in range(self.N)}
        for d in range(self.N):
            dx, dy = divmod(d, 3)
            used.add(board[cell_x + dx][cell_y + dy])
        return hint - used

    def naive(self, board, depth):
        if depth >= len(self.candidates):
            return board
        (i, j), pre_calc_cands = self.candidates[depth]
        for v in self.possible_candidates(board, i, j, hint=pre_calc_cands):  # 遍历尝试可行的选项
            board[i][j] = v
            ret = self.naive(board, depth + 1)  # 只要求就地改动，也可以只返回bool
            if ret:
                return ret
            board[i][j] = '.'
        return None

    def get_candidates(self, board):
        """ 预处理，算好每个坑位的可行选项 """
        candidates = dict()
        for i in range(self.N):
            for j in range(self.N):
                if board[i][j] != '.':  # 注意不要把题目给出数字的位置当做坑位
                    continue
                candidates[(i, j)] = self.possible_candidates(board, i, j)
        self.candidates = candidates.items()
        self.candidates.sort(key=lambda x: len(x[1]))  # 优先解决选项少的坑位

    def solveSudoku(self, board):
        self.N = len(board)
        self.get_candidates(board)
        return self.naive(board, depth=0)  # 此题要求就地改动；但是这里也返回了正确的值


if __name__ == '__main__':
    board = [["5", "3", ".", ".", "7", ".", ".", ".", "."],
             ["6", ".", ".", "1", "9", "5", ".", ".", "."],
             [".", "9", "8", ".", ".", ".", ".", "6", "."],
             ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
             ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
             ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
             [".", "6", ".", ".", ".", ".", "2", "8", "."],
             [".", ".", ".", "4", "1", "9", ".", ".", "5"],
             [".", ".", ".", ".", "8", ".", ".", "7", "9"]]
    res = Solution().solveSudoku(board)
    assert res == board
    print(board)
