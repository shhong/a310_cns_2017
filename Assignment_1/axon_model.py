from neuron import h, gui

## Define an axon

axon = h.Section(name='axon')
axon.diam = 1.
axon.L = 1000.
axon.nseg = 100 # We segment the axon into 100 pieces


## Passive membrane
axon.insert('pas')

## Parameters
axon.cm = 1.      # 1 uF/cm^2
axon.Ra = 150.    # 150 Ohm cm
axon.g_pas = 5e-5 # 5*10^-5 S/cm^2


# We attach an electrode at one end and set parameters
ic = h.IClamp(0.005, sec=axon)

ic.delay = 100 # The injection starts at t=100ms
ic.dur = 200   # It last for 400ms
ic.amp = 0.1   # Current = 0.2 nA = 200 pA


# We will record the voltage at the mid point (x=0.5) with a  10 kHz (dt = 0.1 ms) sampling rate
vc = h.Vector()
vc.record(axon(0.5)._ref_v, 0.1)


## We begin the simulation at v=-70 mV everywhere
h.v_init = -70.

## We run the simulation for 500ms
h.tstop = 500

## Run!
h.init()
h.run()

## Now we save the data
h.load_file("CNSutils.hoc")
h.CNSsaveVectors("v_0_5.csv", 0.1, vc)
