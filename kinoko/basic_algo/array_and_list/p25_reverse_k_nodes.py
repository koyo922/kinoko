#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给你一个链表，每 k 个节点一组进行翻转，请你返回翻转后的链表。
k 是一个正整数，它的值小于或等于链表的长度。
如果节点总数不是 k 的整数倍，那么请将最后剩余的节点保持原有顺序。

示例 :
给定这个链表：1->2->3->4->5
当 k = 2 时，应当返回: 2->1->4->3->5
当 k = 3 时，应当返回: 3->2->1->4->5

说明 :
你的算法只能使用常数的额外空间。
你不能只是单纯的改变节点内部的值，而是需要实际的进行节点交换。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/reverse-nodes-in-k-group
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/1 上午8:49
"""


class Solution(object):
    def reverseKGroup(self, head, k):
        pre, pre.next, cur = self, head, head  # 注意在 self和head之间要搭好链接
        while cur:
            region = []  # 将待翻转的K个节点组织成区段
            for i in range(k):  # 尝试将k个节点放入区段
                if not cur:  # 遇到None，就说明队尾不足k个，跳出
                    break
                region.append(cur)
                cur = cur.next
            else:  # 如果慢k个
                post = region[-1].next  # 就记住post（后面用到）
                for i, j in zip(region, region[1:]):  # TRICK: 相邻翻转的写法
                    j.next = i
                pre.next = region[-1]  # 上轮迭代时，得到的前驱节点 指向区段尾节点
                region[0].next = post  # 区段头节点 指向post
                pre = region[0]  # 设置好本轮迭代的pre，下次用
        return self.next
    # 如果想省内存，可以调用单链表翻转算法
