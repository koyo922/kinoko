#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给定不同面额的硬币 coins 和一个总金额 amount。编写一个函数来计算可以凑成总金额所需的最少的硬币个数。如果没有任何一种硬币组合能组成总金额，返回 -1。

示例 1:

输入: coins = [1, 2, 5], amount = 11
输出: 3
解释: 11 = 5 + 5 + 1
示例 2:

输入: coins = [2], amount = 3
输出: -1
说明:
你可以认为每种硬币的数量是无限的。



来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/coin-change
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/23 上午7:57
"""


class Solution(object):
    def coinChange(self, coins, amount):
        """
        等价于爬楼梯问题，每次可以爬 coins[:] 中的任意一种步长
        转移方程 f[i] = min(f[i-c] for c in coins) + 1
        """
        f = [0] + [-1] * amount  # 默认为-1，表示不可达
        for i in range(1, amount + 1):
            # 注意 同时要求 start_points中的每个元素都要可达(>=0)
            start_points = [f[i - c] for c in coins if i - c >= 0 and f[i - c] >= 0]
            if start_points:
                f[i] = min(start_points) + 1
        return f[amount]
