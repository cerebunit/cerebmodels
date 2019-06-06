#Template of the Granue cell model (multi-compartment), Gabbiani et al. 1994)
#Templating by Lungsi 2019 based on ~/GrC1994Gabbiani/granule2.oc granule2.proto & granule.nrn
from neuron import h
#from pdb import set_trace as breakpoint

class Granule(object):
    """Multi-compartment cell
    """
    def __init__(self):
        h.xopen("granule2.proto") # Within it parameters are defined and
        # its geometry is set by loading granuel.nrn

        # There are thirteen compartments and the following are chosen as
        # attributes to this python class for potential recording
        self.soma = h.soma
        self.dend = h.dendrite # len(h.dendrite) -> 4
        self.bulb = h.bulb    # len(h.bulb) -> 4

