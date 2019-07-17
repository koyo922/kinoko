#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
假设你正在爬楼梯。需要 n 阶你才能到达楼顶。

每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？

注意：给定 n 是一个正整数。

示例 1：

输入： 2
输出： 2
解释： 有两种方法可以爬到楼顶。
1.  1 阶 + 1 阶
2.  2 阶
示例 2：

输入： 3
输出： 3
解释： 有三种方法可以爬到楼顶。
1.  1 阶 + 1 阶 + 1 阶
2.  1 阶 + 2 阶
3.  2 阶 + 1 阶


来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/climbing-stairs
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/17 下午10:33
"""


class Solution(object):
    def using_array(self, n):
        f = [1, 1]
        for i in range(2, n + 1):
            f.append(f[i - 1] + f[i - 2])
        return f[-1]

    def using_var(self, n):
        a = b = 1
        for _ in range(n - 1):
            a, b = b, a + b
        return b

    def climbStairs(self, n):
        """ 第n楼 的前一步是 n-1 或者 n-2楼  """
        # return self.using_array(n)
        return self.using_var(n)
