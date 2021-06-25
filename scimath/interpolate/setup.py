#!/usr/bin/env python

# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import os


def configuration(parent_package='scimath', top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration('interpolate', parent_package, top_path)
    config.add_extension('_interpolate',
                         ['_interpolate.cpp'],
                         include_dirs=['.'],
                         depends=['interpolate.h'])

    config.add_data_dir('tests')
    return config
