#!/usr/bin/env python
import os

def configuration(parent_package='enthought',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('interpolate',parent_package,top_path)

    config.add_extension('_interpolate',
                         ['_interpolate.cpp'],
                         include_dirs = ['.'],
                         depends = ['interpolate.h'])
                         
    config.add_data_dir('tests')
    return config


