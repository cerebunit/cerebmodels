#Template of the Purkinje cell model (single compartment), Khaliq et al. 2003)
#Templating by Lungsi 2019 based on ~/PC2003Khaliq/resurgesim.hoc
from neuron import h
#from pdb import set_trace as breakpoint

class Purkinje(object):
    """Single-compartment cell
    """
    def __init__(self):
        h.xopen("resurgesim.hoc")

        # Since it has only one compartment the attribute for this
        # python class for recording is just soma
        self.soma = h.soma

        # based on the readme.txt
        h.dt = 0.025
        h.steps_per_ms = 1/h.dt

