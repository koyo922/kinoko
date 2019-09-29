#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Setup script.

Authors: qianweishuo(qzy922@gmail.com)
Date:    2019/06/27 22:23:26
"""
from __future__ import unicode_literals

import os
import subprocess
from io import open

import setuptools
from setuptools.command.install import install

from kinoko.misc.setup_utils import get_setuptools_script_dir


class CustomInstallCommand(install):
    def run(self):
        # DO NOT write like this: super(CustomInstallCommand, self).run()
        # maybe legacy class issue: https://blog.csdn.net/kinghace/article/details/73244659
        install.run(self)
        installed_optparse = os.path.join(get_setuptools_script_dir(), 'optparse.bash')
        subprocess.check_call(['echo', 'source ' + installed_optparse],  # NOT `cat`
                              stdout=open(os.path.expanduser('~/.bashrc'), mode='a'))


setuptools.setup(
    cmdclass={
        'install': CustomInstallCommand,
    },
)
