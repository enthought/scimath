
#------------------------------------------------------------------------------
#
#  Trait definitions for dealing with physical quantities in various unit
#  systems
#
#  Written by: David C. Morrill
#
#  Date: 09/09/2004
#
#  Functions defined:
#     QuantityTrait
#
#  (c) Copyright 2004 by Enthought, Inc.
#
#  Changes:
#  Added system for setting unit used on display on a per trait basis. Sigve Tjora, 2006
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import wx

from enthought.traits.api import TraitHandler, Instance, true, Trait, Str
from enthought.traits.ui.wx.editor import Editor
from enthought.traits.ui.wx.editor_factory import EditorFactory
from enthought.traits.ui.wx.constants import ReadonlyColor
from enthought.units.unit_manager import unit_manager
from enthought.units.quantity import Quantity
from enthought.units.unit import unit

from enthought.traits.ui.wx.constants import OKColor, ErrorColor

#------------------------------------------------------------------------------
#  Data:
#------------------------------------------------------------------------------

# Dictionary of all used quantity editors:
quantity_editors = {}

#------------------------------------------------------------------------------
#  'QuantityTrait' trait factory:
#------------------------------------------------------------------------------

def QuantityTrait ( default_value, units, family_name, auto_set = False, display_units = None ):
    """ Returns a trait definition for a Quantity whose default value is
        'default_value' (a float). The quantity's units are specified by
        'units' (a units object), and the family name of the units
        (e.g. density) is specified by 'family_name' (a string).
        If display_units is given, it is used for the display of the Quantity, otherwise
        the default units for the given family_name is used.
    """
    return Trait( Quantity( default_value, units       = units,
                                           family_name = family_name ),
                  QuantityHandler( family_name, display_units ),
                  auto_set = auto_set)

#------------------------------------------------------------------------------
#  'QuantityHandler' class:
#------------------------------------------------------------------------------

class QuantityHandler ( TraitHandler ):

    def __init__ ( self, family_name, display_units ):
        self.family_name = family_name
        self.display_units = display_units

    def validate ( self, object, name, value ):
        try:
            if isinstance( value, Quantity ):
                if value.family_name == self.family_name:
                    return value
            else:
                if self.display_units is None:
                    units = unit_manager.default_units_for( self.family_name )
                else:
                    units = self.display_units
                return Quantity( value, units       = units,
                                        family_name = self.family_name )
        except:
            pass
        self.error( object, name, self.repr( value ) )

    def info ( self ):
        article = 'a'
        fn      = self.family_name
        if fn[:1].lower() in 'aeiou':
            article = 'an'
        return '%s %s Quantity' % ( article, fn )

    def get_editor ( self, trait ):
        auto_set = trait.auto_set
        if auto_set is None:
            auto_set = True
        return ToolkitEditorFactory(self,
                                    auto_set = auto_set,
                                    family_name = self.family_name,
                                    display_units = self.display_units)

class ToolkitEditorFactory(EditorFactory):
    """ EditorFactory for creating Quantity editors. """

    # The family name for the Quantity.
    family_name = Str
    display_units = Instance(unit)

    auto_set    = true

    def init(self, *args):
        pass


    ###########################################################################
    # 'EditorFactory' interface:
    ###########################################################################

    def simple_editor(self, ui, object, name, description, parent):
        return SimpleQuantityEditor(parent,
                                    factory     = self,
                                    ui          = ui,
                                    object      = object,
                                    name        = name,
                                    description = description)

    def readonly_editor(self, ui, object, name, description, parent):
        return ReadOnlyQuantityEditor(parent,
                                      factory     = self,
                                      ui          = ui,
                                      object      = object,
                                      name        = name,
                                      description = description)


