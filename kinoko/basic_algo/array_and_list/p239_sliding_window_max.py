#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给定一个数组 nums，有一个大小为 k 的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口 k 内的数字。滑动窗口每次只向右移动一位。

返回滑动窗口最大值。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/sliding-window-maximum
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/2 上午8:33
"""


class Solution(object):
    def by_heap(self, nums, k):
        raise NotImplemented

    def by_deque(self, nums, k):
        """
        原理在于
        1. window_size 固定
        2. 窗口内 比自己老且小的元素必然不会 成为结果，可以去掉
        """
        from collections import deque

        if len(nums) < k:  # 严谨习惯
            return []

        # 前k个直接入队，记录下标和值
        window = deque([])
        res = []
        # 每来一个新元素，看看队首是否需要过期，然后干掉比它小且老的元素，自己入队
        for i, v in enumerate(nums):
            while window and window[0][0] <= i - k:  # 队首可能过期
                window.popleft()
            while window and window[-1][1] <= v:  # 干掉左侧<=自己的; 注意判断队空
                window.pop()
            window.append((i, v))  # 自己入队
            if i >= k - 1:  # 注意从k-1开始，就要每次抛出窗口内最大值了
                res.append(window[0][1])  # 返回队首（必然是窗口内最大值）
        return res

    def maxSlidingWindow(self, nums, k):
        return self.by_deque(nums, k)


if __name__ == '__main__':
    obj = Solution()
    print(obj.maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3))
