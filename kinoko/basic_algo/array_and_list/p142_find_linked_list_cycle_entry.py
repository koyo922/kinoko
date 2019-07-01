#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给定一个链表，返回链表开始入环的第一个节点。 如果链表无环，则返回 null。
为了表示给定链表中的环，我们使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。 如果 pos 是 -1，则在该链表中没有环。

https://leetcode.com/problems/linked-list-cycle-ii/discuss/44783/Share-my-python-solution-with-detailed-explanation
注意思路：
2(H+D) = H+D+nL
H + D = nL
H = nL - D
所以拉回原点后，fast从+D出发再走(nL-D)步 刚好到圈头，此时又能相遇

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/linked-list-cycle-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/1 上午8:24
"""


class Solution(object):
    def detectCycle(self, head):
        try:
            # 注意两个不要放在同一起点
            fast, slow = head.next, head  # 另外，可能就是个空表；所以这一行也要放try里面
            while fast != slow:  # 否则这个循环就不会开始
                fast = fast.next.next
                slow = slow.next
        except AttributeError:  # 可能没有环，一直找到表尾的None
            return None

        fast = fast.next  # 之前让起点错了一位（导致提前相遇上）；现在修复
        slow = head
        while fast != slow:
            fast, slow = fast.next, slow.next
        return fast
