""" A Scalar is a Quantity object that limits data to floats.
"""

from enthought.traits.api import Trait
from enthought.units.quantity import Quantity

class Scalar( Quantity ):
    """ A Scalar is a Quantity object that limits data to floats.
    """
    data = Trait( float )


### EOF #######################################################################
