""" Set the system-wide default unit system. """
# Standard library imports.
from __future__ import absolute_import
import logging

# Enthought library imports.
from envisage.ui import WorkbenchAction
from traits.api import HasTraits
from traitsui.api import Group, Item, View
from traitsui.menu import OKCancelButtons
from scimath.units.unit_traits import unit_system_trait

from scimath.units.plugin.units_plugin import UnitsPlugin


logger = logging.getLogger(__name__)


class UnitChooser(HasTraits):

    unit_system = unit_system_trait

    view = View(Item(name = 'unit_system'),
                buttons = OKCancelButtons)

class SetUnitSystem(WorkbenchAction):
    """ Set the system-wide default unit system. """

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform (self, event = None):
        """ Perform the action. """

        from scimath.units import unit_manager
        chooser = UnitChooser(unit_system = unit_manager.get_default())
        ui = chooser.edit_traits(kind = 'livemodal')

        if ui.result:
            from scimath.units.unit_manager import unit_manager
            unit_manager.set_default(chooser.unit_system)

            UnitsPlugin.instance.set_default_unit_system(chooser.unit_system)

        return

#### EOF ######################################################################
