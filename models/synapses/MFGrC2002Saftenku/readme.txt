    This model was published in E.E. Saftenku "A simplified model of
    the long-term plasticity in cerebellar mossy fiber-granule cell
    synapses", Neurophysiology/Neirofiziologiya, 2002, 34, N 2-3, P.216-219.

    Activation of cerebellar mossy fibers using either a theta burst 
    stimulation mode (TBS; 100 Hz for 100 ms repeated 4 times at 250
    ms intervals) or a single tetanus stimulation train (100 Hz for 
    1 s) results in long-term potentiation (LTP) of both AMPA and 
    NMDA components of EPSC in granule cells, whereas low-frequency 
    stimulation (2 Hz) causes long-term depression. These forms of 
    plasticity require Ca2+ influx through NMDA receptor channels. 
    When about two synapses were initially activated by TBS, the 
    amplitude of evoked EPSPs exceeded the control value by 70+-16%
    in 1 min and then continued to slowly increase reaching in 7 min
    an increment of 84+-16%. We modified a simple model for LTP/LTD 
    developed by Migliore and Lansky (1999) and combined it with the
    model of the electrical activity in the cerebellar granule cells
    developed by D'Angelo et al (Bursting and resonance in cerebellar
    granule cells by D’Angelo et al., 2001 in ModelDB)with addition 
    of the description of AMPA and NMDA receptor kinetics. In 
    contrast to the model of Migliore and Lansky, an activation of
    autocatalytic processes is controlled not by postsynaptic 
    depolarization, but by Ca2+ influx through the NMDA receptor 
    channels. The model completely reproduces experimental conditions
    and results of LTP manifestation in the presence of bicuculline
    and short-term depression of AMPA EPSPs during TBS published in
    Armano S. et al. "Long-term potentiation of intrinsic 
    excitability at the mossy fiber-granule cell synapse of rat 
    cerebellum", J. Neurosci., 2000, 20, P. 5208-5216. The 
    observed nonlinearity in the development of long-term changes of 
    EPSP in granule cells was modeled by a difference in the rate 
    constants of two independent autocatalytic processes. The model 
    can be easily modified for presynaptic expression of LTP by 
    multiplying freqdel*(Np-Nd) by variable  "u" instead of synaptic
    conductances.

The transmitter concentration profile in the cleft was described by 
three exponential components to reproduce the profile of glutamate 
concentration from Rusakov (2001). Neurotransmitter concentration was
made proportional to release probability of glutamate on the APs. 
Short-term plasticity was modeled with the use of phenomenological
model of  Tsodyks and Markram, but  release probability in the model
corresponds not to xu, but to x(u/U)*weight in their designations, 
where "weight" can be considered as the probability to release on the
first AP. This allowed us to reproduce slower decrease of release 
probability during repetitive stimulation, which occurs presumably 
due to several vesicles in the ready-to-release pool under condition
of one-vesicle constraint. 

Keywords: Cerebellar granule cells, Long-term plasticity.

Simulations.
      Begin from start.hoc and reproduce the maintenance of LTP and 
      LTD as in Fig.1 from our paper. All parameters of the model 
      can be changed in the respective boxes.
