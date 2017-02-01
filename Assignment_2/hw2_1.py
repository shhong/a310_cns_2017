from r18_1 import *

h.load_file("CNSutils.hoc")

def distance_from_soma(segname):
    """d = distance_from_soma(segname) returns the distance of the segment
    from the center of the soma. segname should have be a string that follows
    the convention how the NEURON refers to a point in a segment, e.g., 'dend1[802](0.5)'."""
    h.dend1[21].push() # This is an actual center of the soma.
    h.distance()
    h.pop_section()
    secname, xstr = segname.split('(')
    x = float(xstr.replace(')', ''))
    sec = eval('h.' + secname)
    sec.push()
    d = h.distance(x)
    h.pop_section()
    return d

h.v_init = -76.  # The whole neuron will reset to v = -76 mV in the beginning.
h.tstop = 250    # Runtime = 250 ms.

h.xopen("hw2_1.ses")

vsoma = h.Vector()
vsoma.record(h.soma(0.5)._ref_v, 0.1)  # Record voltage from the "soma" at 10 kHz


## To run the simulation, use the following or the RunControl
h.init()
h.run()

print "Max EPSP = ", vsoma.max() - h.v_init

#### To save the data after a simulation:
# h.CNSsaveVectors("hw2_1_vsoma.csv", 0.1, vsoma)
