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
-------------
1. Setup the EDM (with click, setuptools and coverage): edm install -e bootstrap click, setuptools, coverage
2. Activate the EDM environment: edm shell -e bootstrap
3. Install packages for development: python etstool.py install
4. Run the tests: python etstool.py test
