#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
使用队列实现栈的下列操作：

push(x) -- 元素 x 入栈
pop() -- 移除栈顶元素
top() -- 获取栈顶元素
empty() -- 返回栈是否为空

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/implement-stack-using-queues
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/1 上午10:22
"""

from collections import deque


class MyStack(object):

    def __init__(self):
        self.q1, self.q2 = deque(), deque()

    def push(self, x):
        self.q1.append(x)

    def pop(self):
        while len(self.q1) > 1:  # q1中除最后一个以外的元素，都dump到q2
            self.q2.append(self.q1.popleft())
        v = self.q1.popleft()
        self.q1, self.q2 = self.q2, self.q1  # 对调, q2恒为空
        return v

    def top(self):
        return self.q1[-1]  # 这里不用 check_dump()

    def empty(self):
        return not self.q1  # 不用看 self.q2, q2恒为空
