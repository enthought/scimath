#-----------------------------------------------------------------------------
#
#  Copyright (c) 2004-2006 by Enthought, Inc.
#  All rights reserved.
#
#  Author: Greg Rogers
#
#-----------------------------------------------------------------------------

from traits.api import Bool, HasTraits, List, Str, \
    Trait, TraitError, TraitFactory, TraitHandler

from unit_manager import unit_manager
from unit_system import UnitSystem
from unit_parser import unit_parser, UnableToParseUnits
from unit import unit



def unit_system_trait_factory_function(value=None, editor=None, **metadata):
    if value is None:
        value = unit_manager.get_default(),

    if editor is None:
        # Delay UI imports until here such that this library can be used without
        # a UI.
        from traitsui import EnumEditor
        editor = EnumEditor(values=dict((str(us), us) for us in
            unit_manager.unit_systems), mode='list')

    return Trait(value, UnitSystem, editor=editor, **metadata)

UnitSystemTrait = TraitFactory(unit_system_trait_factory_function)

unit_system_trait = UnitSystemTrait




class UnitsTraitHandler(TraitHandler, HasTraits):
    """ TraitHandler for units that validates unit string parsing and,
    optionally, compatibility with a family.
    """

    # If True, None is allowed as a valid value.
    allow_none = Bool(True)

    # If True, attempts to assign values that cannot be parsed raise exceptions.
    # If False, values that cannot be parsed default to 'dimensionless'.
    is_strict = Bool(False)

    # When set, the name of the units family_name trait that the units
    # value must be compatible with.
    family_trait = Str

    def validate(self, obj, name, value):
        """ Requires that value be either a valid units expression or
        units object.  If not, the value 'dimensionless' is assumed.
        The returned value, and thus the value of a units trait will alawys
        be the unit object.
        """
        if value is None:
            if self.allow_none:
                return None
            else:
                self.error(obj, name, value)

        if not isinstance(value, unit):
            try:
                value = unit_parser.parse_unit(value,
                                           suppress_unknown=not self.is_strict)
            except UnableToParseUnits, ex:
                self.error(obj, name, value)

        # During Traits class definition the unit trait might be processed
        # prior to the family_trait.  During that processing validate is called
        # and getattr below can fail unless guarded, hence the hasattr.
        if self.family_trait is not '' and hasattr(obj, self.family_trait):
            family_name = getattr(obj, self.family_trait )
            if not unit_manager.is_compatible( value, family_name ):
                self.error(obj, name, value)

        return value

#    def post_setattr ( self, object, name, value ):
#        return

    def info(self):
        """ Returns message substring. """
        msg_parts = ['a unit object or']

        if self.is_strict:
            msg_parts.append('strictly parsable')

        msg_parts.append('unit string')

        if self.family_trait != '':
            msg_parts.append("compatible with the object's family trait (%s)"
                             % self.family_trait)

        if self.allow_none:
            msg_parts.append('or None')

        msg = ' '.join(msg_parts)
        return msg


def units_traits_factory_function( value=None, is_strict=False, allow_none=True,
                                  family_trait='',
                                  **metadata):
    if not allow_none and value is None:
        raise TraitError, "value must not be None"

    # Force identity comparison for change notification.
    # This considers 'ft' to 'feet' to be a change, but more importantly
    # 'none' to 'gapi' or other units with the same derivation are considered
    # different.
    metadata.setdefault( 'rich_compare', False )

    return Trait( value, UnitsTraitHandler(allow_none=allow_none,
                                          is_strict=is_strict,
                                          family_trait=family_trait),
                  **metadata )

# A Trait where the value is a Unit object.  See UnitTraitHandler for details.
UnitsTrait = TraitFactory( units_traits_factory_function )


### EOF
