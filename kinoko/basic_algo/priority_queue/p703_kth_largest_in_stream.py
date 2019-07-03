#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
设计一个找到数据流中第K大元素的类（class）。注意是排序后的第K大元素，不是第K个不同的元素。

你的 KthLargest 类需要一个同时接收整数 k 和整数数组nums 的构造器，它包含数据流中的初始元素。
每次调用 KthLargest.add，返回当前数据流中第K大的元素。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/kth-largest-element-in-a-stream
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/2 上午7:57
"""

import heapq


class KthLargest(object):

    def __init__(self, k, nums):
        self.k = k
        # python中的堆不支持设置size, 注意不要写成
        # heapq.heapify(nums)
        # self.nums = nums
        self.nums = []
        for v in nums:
            heapq.heappush(self.nums, v)
            if len(self.nums) > k:  # 注意自己控制size
                heapq.heappop(self.nums)

    def add(self, val):
        if len(self.nums) < self.k:
            heapq.heappush(self.nums, val)
        elif self.nums[0] < val:  # 如果val比当前的第k大 还小，就不考虑
            heapq.heapreplace(self.nums, val)  # 注意是 先pop再push
        return self.nums[0]  # size为k的 min-heap的堆顶，恰好是 kth-largest
