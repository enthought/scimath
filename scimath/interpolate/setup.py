#!/usr/bin/env python
from __future__ import absolute_import
import os


def configuration(parent_package='scimath', top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration('interpolate', parent_package, top_path)
    config.add_extension('_interpolate',
                         ['_interpolate.cpp'],
                         include_dirs = ['.'],
                         depends = ['interpolate.h'])

    config.add_data_dir('tests')
    return config
