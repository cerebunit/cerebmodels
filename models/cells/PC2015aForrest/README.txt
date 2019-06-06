
REFERENCE: Forrest MD (2015) Simulation of alcohol action upon a
detailed Purkinje neuron model and a simpler surrogate model that runs
>400 times faster. BMC Neuroscience

There are 2 seperate NEURON models here:

1) A Two compartment Purkinje cell model (reduced model, fast run
time)
2) A 1089 compartment Purkinje cell model (detailed model with
realistic morphology, slow run time)

To run the Two compartment model: Click on "mosinit_simple.hoc"
To run the 1089 compartment model: Click on "mosinit_full.hoc"

Both these models share and use the same .mod mechanisms. 

As an adside the NEURON code used to generate the reduced, Two
compartment model from the 1089 compartment model is included in the
folder called "collapse_algorithm"

Region: Cerebellum
Cell Type: Purkinje cell
Simulator: NEURON 
Topics: Activity Patterns, Bursting, Oscillations, Active Dendrites,
Calcium dynamics, Depolarisation block, Detailed Neurnal Models,
Sodium pump, Simplified Models, Influence of Dendritic Geometry
