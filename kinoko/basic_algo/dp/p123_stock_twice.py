#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给定一个数组，它的第 i 个元素是一支给定的股票在第 i 天的价格。

设计一个算法来计算你所能获取的最大利润。你最多可以完成 两笔 交易。

注意: 你不能同时参与多笔交易（你必须在再次购买前出售掉之前的股票）。

示例 1:

输入: [3,3,5,0,0,3,1,4]
输出: 6
解释: 在第 4 天（股票价格 = 0）的时候买入，在第 6 天（股票价格 = 3）的时候卖出，这笔交易所能获得利润 = 3-0 = 3 。
     随后，在第 7 天（股票价格 = 1）的时候买入，在第 8 天 （股票价格 = 4）的时候卖出，这笔交易所能获得利润 = 4-1 = 3 。
示例 2:

输入: [1,2,3,4,5]
输出: 4
解释: 在第 1 天（股票价格 = 1）的时候买入，在第 5 天 （股票价格 = 5）的时候卖出, 这笔交易所能获得利润 = 5-1 = 4 。  
     注意你不能在第 1 天和第 2 天接连购买股票，之后再将它们卖出。  
     因为这样属于同时参与了多笔交易，你必须在再次购买前出售掉之前的股票。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-iii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/19 下午12:23
"""


class Solution(object):
    def using_arr(self, prices):
        """
        直观上，定义DP状态应该与日期有关 max_profit := mp[i] 表示 到第i天为止的最大收益
        但是，这样一维的状态定义 无法反映题意要求的 交易规则约束； 可以通过添加状态维度来细化转移约束
        mp[i][k][j] := 第i天，已经交易了k笔，手上持有j股的情况下，最大收益
        则，最后结果为 max(mp[T][:][0])
        转移方程为
        mp[i][k][0] = max(mp[i-1][k][0], mp[i-1][k-1][1] + prices[i]) # 可以什么都不做或者卖出
        mp[i][k][1] = max(mp[i-1][k][1], mp[i-1][k-1][0] - prices[i]) # 可以什么都不做或者买入
        """
        if not prices:  # 边界条件
            return 0
        mp = [[[0 for j in range(2)] for k in range(3)] for i in range(len(prices))]
        mp[0][0][0], mp[0][0][1] = 0, -prices[0]
        mp[0][1] = mp[0][2] = [-float('inf')] * 2  # 0时刻就交易过1/2次，是不可能的

        for i, e in enumerate(prices[1:], start=1):  # 注意 start=1
            mp[i][0][0] = mp[i - 1][0][0]  # i时刻交易过0次且持有0股，必然只能来源于前一时刻同样状态
            mp[i][0][1] = max(mp[i - 1][0][1], mp[i - 1][0][0] - e)  # 可以啥都不做或者买入; 注意只有"卖出"时占用交易次数

            mp[i][1][0] = max(mp[i - 1][1][0], mp[i - 1][0][1] + e)  # 可能卖出
            mp[i][1][1] = max(mp[i - 1][1][1], mp[i - 1][1][0] - e)  # 可能买入

            mp[i][2][0] = max(mp[i - 1][2][0], mp[i - 1][1][1] + e)  # 可能卖出
            # mp[i][2][1] 交易完两次后再买入，多余的那次买入必然不划算，无需考虑
        return max(mp[-1][k][0] for k in range(3))

    def dp_compress(self, prices):
        """
        去掉时间轴；手上的状态有4种
        # hold0 未进行任何交易，就是0，不用考虑
        hold1 刚刚买完第一股
        release1 刚刚卖完第一股
        hold2 ...
        release2 ...
        """
        hold1, hold2 = -float('inf'), -float('inf')
        release1 = release2 = 0
        for p in prices:  # 下面四句应该倒着写，以免干扰；不过，顺着也没报错
            hold1 = max(hold1, -p)
            release1 = max(release1, hold1 + p)
            hold2 = max(hold2, release1 - p)
            release2 = max(release2, hold2 + p)
        return release2

    def maxProfit(self, prices):
        # return self.using_arr(prices)
        return self.dp_compress(prices)


if __name__ == '__main__':
    print Solution().maxProfit([3, 3, 5, 0, 0, 3, 1, 4])
