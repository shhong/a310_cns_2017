"""

demo4.py

f-I curves
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
soma.betaw_ml = 0 # This controls the half-maximum voltage of the K+ channel.

h.tstop = 1000

# Adding a current injection
ic = h.IClamp(0.5, sec=soma)
ic.delay = 50
ic.dur = 1000
ic.amp = 0.300  # We inject 300pA into the cell.

# We add a spike counter and recorder
apc = h.APCount(0.5, sec=soma)
apc.thresh = -10. # If the voltage crosses this, it is regarded as a spike.
spiketime = h.Vector()
apc.record(spiketime)

# Now we run the simulation and save the number of spikes
h.init()
h.run()

with open('nspikes.csv', 'w') as f:
    f.write('%g,%g\n' % (ic.amp, spiketime.size()))

# Here is how to save the spike time data.
with open('spikes.csv', 'w') as f:
    for t in spiketime:
        f.write('%g,%d\n' % (t,1))
