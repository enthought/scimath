from __future__ import absolute_import
from copy import copy

from scimath.units.SI import ampere, coulomb, farad, henry, joule, ohm, \
    meter, micro, milli, pico, siemens, tesla, volt, watt, weber, kilo

###############################################################################
# electric charge
###############################################################################

C = coulomb

###############################################################################
# electric current
###############################################################################

A = ampere
amp = ampere
amps = ampere
amperes = ampere

milli_ampere = milli * ampere
milli_ampere.label = 'mA'
mA = milli_ampere
milli_amp = milli_ampere


###############################################################################
# electric potential
###############################################################################

volts = volt
v = volt
V = volt

millivolt = milli * volt
millivolt.label = 'mv'
milli_volt = millivolt
mv = millivolt
mV = millivolt
millivolts = millivolt

kilovolt = kilo * volt
kilovolt.label = 'kv'
kv = kilovolt
kV = kilovolt

###############################################################################
# resistivity
###############################################################################

ohms = ohm
Ohm = ohm
Ohms = ohms
ohmm = ohm * meter
ohmm.label = 'ohmm'
ohm_m = ohmm
ohm_meter = ohmm
ohms_per_m = ohmm
ohms_per_meter = ohmm

###############################################################################
# capacitance
###############################################################################

F = farad

micro_farad = micro * farad
micro_farad.label = 'uf'
mf = micro_farad
mF = micro_farad

pico_farad = pico * farad
pico_farad.label = 'pf'
pf = pico_farad
pF = pico_farad

###############################################################################
# conductivity
###############################################################################

siemen = siemens
S = siemens
mSiemens = milli * siemens
mSiemens.label = 'mS'
mSiemen = mSiemens
mS = mSiemens

siemens_per_meter = siemens / meter
siemens_per_meter.label = 'S/m'
siemens_per_m = siemens_per_meter

mho = copy(siemens)
mho.label = 'mho'

mmho = milli * siemens
mmho.label = 'mmho'

###############################################################################
# Inductance
###############################################################################

henrys = henry
H = henry

###############################################################################
# Magnetic Flux
###############################################################################

webers = weber
Wb = weber

###############################################################################
# Magnetic Field
###############################################################################

teslas = tesla
T = tesla
