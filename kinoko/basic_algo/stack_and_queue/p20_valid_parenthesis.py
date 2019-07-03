#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串，判断字符串是否有效。

有效字符串需满足：

左括号必须用相同类型的右括号闭合。
左括号必须以正确的顺序闭合。
注意空字符串可被认为是有效字符串。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/valid-parentheses
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/1 上午9:30
"""


class Solution(object):
    def simple_assertion(self, s):
        # 直接用assert写法，思维比较直观
        stack = []
        paren_map = dict(zip(')]}', '([{'))
        try:
            for c in s:
                if c in paren_map:
                    # 直接写assert，保障括号串合法
                    assert stack.pop() == paren_map[c]
                else:
                    stack.append(c)
            assert not stack  # 保障栈空
            return True
        except (AssertionError, IndexError):
            return False

    def condition(self, s):
        # 用条件判断的写法，比较规范
        stack = []
        paren_map = dict(zip(')]}', '([{'))
        for c in s:
            if c not in paren_map:
                stack.append(c)
            # 如果栈空，或者不匹配
            elif not stack or stack.pop() != paren_map[c]:
                return False
        return not stack  # 记得检测栈空

    def isValid(self, s):
        return self.condition(s)
