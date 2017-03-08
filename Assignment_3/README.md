# Assignment 3

**To complile mod files (`*.mod`), run `nrnivmodl` in the directory where the mod files are. Also run your simulations in this directory.**

### 1. f-I curves

Here we reproduce Fig. 7.2 and 7.6 in Rinzel and Ermentrout.

1. By editing and running `demo3.py`, find out how the I-V relation (panel A in Fig. 7.2 and 7.6) changes with the half-maximum voltage of the K+ channel, a variable named `soma.betaw_ml`. Try a few different values from -20 mV to 0 mV.
2. Modify `demo4.py` to compute the _f-I_ curve (panel B) of a Morris-Lecar neuron with the same sets of the half-maximum voltage ( `soma.betaw_ml` ) used in 1. Verify the relationship between the I-V relation and firing property.
3. Try the Hodgekin-Huxley mechanisms (`hh`) instead of the Morris-Lecar, and discuss the result.

### 2. Channel dynamics during spike generation

"hw3_2.py" simulates a single compartment cell with the Morris-Lecar mechanism with a sharp current injection. In the simulation, the Na+ and K+ ionic currents (`soma.ina` and `soma.ik`) and channel variables (`soma.m_ml` and `soma.w_ml`) are recorded. Note that the half-maximum voltage of the K+ channel (`soma.betaw_ml`) is set to -15 mV. Also, there is a bias current injected via `ic_bias` to make the cell a bit more excitable. It causes a fluctuation around t=0, but you can ignore it.

1. Discuss how the channel activates during spike generation in a similar way to Fig. 6.5 in Koch. If the half-maximum voltage of the K+ channel (`soma.betaw_ml`) is 0 mV, what difference do you see?
2. __(Anode break excitation)__ Change the amplitude of the injected current (`ic.amp`) to -0.1 nA, run the simulation, and explain the result. Can you get a similar result when `soma.betaw_ml` = 0 mV? Explain why.
3. If the neuron has the Hodgekin-Huxley ion channels, instead of the Morris-Lecar, would you observe a similar phenomenon with the negative current injection? Make a prediction and test it with a simulation.
