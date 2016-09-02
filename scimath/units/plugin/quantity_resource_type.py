""" The resource type for quantities. """


# Enthought library imports.
from __future__ import absolute_import
from envisage.resource import ObjectResourceType
from traits.api import Instance
from scimath.units.quantity import Quantity

# Local imports.
from .quantity_node_type import QuantityNodeType
from .quantity_resource_editor import QuantityResourceEditor

class QuantityResourceType(ObjectResourceType):
    """ The resource type for quantities. """

    #### 'ResourceType' interface #############################################

    # A trait that describes the kind of domain object that the resource type
    # represents.
    type = Instance(Quantity)

    ###########################################################################
    # 'ResourceType' interface.
    ###########################################################################

    # Properties editor class.
    editor = QuantityResourceEditor

    #### Initializers #########################################################

    def _node_type_default(self):
        """ Initializes the node type. """

        return QuantityNodeType(resource_type=self)


    #### Methods ##############################################################

    def clone(self, obj):
        """ Returns a clone of a resource of this type. """

        return obj.clone()

    def get_name(self, obj):
        """ Returns the name of a resource of this type. """

        return obj.name

    def set_name(self, obj, name):
        """ Sets the name of a resource of this type. """

        obj.name = name

        return

##### EOF #####################################################################
