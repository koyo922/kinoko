#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给定一个二维网格 board 和一个字典中的单词列表 words，找出所有同时在二维网格和字典中出现的单词。

单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母在一个单词中不允许被重复使用。

示例:

输入:
words = ["oath","pea","eat","rain"] and board =
[
  ['o','a','a','n'],
  ['e','t','a','e'],
  ['i','h','k','r'],
  ['i','f','l','v']
]

输出: ["eat","oath"]
说明:
你可以假设所有输入都由小写字母 a-z 组成。

提示:

你需要优化回溯算法以通过更大数据量的测试。你能否早点停止回溯？
如果当前单词不存在于所有单词的前缀中，则可以立即停止回溯。什么样的数据结构可以有效地执行这样的操作？散列表是否可行？为什么？ 前缀树如何？如果你想学习如何实现一个基本的前缀树，请先查看这个问题： 实现Trie（前缀树）。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/word-search-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/15 下午10:50
"""


class Solution(object):
    def findWords(self, board, words):
        if not board or not board[0] or not words:  # 注意空行
            return []

        self.results = set()  # 结果去重

        # 构造Trie
        self.EOW = '#'
        root = dict()
        for word in words:
            node = root
            for c in word:
                node = node.setdefault(c, dict())
            node[self.EOW] = True

        # 注意行列数可能不同
        self.M, self.N = len(board), len(board[0])
        for i, row in enumerate(board):
            for j, c in enumerate(row):
                if c in root:
                    self._dfs(board, i, j, '', root)

        return list(self.results)  # 题目要求返回list

    def _dfs(self, board, i, j, cur_word, cur_dict):
        # 传进来的时候 还没改 cur_word, cur_dict
        c = board[i][j]
        cur_word += c
        cur_dict = cur_dict[c]

        if self.EOW in cur_dict:
            self.results.add(cur_word)

        board[i][j] = '@'  # placeholder
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = i + dx, j + dy
            if 0 <= x < self.M and 0 <= y < self.N:
                t = board[x][y]
                if t != '@' and t in cur_dict:  # 如果这个方向没有任何前缀，就放弃搜索
                    self._dfs(board, x, y, cur_word, cur_dict)
        board[i][j] = c
