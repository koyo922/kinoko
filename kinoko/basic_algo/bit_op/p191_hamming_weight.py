#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
编写一个函数，输入是一个无符号整数，返回其二进制表达式中数字位数为 ‘1’ 的个数（也被称为汉明重量）。

示例 1：

输入：00000000000000000000000000001011
输出：3
解释：输入的二进制串 00000000000000000000000000001011 中，共有三位为 '1'。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/number-of-1-bits
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/16 下午9:47
"""


class Solution(object):
    def loop(self, n):
        w = 0
        while n:
            w += n & 1
            n >>= 1  # 注意不是 >>
        return w

    def eliminating_last_one(self, n):
        w = 0
        while n:
            n &= n - 1  # 干掉最低位的1
            w += 1
        return w

    def hammingWeight(self, n):
        # return self.loop(n)
        return self.eliminating_last_one(n)
