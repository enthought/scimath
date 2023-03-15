=================================================
scimath: Scientific and Mathematical calculations
=================================================

http://scimath.readthedocs.org/en/latest/

The SciMath project includes packages to support scientific and mathematical
calculations, beyond the capabilities offered by SciPy.

- scimath.interpolate
- scimath.mathematics
- scimath.units
- scimath.physical_quantities

Prerequisites
-------------

* `Traits <https://pypi.python.org/pypi/traits>`_
* `NumPy <https://pypi.python.org/pypi/numpy>`_
* `SciPy <https://pypi.python.org/pypi/scipy>`_

Development Environment Setup
-----------------------------

To set up an EDM environment for this project::

    $ edm install -e name_of_your_scimath_env click
    $ edm shell -e name_of_your_scimath_env
    $ python etstool.py install
    $ python etstool.py test
