#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
实现 pow(x, n) ，即计算 x 的 n 次幂函数。

示例 1:

输入: 2.00000, 10
输出: 1024.00000

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/7 下午8:46
"""


class Solution(object):
    def myPow(self, x, n):
        # sol1: brute-force
        return x ** n

        # sol2: divide_and_conquer using recursion
        if n < 0:  # 先考虑负次幂
            return 1 / self.myPow(x, -n)
        if n in (0, 1):
            return x ** n
        if n % 2 == 0:
            return self.myPow(x * x, n // 2)  # x*x 比 x**2稳；后者偶尔溢出
        else:
            return self.myPow(x, n - 1) * x

        # sol3: divide_and_conquer iteration
        if n < 0:
            x, n = 1 / x, -n
        power = 1  # 最后累计的积
        while n:  # 对于二进制的n，从右往左取位
            if n & 1:
                power *= x
            x *= x  # 每次x都对自己平方；依次变为 x, x^2, x^4, x^8 ...
            n >>= 1  # 下次取n的左边一位
        return power
