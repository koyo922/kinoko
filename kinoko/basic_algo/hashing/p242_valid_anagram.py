#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给定两个字符串 s 和 t ，编写一个函数来判断 t 是否是 s 的字母异位词。

示例 1:

输入: s = "anagram", t = "nagaram"
输出: true

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/valid-anagram
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/4 上午8:05
"""


class Solution(object):
    def using_sort(self, s, t):
        return sorted(s) == sorted(t)  # 排序 O(NlogN)

    def using_dict(self, s, t):
        from collections import Counter
        return Counter(s) == Counter(t)  # hashmap存每个字符 O(1)*N

    def _str2arr(self, s):
        count = [0] * 26  # 全小写字母，可以手动用list模拟hash
        for c in s:
            count[ord(c) - ord('a')] += 1
        return count

    def using_hand_dict(self, s, t):
        return self._str2arr(s) == self._str2arr(t)  # 比Counter稍快

    def isAnagram(self, s, t):
        return self.using_hand_dict(s, t)
