# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import os
import re
from setuptools import Extension, find_packages, setup
from subprocess import check_output

from numpy import get_include


MAJOR = 5
MINOR = 0
MICRO = 1
IS_RELEASED = False
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)
VERSION_FILE_TEMPLATE = """\
# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

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


DEPENDENCIES = [
    'traits',
    'numpy',
    'scipy',
]

EXTRAS_REQUIRE = {
    "docs": ["enthought-sphinx-theme", "sphinx"],
}


if __name__ == "__main__":
    __version__ = write_version_py()


    # Register Python extensions
    interpolate = Extension(
        'scimath.interpolate._interpolate',
        sources=['scimath/interpolate/_interpolate.cpp'],
        define_macros=[
            ("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION"),
        ],
        include_dirs=[get_include(), 'scimath/interpolate'],
        depends=['interpolate.h']
    )

    extensions = [interpolate]

    # The actual setup call.
    setup(
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
        long_description_content_type = "text/x-rst",
        ext_modules=extensions,
        packages=find_packages(exclude=['docs', 'examples']),
        install_requires = DEPENDENCIES,
        extras_require = EXTRAS_REQUIRE,
        license = "BSD",
        package_data = {'': ['images/*', 'data/*', 'scimath/units/data/*']},
        platforms = ["Windows", "Linux", "Mac OS-X", "Unix", "Solaris"],
        zip_safe = False,
    )
