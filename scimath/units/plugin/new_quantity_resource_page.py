
from __future__ import absolute_import
import wx  # ugh!

from pyface.api import HeadingText, ImageResource, Sorter
from pyface.wizard.api import WizardPage
from traits.api import Any, Str
from traitsui.api import View

from scimath.units.unit_manager import unit_manager

class NewQuantityResourcePage(WizardPage):

    # The image used when displaying error messages.
    ERROR_IMAGE = ImageResource('error')

    # The object this wizard is configuring (i.e., the factory).
    obj = Any

    text = Str

    ###########################################################################
    # 'WizardPage' interface.
    ###########################################################################

    def create_page(self, parent):
        """ Creates the wizard page. """

        panel = wx.Panel(parent, -1, style=wx.CLIP_CHILDREN)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)

        # The 'pretty' title bar ;^)
        title = HeadingText(panel, text=self.text)
        sizer.Add(title.control, 0, wx.EXPAND | wx.BOTTOM, 5)

        # The editor for the quantity properties.
        view = View(
            [ 'value{Value}',
              'units{Units}',
              'value_unit_family{Measure of}']
        )

        ui = self.obj.edit_traits(parent=panel, view=view, kind='subpanel')
        sizer.Add(ui.control, 1, wx.EXPAND)

        # A panel to display any error messages.
        self._error_panel = error_panel = self._create_error_panel(panel)
        sizer.Add(error_panel, 0, wx.EXPAND | wx.TOP | wx.LEFT, 5)

        # Resize the panel to match the sizer's minimum size.
        sizer.Fit(panel)

        # Check if the default values constitute a valid quantity.
        self._validate()

        self.obj.on_trait_change( self._on_units_changed, 'units' )
        self.obj.on_trait_change( self._on_family_changed, 'value_unit_family' )
        return panel




    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_error_panel(self, parent):
        """ Creates the error panel. """

        panel = wx.Panel(parent, -1, style=wx.CLIP_CHILDREN)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)

        # The error bitmap.
        bmp = self.ERROR_IMAGE.create_image().ConvertToBitmap()
        error_bitmap = wx.StaticBitmap(panel, -1, bmp)
        sizer.Add(error_bitmap, 0, wx.EXPAND)

        # The error text.
        self._error_text = wx.StaticText(panel, -1, '')
        sizer.Add(self._error_text, 1, wx.EXPAND | wx.LEFT, 5)

        # Resize the panel to match the sizer's minimum size.
        sizer.Fit(panel)

        return panel

    def _validate(self):
        """ Validate the current state to see if the wizard can finish. """

        # Can't have a sample interval of 0.0 or less, since we would never
        # reach the bottom of the log.

        if not unit_manager.is_compatible( self.obj.units,
                                           self.obj.value_unit_family):
            self.complete = False
            self._error_text.SetLabel(
                'Units and family are incompatible. Try one of: %s'
                    % unit_manager.get_valid_unit_strings(
                                    self.obj.value_unit_family )
            )
            if self._error_panel is not None:
                self._error_panel.Show(True)
                self._error_panel.GetParent().GetSizer().Layout()

        elif self.obj.units is None or self.obj.units == '':
            self.complete = False
            self._error_text.SetLabel(
                'Units are required.'
            )
            if self._error_panel is not None:
                self._error_panel.Show(True)
                self._error_panel.GetParent().GetSizer().Layout()

        else:
            self.complete = True
            if self._error_panel is not None:
                self._error_panel.Show(False)
                self._error_panel.GetParent().GetSizer().Layout()

        return

    def _on_units_changed(self, old, new):
        """ Called when the units is changed. """
        self.obj.units = new.strip()
        self._validate()

        return

    def _on_family_changed(self, old, new):
        """ Called when the family name is changed. """
        self._validate()

        return

#### EOF ######################################################################
