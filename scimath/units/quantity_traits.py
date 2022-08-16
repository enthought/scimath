# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Trait definitions for dealing with physical quantities in various unit
systems.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

from traits.etsconfig.api import ETSConfig
from traits.api import TraitHandler, Instance, Bool, Trait, Str
from traitsui.editor_factory import EditorFactory
from scimath.units.unit_manager import unit_manager
from scimath.units.quantity import Quantity
from scimath.units.unit import unit


#------------------------------------------------------------------------------
#  Data:
#------------------------------------------------------------------------------

# Dictionary of all used quantity editors:
quantity_editors = {}

#------------------------------------------------------------------------------
#  'QuantityTrait' trait factory:
#------------------------------------------------------------------------------


def QuantityTrait(default_value, units, family_name, auto_set=False, display_units= None):
    """ Returns a trait definition for a Quantity whose default value is
        'default_value' (a float). The quantity's units are specified by
        'units' (a units object), and the family name of the units
        (e.g. density) is specified by 'family_name' (a string).
        If display_units is given, it is used for the display of the Quantity, otherwise
        the default units for the given family_name is used.
    """
    return Trait(Quantity(default_value, units=units,
                          family_name=family_name),
                 QuantityHandler(family_name, display_units),
                 auto_set=auto_set)

#------------------------------------------------------------------------------
#  'QuantityHandler' class:
#------------------------------------------------------------------------------


class QuantityHandler (TraitHandler):

    def __init__(self, family_name, display_units):
        self.family_name = family_name
        self.display_units = display_units

    def validate(self, object, name, value):
        try:
            if isinstance(value, Quantity):
                if value.family_name == self.family_name:
                    return value
            else:
                if self.display_units is None:
                    units = unit_manager.default_units_for(self.family_name)
                else:
                    units = self.display_units
                return Quantity(value, units=units,
                                family_name=self.family_name)
        except:
            pass
        self.error(object, name, value)

    def info(self):
        article = 'a'
        fn = self.family_name
        if fn[:1].lower() in 'aeiou':
            article = 'an'
        return '%s %s Quantity' % (article, fn)

    def get_editor(self, trait):
        auto_set = trait.auto_set
        if auto_set is None:
            auto_set = True
        return ToolkitEditorFactory(self,
                                    auto_set=auto_set,
                                    family_name=self.family_name,
                                    display_units=self.display_units)


class ToolkitEditorFactory(EditorFactory):
    """ EditorFactory for creating Quantity editors. """

    # The family name for the Quantity.
    family_name = Str
    display_units = Instance(unit)

    auto_set = Bool(True)

    def init(self, *args):
        pass

    ###########################################################################
    # 'EditorFactory' interface:
    ###########################################################################

    def simple_editor(self, ui, object, name, description, parent):
        if ETSConfig.toolkit == 'wx':
            from .wx.quantity_editor import SimpleQuantityEditor
        else:
            msg = 'QuantityEditor not implemented for %r' % ETSConfig.toolkit
            raise NotImplementedError(msg)
        return SimpleQuantityEditor(parent,
                                    factory=self,
                                    ui=ui,
                                    object=object,
                                    name=name,
                                    description=description)

    def readonly_editor(self, ui, object, name, description, parent):
        if ETSConfig.toolkit == 'wx':
            from .wx.quantity_editor import ReadOnlyQuantityEditor
        else:
            msg = 'QuantityEditor not implemented for %r' % ETSConfig.toolkit
            raise NotImplementedError(msg)
        return ReadOnlyQuantityEditor(parent,
                                      factory=self,
                                      ui=ui,
                                      object=object,
                                      name=name,
                                      description=description)
