#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给定一个整数数组 nums ，找出一个序列中乘积最大的连续子序列（该序列至少包含一个数）。

示例 1:

输入: [2,3,-2,4]
输出: 6
解释: 子数组 [2,3] 有最大乘积 6。
示例 2:

输入: [-2,0,-1]
输出: 0
解释: 结果不能为 2, 因为 [-2,-1] 不是子数组。


来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/maximum-product-subarray
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/19 上午10:51
"""


class Solution(object):
    def using_array(self, nums):
        """
        状态
            M[i]:= 以nums[i] 结尾的最大值
            m[i]:= 以nums[i] 结尾的最小值
        结果
            max(M)
        递推式 (可以接续前一个节点，也可以新开区间)
            M[i] = max(M[i-1] * nums[i], m[i-1] * nums[i], nums[i])
            m[i] = min(M[i-1] * nums[i], m[i-1] * nums[i], nums[i])
        """
        M, m = [nums[0]], [nums[0]]
        for i, e in enumerate(nums[1:], start=1):
            candidates = M[i - 1] * e, m[i - 1] * e, e
            M.append(max(candidates))
            m.append(min(candidates))
        return max(M)

    def dp_compress(self, nums):
        """
        观察发现只依赖于前一个时刻的DP状态，可以压缩
        M 和 m 分别表示 curMax, curMin
        则递推公式为
        M = max(M*e, m*e, e)
        m = min(M*e, m*e, e)
        res = max(res, M)
        """
        res = M = m = nums[0]
        for e in nums[1:]:
            candidates = M * e, m * e, e
            M, m = max(candidates), min(candidates)
            res = max(res, M)
        return res

    def maxProduct(self, nums):
        # return self.using_array(nums)
        return self.dp_compress(nums)
