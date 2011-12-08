from scimath.units.api import has_units
from scimath.units.length import foot, meter

@has_units
def add(a,b):
     """ Add two arrays in ft and convert them to m.

         Parameters
         ----------
         a : array : units=ft
             An array
         b : array : units=ft
             Another array

         Returns
         -------
         c : array : units=m
             c = a + b

     """
     return (a + b) * foot / meter

