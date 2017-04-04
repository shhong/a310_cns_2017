'''
hw4_3.py

Vogels-Abbott network

'''

from neuron import h, gui
import random

h.load_file("stdrun.hoc")
h.load_file("CNSutils.hoc")

# Fix the seed for random number generators
seed = 1
random.seed(seed)
r = h.Random(seed)
r.uniform(0,1)
# The simulation will run for 100 ms.
h.tstop = 200

# Variable step controller to speed up simulation
cvode = h.CVode()
cvode.active(1)

def create_cell(gid):
    # Create a cell
    soma = h.Section()
    soma.diam = 100/h.PI
    soma.L = 100
    soma.insert('pas')
    soma.g_pas = 5e-5  # This makes tau = 20 ms
    soma.e_pas = -65

    adexp = h.AdExpIF(0.5, sec=soma)
    adexp.a = 0
    adexp.tauw = 5
    adexp.EL = soma.e_pas
    adexp.GL = 100*soma.g_pas

    # Synapses
    syns = []

    # Embed one excitatory synapse
    syns.append(h.Exp2Syn(0.5, sec=soma))
    syns[-1].tau1 = 0.1 # rise time
    syns[-1].tau2 = 2 # decay time
    syns[-1].e = 0      # reversal potential

    # Embed one inhibitory synapse
    syns.append(h.Exp2Syn(0.5, sec=soma))
    syns[-1].tau1 = 0.1   # rise time
    syns[-1].tau2 = 2   # decay time
    syns[-1].e = -75    # reversal potential

    # Kickstart neuron by giving random inputs for 7 ms in the beginning.
    ic = h.NetStimFD(0.5, sec=soma)
    ic.interval = 2
    ic.noise = 1
    ic.start = 0
    nc = h.NetCon(ic, syns[0])
    ic.duration = 7
    nc.weight[0] = 5e-3

    # Record spike times
    spiketime = h.Vector()
    spike_recorder = h.APCount(0.5, sec=soma)
    spike_recorder.thresh = -40
    spike_recorder.record(spiketime)

    return {'soma': soma, 'syns': syns, 'spike': spiketime, 'external_stims': (ic, nc), 'others': (adexp, spike_recorder), 'gid':gid}


cells = []
Ncells = 1000                    # Number of cells
for i in range(Ncells):
    cells.append(create_cell(i)) # Create cells

Nexc = (Ncells/5)*4              # Excitatory cells = 80%
Ninh = Ncells/5                  # Inhibitory cells = 20%
exc_cells = cells[:Nexc]         # Make references to two groups
inh_cells = cells[Nexc:]

# Define synaptic conductances
gexc = 1.5e-3   # g_exc = 1.5 nS
ginh = 6.2*gexc   # g_inh = 6.2 g_exc

# Wire neurons
nc_exc = []
nc_inh = []
for i in range(Ncells):
    cell_post = cells[i]                        # Loop around the cells
    exc_pre = random.sample(exc_cells, Nexc/10) # Randomly choose 10% of the exc cells
    inh_pre = random.sample(inh_cells, Ninh/10) # Randomly choose 10% of the inh cells

    for cell in exc_pre:
        if i!=cell['gid']:  # No self-connection
            nc_exc.append(h.NetCon(cell['soma'](0.5)._ref_v, cell_post['syns'][0], sec=cell['soma']))      # Wire excitatory cells to an exc synapse
            nc_exc[-1].threshold = -40
            nc_exc[-1].weight[0] = gexc
            nc_exc[-1].delay = 0.1

    for cell in inh_pre:
        if i!=cell['gid']:  # No self-connection
            nc_inh.append(h.NetCon(cell['soma'](0.5)._ref_v, cell_post['syns'][1], sec=cell['soma']))      # Wire inhibitory cells to an inh synapse
            nc_inh[-1].threshold = -40
            nc_inh[-1].weight[0] = ginh
            nc_inh[-1].delay = 0.1

h.xopen('hw4_3.ses') # Monitor cell[0]

h.v_init = -65
h.init()
h.run()

# Save spike time data
with open('spikes_hw4_3.csv', 'w') as f:
    for i in range(Ncells):
        for t in cells[i]['spike'].to_python():
            f.write('%g,%d\n' % (t, i+1))
