#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给定一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？找出所有满足条件且不重复的三元组。

注意：答案中不可以包含重复的三元组。

例如, 给定数组 nums = [-1, 0, 1, 2, -1, -4]，

满足要求的三元组集合为：
[
  [-1, 0, 1],
  [-1, -1, 2]
]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/3sum
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/4 上午8:46
"""


class Solution(object):
    def bruteforce(self, nums):
        res = set()
        nums.sort()  # 有利于减少重复，减轻判重压力
        for i, x in enumerate(nums):
            for j, y in enumerate(nums[i + 1:], start=i + 1):  # 注意start
                for z in nums[j + 1:]:
                    if x + y + z == 0:
                        res.add((x, y, z))
        return list(res)

    def using_set(self, nums):
        if len(nums) < 3:  # 边界条件
            return []
        res = set()
        nums.sort()  # 先排序，减轻判重压力
        for i, v in enumerate(nums[:-2]):
            if i - 1 >= 0 and nums[i - 1] == v:  # 如果跟左边值相等，避免重复解
                continue
            trap = set()  # 类似two-sum，不过返回的是值而非下标；所以能用set代替dict
            for x in nums[i + 1:]:
                if x in trap:
                    res.add((v, -v - x, x))
                else:
                    trap.add(-v - x)
        return res

    def using_pinch(self, nums):
        res = set()
        nums.sort()
        for i, v in enumerate(nums[:-2]):
            if i - 1 >= 0 and nums[i - 1] == v:  # 重复值跳过
                continue
            l, r = i + 1, len(nums) - 1  # 开始就地两边夹逼，避免了额外空间
            while l < r:
                s = v + nums[l] + nums[r]
                if s < 0:
                    l += 1
                elif s > 0:
                    r -= 1
                else:
                    res.add((v, nums[l], nums[r]))
                    # 如果res是list，则此处要手动去重 while l<r and nums[l+1]==nums[l]: l+=1
                    l += 1
                    r -= 1
        return res

    def threeSum(self, nums):
        # return self.bruteforce(nums)
        # return self.using_set(nums)
        return self.using_pinch(nums)


if __name__ == '__main__':
    print(Solution().threeSum([-1, 0, 1, 2, -1, -4]))