class QuantityEditor(Editor):
    """ Base class for Quantity editors.

        Defines convenience methods for converting between unit systems.
    """

    ############################################################################
    # Private interface.
    ############################################################################

    #--------------------------------------------------------------------------
    #  Find the units to use for display
    #--------------------------------------------------------------------------

    def _get_display_units(self, quantity):
        if self.factory.display_units is None:
            du = unit_manager.default_units_for(self._get_family_name(quantity))
        else:
            du = self.factory.display_units
        return du

    #--------------------------------------------------------------------------
    #  Convert an object trait Quantity value to a string value in units used
    #  for display:
    #--------------------------------------------------------------------------

    def _to_display_units(self, quantity):

        family_name = self._get_family_name(quantity)
        project_quantity = Quantity(quantity,
                                    units = self._get_display_units(quantity),
                                    family_name = family_name)
        return project_quantity.data

    #--------------------------------------------------------------------------
    #  Convert a user supplied float value to a Quantity object in the same
    #  unit system as the display uses:
    #--------------------------------------------------------------------------

    def _from_display_units(self, value, quantity):
        family_name = self._get_family_name(quantity)
        project_quantity = Quantity(value,
                                    units = self._get_display_units(quantity),
                                    family_name = family_name)
        return Quantity(project_quantity,
                        units = quantity.units,
                        family_name = family_name)


    def _get_family_name(self, quantity):

        if self.factory.family_name is not None and \
               self.factory.family_name != '':
            fn = self.factory.family_name
        else:
            fn = quantity.family_name

        return fn

class SimpleQuantityEditor(QuantityEditor):
    """ Editor for editing Quantity traits. """

    text_control = Instance(wx.TextCtrl)

    ############################################################################
    # 'Editor' interface.
    ############################################################################

    def init(self, parent):
        """ Finishes initializing the editor by creating the underlying toolkit
            widget.

            The toolkit widget for Quantity traits is a text box followed by
            a label for the units.
        """
        self._updating_editor = False
        panel = wx.Panel(parent, -1)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.text_control = control = wx.TextCtrl(panel, -1, 
                                                  size = wx.Size(60, 20))
        sizer.Add(control, 1)

        # Add space before units to ensure attractive layout
        unit_string = " " + self._get_display_units(self.value).label

        label = wx.StaticText(panel, -1,
                              unit_string,
                              style = wx.ALIGN_LEFT)
        sizer.Add(label, 0, wx.ALIGN_CENTER)

        # Update the trait object if the text control loses focus or enter is
        # pressed.  If this editor is in 'auto_set' mode, also update the
        # trait object whenever the text changes.
        wx.EVT_KILL_FOCUS(control, self.update_object)
        wx.EVT_TEXT_ENTER(parent, control.GetId(), self.update_object)
        handler = self.check_value
        if self.factory.auto_set:
            handler = self.update_object
        wx.EVT_TEXT(parent, control.GetId(), handler)

        panel.SetAutoLayout(True)
        panel.SetSizer(sizer)
        sizer.Fit(panel)

        self.control = panel

        return

    def update_editor(self):
        """ Updates the editor when the object trait changes external to the
            editor.
        """
        self._updating_editor = True
        string_value = self.string_value(self._to_display_units(self.value))
        self.text_control.SetValue(string_value)
        self._updating_editor = False

        return
        
    def update_object ( self, event, assign = True ):
        """ Handles the user changing the contents of the edit control.
        """
        if not self._updating_editor:
            try:
                value = float( self.text_control.GetValue() )
                if assign:
                    self.value = self._from_display_units(value, self.value)
                if self.text_control is not None:
                    self.text_control.SetBackgroundColour( OKColor )
                    self.text_control.Refresh()
                    if self._error is not None:
                        self._error     = None
                        self.ui.errors -= 1
            except:
                self.text_control.SetBackgroundColour( ErrorColor )
                self.text_control.Refresh()
                if self._error is None:
                    self._error     = True
                    self.ui.errors += 1
                
    def check_value ( self, event ):
        """ Handles the user changing the contents of the edit control, but
            the value should only be checked, not assigned.
        """
        self.update_object( event, assign = False )

    def dispose ( self ):
        """ Disposes of the contents of an editor.
        """
        super( SimpleQuantityEditor, self ).dispose()
        self.text_control = None


class ReadOnlyQuantityEditor(Editor):

    ############################################################################
    # 'Editor' interface.
    ############################################################################

    def init(self, parent):
        """ Finishes initializing the editor by creating the underlying toolkit
            widget.

            The read only widget is a text label with the units and the family name.
        """
        control = wx.TextCtrl(parent, -1,
                              style = wx.TE_READONLY | wx.STATIC_BORDER),
        control.SetBackgroundColour(ReadonlyColor)
        self.control = control

        return

    def update_editor(self):
        """ Updates the editor when the object trait changes external to the
            editor.
        """
        # FIXME: The following line should fail...to_default_units is not defined for
        # this context. (TNV)
        string_value = '%s %s' % (self.to_default_units(self.value),
                                  self._get_family_name(self.value))
        self.control.SetValue(string_value)

        return


### EOF ########################################################################
