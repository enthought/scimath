import setuptools
from numpy.distutils.core import setup
from setup_data import INFO


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)
    config.set_options(
        ignore_setup_xxx_py=True,
        assume_default_configuration=True,
        delegate_options_to_subpackages=True,
        quiet=True,
    )

    config.add_subpackage('enthought.interpolate')
    config.add_data_files('enthought/__init__.py')

    config.add_data_dir('enthought/units/data')

    return config


# Build the full set of packages by appending any found by setuptools'
# find_packages to those discovered by numpy.distutils.
config = configuration().todict()
packages = setuptools.find_packages(exclude=config['packages'] +
    ['docs', 'examples'])
config['packages'] += packages


setup(
    author = 'Enthought, Inc',
    author_email = 'info@enthought.com',
    dependency_links = [
        'http://code.enthought.com/enstaller/eggs/source',
        ],
    description = "Science and mathematics features",
    extras_require = INFO['extras_require'],
    include_package_data = True,
    install_requires = INFO['install_requires'],
    license = "BSD",
    name = INFO['name'],
    namespace_packages = [
        "enthought",
        ],
    tests_require = [
        'nose >= 0.9',
        ],
    test_suite = 'nose.collector',
    url = 'http://code.enthought.com/ets',
    version = INFO['version'],
    **config
    )

