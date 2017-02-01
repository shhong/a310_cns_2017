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

