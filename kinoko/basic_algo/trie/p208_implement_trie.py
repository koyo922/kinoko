#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
实现一个 Trie (前缀树)，包含 insert, search, 和 startsWith 这三个操作。

示例:

Trie trie = new Trie();

trie.insert("apple");
trie.search("apple");   // 返回 true
trie.search("app");     // 返回 false
trie.startsWith("app"); // 返回 true
trie.insert("app");
trie.search("app");     // 返回 true
说明:

你可以假设所有的输入都是由小写字母 a-z 构成的。
保证所有输入均为非空字符串。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/implement-trie-prefix-tree
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/14 下午10:46
"""


class Trie(object):

    def __init__(self):
        self.root = dict()  # 注意不要过度设计，不要把Trie做成类似Node的类
        self.EOW = '#'  # end of word

    def insert(self, word):
        node = self.root
        for c in word:
            node = node.setdefault(c, dict())  # 注意此处写法
        node[self.EOW] = True  # 这里值无所谓，关键是 self.EOW in node

    def _find_path(self, word):
        node = self.root
        for c in word:
            if c not in node:
                return None
            node = node[c]  # 记得
        return node

    def search(self, word):
        node = self._find_path(word)
        return node is not None and self.EOW in node  # 注意先判断None

    def startsWith(self, prefix):
        return self._find_path(prefix) is not None
