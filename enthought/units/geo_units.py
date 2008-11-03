from copy import copy
from enthought.units.SI import *
from enthought.units.length import foot, inch, m, meter, kilometers
from enthought.units.mass import grams, lb
from enthought.units.force import lbf
from enthought.units.time import microsecond
from enthought.units.volume import cubic_centimeter, cubic_meter, us_fluid_gallon, \
                         liter, cubic_foot
from enthought.units.pressure import GPa, MPa, bar

#############################################################################
# impedance_units          g*km/cc/s, g*f/cc/s
#############################################################################
g_km_per_cc_s = (grams*kilometers)/(cubic_centimeter*second)
g_km_per_cc_s.label = 'g*km/(cc*s)'
g_ft_per_cc_s = (grams*foot)/(cubic_centimeter*second)
g_ft_per_cc_s.label = 'g*ft/(cc*s)'

#############################################################################
# modulus_units            GPa, MPa
# pressure_units           MPa, psi, kbar, bar
#############################################################################
GPa.label = 'GPa'
MPa.label = 'MPa'
bar.label = 'bar'
pounds_per_square_inch = lbf/inch**2
pounds_per_square_inch.label = 'psi'
kilobar = kilo*bar
kilobar.label = 'kbar'

#shorthand
gpa = GPa
Gpa = GPa
GPA = GPa
mpa = MPa
Mpa = MPa
MPA = MPa

lbs = lbf
lbs.label = 'lbs'
psi = pounds_per_square_inch
apsi = psi
psig = psi
N = newton

bars = bar
kbar = kilobar
kbars = kbar


#############################################################################
# pressure_gradient_units  psi/f, MPa/m, lb/gal, MPa/100f
#############################################################################

psi_per_f  = psi/foot
psi_per_f.label  = 'psi/ft'
psi_per_ft = psi_per_f

MPa_per_m = MPa/meter
MPa_per_m.label = 'MPa/m'

lb_per_gal    = lb/us_fluid_gallon
lb_per_gallon = lb_per_gal

#############################################################################
# PPG seems to have units of mass/volume and not weight/volume so we cannot
# use the unit system to automatically convert for us unless we lie about
# the dimensionality of ppg and pretend it is the same as psi/ft.
#############################################################################
# This is dimensionally inconsistant which may bite us later.
#############################################################################

psi_per_ft = pounds_per_square_inch /foot
ppg        = psi_per_ft / 0.0519

MPa_per_f  = MPa/foot
MPa_per_f.label = 'MPa/ft'
MPa_per_ft = MPa_per_f
MPa_per_100f  = MPa/(100*foot)
MPa_per_100f.label = 'MPa/100ft'
MPa_per_100ft = MPa_per_100f

#############################################################################
# electric_potential_units mv -- TODO: this may need to be avialable in the
#                                general units stuff
#############################################################################

volt.label = 'volts'
volts = volt
v = volt

millivolts = milli*volts
millivolts.label = 'mv'
mv = millivolts

#############################################################################
# resistivity_units        ohmm
#############################################################################

ohm.label = 'ohm'
ohms = ohm
ohmm = ohm*meter
ohmm.label = 'ohmm'
ohm_m = ohmm
ohm_meter = ohmm
ohms_per_m = ohmm
ohms_per_meter = ohmm

#############################################################################
# conductivity_units       S/m, mmhos, mh/m
#############################################################################

siemen = siemens
mSiemen = siemens * milli
mS = mSiemen
siemens.label = 'S'
siemens_per_meter = siemens/meter
siemens_per_meter.label = 'S/m'
siemens_per_m = siemens_per_meter
mho = copy(siemens)
mho.label = 'mho'
mmho = siemens*milli
mmho.label = 'mmho'

#############################################################################
# fractional or percentage units.
#############################################################################

fractional = copy(dimensionless)
fractional.label = 'V/V'
fraction = fractional
ratio = frac = fractional

percent = fractional / 100.
percent.label = '%'
percentage = percent
pct = percent

#############################################################################
# concentration (parts per million)
#############################################################################
parts_per_one = dimensionless
parts_per_million = parts_per_one / 1e6
parts_per_million.label = 'ppm'
ppm = parts_per_million
#############################################################################
# Gamma Ray
#############################################################################
api = gapi = dimensionless

#############################################################################
# psonic
#############################################################################
us_per_ft = microsecond/foot
us_per_ft = 'us/ft'
