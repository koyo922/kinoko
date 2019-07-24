#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给定两个单词 word1 和 word2，计算出将 word1 转换成 word2 所使用的最少操作数 。

你可以对一个单词进行如下三种操作：

插入一个字符
删除一个字符
替换一个字符
示例 1:

输入: word1 = "horse", word2 = "ros"
输出: 3
解释:
horse -> rorse (将 'h' 替换为 'r')
rorse -> rose (删除 'r')
rose -> ros (删除 'e')
示例 2:

输入: word1 = "intention", word2 = "execution"
输出: 5
解释:
intention -> inention (删除 't')
inention -> enention (将 'i' 替换为 'e')
enention -> exention (将 'n' 替换为 'x')
exention -> exection (将 'n' 替换为 'c')
exection -> execution (插入 'u')

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/edit-distance
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/23 上午8:31
"""


class Solution(object):
    def minDistance(self, word1, word2):
        """
        字符串比较类的题目一般这样定义状态
        f[i][j] := edit_dist(word1[:i], word2[:j])

        转移方程
        if word1[i-1] == word2[j-1]:  # 如果尾字符相等，直接从左侧子串结果，零成本转移即可
            f[i][j] = f[i-1][j-1] + 0 # 注意这里有BUG 直接从这里0成本转移未必最优
        else:
            f[i][j] = min(
                f[i][j-1] + ins_cost,  # 变换过程 word1[:i] --(f[i][j-1])--> word2[:j-1] --(ins_cost)--> word2[:j]
                del_cost + f[i-1][j],  # word1[:i] --(del_cost)-->  word1[:i-1] --(f[i-1][j])--> word2[:j]
                f[i-1][j-1] + rep_cost,  # word1[:i-1] --(f[i-1][j-1])--> word2[:j-1] 然后对两边各加一个尾字符后做replace
            )
        """
        ins_cost, del_cost, rep_cost = 1, 1, 1  # 简化题意
        M, N = len(word1), len(word2)
        f = [[0] * (N + 1) for _ in range(M + 1)]  # 注意边界

        for i in range(M + 1):  # 注意范围
            for j in range(N + 1):
                if i == 0:  # 如果word1[:i]是空串，则只能insert
                    f[i][j] = ins_cost * j
                elif j == 0:  # 如果word2[:j]是空串，则只能delete
                    f[i][j] = del_cost * i
                else:  # 否则DP
                    f[i][j] = min(
                        f[i][j - 1] + ins_cost,
                        del_cost + f[i - 1][j],
                        # 如果尾字符相同，直接用左侧结果零成本转移
                        f[i - 1][j - 1] + (0 if word1[i - 1] == word2[j - 1] else rep_cost)
                    )
        return f[-1][-1]


if __name__ == '__main__':
    assert 3 == Solution().minDistance("horse", "ros")
