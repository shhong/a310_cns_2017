'''
hw4_2.py

A single cell driven by synaptic inputs.

Written by Sungho Hong, Computational Neuroscience Unit, OIST, 2017
'''

from neuron import h, gui

h.load_file("stdrun.hoc")
h.load_file("CNSutils.hoc") # CNSsaveVectors

# The simulation will run for 100 ms.
h.tstop = 300
# Global sampling period will be 0.1 ms -> 10 kHz sampling..
Dt = 0.1

# Creating a cell
soma = h.Section()
soma.diam = 100/h.PI
soma.L = 100         # With these, the membrane area = 1e-4 cm^2
soma.insert("pas")
soma.g_pas = 5e-5  # This makes tau = 20 ms
soma.e_pas = -70  # Reversal potential

# Add an excitatory and inhibitory synapse to the cells
syns = []

# 1 excitatory synapses
syns.append(h.Exp2Syn(0.5, sec=soma))
syns[-1].tau1 = 0.1 # rise time
syns[-1].tau2 = 1.25 # decay time
syns[-1].e = 0      # reversal potential

# 1 inhibitory synapses
syns.append(h.Exp2Syn(0.5, sec=soma))
syns[-1].tau1 = 1   # rise time
syns[-1].tau2 = 10  # decay time
syns[-1].e = -75    # reversal potential



# Define 100 excitatory ahd 20 inhibitory synapses firing at 10 Hz
Nexc = 100   # Number of excitatory stimuli
Ninh = 20    # Number of inhibitory stimuli
fexc = 10.   # Average firing rate of excitatory inputs
finh = 0.001   # Average firing rate of inhibitory inputs

stims = []
# Define Nexc excitatory stimuli
for i in range(Nexc):
    stims.append(h.NetStimFD(0.5))
    stims[-1].noise = 1          # random firing
    stims[-1].start = 0
    stims[-1].duration = h.tstop
    stims[-1].interval = 1e3/fexc

# Define Ninh inhibitory stimuli
for i in range(Ninh):
    stims.append(h.NetStimFD(0.5))
    stims[-1].noise = 1          # random firing
    stims[-1].start = 0
    stims[-1].duration = h.tstop
    stims[-1].interval = 1e3/finh


stims[0].seed(1) # Set seed for noise

# Make connections
ncs = []
for i in range(Nexc):
    ncs.append(h.NetCon(stims[i], syns[0]))
    ncs[-1].weight[0] = 1e-3

for i in range(Ninh):
    ncs.append(h.NetCon(stims[i+Nexc], syns[1]))
    ncs[-1].weight[0] = 0


# Insert a current clamp to probe the neuron
# ic = h.IClamp(0.5, sec=soma)
# ic.delay = 50
# ic.amp = 0.1
# ic.dur = 150

# Open the GUI
h.xopen("week2.ses")

# Set up the recording for membrane potential
vtemp = h.Vector()
vtemp.record(soma(0.5)._ref_v, Dt)

# For repeated run
vrecords = h.List()
Nrepeat = 100
for i in range(Nrepeat):
    h.v_init = -70
    h.init()
    h.run()
    vrecords.append(vtemp.c()   )
    print "Simulation:", i
h.CNSsaveListOfVectors("voltages_hw4_2.csv", Dt, vrecords)
