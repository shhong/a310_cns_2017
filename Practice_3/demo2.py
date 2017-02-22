"""

demo2.py

A demo of the voltage clamp simulation

"""

import neuron
# neuron.load_mechanisms('.')
from neuron import h, gui

h.load_file("stdrun.hoc")   # load init(), run(), etc.

# Creating a cell
soma = h.Section(name="soma")
soma.diam = 15
soma.L = 15
soma.insert("ml")
# soma.betaw_ml = 0

h.tstop = 300

# Adding a voltage clamp
vc = h.SEClamp(0.5, sec=soma)
#vc.rs = 0.01 # Serial resistance https://www.neuron.yale.edu/neuron/static/new_doc/modelspec/programmatic/mechanisms/mech.html?SEClamp#SEClamp

vc.dur1 = 100
vc.dur2 = 100
vc.dur3 = 100
vc.amp1 = -70
vc.amp2 = -0
vc.amp3 = -10

h.xopen('demo2.ses')

# Recording currents!
ina_rec = h.Vector()
ik_rec = h.Vector()

ina_rec.record(soma(0.5)._ref_ina, 0.1) # Recoring ionic currents at 10 kHz
ik_rec.record(soma(0.5)._ref_ik, 0.1)

## In case that you want to record the currents only from a specific mechanism...
# ina_rec.record(soma(0.5)._ref_ina_ml, 0.1)
# ik_rec.record(soma(0.5)._ref_ik_ml, 0.1)

# Running the simulation
h.init()
h.run()

# Saving the data
h.load_file("CNSutils.hoc")
h.CNSsaveVectors("ina_ik.csv", 0.1, ina_rec, ik_rec)
