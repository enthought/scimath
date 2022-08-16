# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import wx

from traits.api import Instance
from traitsui.wx.editor import Editor
from traitsui.wx.constants import OKColor, ErrorColor, ReadonlyColor

from scimath.units.quantity import Quantity
from scimath.units.unit_manager import unit_manager


class QuantityEditor(Editor):
    """ Base class for Quantity editors.

        Defines convenience methods for converting between unit systems.
    """

    ##########################################################################
    # Private interface.
    ##########################################################################

    #--------------------------------------------------------------------------
    #  Find the units to use for display
    #--------------------------------------------------------------------------

    def _get_display_units(self, quantity):
        if self.factory.display_units is None:
            du = unit_manager.default_units_for(
                self._get_family_name(quantity))
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
                                    units=self._get_display_units(quantity),
                                    family_name=family_name)
        return project_quantity.data

    #--------------------------------------------------------------------------
    #  Convert a user supplied float value to a Quantity object in the same
    #  unit system as the display uses:
    #--------------------------------------------------------------------------

    def _from_display_units(self, value, quantity):
        family_name = self._get_family_name(quantity)
        project_quantity = Quantity(value,
                                    units=self._get_display_units(quantity),
                                    family_name=family_name)
        return Quantity(project_quantity,
                        units=quantity.units,
                        family_name=family_name)

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

    ##########################################################################
    # 'Editor' interface.
    ##########################################################################

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
                                                  size=wx.Size(60, 20))
        sizer.Add(control, 1)

        # Add space before units to ensure attractive layout
        unit_string = " " + self._get_display_units(self.value).label

        label = wx.StaticText(panel, -1,
                              unit_string,
                              style=wx.ALIGN_LEFT)
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

    def update_editor(self):
        """ Updates the editor when the object trait changes external to the
            editor.
        """
        self._updating_editor = True
        string_value = self.string_value(self._to_display_units(self.value))
        self.text_control.SetValue(string_value)
        self._updating_editor = False

    def update_object(self, event, assign=True):
        """ Handles the user changing the contents of the edit control.
        """
        if not self._updating_editor:
            try:
                value = float(self.text_control.GetValue())
                if assign:
                    self.value = self._from_display_units(value, self.value)
                if self.text_control is not None:
                    self.text_control.SetBackgroundColour(OKColor)
                    self.text_control.Refresh()
                    if self._error is not None:
                        self._error = None
                        self.ui.errors -= 1
            except:
                self.text_control.SetBackgroundColour(ErrorColor)
                self.text_control.Refresh()
                if self._error is None:
                    self._error = True
                    self.ui.errors += 1

    def check_value(self, event):
        """ Handles the user changing the contents of the edit control, but
            the value should only be checked, not assigned.
        """
        self.update_object(event, assign=False)

    def dispose(self):
        """ Disposes of the contents of an editor.
        """
        super(SimpleQuantityEditor, self).dispose()
        self.text_control = None


class ReadOnlyQuantityEditor(Editor):

    ##########################################################################
    # 'Editor' interface.
    ##########################################################################

    def init(self, parent):
        """ Finishes initializing the editor by creating the underlying toolkit
            widget.

            The read only widget is a text label with the units and the family name.
        """
        control = wx.TextCtrl(parent, -1,
                              style=wx.TE_READONLY | wx.STATIC_BORDER),
        control.SetBackgroundColour(ReadonlyColor)
        self.control = control

    def update_editor(self):
        """ Updates the editor when the object trait changes external to the
            editor.
        """
        # FIXME: The following line should fail...to_default_units is not defined for
        # this context. (TNV)
        string_value = '%s %s' % (self.to_default_units(self.value),
                                  self._get_family_name(self.value))
        self.control.SetValue(string_value)
