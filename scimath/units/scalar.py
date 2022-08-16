# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A Scalar is a Quantity object that limits data to floats.
"""

from traits.api import Trait
from scimath.units.quantity import Quantity


class Scalar(Quantity):
    """ A Scalar is a Quantity object that limits data to floats.
    """
    data = Trait(float)
