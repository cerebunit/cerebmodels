#Template of the Purkinje cell model (1088 compartments), Miyasho et al. 2001)
#Templating by Lungsi 2019 based on ~/PC2001Miyaho/purkinje.hoc
from neuron import h
#from pdb import set_trace as breakpoint
from random import randint

class Purkinje(object):
    """Multi-compartment cell
    """
    def __init__(self):
        h.xopen("purkinje.hoc")

        # There are thirteen compartments and the following are chosen as
        # attributes to this python class for potential recording
        self.soma = h.soma
        #
        dend_sm = h.SmoothDendrite # len(h.SmoothDendrite) -> 85
        dend_sp = h.SpinyDendrite  # len(h.SpinyDendrite) -> 1002
        #
        self.dend_sm = dend_sm[ randint(0, len(dend_sm)-1) ]
        self.dend_sp = dend_sp[ randint(0, len(dend_sp)-1) ]

        # based on purkinje.ses dt = 0.025(default) and v_init = -65
