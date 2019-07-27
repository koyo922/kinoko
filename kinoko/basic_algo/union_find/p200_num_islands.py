#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给定一个由 '1'（陆地）和 '0'（水）组成的的二维网格，计算岛屿的数量。一个岛被水包围，并且它是通过水平方向或垂直方向上相邻的陆地连接而成的。你可以假设网格的四个边均被水包围。

示例 1:

输入:
11110
11010
11000
00000

输出: 1
示例 2:

输入:
11000
11000
00100
00011

输出: 3

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/number-of-islands
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/25 下午10:42
"""
from collections import deque


class UnionFind(object):
    def __init__(self, points):
        self.root = {p: p for p in points}

    def find(self, p):
        # 沿途收集所有路劲上的节点
        path = []
        while p != self.root[p]:  # 注意 需要while找到真正的根
            path.append(p)
            p = self.root[p]
        for e in path:  # 将沿途点都直接指向根
            self.root[e] = p
        # 上述标准写法的效率跟 近似写法差不多
        # while p != self.root[p]; self.root[p] = p = self.root[self.root[p]]
        return p

    def union(self, p, q, callback=None):
        P, Q = self.find(p), self.find(q)
        if P != Q:
            self.root[P] = Q
            callback()


class Solution(object):

    def floodfill(self, grid):
        if not grid or not grid[0]:  # 空的边界情况
            return 0
        m, n = len(grid), len(grid[0])

        def sink_dfs(i, j):
            if 0 <= i < m and 0 <= j < n and grid[i][j] == '1':
                grid[i][j] = '0'  # 注意 这里不要忘记
                # py3要再套一层tuple, lazy-map; 注意两个参数的写法
                map(sink_dfs, (i - 1, i + 1, i, i), (j, j, j - 1, j + 1))
                return 1
            return 0

        def sink_bfs(i, j):
            if not (0 <= i < m and 0 <= j < n and grid[i][j] == '1'):
                return 0
            grid[i][j] = '0'  # 注意入队之前处理干净
            queue = deque([(i, j)])
            while queue:
                ni, nj = queue.popleft()
                for x, y in ((ni + 1, nj), (ni - 1, nj), (ni, nj + 1), (ni, nj - 1)):
                    if 0 <= x < m and 0 <= y < n and grid[x][y] == '1':
                        grid[x][y] = '0'
                        queue.append((x, y))
            return 1

        # return sum(sink_dfs(i, j) for i in range(m) for j in range(n))
        return sum(sink_bfs(i, j) for i in range(m) for j in range(n))

    def using_UF(self, grid):
        if not grid or not grid[0]:  # 空的边界情况
            return 0
        m, n = len(grid), len(grid[0])

        self.cnt_island = sum(cell == '1' for row in grid for cell in row)

        def decreasing_island():  # 后面用作callback
            self.cnt_island -= 1

        uf = UnionFind((i, j) for i in range(m) for j in range(n))
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == '0':
                    continue
                for qx, qy in zip((i - 1, i + 1, i, i), (j, j, j - 1, j + 1)):
                    if 0 <= qx < m and 0 <= qy < n and grid[qx][qy] == '1':
                        uf.union((i, j), (qx, qy), decreasing_island)
        return self.cnt_island

    def numIslands(self, grid):
        # return self.dfs_floodfill(grid)
        return self.using_UF(grid)


if __name__ == '__main__':
    print Solution().numIslands(
        [["1", "1", "1", "1", "0"],
         ["1", "1", "0", "1", "0"],
         ["1", "1", "0", "0", "0"],
         ["0", "0", "0", "0", "0"]])
