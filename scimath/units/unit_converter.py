#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Travis N. Vaught
# Date: 05/25/2005
# Description: Define dictionary of unit conversion methods by object type
#
# Symbols defined: default_unit_converters, [add_unit_converter]
#
#------------------------------------------------------------------------------

#############################################################################
# Imports:
#############################################################################

# Standard library imports.
from __future__ import absolute_import
import logging, numpy

# Enthought library imports.
from scimath.units import convert as units_convert


logger = logging.getLogger(__name__)


def typecode(x):
    try:
        return x.dtype.char
    except AttributeError:
        return x.typecode()

def convert_unit_array(unit_array, unit_system=None, to_unit=None,
                       family_name=None ):
    """ Function to convert the units of a unit_array

        Parameters:
        -----------
        unit_array
            Unit_array to be converted
        unit_system
            the unit system of the current unit_array units, defaults to the
            unit_managers default system (current unit_system):
        to_units
            new_units to convert to
        family_name
            provided in cases where the family_name attribute is not present
            in the provided unit_array object

    """
    from scimath.units.unit_array import UnitArray

    if family_name==None and unit_array.units is not None:
        family_name=_get_family_name_for_array(unit_array.units)

    if unit_array.units is None:
        family_name= None

    if to_unit==None:
        unit_system = _get_unit_system()
        try:
            to_unit = unit_system.units(family_name)
        except KeyError:
            logger.exception("Could not convert UnitArray: %s to system: %s" %\
                             (unit_array, unit_system))
            return unit_array.copy()

    if unit_array.units == to_unit:
        new_array = UnitArray(unit_array, units=unit_array.units)
    else:
        data = units_convert(unit_array.view(numpy.ndarray),
                             unit_array.units, to_unit)
        new_array = UnitArray(data, units=to_unit)

    return new_array


# TODO: move this to cp.log.log_type_converters
def convert_log_index(log_index, unit_system=None, to_unit=None, family_name=None):
    """ Function to convert the units of a LogIndex

        Parameters
        ----------
        log_index
            index to be converted
        unit_system
            the unit system of the current log_index units, defaults to the
            unit_managers default system (current unit_system):
        to_units
            new_units to convert to
        family_name
            provided in cases where the family_name attribute is not present
            in the provided log_index object
        """


    if family_name==None:
        family_name=log_index.family_name or log_index.name

    if to_unit==None:
        unit_system = _get_unit_system(unit_system)
        try:
            to_unit = unit_system.units(family_name)

        except KeyError:
            logger.exception("Could not convert LogIndex: %s to system: %s" % \
                              (log_index, unit_system))
            return log_index.clone()

    if log_index.units == to_unit:
        new_log_index = log_index.clone()
        new_log_index.family_name = family_name # TODO: not sure if I need this
    else:
#        print "To_units", to_unit, log_index.units, family_name, unit_system
        data = units_convert(log_index.data, log_index.units, to_unit)
        new_log_index = log_index.clone(data=data)
        new_log_index.family_name = family_name
        new_log_index.units = to_unit

    return new_log_index


def convert_log(log, unit_system=None, to_unit=None, family_name=None):
    """ Function to convert the units of a Log

        Parameters
        ----------
        log
            Log to be converted
        unit_system
            the unit system of the current log units, defaults to the
            unit_managers default system (current unit_system):
        to_units
            new_units to convert to
        family_name
            provided in cases where the family_name attribute is not present
            in the provided log object
        """

    from numpy.numarray.numerictypes import ObjectType

    if family_name==None:
        family_name=log.family_name or log.name

    unit_system = _get_unit_system(unit_system)
    new_index = convert_log_index(log.index, unit_system=unit_system)

    # Do not convert unknown log values
    if family_name == 'unknown':
        return log.clone(index=new_index)

    if to_unit==None:
        try:
            to_unit = unit_system.units(family_name)
        except KeyError:
            logger.exception("Could not convert Log: %s to system: %s" \
                              % (log,unit_system))
            return log.clone(index=new_index)

    if typecode(log.data) == ObjectType:
        # handle string logs
        new_log = log.clone(index=new_index)
    else:
        new_log = convert_log_index(log, family_name=family_name, to_unit=to_unit)
        new_log.index = new_index
    return new_log


