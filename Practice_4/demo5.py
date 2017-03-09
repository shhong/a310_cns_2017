'''
demo5.py

Demo of a simple cell driven by synaptic inputs.

Written by Sungho Hong, Computational Neuroscience Unit, OIST, 2017
'''

from neuron import h, gui

h.load_file("stdrun.hoc")
h.load_file("CNSutils.hoc") # CNSsaveVectors

# The simulation will run for 100 ms.
h.tstop = 200
# Global sampling period will be 0.1 ms -> 10 kHz sampling..
Dt = 0.1

# Creating a cell
soma = h.Section()
soma.diam = 100/h.PI
soma.L = 100
soma.insert("pas")
soma.g_pas = 1e-4

# Synapses
syns = []

# 400 excitatory synapses
for i in range(400):
    syns.append(h.Exp2Syn(0.5, sec=soma))
    syns[-1].tau1 = 0.5 # rise time
    syns[-1].tau2 = 1.5 # decay time
    syns[-1].e = 0      # reversal potential

# 100 inhibitory synapses
for i in range(100):
    syns.append(h.Exp2Syn(0.5, sec=soma))
    syns[-1].tau1 = 1   # rise time
    syns[-1].tau2 = 10  # decay time
    syns[-1].e = -75    # reversal potential

# Stimuli = random spike trains
isi = 1000./0.01  # average interspike interval for 0.01 Hz
stims = []
for i in range(500):
    stims.append(h.NetStimFD(0.5))
    stims[-1].noise = 1          # random firing
    stims[-1].start = 0
    stims[-1].duration = h.tstop
    stims[-1].interval = isi

stims[0].seed(1) # Set seed for noise

# Connections
ncs = []
for i in range(400):
    ncs.append(h.NetCon(stims[i], syns[i]))
    ncs[-1].weight[0] = 0.5e-3 

for i in range(100):
    ncs.append(h.NetCon(stims[i+400], syns[i+400]))
    ncs[-1].weight[0] = 2e-3

# Set up a current clamp to probe the neuron
ic = h.IClamp(0.5, sec=soma)
ic.delay = 50
ic.amp = 0.1 
ic.dur = 100

# open the GUI
h.xopen("week2.ses")

vtemp = h.Vector()
vtemp.record(soma(0.5)._ref_v, Dt)

h.v_init = -70
h.init()
h.run()

h.CNSsaveVectors("voltage.csv", Dt, vtemp)

## For repeated run
# Nrepeat = 100
# for i in range(Nrepeat):
#     h.v_init = -70
#     h.init()
#     h.run()
#     if i==0:
#         vave = vtemp.c()
#     else:
#         vave.add(vtemp)
#     print i

# vave.div(Nrepeat)

# h.CNSsaveVectors("voltage.csv", Dt, vave)
