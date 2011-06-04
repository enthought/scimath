#!/usr/bin/env python
#
# Copyright (c) 2008-2011 by Enthought, Inc.
# All rights reserved.

"""
Scientific and Mathematical calculations.

The SciMath project includes packages to support scientific and mathematical
calculations, beyond the capabilities offered by SciPy.

- scimath.interpolate
- scimath.mathematics
- scimath.units

Prerequisites
-------------
You must have the following libraries installed before building or installing
SciMath:

* `NumPy <http://pypi.python.org/pypi/numpy>`_
* `SciPy <http://pypi.python.org/pypi/scipy>`_
"""

# NOTE: Setuptools must be imported BEFORE numpy.distutils or else
# numpy.distutils won't do the correct thing.
import setuptools

import numpy.distutils.core


# This works around a setuptools bug which gets setup_data.py metadata
# from incorrect packages.
setup_data = dict(__name__='', __file__='setup_data.py')
execfile('setup_data.py', setup_data)
INFO = setup_data['INFO']


# Pull the description values for the setup keywords from our file docstring.
DOCLINES = __doc__.split("\n")


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
    author = 'Enthought, Inc',
    author_email = 'info@enthought.com',
    download_url = ('http://www.enthought.com/repo/ets/SciMath-%s.tar.gz' %
                    INFO['version']),
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
    description = DOCLINES[1],
    install_requires = INFO['install_requires'],
    license = "BSD",
    long_description = '\n'.join(DOCLINES[3:]),
    maintainer = 'ETS Developers',
    maintainer_email = 'enthought-dev@enthought.com',
    name = INFO['name'],
    package_data = {'': ['images/*', 'data/*']},
    platforms = ["Windows", "Linux", "Mac OS-X", "Unix", "Solaris"],
    tests_require = [
        'nose >= 0.10.3',
        ],
    test_suite = 'nose.collector',
    url = 'http://code.enthought.com/projects/sci_math.php',
    version = INFO['version'],
    zip_safe = False,
    **config
)