def convert_log_suite(log_suite, unit_system=None, to_unit=None, family_name=None):
    from cp.log.log_suite import LogSuite

    new_index = convert_log_index(log_suite.index, unit_system)
    new_logs = []
    for log in log_suite.get_logs():
        new_logs.append(convert_log(log))
    return LogSuite(log_suite.name, new_index, *new_logs)



def convert_quantity_old(q, unit_system):
    # I think importing within the function is needed to avoid circularity
    from scimath.units.quantity import Quantity

    try:
        units = unit_system.units(q.family_name)
    except KeyError:
        logger.exception("Could not convert quantity: %s to system: %s" % (q,unit_system))
        return q.clone()

    if q.units == units:
        q = q.clone()

    else:
        data = units_convert(q.data, q.units, units)
        q = Quantity(data, units=units, name=q.name or q.family_name, family_name=q.family_name)
    return q

def convert_action_variable(q, unit_system=None, to_unit=None, family_name=None):
    import copy

    if family_name==None:
        family_name=q.family_name

    if to_unit==None:
        unit_system = _get_unit_system(unit_system)
        try:
            to_unit = unit_system.units(family_name)

        except KeyError:
            logger.exception("Could not convert quantity: %s to system: %s" % (q,unit_system))
            return copy.deepcopy(q)

    q = copy.deepcopy(q)
    if q.units == to_unit.get_label():
        return q

    else:
        q.units = to_unit.get_label()

    return q

def convert_log_proxy(q, unit_system=None, to_unit=None, family_name=None):
    from cp.log.api import Log, LogIndex

    index_copy = LogIndex(data=q.index.data, units=q.index.units, name=q.index.name, family_name=q.index.family_name)
    log_copy = Log(q.data, index=index_copy, units=q.units, name=q.name, family_name=q.family_name)
    return convert_log(log_copy, unit_system=unit_system, to_unit=to_unit, family_name=family_name)

def convert_quantity(q, unit_system=None, to_unit=None, family_name=None):
    if family_name==None:
        family_name=q.family_name

    if to_unit==None:
        unit_system = _get_unit_system(unit_system)
        try:
            to_unit = unit_system.units(family_name)

        except KeyError:
            logger.exception("Could not convert quantity: %s to system: %s" % (q,unit_system))
            return q.clone()

    if q.units == to_unit:
        q = q.clone()

    else:
        data = units_convert(q.data, q.units, to_unit)
        # create a new object of the same type as the input Quantity object
        # could be a subclass, so use __class__
        q = q.__class__(data, units=to_unit, name=q.name or family_name, family_name=family_name)
    return q

def _get_unit_system(unit_system=None):
    from scimath.units.unit_manager import unit_manager
    return unit_manager.get_unit_system(unit_system)

def _get_family_name_for_array(units=None):
    from scimath.units.unit_manager import unit_manager
    return unit_manager.get_family_name_for_value(units)

# The dict of defaults
default_unit_converters = {
       "<class 'scimath.units.unit_array.UnitArray'>" :
                                                   convert_unit_array,
       "<class 'scimath.units.quantity.Quantity'>": convert_quantity,
       "<class 'scimath.units.scalar.Scalar'>": convert_quantity,
       "<class 'cp.log.log_index.LogIndex'>": convert_log_index,
       "<class 'cp.log.log.Log'>": convert_log,
       "<class 'cp.log.log_suite_proxy.LogProxy'>": convert_log,
       "<class 'cp.log.log_suite.LogSuite'>": convert_log_suite,
       "<class 'cp.lab.action_variable.ActionVariable'>":
                                                   convert_action_variable,
       "<class 'cp.log.editable_log_suite_proxy.EditableLogProxy'>":
                                                   convert_log_proxy,
       "<class 'cp.log.log_suite_proxy.LogSuiteProxy'>" : convert_log_proxy,
       }
