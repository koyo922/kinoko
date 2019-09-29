#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/9/29 下午8:40
"""
from __future__ import unicode_literals

import re
import threading
from typing import Text

import pytest
import requests

import kinoko
from kinoko.misc.web import RESTful


@pytest.fixture()
def rest_server(mocker):
    mocker.patch('warnings.warn')  # before @RESTful, to suppress output

    @RESTful(port=8004, route='/')
    def introduce(name, friends):
        friends = friends if isinstance(friends, Text) else ', '.join(friends)  # maybe Tuple[Text, ...]
        return '{} has friends: {}'.format(name.upper(), friends)

    thread = threading.Thread(target=introduce.serve)
    thread.daemon = True
    thread.start()
    yield introduce


def test_web_server(mocker, rest_server):
    mocked_logger = mocker.patch.object(kinoko.misc.web, 'logger')

    # make some requests from the client
    response_post = requests.post('http://localhost:8004',
                                  data={'name': 'koyo', 'friends': ['tsuga', 'Uncle.Li', '肉饼']})
    response_get = requests.get('http://localhost:8004',
                                data={'name': 'koyo', 'friends': ['tsuga', 'Uncle.Li', '肉饼']})
    # assert correct response on client side
    assert 'KOYO has friends: tsuga, Uncle.Li, 肉饼' == response_post.text == response_get.text

    # assert correct logging on server side
    assert re.match(r'---------- serving `introduce` at http://\S+:8004',
                    mocked_logger.info.call_args_list[0][0][0])  # first call, args, first arg
    assert (('----- got request_param: %s', '{"friends": ["tsuga", "Uncle.Li", "肉饼"], "name": "koyo"}')
            == mocked_logger.info.call_args_list[1][0]
            == mocked_logger.info.call_args_list[2][0])
