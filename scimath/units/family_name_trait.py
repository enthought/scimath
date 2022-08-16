# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Trait definitions for the measure-of family name when dealing with physical
quantities in various unit systems.
"""

from traits.api import TraitError, TraitType

from .unit_manager import unit_manager


class FamilyNameTrait(TraitType):
    """ Trait for units that validates unit string parsing and, optionally,
    compatibility with a family.
    """

    #: If True, None is allowed as a valid value.
    allow_none = True

    #: If True, attempts to assign values that cannot be found in the family
    #: name database raise exceptions.
    #: If False, values that cannot be found are replaced with 'unknown'.
    is_strict = False

    #: When set, the name of the units trait that is required to be compatible
    #: with the family name. This units value on the object will be reset to
    #: the default units for the current family name whenever the family name
    #: is changed. That is, the family name acts as master and units as the
    #: servant.
    units_trait = ''

    def __init__(self, value=None, is_strict=False, allow_none=True,
                 units_trait='', **metadata):
        if not allow_none and value is None:
            raise TraitError("value must not be None")
        self.allow_none = allow_none
        self.is_strict = is_strict
        self.units_trait = units_trait
        super(FamilyNameTrait, self).__init__(default_value=value, **metadata)

    def validate(self, obj, name, value):
        """ Requires that value be either a valid family name according to
        the registered family names (see UnitManager) and the allow_none
        and is_strict attributes.
        """
        if ((value is None and not self.allow_none) or
                (self.is_strict and value not in unit_manager.unit_families)):
            self.error(obj, name, value)

        return value

    def post_setattr(self, obj, name, value):
        """ Object's family name trait has been validated and changed,
        now enforce compatibility of the units if required.
        """
        # reminder: assert( getattr(obj,name) == value )

        if self.units_trait != '':
            if (value is not None and
                    value != '' and
                    hasattr(obj, self.units_trait)):
                units = getattr(obj, self.units_trait)

                force = value in ['unknown', 'none']
                if force or not unit_manager.is_compatible(units, value):
                    default_units = unit_manager.default_units_for(value)
                    setattr(obj, self.units_trait, default_units)

    def info(self):
        """ Returns a description of the trait.
        """
        msg_parts = ["a string"]

        if self.is_strict:
            msg_parts.append(
                "recognized as a family name by the units manager")

        if self.allow_none:
            msg_parts.append("or None")

        msg = " ".join(msg_parts)
        return msg

    def create_editor(self):
        from traitsui.api import EnumEditor
        editor = EnumEditor(values=sorted(unit_manager.unit_families.keys()),
                            mode='list')
        return editor
