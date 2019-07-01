#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
使用栈实现队列的下列操作：

push(x) -- 将一个元素放入队列的尾部。
pop() -- 从队列首部移除元素。
peek() -- 返回队列首部的元素。
empty() -- 返回队列是否为空。


来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/implement-queue-using-stacks
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/1 上午10:15
"""


class MyQueue(object):
    """
    注意: 下述解法是 push O(1), pop O(n) 稍加改造也可以换过来
    没有检查操作是否合法；严谨的写法应该抛 IndexError
    """

    def __init__(self):
        self.s1, self.s2 = [], []

    def _check_dump(self):
        """ 检测 如果s2为空，就把s1中所有元素dump过来 """
        if not self.s2:
            while self.s1:
                self.s2.append(self.s1.pop())

    def push(self, x):
        self.s1.append(x)

    def pop(self):
        self._check_dump()  # 注意check_dump
        return self.s2.pop()

    def peek(self):
        self._check_dump()  # 注意check_dump
        return self.s2[-1]

    def empty(self):
        return not (self.s1 or self.s2)
