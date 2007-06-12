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


# Function to convert simple ETS component names and versions to a requirements
# spec that works for both development builds and stable builds.
def gendeps(list):
    return ['%s >=%s.dev, <=%s.dev' % (p,min,max) for p,min,max in list]

# Declare our installation requirements.
install_requires = gendeps([
    ])
print 'install_requires:\n\t%s' % '\n\t'.join(install_requires)


setup(
    name = 'enthought.interpolate',
    version = '2.0b1',
    description = "Array interpolation/extrapolation",
    author       = 'Enthought, Inc',
    author_email = 'info@enthought.com',
    url = 'http://code.enthought.com/ets',
    license = "BSD",
    install_requires = install_requires,
    extras_require = {
        # All non-ets dependencies should be in this extra to ensure users can
        # decide whether to require them or not.
        'nonets': [
            "numpy >=1.0.2",
        ],
    },
    namespace_packages = [
        "enthought",
    ],
    **configuration().todict()
)
