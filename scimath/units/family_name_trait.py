#-----------------------------------------------------------------------------
#
#  Copyright (c) 2005-2006 by Enthought, Inc.
#  All rights reserved.
#
#  Author: Greg Rogers
#
#-----------------------------------------------------------------------------


""" Trait definitions for the measure-of family name when dealing with physical
quantities in various unit systems.
"""

from traits.api import Bool, HasTraits, List, Str, \
    Trait, TraitError, TraitFactory, TraitHandler

from unit_manager import unit_manager

class FamilyNameTraitHandler(TraitHandler, HasTraits):
    """ TraitHandler for units that validates unit string parsing and,
    optionally, compatibility with a family.
    """

    # If True, None is allowed as a valid value.
    allow_none = Bool(True)

    # If True, attempts to assign values that cannot be found in the family
    # name database raise exceptions.
    # If False, values that cannot be found are replaced with 'unknown'.
    is_strict = Bool(False)

    # When set, the name of the units trait that is required to be compatible
    # with the family name.  This units value on the object will be reset
    # to the default units for the current family name whenever the family name
    # is changed.  That is, the family name acts as master and units as the
    # servant.
    units_trait = Str

    def validate(self, obj, name, value):
        """ Requires that value be either a valid family name according to
        the registered family names (see UnitManager) and the allow_none
        and is_strict attributes.
        """
        if ( (value is None and not self.allow_none)
            or (self.is_strict and not unit_manager.unit_families.has_key(value))):
            self.error(obj, name, value)

        return value

    def post_setattr ( self, obj, name, value ):
        """ object's family name trait has been validated and changed,
        now enforce compatibility of the units if required.
        """
        # reminder: assert( getattr(obj,name) == value )

        if self.units_trait is not '':
            if value is not None and value is not '' \
                and hasattr(obj, self.units_trait):

                units = getattr(obj, self.units_trait )

                force = value in ['unknown', 'none']
                if force or not unit_manager.is_compatible( units, value ):
                    default_units = unit_manager.default_units_for( value )
                    setattr( obj, self.units_trait, default_units )

        return

    def info(self):
        """ Returns message substring. """
        msg_parts = ['a string']

        if self.is_strict:
            msg_parts.append('recognized as a family name by the units manager')

        if self.allow_none:
            msg_parts.append('or None')

        msg = ' '.join(msg_parts)
        return msg



class FamilyNameList(HasTraits):
    """ Model class for ParameterChoiceEditor that provides the list of
    family names known to the unit manager.
    """
    names = List(Str)

    def __init__(self, ingore):

        self.names = unit_manager.unit_families.keys()
        self.names.sort()

    def get_labels(self):
        return self.names

    def get_object(self, idx):
        return self.names[idx]

    def index_of(self, obj):
        for i in xrange(len(self.names)):
            if self.names[i] == obj:
                return i
        return -1



def family_name_traits_factory_function( value=None, is_strict=False,
                                         allow_none=True, units_trait='',
                                         editor=None,
                                         **metadata):
    if not allow_none and value is None:
        raise TraitError, "value must not be None"

    if editor is None:
        # Delay UI imports until here such that this library can be used without
        # a UI.
        from traits.etsconfig.api import ETSConfig
        if ETSConfig.toolkit == 'wx':
            from traits.util.trait_defs.editor.parameter_choice_editor  \
                import ParameterChoiceEditorFactory

            editor = ParameterChoiceEditorFactory(model_class=FamilyNameList)

    return Trait( value, FamilyNameTraitHandler(allow_none=allow_none,
                                          is_strict=is_strict,
                                          units_trait=units_trait),
                  editor=editor,
                  **metadata )

# A Trait where the value is a units family name string.
# See FamilyNameTraitHandler for details.
FamilyNameTrait = TraitFactory( family_name_traits_factory_function )


### EOF
