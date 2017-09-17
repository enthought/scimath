""" The resource type for quantities. """


# Enthought library imports.
from __future__ import absolute_import
from envisage.resource import ObjectNodeType
from pyface.api import ImageResource


class QuantityNodeType(ObjectNodeType):
    """ The resource type for quantities. """

    #### 'NodeType' interface #################################################

    # The image used to represent nodes of this type.
    image = ImageResource('quantity')

    ###########################################################################
    # 'NodeType' interface.
    ###########################################################################

    def allows_children(self, node):
        """ Does the node allow children (ie. a folder vs a file). """

        return False

##### EOF #####################################################################
