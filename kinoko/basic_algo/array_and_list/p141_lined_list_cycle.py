#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给定一个链表，判断链表中是否有环。

为了表示给定链表中的环，我们使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。 如果 pos 是 -1，则在该链表中没有环。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/linked-list-cycle
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/6/30 下午11:09
"""


class Solution(object):
    def remember_path(self, head):
        met = set()  # 记住所有走过的节点
        while head:
            if head in met:
                return True
            met.add(head)
            head = head.next
        return False

    def fast_slow_pointers(self, head):
        fast = slow = head  # 写法技巧，链式赋值
        # 注意技巧: fast在前面，slow.next一定存在
        # 另外，fast 可能恰好到了 None; 不要写成 `while fast.next and slow.next`
        while slow and fast and fast.next:
            fast = fast.next.next
            slow = slow.next
            if fast is slow:
                return True
        return False

    def hasCycle(self, head):
        return self.fast_slow_pointers(head)
