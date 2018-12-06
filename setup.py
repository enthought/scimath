# Copyright (c) 2008-2013 by Enthought, Inc.
# All rights reserved.
import os
import re
from setuptools import find_packages, setup
from subprocess import check_output

import numpy.distutils.core


MAJOR = 4
MINOR = 1
MICRO = 3
IS_RELEASED = False
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)
VERSION_FILE_TEMPLATE = """\
# This file is generated from setup.py
version = '{version}'
full_version = '{full_version}'
git_revision = '{git_revision}'
is_released = {is_released}
if not is_released:
    version = full_version
"""
DEFAULT_VERSION_FILE = os.path.join('scimath', '_version.py')


# Return the git revision as a string
def git_version():
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}

        for k in ['SYSTEMROOT', 'PATH', 'HOME']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = check_output(cmd, env=env)
        return out
    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        git_revision = out.strip().decode('ascii')
    except OSError:
        git_revision = "Unknown"
    try:
        out = _minimal_ext_cmd(['git', 'rev-list', '--count', 'HEAD'])
        git_count = out.strip().decode('ascii')
    except OSError:
        git_count = '0'
    return git_revision, git_count


def write_version_py(filename=DEFAULT_VERSION_FILE,
                     template=VERSION_FILE_TEMPLATE):
    # Adding the git rev number needs to be done inside
    # write_version_py(), otherwise the import of scimath._version messes
    # up the build under Python 3.
    fullversion = VERSION
    if os.path.exists('.git'):
        git_rev, dev_num = git_version()
    elif os.path.exists(DEFAULT_VERSION_FILE):
        # must be a source distribution, use existing version file
        try:
            from scimath._version import git_revision as git_rev
            from scimath._version import full_version as full_v
        except ImportError:
            raise ImportError("Unable to import git_revision. Try removing "
                              "scimath/_version.py and the build directory "
                              "before building.")
        match = re.match(r'.*?\.dev(?P<dev_num>\d+)$', full_v)
        if match is None:
            dev_num = '0'
        else:
            dev_num = match.group('dev_num')
    else:
        git_rev = "Unknown"
        dev_num = '0'
    if not IS_RELEASED:
        fullversion += '.dev{0}'.format(dev_num)
    with open(filename, "wt") as fp:
        fp.write(template.format(version=VERSION,
                                 full_version=fullversion,
                                 git_revision=git_rev,
                                 is_released=IS_RELEASED))
    return fullversion


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


DEPENDENCIES = [
    'traits',
]


if __name__ == "__main__":
    __version__ = write_version_py()

    # Build the full set of packages by appending any found by setuptools'
    # find_packages to those discovered by numpy.distutils.
    config = configuration().todict()
    packages = find_packages(exclude=config['packages'] +
                                        ['docs', 'examples'])
    config['packages'] += packages

    # The actual setup call.
    numpy.distutils.core.setup(
        name = 'scimath',
        version = __version__,
        author = 'Enthought, Inc',
        author_email = 'info@enthought.com',
        maintainer = 'ETS Developers',
        maintainer_email = 'enthought-dev@enthought.com',
        url = 'https://github.com/enthought/scimath',
        download_url = ('https://github.com/enthought/scimath/archive/%s.tar.gz' %
                        __version__),
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
        install_requires = DEPENDENCIES,
        setup_requires=['numpy'],
        license = "BSD",
        package_data = {'': ['images/*', 'data/*']},
        platforms = ["Windows", "Linux", "Mac OS-X", "Unix", "Solaris"],
        zip_safe = False,
        **config
    )
