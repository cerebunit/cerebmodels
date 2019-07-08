#Template of the Purkinje cell model, Mike Hausser (version 3, 20.2.97)
#Templating by Lungsi 2019 based on ~/PC1997bHausser/P19.hoc
#This template was sourced from Vetter et al. 2001 Dendritica ModelDB
from neuron import h
#from pdb import set_trace as breakpoint

class Purkinje(object):
    """Multi-compartment cell
    """
    def __init__(self):
        h.xopen("P20.hoc")

        # The following are chosen as attributes for potential recording
        self.soma = h.soma
        self.dend_root = h.dendA1_0 # see Fig.2A Zang et al. 2018 10.1016/j.celrep.2018.07.011
        # Zang et al. 2018 used a modified version of this.
        # This model has smooth and spiny dendrites such that the
        # sparsely spiny dendrite sections are assumed to be likely innervated
        # by the climbing fibre.
        # However, since the cell is the main region of interest
        # PC1997aHausser is in ~/models/cells/ NOT in ~/models/synapses

        # no explicit dt is known to be given so use the default = 0.025
