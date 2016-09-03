""" Resource editor for QuantityResourceType """


from __future__ import absolute_import
from traits.api import Instance
from traitsui.api import Handler
from traitsui.menu import NoButtons

from envisage.ui.traits_ui_editor import TraitsUIEditor

from apptools.naming.api import Context, NameNotFoundError


class QuantityResourceEditor(TraitsUIEditor):
    """ Resource editor for QuantityResourceType """

    context = Instance(Context)

    ### TraitsUIEditor interface ##############################################

    def create_ui(self, parent=None):
        """ Return the traits ui panel for self.resource. """

        qty = self.resource

        self.title = "Edit %s" % qty.name

        traits_ui = qty.edit_traits(parent=parent, kind='panel')

        # Reach into the Quantity traits view and 1) turn off the buttons
        traits_ui.view.buttons = NoButtons

        # and 2) make the name readonly as name should only change via
        # the nameing system interface.
        for item in traits_ui.view.content.content[0].content:
            if item.name == 'name':
                item.style = 'readonly'
                break

        traits_ui.updated = True

        self.size = (max(300, traits_ui.view.width),
                     max(200, traits_ui.view.height))

        return traits_ui


# EOF
