#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
班上有 N 名学生。其中有些人是朋友，有些则不是。他们的友谊具有是传递性。如果已知 A 是 B 的朋友，B 是 C 的朋友，那么我们可以认为 A 也是 C 的朋友。所谓的朋友圈，是指所有朋友的集合。

给定一个 N * N 的矩阵 M，表示班级中学生之间的朋友关系。如果M[i][j] = 1，表示已知第 i 个和 j 个学生互为朋友关系，否则为不知道。你必须输出所有学生中的已知的朋友圈总数。

示例 1:

输入:
[[1,1,0],
 [1,1,0],
 [0,0,1]]
输出: 2
说明：已知学生0和学生1互为朋友，他们在一个朋友圈。
第2个学生自己在一个朋友圈。所以返回2。
示例 2:

输入:
[[1,1,0],
 [1,1,1],
 [0,1,1]]
输出: 1
说明：已知学生0和学生1互为朋友，学生1和学生2互为朋友，所以学生0和学生2也是朋友，所以他们三个在一个朋友圈，返回1。
注意：

N 在[1,200]的范围内。
对于所有学生，有M[i][i] = 1。
如果有M[i][j] = 1，则有M[j][i] = 1。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/friend-circles
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/27 下午5:14
"""


class UnionFind(object):
    def __init__(self, elements):
        self.root = list(elements)
        self.num_islands = len(self.root)

    def find(self, p):
        while p != self.root[p]:  # 压缩路径的简化写法，不保证一次到根
            self.root[p] = p = self.root[self.root[p]]
        return p

    def union(self, p, q):
        P, Q = self.find(p), self.find(q)
        if P != Q:
            self.root[P] = Q
            self.num_islands -= 1


class Solution(object):
    def floodfill(self, M):
        met = set()

        def dfs(i):
            if i in met:
                return 0
            met.add(i)
            # 注意题目中的值是int，不是 '1'
            [dfs(j) for j, v in enumerate(M[i]) if v == 1]
            return 1

        return sum(map(dfs, range(len(M))))

    def using_UF(self, M):
        uf = UnionFind(range(len(M)))  # 注意不是 range(M)
        for i, row in enumerate(M):
            for j, v in enumerate(row[i + 1:], start=i + 1):
                if v == 0:
                    continue
                uf.union(i, j)
        return uf.num_islands

    def findCircleNum(self, M):
        # return self.floodfill(M)
        return self.using_UF(M)
