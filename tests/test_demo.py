#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
演示pytest的常用写法

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/6/27 下午11:12
"""

import os

import pytest

# **参数化测试**
url_jumps = [
    ('http://www.cyberciti.biz/tips/', ['http://www.cyberciti.biz/tips/', 'https://www.cyberciti.biz/tips/']),
    ('http://apollo.auto/index_cn.html', ['http://apollo.auto/index_cn.html']),
    ('http://nonexist.site', [])
]

JINGDONG_REACHABLE = True  # os.system("ping -c 1 jd.com") == 0
pytestmark = pytest.mark.skipif(not JINGDONG_REACHABLE, reason='not internet available')


@pytest.mark.parametrize("url, jumps", url_jumps)
def test_chase_redirection(url, jumps):
    """ 测试chase_redirection的逻辑，包括异常 """
    # try:
    #     all_jumps = chase_redirection(url, max_depth=3)
    #     pass
    # except ChaseError:
    #     all_jumps = []
    # assert jumps == all_jumps
    pass


# **mock一个object**
# 是最常见的需求。由于function也是一个object，以`function`举例。
# 注:
#   - 这里是patch了一个module对象里面的函数，下面讲的第二类方法也可以
#   - 只能对已经存在的东西使用mock; 要先import os

def rm(filename):
    os.remove(filename)


def test_patch_object(mocker):
    mocked_func = mocker.patch('os.remove')  # 给os.remove打patch，让它变成了一个MagicMock
    filename = 'test.file'
    rm(filename)
    mocked_func.assert_called_once_with(filename)  # 查看是否被调一次，且参数为filename

    # 也可以直接验证被mock过的原函数(无需开个额外变量 `mock_func`)
    os.remove.assert_called_once_with(filename)


# **patch一个object**
# 有时，仅仅需要mock一个object里的method，而无需mock整个object。
# 例如，在对当前object的某个method进行测试时。这时，可以用`patch.object`

# 对于一个指定object, patch它的field和method
class ForTest:
    field = 'origin'

    def method(self):
        pass


def test_patch_members_of_obj(mocker):
    test = ForTest()
    mock_method = mocker.patch.object(test, 'method')  # patch它的method
    test.method()
    assert mock_method.called  # 验证被调用过一次

    assert 'origin' == test.field
    mocked_field = mocker.patch.object(test, 'field', new='mocked')  # patch它的field，值改成'mocked'
    assert 'mocked' == mocked_field

    # 也可以直接验证被mock过的原方法(无需开个额外变量 `mock_method`)
    assert test.method.called  # 验证被调用过一次
    # 也可以直接验证被mock过的原方法(...)
    assert 'mocked' == test.field


# 对于一个指定module, patch它的function
def test_patch_function_of_obj(mocker):
    mocker.patch.object(os, 'remove')  # 等效于上面直接 patch一个object (`os.remove`)
    filename = 'test.file'
    rm(filename)
    os.remove.assert_called_once_with(filename)
    # 也支持不省变量的写法，略


# **用spy包装**
# 如果只是想用MagicMock包装一个东西，而又不想改变其功能，可以用`spy`
# 与上例中的 `patch.object`不同的是，上例中被patch的方法/函数不会真的执行，而本例中则会

def test_spy(mocker):
    mocker.spy(os, 'listdir')
    print(os.listdir('/'))  # 用`-s`选项看命令行输出 PYTHONPATH=. py.test -s -vv ./tests/test_demo.py
    assert os.listdir.called


# **mocker的高级用法: return_value、side_effect和wraps**

def name_length(filename):
    if not os.path.isfile(filename):
        raise ValueError('{} is not a file!'.format(filename))
    return len(filename)


def test_return_value(mocker):
    # 指定 os.path.isfile 始终返回True; 注意 return_value 只适合简单固定返回值的情况
    isfile = mocker.patch('os.path.isfile', return_value=True)
    assert 4 == name_length('test')
    isfile.assert_called_once()

    isfile.return_value = False  # 修改 os.path.isfile的返回值, 使恒为False
    with pytest.raises(ValueError):
        name_length('test')
    assert 2 == isfile.call_count


def test_wraps(mocker):
    mocker.patch('os.path.isfile', return_value=True)  # 同上，指定 os.path.isfile 始终返回True
    # mock `len()`函数，但是实际的逻辑也要透传，有点类似spy
    # 注意不要写 mocker.patch.object(__name__, 'len', ...) 因为 `__name__`是个 str，而非module对象
    mock_len = mocker.patch(__name__ + '.len', wraps=len)
    assert 4 == name_length('test')
    assert mock_len.called

    # # patch全局函数，比较危险 'builtins.len' 会导致无限循环递归
    # mock_len = mocker.patch('builtins.len', wraps=len)
    # # spy全局函数也是无限递归; 而如果是针对__name__ 则又找不到函数；因为spy本来只支持method of object
    # import builtins, tests
    # mock_len = mocker.spy(builtins, 'len')  # 直接跑会无限递归，而换成tests.test_demo就找不到len


def test_side_effect(mocker):
    mocker.patch('os.path.isfile', side_effect=TypeError)  # 指定 os.path.isfile 抛出TypeError
    with pytest.raises(TypeError):
        name_length('test')

    # 指定 当前模块的 name_length() 函数，依次返回 True, False
    mocked_name_len = mocker.patch(__name__ + '.name_length', side_effect=[True, False])
    assert True == name_length('test')
    assert False == name_length('test')
    with pytest.raises(StopIteration):
        name_length('test')

    # 指定 当前模块的 name_length() 函数，返回输入长度的两倍
    mocked_name_len.side_effect = lambda x: len(x) * 2
    assert 8 == name_length('test')
