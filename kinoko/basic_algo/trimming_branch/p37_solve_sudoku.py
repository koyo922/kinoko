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

    def is_valid(self, board, row, col, v):
        cell_x, cell_y = (row // 3) * 3, (col // 3) * 3  # cell左上角坐标; 注意还要乘以3
        for i in range(self.N):  # 遍历的不是行或者列或者cell；而是一起逐个遍历
            x, y = divmod(i, 3)  # cell内部的 行/列偏移
            if v in (board[i][col], board[row][i], board[cell_x + x][cell_y + y]):
                return False
        return True

    def naive(self, board):
        for i in range(self.N):
            for j in range(self.N):
                if board[i][j] != '.':
                    continue
                for v in map(str, range(1, 10)):  # 遍历尝试 1~9
                    if not self.is_valid(board, i, j, v):
                        continue
                    board[i][j] = v
                    ret = self.naive(board)  # 只要求就地改动，也可以只返回bool
                    if ret:
                        return ret
                    board[i][j] = '.'
                return None
        return board

    def solveSudoku(self, board):
        self.N = len(board)
        return self.naive(board)  # 此题要求就地改动；但是这里也返回了正确的值


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
