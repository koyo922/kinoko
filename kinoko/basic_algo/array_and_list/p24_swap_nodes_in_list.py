#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给定一个链表，两两交换其中相邻的节点，并返回交换后的链表。
你不能只是单纯的改变节点内部的值，而是需要实际的进行节点交换。

示例:

给定 1->2->3->4, 你应该返回 2->1->4->3.

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/6/30 下午10:43
"""


class Solution(object):
    def swapPairs(self, head):
        prev, prev.next = self, head  # 这里是拿self当队首哨兵节点了
        while prev.next and prev.next.next:
            a, b = prev.next, prev.next.next
            # prev > a > b > b.next 三者之间 本来存在 3根链接
            # 重新链接成: prev > b > a > b.next
            prev.next, b.next, a.next = b, a, b.next
            # 然后把 prev设置成a 使得下一轮的a指向a.next，即旧的b.next
            prev = a
        return self.next  # 最后返回哨兵的next
