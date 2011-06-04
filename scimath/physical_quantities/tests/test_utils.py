
from unittest import TestCase

from scimath.physical_quantities.util import dict_add, dict_sub, dict_mul, \
    dict_div, format_expansion, unicode_powers, tex_powers, name_powers


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


class FormatTest(TestCase):
    def setUp(self):
        self.coulomb = {"A": 1.0, 's': 1.0}
        self.joule = {"kg": 1.0, "m": 2.0, "s": -2.0}
        self.volt = {"kg": 1.0, "m": 2.0, "s": -3.0, "A": -1.0}
        self.hertz = {"s": -1.0}
        self.ohm = {u"\u2126": 1.0}
        self.siemens = {u"\u2126": -1.0}

    def test_python_defaults(self):
        assert format_expansion(self.volt) == "A**-1*kg*m**2*s**-3"

    def test_python_division(self):
        assert format_expansion(self.volt, div=True) == "kg*m**2/(A*s**3)"

    def test_python_division_simple_denominator(self):
        assert format_expansion(self.joule, div=True) == "kg*m**2/s**2"

    def test_python_division_no_denominator(self):
        assert format_expansion(self.coulomb, div=True) == "A*s"

    def test_python_division_no_numerator_simple_denominator(self):
        assert format_expansion(self.hertz, div=True) == "1/s"

    def test_python_division_no_numerator_no_denominator(self):
        assert format_expansion({}, div=True) == "1"

    def test_python_rational_power(self):
        assert format_expansion({'m': 0.5}) == "m**0.5"

    def test_unicode(self):
        assert format_expansion(self.volt, mul=" ",
                                pow_func=unicode_powers) == u"A\u207B\u00B9 kg m\u00B2 s\u207B\u00B3"

    def test_unicode_symbol(self):
        assert format_expansion(self.volt, mul=" ",
                                pow_func=unicode_powers) == u"A\u207B\u00B9 kg m\u00B2 s\u207B\u00B3"

    def test_unicode_division(self):
        assert format_expansion(self.volt, mul=" ", div=True,
                                pow_func=unicode_powers) == u"kg m\u00B2/(A s\u00B3)"

    def test_unicode_division_simple_denominator(self):
        assert format_expansion(self.joule, mul=" ", div=True,
                                pow_func=unicode_powers) == u"kg m\u00B2/s\u00B2"

    def test_unicode_division_no_denominator(self):
        assert format_expansion(self.coulomb, mul=" ", div=True,
                                pow_func=unicode_powers) == u"A s"

    def test_unicode_symbol(self):
        assert format_expansion(self.siemens, mul=" ",
                                pow_func=unicode_powers) == u"\u2126\u207B\u00B9"

    def test_unicode_symbol_division(self):
        assert format_expansion(self.siemens, mul=" ", div=True,
                                pow_func=unicode_powers) == u"1/\u2126"

    def test_unicode_rational_power(self):
        assert format_expansion({'m': 0.5}, mul=" ",
                                pow_func=unicode_powers) == u"m^0.5"

    def test_TeX_defaults(self):
        assert format_expansion(self.volt, mul="\/",
                                pow_func=tex_powers) == "A^{-1}\/kg\/m^{2}\/s^{-3}"

    def test_TeX_division(self):
        assert format_expansion(self.volt, mul="\/", div=True,
                                pow_func=tex_powers) == "kg\/m^{2}/(A\/s^{3})"

    def test_TeX_division_simple_denominator(self):
        assert format_expansion(self.joule, mul="\/", div=True,
                                pow_func=tex_powers) == "kg\/m^{2}/s^{2}"

    def test_TeX_division_no_denominator(self):
        assert format_expansion(self.coulomb, mul="\/", div=True,
                                pow_func=tex_powers) == "A\/s"

    def test_TeX_division_no_numerator_simple_denominator(self):
        assert format_expansion(self.hertz, mul="\/", div=True,
                                pow_func=tex_powers) == "1/s"

    def test_unicode_rational_power(self):
        assert format_expansion({'m': 0.5}, mul="\/",
                                pow_func=tex_powers) == "m^{0.5}"

    def test_name_defaults(self):
        assert format_expansion(self.volt, mul=" ", empty_numerator="1",
                                div_symbol=" per ", group_symbols=("", ""),
                                pow_func=name_powers) == "A to the -1 kg square m s to the -3"

    def test_name_division(self):
        assert format_expansion(self.volt, mul=" ", empty_numerator="1",
                                div_symbol=" per ", group_symbols=("", ""),
                                div=True,
                                pow_func=name_powers) == "kg square m per A cubic s"

    def test_name_division_no_numerator_simple_denominator(self):
        assert format_expansion(self.hertz, mul=" ", empty_numerator="",
                                div_symbol=" per ", group_symbols=("", ""),
                                div=True,
                                pow_func=name_powers) == " per s"
