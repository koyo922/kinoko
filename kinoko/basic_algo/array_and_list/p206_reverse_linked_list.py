#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
反转一个单链表。

示例:

输入: 1->2->3->4->5->NULL
输出: 5->4->3->2->1->NULL
进阶:
你可以迭代或递归地反转链表。你能否用两种方法解决这道题？

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/reverse-linked-list
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/6/30 下午10:02
"""


class Solution(object):
    def reverseList(self, head):
        prev, cur = None, head  # 将cur指向对首，即head; prev是其前驱，即None
        while cur:
            # 每次做两件事
            # 1. 翻转prev->cur的指针 cur.next = prev
            # 2. 两个指针都往前走一步  prev, cur = cur, cur.next
            cur.next, prev, cur = prev, cur, cur.next
        return prev
