# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import (
    Instance, TraitError, TraitType, OBJECT_IDENTITY_COMPARE
)

from .unit import unit
from .unit_manager import unit_manager
from .unit_parser import UnableToParseUnits, unit_parser
from .unit_system import UnitSystem


class UnitSystemTrait(Instance):

    def __init__(self, value=None, **metadata):
        if value is None:
            value = unit_manager.get_default()
        super(UnitSystemTrait, self).__init__(
            klass=UnitSystem, factory=lambda: value, args=())

    def create_editor(self):
        from traitsui.api import EnumEditor
        editor = EnumEditor(values=dict((str(us), us) for us in
                            unit_manager.unit_systems), mode='list')
        return editor


# Alias
unit_system_trait = UnitSystemTrait


class UnitsTrait(TraitType):
    #: If True, None is allowed as a valid value.
    allow_none = True

    #: If True, attempts to assign values that cannot be parsed raise
    #: exceptions.
    #: If False, values that cannot be parsed default to 'dimensionless'.
    is_strict = False

    #: When set, the name of the units family_name trait that the units
    #: value must be compatible with.
    family_trait = ''

    def __init__(self, value=None, is_strict=False, allow_none=True,
                 family_trait='', **metadata):
        if not allow_none and value is None:
            raise TraitError("value must not be None")
        # Force identity comparison for change notification.
        # This considers 'ft' to 'feet' to be a change, but more importantly
        # 'none' to 'gapi' or other units with the same derivation are
        # considered different.
        metadata.setdefault('comparison_mode', OBJECT_IDENTITY_COMPARE)
        self.allow_none = allow_none
        self.is_strict = is_strict
        self.family_trait = family_trait
        # Validate/coerce the default value.
        value = self.validate(None, 'value', value)
        super(UnitsTrait, self).__init__(default_value=value, **metadata)

    def info(self):
        """ Returns a description of the trait.
        """
        msg_parts = ["a unit object or"]

        if self.is_strict:
            msg_parts.append("strictly parseable")

        msg_parts.append("unit string")

        if self.family_trait != '':
            msg_parts.append("compatible with the object's family trait "
                             "({0.family_trait!s})".format(self))

        if self.allow_none:
            msg_parts.append("or None")

        msg = " ".join(msg_parts)
        return msg

    def validate(self, obj, name, value):
        """ Requires that value be either a valid units expression or units
        object.

        If not, the value 'dimensionless' is assumed.  The returned value, and
        thus the value of a units trait will always be the unit object.
        """
        if value is None:
            if self.allow_none:
                return None
            else:
                self.error(obj, name, value)

        if not isinstance(value, unit):
            try:
                value = unit_parser.parse_unit(
                    value, suppress_unknown=not self.is_strict)
            except UnableToParseUnits:
                self.error(obj, name, value)

        # During Traits class definition the unit trait might be processed
        # prior to the family_trait.  During that processing validate is called
        # and getattr below can fail unless guarded, hence the hasattr.
        if self.family_trait != '' and hasattr(obj, self.family_trait):
            family_name = getattr(obj, self.family_trait)
            if not unit_manager.is_compatible(value, family_name):
                self.error(obj, name, value)

        return value
