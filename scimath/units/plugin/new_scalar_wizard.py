""" A wizard that creates a new Scalar """

from __future__ import absolute_import
from traits.api import Instance

from envisage.project.wizard import NewResourceWizard
from envisage.project.wizard import NewNamedResourcePage

from scimath.units.scalar import Scalar

from .new_quantity_wizard import QuantityFactory
from .new_quantity_resource_page import NewQuantityResourcePage


class ScalarFactory(QuantityFactory):
    """ A factory that creates Scalar resources. """

    def create_resource(self):
        """ Creates the resource. """

        # Create a new scalar.
        scalar = Scalar(self.value, self.units,
                        name=self.name, family_name=self.value_unit_family
                        )

        # Bind it in the namespace
        self.parent_folder.obj.bind(self.name, scalar)

        return


class NewScalarWizard(NewResourceWizard):
    """ A wizard that creates a new Scalar. """

    #### 'Window' interface ###################################################

    # The window title.
    title = 'New Scalar'

    # The resource factory that the wizard is configuring.
    factory = Instance(ScalarFactory, ())

    ###########################################################################
    # 'NewResourceWizard' interface.
    ###########################################################################

    def reset(self):
        """ Reset the wizard to the initial state. """

        # The pages in the wizard.
        self.pages = [
            NewNamedResourcePage(
                id='resource_page',
                text='Select the parent folder',
                prefix='New Scalar',
                obj=self.factory
            ),
            NewQuantityResourcePage(
                id='quantity_details',
                text='Scalar Properties',
                obj=self.factory
            )
        ]

        return
