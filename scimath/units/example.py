from __future__ import absolute_import
from scimath.units.api import has_units
from scimath.units.example_units import a_duck
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

@has_units
def witch_test(mass_of_maiden):
     """ Test to determine if one or more young maidens is a witch.

     Parameters
     ----------
     mass_of_maiden : array : units=a_duck
         array of masses to check against the weight of a duck

     Returns
     -------
     truth : bool

     Description
     -----------
     If she weighs as much as a duck, then she's made of wood, and she floats,
     so she's a witch.
     """
     return mass_of_maiden >= 1
