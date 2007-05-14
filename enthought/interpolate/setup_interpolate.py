#!/usr/bin/env python

import os

def build_interpolate_cpp(extension, build_dir):
    from Numeric import array, zeros, Float64, Int
    from weave import ext_tools

    target = os.path.join(build_dir, '_interpolate.cpp')
    mod = ext_tools.ext_module("_interpolate")
    mod.customize.add_support_code('#include "interpolate.h"')

    x = zeros(1, typecode=Float64)
    y = zeros(1, typecode=Float64)
    new_x = zeros(1, typecode=Float64)
    new_y = zeros(1, typecode=Float64)
    code = """
    linear(x, y, Nx[0], new_x, new_y, Nnew_x[0]);
    """
    func = ext_tools.ext_function("linear_dddd", code,
                                  ['x', 'y', 'new_x', 'new_y'])
    mod.add_function(func)

    x = zeros(1, typecode=Float64)
    y = zeros(1, typecode=Float64)
    new_x = zeros(1, typecode=Float64)
    new_y = zeros(1, typecode=Float64)
    code = """
    loginterp(x, y, Nx[0], new_x, new_y, Nnew_x[0]);
    """
    func = ext_tools.ext_function("loginterp_dddd", code,
                                  ['x', 'y', 'new_x', 'new_y'])
    mod.add_function(func)

    x = zeros(1, typecode=Float64)
    y = zeros(1, typecode=Float64)
    new_x = zeros(1, typecode=Float64)
    new_y = zeros(1, typecode=Float64)
    width = 0.0
    code = """
    window_average(x, y, Nx[0], new_x, new_y, Nnew_x[0], width); 
    """
    func = ext_tools.ext_function("window_average_ddddd", code,
                                  ['x', 'y', 'new_x', 'new_y', 'width'])
    mod.add_function(func)
    
    mod.generate_file(location=build_dir)
    
    info = mod.build_information()
    extension.include_dirs.extend(info.include_dirs())
    
    return [target] + info.sources()


def configuration(parent_package='', parent_path=None):
    from scipy_distutils.misc_util import get_path, dot_join, default_config_dict
    from scipy_distutils.core import Extension

    package = 'interpolate'
    local_path = get_path(__name__, parent_path)
    config = default_config_dict(package,parent_package)

    ext = Extension(dot_join(parent_package,package,'_interpolate'),
                    sources = [build_interpolate_cpp],
                    include_dirs = [local_path],
                    depends = [os.path.join(local_path,'interpolate.h')])
    
    config['ext_modules'].append(ext)

    return config
    
if __name__ == "__main__":    
    from scipy_distutils.core import setup
    setup(**configuration(parent_path=''))
