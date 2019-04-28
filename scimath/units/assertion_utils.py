# -*- coding: utf-8 -*-
""" Utilities providing assertions to support unit tests involving UnitScalars
and UnitArrays.
"""
from nose.tools import assert_false, assert_true

from scimath.units.compare_units import unit_arrays_almost_equal, \
    unit_scalars_almost_equal


def assert_unit_scalar_almost_equal(val1, val2, rtol=1.e-9, msg=None):
    if msg is None:
        msg = "{} and {} are not almost equal with precision {}"
        msg = msg.format(val1, val2, eps)

    assert_true(unit_scalars_almost_equal(val1, val2, rtol=rtol), msg=msg)


def assert_unit_scalar_not_almost_equal(val1, val2, rtol=1.e-9, msg=None):
    if msg is None:
        msg = "{} and {} unexpectedly almost equal with precision {}"
        msg = msg.format(val1, val2, eps)

    assert_false(unit_scalars_almost_equal(val1, val2, rtol=rtol), msg=msg)


def assert_unit_array_almost_equal(uarr1, uarr2, rtol=1e-9, msg=None):
    if msg is None:
        msg = "{} and {} are not almost equal with precision {}"
        msg = msg.format(uarr1, uarr2, eps)

    assert_true(unit_arrays_almost_equal(uarr1, uarr2, rtol=rtol), msg=msg)


def assert_unit_array_not_almost_equal(uarr1, uarr2, rtol=1e-9, msg=None):
    if msg is None:
        msg = "{} and {} are almost equal with precision {}"
        msg = msg.format(uarr1, uarr2, eps)

    assert_false(unit_arrays_almost_equal(uarr1, uarr2, rtol=rtol), msg=msg)
