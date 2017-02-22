"""

hw3_2.py

Monitoring how the ion channels activate
"""

import neuron
# neuron.load_mechanisms('.')
from neuron import h, gui

h.load_file("stdrun.hoc")   # load init(), run(), etc.

# Create a cell
soma = h.Section(name="soma")
soma.diam = 15
soma.L = 15

soma.insert("ml")
soma.betaw_ml = 0 # This controls the half-maximum voltage of the K+ channel.

# Inject bias current
ic_bias = h.IClamp(0.5, sec=soma)
ic_bias.delay = 0
ic_bias.dur = 1000
if soma.betaw_ml < -10:
    ic_bias.amp = 0.29  # if the cell has a low threshold K+ channel
else:
    ic_bias.amp = 0.25  # if the cell has a high threshold K+ channel


# Sharp current injection
ic = h.IClamp(0.5, sec=soma)
ic.delay = 100
ic.dur = 1

ic.amp = 0.1 # We inject 100pA for 1 ms.


# Record variables
vrec, inarec, ikrec, mrec, wrec = [h.Vector() for i in range(5)]
vrec.record(soma(0.5)._ref_v, 0.1)  # Record the voltage
inarec.record(soma(0.5)._ref_ina, 0.1)  # Record the Na+ current
ikrec.record(soma(0.5)._ref_ik, 0.1)  # Record the K+ current
mrec.record(soma(0.5)._ref_m_ml, 0.1)  # Record the m gate
wrec.record(soma(0.5)._ref_w_ml, 0.1)  # Record the w gate

h.v_init = 0
h.tstop = 200
h.xopen("hw3_2.ses")

h.init()
h.run()

h.load_file("CNSutils.hoc")
h.CNSsaveVectors("data.csv", 0.1, vrec, inarec, ikrec, mrec, wrec)
