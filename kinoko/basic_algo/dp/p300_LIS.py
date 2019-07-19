#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给定一个无序的整数数组，找到其中最长上升子序列的长度。

示例:

输入: [10,9,2,5,3,7,101,18]
输出: 4
解释: 最长的上升子序列是 [2,3,7,101]，它的长度是 4。
说明:

可能会有多种最长上升子序列的组合，你只需要输出对应的长度即可。
你算法的时间复杂度应该为 O(n2) 。
进阶: 你能将算法的时间复杂度降低到 O(n log n) 吗?



来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/longest-increasing-subsequence
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/19 下午2:01
"""


class Solution(object):
    def dp(self, nums):
        """
        f[i] := 以nums[i]结尾的最大长度
        结果为 max(f)
        转移方程为 f[i] = max(f[j] for j < i if nums[j] < nums[i]) + 1
        i,j 两层循环 O(N^2)
        """
        if not nums:
            return 0
        f = [1]
        for i, e in enumerate(nums[1:], start=1):
            # 注意提供默认值， py3.4可以写 max(..., default=...)
            f.append(max([f[j] for j in range(i) if nums[j] < e] or [0]) + 1)
        return max(f)

    def bisect(self, nums):
        """
        可以维护一个截止当前的 LIS数组
        - 如果发现更大的数，直接append
        - 否则把LIS中最接近的上界压低; 这里由于LIS有序，可以用二分查找, O(N*logN)
        """
        from bisect import bisect_left
        LIS = []
        for n in nums:
            if not LIS or LIS[-1] < n:
                LIS.append(n)
            idx = bisect_left(LIS, n)
            LIS[idx] = n
        return len(LIS)

    def lengthOfLIS(self, nums):
        # return self.dp(nums)
        return self.bisect(nums)
