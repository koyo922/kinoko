#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。

你可以假设每种输入只会对应一个答案。但是，你不能重复利用这个数组中同样的元素。

示例:

给定 nums = [2, 7, 11, 15], target = 9

因为 nums[0] + nums[1] = 2 + 7 = 9
所以返回 [0, 1]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/two-sum
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/4 上午8:17
"""


class Solution(object):
    def bruteforce(self, nums, target):
        for i, x in enumerate(nums[:-1]):  # 暴力法适合写测试baseline
            for j, y in enumerate(nums[i + 1:], start=i + 1):
                if x + y == target:
                    return i, j

    def using_dict(self, nums, target):
        met = dict()  # n -> idx
        for i, n in enumerate(nums):
            if target - n in met:
                return met[target - n], i
            met[n] = i  # 注意想清楚 n 和 target-n 的写法；可以对调但是不要乱
        assert False

    def twoSum(self, nums, target):
        # return self.bruteforce(nums, target)
        return self.using_dict(nums, target)


if __name__ == '__main__':
    s = Solution()
    print(s.twoSum(nums=[2, 7, 11, 15], target=9))
