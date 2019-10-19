#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
utils for web developing
- a simple RESTful decorater for testing purpose

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/7/11 下午3:59
"""
from __future__ import unicode_literals

import socket
import warnings

import six
import tornado.ioloop
import tornado.web
from typing import Text, Callable, Any

from ..func import try_flatten
from ..misc.log_writer import init_log
from ..text.io import ensure_text, dump_utf8

logger = init_log(__name__)

if six.PY3:  # pragma: no cover
    import asyncio
    from tornado.platform.asyncio import AnyThreadEventLoopPolicy

    asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())


class RESTful(object):
    """
    Decorator class; simply wrapping a function into a RESTful GET service
    Usage:
    #----- Server side
    @RESTful(port=8104, route='/')
    def introduce(name, friends):
        return '{} has friends: {}'.format(name.upper(), ', '.join(friends))
    introduce.serve()

    #----- Client side
    $ curl 'http://localhost:8104?name=koyo' -d 'friends=tsuga' -d 'friends=Uncle.Li' -d 'friends=Robin'
    KOYO has friends: tsuga, yamamura, Robin%
    """

    def __init__(self, port=8104, route='/'):
        # type: (RESTful, int, Text) -> None
        """
        Setting the default params of the RESTful service object
        :param port: which port to listen, default to 8104; if <=1024, need sudo
        :param route: which route to listen
        """
        self.port = port
        self.path = route
        self.handler_class = None
        self.fn_name = None  # the wrapped function name, used as service logger name

    def __call__(self, fn):
        # type: (RESTful, Callable[[Any], Text]) -> RESTful
        """
        wraps the function into a tornado.web.RequestHandler object, for later serving
        :param fn: the function to be wrapped
        :return:
        """
        assert self.fn_name is None, 'The wrapper should not be called more than once'
        self.fn_name = fn.__name__  # for later use in serve()
        warnings.warn('DO NOT USE FOR PRODUCTION ENVIRONMENT, '
                      'this decorator was simply designed for toy-demo purpose', UserWarning)

        # noinspection PyAbstractClass
        class InnerHandler(tornado.web.RequestHandler):
            """ the inner class for wrapping the logic of ``fn`` """

            def post(this):
                """ post """
                request_kwargs = this.request.arguments
                # if param 'name' was only defined once,
                # then flatten the corresponding value(a size==1 list) into a scalar
                request_kwargs = {ensure_text(k): try_flatten([ensure_text(arg) for arg in v])
                                  for k, v in six.iteritems(request_kwargs)}
                logger.info('----- got request_param: %s', dump_utf8(request_kwargs))
                this.write(fn(**request_kwargs))

            def get(this):
                """ get """
                this.post()

        self.handler_class = InnerHandler
        return self

    def serve(self):
        """ start serving """
        app = tornado.web.Application([
            (self.path, self.handler_class)
        ])
        app.listen(self.port)
        logger.info('---------- serving `{}` at http://{}:{}'.format(self.fn_name, socket.gethostname(), self.port))
        tornado.ioloop.IOLoop.current().start()
