#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab number
"""
ref: https://jasonstitt.com/setuptools-bin-directory

Authors: qianweishuo<qzy922@gmail.com>
Date:    2019/9/29 下午2:05
"""
import os

from setuptools import Distribution
from setuptools.command.install import install


class OnlyGetScriptPath(install):
    def run(self):
        self.distribution.install_scripts = self.install_scripts


def get_setuptools_script_dir():
    """ Get the directory setuptools installs scripts to for current python """
    dist = Distribution({'cmdclass': {'install': OnlyGetScriptPath}})
    dist.dry_run = True  # not sure if necessary
    dist.parse_config_files()
    command = dist.get_command_obj('install')
    command.ensure_finalized()
    command.run()
    return dist.install_scripts
