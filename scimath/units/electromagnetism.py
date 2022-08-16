# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from copy import copy

from scimath.units.SI import ampere, coulomb, farad, henry, joule, ohm, \
    meter, micro, milli, pico, siemens, tesla, volt, watt, weber

###############################################################################
# electric current
###############################################################################

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

millivolt = milli * volt
millivolt.label = 'mV'
milli_volt = millivolt
mv = millivolt
millivolts = millivolt

###############################################################################
# resistivity
###############################################################################

ohms = ohm
ohmm = ohm * meter
ohmm.label = 'ohmm'
ohm_m = ohmm
ohm_meter = ohmm
ohms_per_m = ohmm
ohms_per_meter = ohmm

###############################################################################
# capacitance
###############################################################################

micro_farad = micro * farad
micro_farad.label = 'uf'
mf = micro_farad

pico_farad = pico * farad
pico_farad.label = 'pf'
pf = pico_farad

###############################################################################
# conductivity
###############################################################################

siemen = siemens
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

###############################################################################
# Magnetic Flux
###############################################################################

webers = weber

###############################################################################
# Magnetic Field
###############################################################################

teslas = tesla
