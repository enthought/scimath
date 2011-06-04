""" A Scalar is a Quantity object that limits data to floats.
"""

from traits.api import Trait
from scimath.units.quantity import Quantity

class Scalar( Quantity ):
    """ A Scalar is a Quantity object that limits data to floats.
    """
    data = Trait( float )


### EOF #######################################################################
