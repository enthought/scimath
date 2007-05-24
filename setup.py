import setuptools
from numpy.distutils.core import setup


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

    return config


setup(
    name = 'enthought.interpolate',
    version = '2.0',
    description = "Array interpolation/extrapolation",
    author       = 'Enthought, Inc',
    author_email = 'info@enthought.com',
    url = 'http://code.enthought.com/ets',
    license = "BSD",
    install_requires = [
        "numpy",
    ],
    namespace_packages = [
        "enthought",
    ],
    **configuration().todict()
)
