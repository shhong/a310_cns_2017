from neuron import h

h.load_file("stdrun.hoc")   # load init(), run(), etc.

# Creating a cell
soma = h.Section(name="soma")
dend = [h.Section(name="dend1"), h.Section(name="dend2")]

dend[0].connect(soma, 1, 0)
dend[1].connect(soma, 1, 0)
# OR
# for d in dend:
#     d.connect(soma, 1, 0)

soma.diam, soma.L = 10, 10
for d in dend:
    d.diam, d.L, d.nseg = 1.5, 30, 10


soma.insert('hh')
for d in dend:
    d.insert('pas')

soma.gnabar_hh = 0.3


# Setting up a current injection
ic = h.IClamp(0.5, sec=soma)
ic.delay = 50  # ic will do nothing for 20 ms.
ic.amp = 0.01 # Inject 10 pA for 1 ms
ic.dur = 50

# Setting up a recording
vsoma = h.Vector()
vsoma.record(soma(0.5)._ref_v, 0.1)

# h.xopen('my_session.ses')

h.tstop = 200

h.init()
h.run()

h.load_file("CNSutils.hoc")
h.CNSsaveVectors("cell1_volt.csv", 0.1, vsoma)
