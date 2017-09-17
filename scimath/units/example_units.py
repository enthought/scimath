from __future__ import absolute_import
from scimath.units.api import unit_parser
from scimath.units.mass import kilogram

apple = 0.2 * kilogram
apple.label = 'label'

bread = 0.5 * kilogram
bread.label = 'loaf of bread'

very_small_rocks = 0.02 * kilogram
very_small_rocks.label = 'very small rocks'

a_duck = 1.3 * kilogram
a_duck.label = 'a duck'

from . import example_units as u
unit_parser.parser.extend(u)
