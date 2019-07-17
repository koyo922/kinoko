#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给定一个三角形，找出自顶向下的最小路径和。每一步只能移动到下一行中相邻的结点上。

例如，给定三角形：

[
     [2],
    [3,4],
   [6,5,7],
  [4,1,8,3]
]
自顶向下的最小路径和为 11（即，2 + 3 + 5 + 1 = 11）。

说明：

如果你可以只使用 O(n) 的额外空间（n 为三角形的总行数）来解决这个问题，那么你的算法会很加分。



来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/triangle
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/17 下午10:54
"""


class Solution(object):
    def naive_dp(self, triangle):
        """
        每个位置的路径cost等于其后继最优cost+自身cost
        f[i][j] = min(f[i + 1][j], f[i + 1][j + 1]) + triangle[i][j]
        """
        N = len(triangle)
        f = [[0] * rs for rs in range(1, N + 1)]

        f[-1] = triangle[-1]  # 最底层一样
        for i in range(N - 2, -1, -1):  # 从倒数第二层开始往上递推
            # 这里j从左往右或者倒过来都可以；(压缩时只能从左往右)
            for j in range(i + 1):  # 注意j的范围
                f[i][j] = min(f[i + 1][j], f[i + 1][j + 1]) + triangle[i][j]
        return f[0][0]

    def dp_compress(self, triangle):
        """
        每次实际上只用到了下面一行而已，可以压缩
        """
        below = triangle[-1]
        for i in range(len(triangle) - 2, -1, -1):
            # 注意这里只能从左往右, 因为 below[j]依赖于 below[j+1]，即右方元素
            for j in range(i + 1):
                below[j] = min(below[j], below[j + 1]) + triangle[i][j]
        return below[0]

    def minimumTotal(self, triangle):
        # 也可以直接DFS暴力搜索+memorize
        # return self.naive_dp(triangle)
        return self.dp_compress(triangle)


if __name__ == '__main__':
    print Solution().minimumTotal([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]])
