""" A wizard that creates a new Quantity. """


# Enthought library imports.
from __future__ import absolute_import
from traits.api import Float, Instance, Str
from scimath.units.family_name_trait import FamilyNameTrait

from envisage.project.wizard import NewNamedResourcePage
from envisage.project.wizard import NewResourceWizard
from envisage.project.wizard import ResourceFactory

from scimath.units.quantity import Quantity

from .new_quantity_resource_page import NewQuantityResourcePage

class QuantityFactory(ResourceFactory):
    """ A factory that creates Quantity resources. """

    # The initial value.
    value = Float

    # units
    units = Str('none')

    # The unit family for the value.
    value_unit_family = FamilyNameTrait

    ###########################################################################
    # 'ResourceFactory' interface.
    ###########################################################################

    def create_resource(self):
        """ Creates the resource. """

        # Create a new quantity.
        quantity = Quantity(self.value, self.units,
            name=self.name, family_name=self.value_unit_family
        )

        # Bind it in the namespace
        self.parent_folder.obj.bind(self.name, quantity)

        return


class NewQuantityWizard(NewResourceWizard):
    """ A wizard that creates a new quantity. """

    #### 'Window' interface ###################################################

    # The window title.
    title = 'New Quantity'

    # The resource factory that the wizard is configuring.
    factory = Instance(QuantityFactory, ())

    ###########################################################################
    # 'NewResourceWizard' interface.
    ###########################################################################

    def reset(self):
        """ Reset the wizard to the initial state. """

        # The pages in the wizard.
        self.pages = [
            NewNamedResourcePage(
                id     = 'resource_page',
                text   = 'Select the parent folder',
                prefix = 'New Quantity',
                obj    = self.factory
            ),
            NewQuantityResourcePage(
                id     = 'quantity_details',
                text   = 'Quantity Properties',
                obj    = self.factory
            )
        ]

        return

#### EOF ######################################################################
