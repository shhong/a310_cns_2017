"""

demo3.py

Getting an I-V relation by voltage clamp simulation

"""

import neuron
# neuron.load_mechanisms('.')
from neuron import h, gui

h.load_file("stdrun.hoc")   # load init(), run(), etc.

# Creating a cell
soma = h.Section(name="soma")
soma.insert("ml")
soma.diam = 15
soma.L = 15
# soma.betaw_ml = 0

# Adding a voltage clamp
vc = h.SEClamp(0.5, sec=soma)
vc.rs = 0.01 # Serial resistance https://www.neuron.yale.edu/neuron/static/new_doc/modelspec/programmatic/mechanisms/mech.html?SEClamp#SEClamp

# Let's make sure that we simulate for a sufficently long time.
h.tstop = 200
vc.dur1 = h.tstop

# Let's prepare an empty list to store our data.
irec = []

# Here we run simulation for many voltage levels, from -70 mV to 0 mV
vrange = range(-70, 0)
for v in vrange:
    vc.amp1 = v  # This is our target membrane voltage.
    h.init()
    h.run()      # we should reach a steady state when the simulation finishes.
    i_steady = vc.i # This is the current that we need to inject for have voltage=v
    irec.append(i_steady) # Append the measured i_steady in the list

# Save the data to a csv file
with open('IV.csv', 'w') as f:
    f.write('I,V\n')
    for v, i in zip(vrange, irec):
        f.write('%f,%f\n' % (i, v))
