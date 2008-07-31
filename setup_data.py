# Function to convert simple ETS project names and versions to a requirements
# spec that works for both development builds and stable builds.  Allows
# a caller to specify a max version, which is intended to work along with
# Enthought's standard versioning scheme -- see the following write up:
#    https://svn.enthought.com/enthought/wiki/EnthoughtVersionNumbers
def etsdep(p, min, max=None, literal=False):
    require = '%s >=%s.dev' % (p, min)
    if max is not None:
        if literal is False:
            require = '%s, <%s.a' % (require, max)
        else:
            require = '%s, <%s' % (require, max)
    return require


# Declare our ETS project dependencies.
APPTOOLS = etsdep('AppTools', '3.0.0b1')
BLOCKCANVAS = etsdep('BlockCanvas', '3.0.0b1')
#DEVTOOLS -- all gotcha imports enclosed in try...except blocks so not needed
ENTHOUGHTBASE_TRAITS = etsdep('EnthoughtBase[traits]', '3.0.0b1')
ENVISAGECORE = etsdep('EnvisageCore', '3.0.0b1')
ENVISAGEPLUGINS = etsdep('EnvisagePlugins', '3.0.0b1')
TRAITS = etsdep('Traits', '3.0.0b1')
TRAITSBACKENDWX = etsdep('TraitsBackendWX', '3.0.0b1')
TRAITSGUI = etsdep('TraitsGUI', '3.0.0b1')
TRAITS_UI = etsdep('Traits[ui]', '3.0.0b1')


# A dictionary of the pre_setup information.
INFO = {
    'extras_require': {
        'converter':[
            BLOCKCANVAS,
            ],
        "envisage": [
            APPTOOLS,
            ENVISAGECORE,
            ENVISAGEPLUGINS,
            TRAITSGUI,
            TRAITS_UI,
            ],
        'traits': [
            TRAITSBACKENDWX,
            ],

        # All non-ets dependencies should be in this extra to ensure users can
        # decide whether to require them or not.
        'nonets': [
            "numpy >=1.0.3",
            "scipy >=0.5.2",
            # "wx",  # wx does not build as an egg cleanly on all platforms.
            ],
        },
    'install_requires': [
        ENTHOUGHTBASE_TRAITS,
        TRAITS,
        ],
    'name': 'SciMath',
    'version': '3.0.0b2',
    }
