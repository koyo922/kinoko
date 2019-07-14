#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
实现 int sqrt(int x) 函数。

计算并返回 x 的平方根，其中 x 是非负整数。

由于返回类型是整数，结果只保留整数的部分，小数部分将被舍去。

示例 1:

输入: 4
输出: 2
示例 2:

输入: 8
输出: 2
说明: 8 的平方根是 2.82842...,
     由于返回类型是整数，小数部分将被舍去。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/sqrtx
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/14 下午10:03
"""


# from __future__ import division


class Solution(object):
    def using_bisect(self, x):
        if x in (0, 1):  # 避免后面除零
            return x
        l, r = 1, x
        while l <= r:
            m = (l + r) // 2
            # 不要试图用平方去比，比较难处理边界情况 s = m ** 2
            if m == x // m:
                return m
            elif m > x // m:
                r = m - 1
            else:
                l = m + 1
        return (l + r) // 2

    def newton_iter(self, x):
        """
        f(t) = t**2 - x = 0
        t' = t - f(t) / f'(t)
           = t - (t*t - x) / 2*t
           = (t*t + x) / 2*t
           = (t + x/t) / 2
        """
        if x in (0, 1):
            return x
        prev_t, t = 0, 1.0
        while int(t) != int(prev_t):  # 注意还是要比较整数部分
            prev_t, t = t, (t + x / t) / 2
        return int(t)

    def mySqrt(self, x):
        # return self.using_bisect(x)
        return self.newton_iter(x)


if __name__ == '__main__':
    print Solution().mySqrt(8)
