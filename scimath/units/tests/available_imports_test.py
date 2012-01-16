# Standard Library imports
import unittest

# Enthought Library imports
from traits.testing.api import doctest_for_module

geo_imports = [
    'GPA', 'GPa', 'Gpa', 'MPA', 'MPa', 'MPa_per_100f', 'MPa_per_100ft',
    'MPa_per_f', 'MPa_per_ft', 'MPa_per_m', 'Mpa', 'N', 'ampere', 'api',
    'apsi', 'atto', 'bar', 'bars', 'becquerel', 'candela', 'centi', 'copy',
    'coulomb', 'cubic_centimeter', 'cubic_foot', 'cubic_meter', 'deci', 'deka',
    'dimensionless', 'exa', 'farad', 'femto', 'foot', 'frac', 'fraction',
    'fractional', 'g_ft_per_cc_s', 'g_km_per_cc_s', 'gapi', 'giga', 'gpa',
    'grams', 'gray', 'hecto', 'henry', 'hertz', 'inch', 'joule', 'katal',
    'kbar', 'kbars', 'kilo', 'kilobar', 'kilogram', 'kilometers', 'lb',
    'lb_per_gal', 'lb_per_gallon', 'lbf', 'lbs', 'liter', 'lumen', 'lux', 'm',
    'mS', 'mSiemen', 'mega', 'meter', 'mho', 'micro', 'microsecond', 'milli',
    'millivolts', 'mmho', 'mole', 'mpa', 'mv', 'nano', 'newton', 'none', 'ohm',
    'ohm_m', 'ohm_meter', 'ohmm', 'ohms', 'ohms_per_m', 'ohms_per_meter',
    'parts_per_million', 'parts_per_one', 'pascal', 'pct', 'percent',
    'percentage', 'peta', 'pico', 'pounds_per_square_inch', 'ppg', 'ppm',
    'psi', 'psi_per_f', 'psi_per_ft', 'psig', 'radian', 'ratio', 'second',
    'siemen', 'siemens', 'siemens_per_m', 'siemens_per_meter', 'sievert',
    'steradian', 'tera', 'tesla', 'unit', 'us_fluid_gallon', 'us_per_ft', 'v',
    'volt', 'volts', 'watt', 'weber', 'yocto', 'yotta', 'zepto', 'zetta'
    ]

def write_geo_err_msg(name):
    """write the message describing the import not found in geo_units"""
    msg = """Could not find previously available import '{0}' in 
    scimath.units.geo_units module. Check to ensure that '{0}' is
    available as an import from scimath.units.geounits."""
    return msg.format(name)

class GeoUnitsImportsTestCase(unittest.TestCase):
    """ When geo_units was initially set up, many units were defined there
    which should have been defined elsewhere and imported to geo_units, causing
    some problems later when things like "psi" could not be imported from
    scimath.units.pressure but were instead found in
    scimath.units.geo_units. In Dec 2011, the units were reorganized to make
    units available in their expected location. This test was set up to ensure
    that not code that imported a unit from geo_units would break in the
    reorganization.
    
    """
    def test_geo_imports(self):
        """ Test whether everything that was availabile in geo_units still is available.
        """
        from scimath.units import geo_units

        available_now = geo_units.__dict__
        
        for name in geo_imports:
            self.assertIn(name, available_now, msg=write_geo_err_msg(name))
            
if __name__ == '__main__':
    unittest.main()
