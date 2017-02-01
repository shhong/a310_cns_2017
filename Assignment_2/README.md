# Assignment 2

### 1. Synaptic scaling

Here you wll work with a simulation `hw2_1.py` for a cortical pyramidal neuron with the passive membrane. The simulated neuron also has one excitatory synapse that activates at _t_=50 ms. The simulation will open a point process manager for the synapse so that you can change the location and parameters.

We also provide a function `distance_from_soma` to calculate the distance of the synapse from the soma. To use the function, simply provide the location shown in the point process manager to the function as a string. For example, if the point process manager says that the synapes is at `dend1[802](0.5)`, then running `distance_from_soma('dend1[802](0.5)')` will give you the distance.

1. Some studies claimed that an amplitude of an EPSP measured _at a soma_ is approximately independent of the input location, because the synaptic conductance increases with the distance (e.g., [Magee and Cook, Nat Neurosci, 2002](http://www.nature.com/neuro/journal/v3/n9/full/nn0900_895.html)). Here we ask you to find how the synaptic conductance should scale to reproduce their results:
   1. In the beginning, the synapse is located very close to the soma. Run the simulation with the synaptic conductance gmax=0.1 nS and record the EPSP amplitude. Then, tune the synaptic conductance to find the conductance value to give an EPSP with an amplitude ~0.2 mV.
   2. Move the synapses to several different locations along 1) a basal and 2) apical dendrite, and find a synaptic conductance to evoke the same EPSP. For each branch, try at least four locations, and make sure that at least one of them is very far from the soma (distance > 950 μm). Also record the distance from the soma at each point (see above).
   3. For each branch, plot two graphs: 1) Distance vs. scaled synaptic conductance. 2) Original EPSP amplitude (with gmax=0.1 nS) vs. Scaling factor (new gmax/0.1 nS). Does the second graph show that the scaling is linear (i.e., scaling factor ~ 1/voltage attenuation)?
2. Now repeat the same procedure for the EPSP amplitude ~2 mV measured at the soma. Does this give you a similar result? If not, discuss why.


### 2. Summation of excitatory inputs

Here you will work with `hw2_2.py`  that simulates two synapses, managed by two point process managers. Both synapses activate at _t_=50 ms, and both are set to excitatory ones (e = 0 mV).

Run three simulations and record the EPSP traces at the soma: 1) Both synapses are active (EPSP~1+2~), 2) only the first synapse is active (gmax = 0 for the second synapse; EPSP~1~), 3) only the second synapse is active (EPSP~2~). Check if linear summation (approximately) holds, i.e., EPSP~1+2~ ≈ EPSP~1~ + EPSP~2~ . By moving two synapses around, find out in which situation the the summation is approximately linear or not.

**Note:** Before you run simulations, make sure that you properly rescale synaptic conductances (as you did in "Synaptic scaling") each time so that the EPSP sizes of two synapses are similar.


### 3. Effects of proximal and distal inhibition

Here we ask you to reproduce a version of Fig 5.1 in the Koch for the transient synaptic inputs. Run `hw2_2.py`, but make one of the synapses inhibitory by changing the reversal potential to -76 mV (Note that this is the same as the resting membrane potential and threfore the synapse will deliver _shunting inhibition_). Also change `tau` and `onset` to 100 ms and 0 ms so that it should activate slowly like GABA~B~ synapses from the beginning of the simulation.

1. __(Proximal inhibition)__ Place the excitatory synapse to a distal part of a basal dendrite and the inhibitory synapse close to soma. Run simulations with different conductance values, make a plot for the EPSP amplitude as Fig. 5.1A.
2. __(Distal inhibition)__ Now move the inhibitory synapse also to a distal part in the _same dendrite_ as the excitatory synapse, and make a plot as 1 (i.e., Fig. 5.1B).
3. __(Different branch)__ Move the inhibitory synapse to a different dendrite than the excitatory synapse, and make a similar plot as 1 and 2.
4. It is known that parvalbumin (PV)-expressing inhibitory interneurons prefer making synapses close to a soma of a pyramidal neuron, whereas other interneurons such as somatostatin (SOM)-expressing neurons are known to prefer dendrites ([Thomson and Lamy, Front. Neurosci., 2007](http://journal.frontiersin.org/article/10.3389/neuro.01.1.1.002.2007)). Discuss what you can predict about the computational roles of different interneurons based on your simulation results.
5. __(Optional)__ Discuss if your conclusion from 4 is compatible with existing experimental studies (e.g. [Wilson et al., Nature, 2012](http://www.nature.com/nature/journal/v488/n7411/full/nature11347.html)).

**Note:** If you want to change the synaptic conductances programatically, you can do it by changing `h.AlphaSynapse[i].gmax`.
