#!/usr/bin/env python
import os

def configuration(parent_package='enthought',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('interpolate',parent_package,top_path)

    config.add_extension('_interpolate',
                         [build_interpolate_cpp],
                         include_dirs = ['.'],
                         depends = ['interpolate.h'])
                         
    config.add_data_dir('tests')
    return config

def build_interpolate_cpp(extension, build_dir):
    import os
    from numpy import zeros, float64
    from scipy.weave import ext_tools

    target = os.path.join(build_dir, '_interpolate.cpp')
    mod = ext_tools.ext_module("_interpolate")
    mod.customize.add_support_code('#include "interpolate.h"')

    x = zeros(1, float64)
    y = zeros(1, float64)
    new_x = zeros(1, float64)
    new_y = zeros(1, float64)
    code = """
    linear(x, y, Nx[0], new_x, new_y, Nnew_x[0]);
    """
    func = ext_tools.ext_function("linear_dddd", code,
                                  ['x', 'y', 'new_x', 'new_y'])
    mod.add_function(func)

    x = zeros(1, float64)
    y = zeros(1, float64)
    new_x = zeros(1, float64)
    new_y = zeros(1, float64)
    code = """
    loginterp(x, y, Nx[0], new_x, new_y, Nnew_x[0]);
    """
    func = ext_tools.ext_function("loginterp_dddd", code,
                                  ['x', 'y', 'new_x', 'new_y'])
    mod.add_function(func)

    x = zeros(1, float64)
    y = zeros(1, float64)
    new_x = zeros(1, float64)
    new_y = zeros(1, float64)
    width = 0.0
    code = """
    window_average(x, y, Nx[0], new_x, new_y, Nnew_x[0], width); 
    """
    func = ext_tools.ext_function("window_average_ddddd", code,
                                  ['x', 'y', 'new_x', 'new_y', 'width'])
    mod.add_function(func)

    x = zeros(1, float64)
    y = zeros(1, float64)
    new_x = zeros(1, float64)
    new_y = zeros(1, float64)
    code = """
    block_average_above(x, y, Nx[0], new_x, new_y, Nnew_x[0]); 
    """
    func = ext_tools.ext_function("block_average_above_dddd", code,
                                  ['x', 'y', 'new_x', 'new_y'])
    mod.add_function(func)

    mod.generate_file(location=build_dir)
    
    info = mod.build_information()
    extension.include_dirs.extend(info.include_dirs())
    
    return [target] + info.sources()

if __name__ == "__main__":
    try:
        from numpy.distutils.core import setup
    except ImportError:
        execfile('setup_interpolate.py')
    else:
        setup(version = '1.1.0',
            description = "Array interpolation/extrapolation",
            author       = 'Enthought, Inc',
            author_email = 'info@enthought.com',
            url = 'http://code.enthought.com/ets',
            license = "BSD",
            zip_safe     = False,
            configuration=configuration)
