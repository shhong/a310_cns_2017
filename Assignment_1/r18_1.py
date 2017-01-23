from neuron import h, gui


#### Here we load the definition of a cell. Ignore this part...
import os
this_dir, this_filename = os.path.split(__file__)
load_model_hoc = lambda x: h.xopen(os.path.join(this_dir, x))
load_model_hoc('ri18geo.hoc')
load_model_hoc('ri18init_passive.hoc')
####


## We set the parameters with two different choices
h.init_params()
h.insert_pass()

### Here we use uniform Rm
h.init_pass1()


## We load the point process manager to insert an IClamp
h.xopen("r18_1_iclamp.ses")

## We first set up recording at soma
vrec = h.Vector()
vdend688 = h.Vector()
vrec.record(h.soma(0.5)._ref_v, 0.1)
vdend688.record(h.dend1[688](0.5)._ref_v, 0.1)


## We begin the simulation at v=-76 mV everywhere
h.v_init = -76.

## Duration of our simulation
h.tstop = 200

## Run!
h.init()
h.run()

## Saving data
h.load_file("CNSutils.hoc")
h.CNSsaveVectors("vsoma.csv", 0.1, vrec, vdend688)


## Function to rescale the membrane resistance
def rescale_memb_res(scale=100.):
    for sec in h.allsec():  # loop through all the sections
        sec.g_pas = sec.g_pas/scale # Reduce conductance => Increase resistance

# To get the original model back, run h.init_pass1()
