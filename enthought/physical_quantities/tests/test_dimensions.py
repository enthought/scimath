
from unittest import TestCase

from enthought.physical_quantities.dimensions import Dimensions, Dim, \
        dict_add, dict_sub, dict_mul, dict_div


class DictArithmeticTest(TestCase):
    def test_add(self):
        a = {'a': 3.0, 'b': -4.0, 'd': 2.0}
        b = {'a': 1.5, 'c': 12.0, 'd': -2.0}
        assert dict_add(a, b) == {'a': 4.5, 'b': -4.0, 'c': 12.0}

    def test_sub(self):
        a = {'a': 3.0, 'b': -4.0, 'd': 2.0}
        b = {'a': 1.5, 'c': 12.0, 'd': 2.0}
        assert dict_sub(a, b) == {'a': 1.5, 'b': -4.0, 'c': -12.0}

    def test_mul(self):
        a = {'a': 2.0, 'b': -4.0}
        n = 1.5
        assert dict_mul(a, n) == {'a': 3.0, 'b': -6.0}

    def test_zero_mul(self):
        a = {'a': 2.0, 'b': -4.0}
        n = 0.0
        assert dict_mul(a, n) == {}

    def test_div(self):
        a = {'a': 2.0, 'b': -4.0}
        n = 0.5
        assert dict_div(a, n) == {'a': 4.0, 'b': -8.0}


class QuantityTypeTest(TestCase):
    def setUp(self):
        self.dimensionless = Dimensions({})
        self.length = Dimensions({"length": 1.0})
        self.mass = Dimensions({"mass": 1.0, 'time': 0.0})
        self.time = Dimensions({"time": 1.0})
        self.acceleration = Dimensions({"length": 1.0, "time": -2.0})
        self.force = Dimensions({"mass": 1.0, "length": 1.0, "time": -2.0})
        self.also_force = Dimensions({"mass": 1.0, "length": 1.0,
                                              "time": -2.0})
    
    # Tests for basic initialization
    def test_setup_simple(self):
        assert self.length.dimension_dict == {"length": 1.0}
    
    def test_setup_remove_dimensions(self):
        assert self.mass.dimension_dict == {"mass": 1.0}
    
    # Tests for expansion property
    def test_expansion_dimensionless(self):
        assert self.dimensionless.expansion == "dimensionless"
      
    def test_expansion_simple(self):
        assert self.length.expansion == "length"
    
    def test_expansion_complex(self):
        assert self.force.expansion == "length*mass*time**-2.0"
    
    def test_expansion_expression(self):
        velocity = self.length/self.time
        assert velocity.expansion == "length*time**-1.0"
    
    def test_expansion_complete_cancellation(self):
        dimensionless = self.force/self.force
        assert dimensionless.expansion == "dimensionless"
    
    # Tests for __str__ method
    def test_str_dimensionless(self):
        assert str(self.dimensionless) == "dimensionless"
    
    def test_str_simple(self):
        assert str(self.length) == "length"
    
    def test_str_complex(self):
        assert str(self.force) == "length*mass*time**-2.0"
    
    def test_str_expression(self):
        velocity = self.length/self.time
        assert str(velocity) == "length*time**-1.0"
    
    # Tests for equality and inequality
    def test_equality(self):
        assert self.force == self.also_force
    
    def test_inequality(self):
        assert self.force != self.acceleration
    
    # Tests for arithmetic operations
    def test_mul(self):
        force = self.acceleration*self.mass
        assert force.dimension_dict == {"length": 1.0, "time": -2.0, "mass": 1.0}
            
    def test_div(self):
        velocity = self.length/self.time
        assert velocity.dimension_dict == {"length": 1.0, "time": -1.0}
    
    def test_pow(self):
        area = self.length**2
        assert area.dimension_dict == {"length": 2.0}
    
    def test_cancellation(self):
        acceleration = self.force*self.time/self.mass
        assert acceleration.dimension_dict == {"length": 1.0, "time": -1.0}
    
    def test_complete_cancellation(self):
        dimensionless = self.force/self.force
        assert dimensionless.dimension_dict == {}
        

# TODO: write tests for Dim trait
 