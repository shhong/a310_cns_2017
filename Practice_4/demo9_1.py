'''
demo9.py

Demo of a network of spiking neurons driven by synaptic inputs.

Written by Sungho Hong, Computational Neuroscience Unit, OIST, 2017
'''

from neuron import h, gui

h.load_file("stdrun.hoc")
h.load_file("CNSutils.hoc")

# The simulation will run for 100 ms.
h.tstop = 200
# Global sampling period will be 0.1 ms -> 10 kHz sampling..
Dt = 0.01

# Variable step controller to speedup simulation
cvode = h.CVode()
cvode.active(1)

def create_cell(seed):
    # Creating a cell
    soma = h.Section()
    soma.diam = 100/h.PI
    soma.L = 100
    adexp = h.AdExpIF(0.5, sec=soma)
    adexp.tauw = 20
    # soma.insert("pas")
    # soma.g_pas = 1e-4

    # Synapses
    syns = []

    # 400 excitatory synapses
    for i in range(1):
        syns.append(h.Exp2Syn(0.5, sec=soma))
        syns[-1].tau1 = 0.5 # rise time
        syns[-1].tau2 = 1.5 # decay time
        syns[-1].e = 0      # reversal potential

    # 100 inhibitory synapses
    for i in range(1):
        syns.append(h.Exp2Syn(0.5, sec=soma))
        syns[-1].tau1 = 1   # rise time
        syns[-1].tau2 = 10  # decay time
        syns[-1].e = -75    # reversal potential

    # Stimuli = random spike trains
    isi = 1000./10  # average interspike interval for 0.01 Hz
    stims = []
    for i in range(500):
        stims.append(h.NetStimFD(0.5))
        stims[-1].noise = 1          # random firing
        stims[-1].start = 0
        stims[-1].duration = h.tstop
        stims[-1].interval = isi

    stims[0].seed(seed) # Set seed for noise

    # Connections
    ncs = []
    for i in range(400):
        ncs.append(h.NetCon(stims[i], syns[0]))
        ncs[-1].weight[0] = 0.5e-3 

    for i in range(100):
        ncs.append(h.NetCon(stims[i+400], syns[1]))
        ncs[-1].weight[0] = 1e-3

    # Set up a current clamp to probe the neuron
    ic = h.IClamp(0.5, sec=soma)
    ic.delay = 50
    ic.amp = 0.4
    ic.dur = 100

    vtemp = h.Vector()
    vtemp.record(soma(0.5)._ref_v, Dt)

    spiketime = h.Vector()
    spike_recorder = h.APCount(0.5, sec=soma)
    spike_recorder.thresh = -50
    spike_recorder.record(spiketime)

    return {'soma': soma, 'syns': syns, 'spike': spiketime, 'v': vtemp, 'external_stims': (stims, ncs, ic), 'others': (adexp, spike_recorder)}

cells = []
Ncells = 20
for i in range(Ncells):
    cells.append(create_cell(i))

cell1 = cells[0]
ncs = []
for cell2 in cells[1:]:
    # Add a synapse in the second cell
    cell2['syns'].append(h.Exp2Syn(0.5, sec=cell2['soma']))
    cell2['syns'][-1].tau1 = 0.5 # rise time
    cell2['syns'][-1].tau2 = 1.5 # decay time
    cell2['syns'][-1].e = -75      # reversal potential

    # Connect the first cell to the synapse
    ncs.append(h.NetCon(cell1['soma'](0.5)._ref_v, cell2['syns'][-1], sec=cell1['soma']))
    ncs[-1].threshold = -50
    ncs[-1].weight[0] = 50e-3 # This one is big!


h.v_init = -70
h.init()
h.run()

h.CNSsaveVectors("voltage1.csv", Dt, cells[0]['v'])
h.CNSsaveVectors("voltage2.csv", Dt, cells[1]['v'])

with open('spikes.csv', 'w') as f:
    for i in range(Ncells):
        for t in cells[i]['spike'].to_python():
            f.write('%g,%d\n' % (t, i+1))
