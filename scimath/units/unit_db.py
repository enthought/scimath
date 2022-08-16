# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Defines the Unit information database access class.
"""

# Standard library imports:
import csv
import os
import logging

# Enthought library imports:
from traits.util.resource import get_path

# Local Imports:
from scimath.units.unit_parser import unit_parser


logger = logging.getLogger(__name__)


class UnitDB(object):
    """ Unit Database Class for wholesale loading of unit conversion,
        aliasing and formatting data from text files of the appropriate
        format. """

    def __init__(self):
        """
        Initialize UnitDB object
        """
        self.member_names = {}
        self.preferred_names = {}
        self.unit_names = unit_names = {}
        self.column_names = column_names = {}
        self.unit_systems = unit_systems = []
        self.unit_formats = unit_formats = {}
        self.unit_ranges = unit_ranges = {}

    def get_family_members_from_file(self, filename=None):
        """Retrieves a list of family names and member lists from a file.

            Parameters
            ----------
            filename:
                full path and name of spec file for member names
        """

        if not filename:
            filename = os.path.join(get_path(self), 'data',
                                    'unit_family_membership.txt')
        fh = open(filename)

        csv_reader = csv.reader(fh, delimiter=' ', skipinitialspace=True)

        logger.debug('Loading default unit info from %s...' % filename)

        for data in csv_reader:
            # Ignore blank lines, comment lines and column names row:
            if (len( data ) == 0) or (data[0][0:1] == '#') or \
               data[0].startswith("FAMILY"):
                pass
            else:
                family_name = data[0].lower()
                # add the family name to the alias list as well ....
                for member_name in data:
                    if member_name in self.member_names:
                        print(
                            'Warning: duplicate key: %s in %s' %
                            (member_name, filename))
                    self.member_names[member_name] = family_name

                # set up the preferred log name for the family to be the
                # first one in the alias list if possible.  Otherwise just
                # use the family_name
                if len(data) > 1:
                    self.preferred_names[family_name] = data[1].lower()
                else:
                    self.preferred_names[family_name] = data[1].lower()

        fh.close()
        logger.debug('Loading default unit info...Done')

    def get_family_format_from_file(self, filename=None):
        """Retrieves a list of formatting parameters from a file.

            Parameters
            ----------
            filename:
                full path and name of spec file for formats
        """

        # this function should probably live somewhere else (refactor style-
        #  manager).

        is_data = False
        column_names = []

        if not filename:
            filename = os.path.join(get_path(self), 'data',
                                    'unit_formatting.txt')
        fh = open(filename)

        csv_reader = csv.reader(fh, delimiter=' ', skipinitialspace=True)

        logger.debug('Loading default unit info from %s...' % filename)

        for data in csv_reader:
            if (len(data) == 0) or (data[0][0:1] == '#'):
                # Ignore blank lines and comment lines:
                pass

            elif is_data:
                try:
                    self.unit_formats[data[0]] = {}
                    for i, column in enumerate(column_names):
                        # skip the first one (family name)
                        if i == 0:
                            pass
                        else:
                            self.unit_formats[data[0]][column] = data[i]
                except KeyError:
                    logger.warn('Duplicate family found for %s' % data[0])

            else:
                # Parse the header line
                is_data = True
                column_names = []
                for column in data:
                    column_names.append(column.lower())

        fh.close()
        logger.debug('Loading default unit info...Done')

    def get_unit_families_from_file(self, filename=None):
        """Retrieves a list of family names and member lists from a file.

            Parameters
            ----------
            filepath:
                full path and name of spec file for member names
        """

        if not filename:
            filename = os.path.join(get_path(self), 'data',
                                    'unit_families.txt')

        is_data = False
        converters = []
        fh = open(filename)

        logger.debug('Loading default unit info from %s...' % filename)

        for data in csv.reader(fh, delimiter=' ', skipinitialspace=True):
            if (len(data) == 0) or (data[0][0:1] == '#'):
                # Ignore blank lines and comment lines:
                pass
            elif is_data:
                self.unit_names[data[0].lower()] = list(map(lambda func,
                                                            x: func(x),
                                                            converters, data))
            else:
                # Parse the header line
                is_data = True
                column_names = self.column_names
                converters = []
                for i, column in enumerate(data):
                    column_names[column] = i
                    if column[-6:] == '_UNITS':
                        converters.append(cvt_unit)
                        self.unit_systems.append(column[:-6])
                    else:
                        converters.append(cvt_str)
        fh.close()
        logger.debug('Loading default unit info...Done')

    def get_family_ranges_from_file(self, filename=None):
        """Retrieves a list of left/right range parameters from a file.

            Parameters
            ----------
            filename:
                full path and name of spec file for ranges
        """

        # this function should probably live somewhere else (refactor style-
        #  manager).

        is_data = False
        column_names = []
        system_names = []

        if not filename:
            filename = os.path.join(get_path(self), 'data',
                                    'unit_ranges.txt')
        fh = open(filename)

        csv_reader = csv.reader(fh, delimiter=' ', skipinitialspace=True)

        logger.debug('Loading default unit info from %s...' % filename)

        for data in csv_reader:
            if (len(data) == 0) or (data[0][0:1] == '#'):
                # Ignore blank lines and comment lines:
                pass

            elif is_data:
                try:
                    self.unit_ranges[data[0]] = {}
                    col_count = 1  # skip first column (family_name)
                    for system in system_names:
                        self.unit_ranges[
                            data[0]][system] = (
                            cvt_float(
                                data[col_count]), cvt_float(
                data[
                    col_count + 1]))
                        col_count += 2

                except KeyError:
                    logger.warn('Duplicate family found for %s')

            else:
                # Parse the header line
                is_data = True
                column_names = []
                system_names = []
                for column in data:
                    if column[-5:] == '_LEFT':
                        system_names.append(column[:-5].lower())
                    column_names.append(column.lower())  # not used?

        fh.close()
        logger.debug('Loading default unit info...Done')

    #  Return a list of the available unit systems eg 'kgs','metric','imperial'
    def get_unit_systems(self):
        return self.unit_systems

    #  Return the family name corresponding to a specified unit name:

    def get_inverse_family_name(self, unit_name):
        family = self.get_family_name(unit_name)
        inverse = self(family, column_name='INVERSE')
        if inverse == "none":
            inverse = ''
        return inverse

    def get_inverse_unit_name(self, unit_name):
        """ Returns the "default" name to use for inverted logs.

            This assumes that the first name in the alias list is
            the "primary" family name,  i.e., the one to use at the
            app level.
        """
        family = self.get_inverse_family_name(unit_name)
        return self.aliases.preferred_names.get(family, '')

    def get_family_name(self, name):

        match = name.lower().split('_')
        while len(match) > 0:
            family = self.member_names.get('_'.join(match))
            if family is not None:
                break

            match = match[:-1]

        else:
            family = 'unknown'
            logger.warn('Could not find the family name for %s ' % name)
        return family

#---------------------------------------------------------------------------
#  Convenience Functions:
#---------------------------------------------------------------------------


def cvt_str(text):
    """ Convert a string to itself or None if its values is '?' """
    if text == '?':
        return None
    return text


def cvt_float(text):
    """ Convert a string to its floating point value or None if its value is '?'
    """
    if text == '?':
        return None
    return float(text)


def cvt_unit(unit_label):
    """ Parse a unit description """
    units = unit_parser.parse_unit(unit_label)
    return units
