#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给定一个大小为 n 的数组，找到其中的众数。众数是指在数组中出现次数大于 ⌊ n/2 ⌋ 的元素。

你可以假设数组是非空的，并且给定的数组总是存在众数。

示例 1:

输入: [3,2,3]
输出: 3

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/majority-element
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/7 下午9:21
"""


class Solution(object):
    def majorityElement(self, nums):
        # sol1: brute-force
        from collections import Counter
        return Counter(nums).most_common(1)[0][0]

        # sol2: 摩尔投票法,O(n)的时间复杂度
        cnt = 0
        for n in nums:
            if cnt == 0:  # 当前候选跌空，换候选
                cand = n
            if n == cand:  # 如果命中候选则加1
                cnt += 1
            else:  # 否则减1
                cnt -= 1
        return cand  # 真正的众数总能 耗光前面的候选并自己坚持到最后

        # sol3: 排序后取中位数
        nums.sort()
        return nums[len(nums) // 2]
