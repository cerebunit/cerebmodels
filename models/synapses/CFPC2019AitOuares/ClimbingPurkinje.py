#Template of the Climbing fiber to Purkinje cell (dendrite), Ait Ouares et al. 2019
#Templating by Lungsi 2010 based on ~/CFPC2019AitOuares/purkinje.hoc and run(d/h/i).hoc
from neuron import h
#from pdb import set_trace as breakpoint

class ClimbingPurkinje(object):
    """Single-compartment Purkinje denrite connected to Climbing fiber
    """
    def __init__(self):
        h.xopen("purkinje.hoc")

        # Since there is only the denrite compartment with CF being inserted
        self.dend = h.dend
