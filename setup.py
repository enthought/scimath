# Copyright (c) 2008-2013 by Enthought, Inc.
# All rights reserved.
from __future__ import absolute_import
from os.path import join

# NOTE: Setuptools must be imported BEFORE numpy.distutils or else
# numpy.distutils won't do the correct thing.
import setuptools

import numpy.distutils.core


info = {}
exec(compile(open(join('scimath', '__init__.py')).read(), join('scimath', '__init__.py'), 'exec'), info)


# Setup our extensions to Python.
def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)
    config.set_options(
        ignore_setup_xxx_py=True,
        assume_default_configuration=True,
        delegate_options_to_subpackages=True,
        quiet=True,
    )

    config.add_subpackage('scimath.interpolate')
    config.add_subpackage('scimath')

    config.add_data_dir('scimath/units/data')

    return config


# Build the full set of packages by appending any found by setuptools'
# find_packages to those discovered by numpy.distutils.
config = configuration().todict()
packages = setuptools.find_packages(exclude=config['packages'] +
                                    ['docs', 'examples'])
config['packages'] += packages


# The actual setup call.
numpy.distutils.core.setup(
    name = 'scimath',
    version = info['__version__'],
    author = 'Enthought, Inc',
    author_email = 'info@enthought.com',
    maintainer = 'ETS Developers',
    maintainer_email = 'enthought-dev@enthought.com',
    url = 'https://github.com/enthought/scimath',
    download_url = ('http://www.enthought.com/repo/ets/scimath-%s.tar.gz' %
                    info['__version__']),
    classifiers = [c.strip() for c in """\
        Development Status :: 4 - Beta
        Intended Audience :: Developers
        Intended Audience :: Science/Research
        License :: OSI Approved :: BSD License
        Operating System :: MacOS
        Operating System :: Microsoft :: Windows
        Operating System :: OS Independent
        Operating System :: POSIX
        Operating System :: Unix
        Programming Language :: C
        Programming Language :: Python
        Topic :: Scientific/Engineering
        Topic :: Software Development
        Topic :: Software Development :: Libraries
        """.splitlines() if len(c.split()) > 0],
    description = 'scientific and mathematical calculations',
    long_description = open('README.rst').read(),
    install_requires = info['__requires__'],
    license = "BSD",
    package_data = {'': ['images/*', 'data/*']},
    platforms = ["Windows", "Linux", "Mac OS-X", "Unix", "Solaris"],
    zip_safe = False,
    **config
)
