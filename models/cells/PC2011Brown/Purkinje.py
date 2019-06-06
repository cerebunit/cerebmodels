#Template of the Purkinje cell model (38 compartments), Brown et al. 2011)
#Templating by Lungsi 2019 based on ~/PC2011Brown/purkinje_reduced_PPR model.hoc
from neuron import h
#from pdb import set_trace as breakpoint

class Purkinje(object):
    """Multi-compartment cell
    """
    def __init__(self):
        h.xopen("purkinje_reduced_PPR model.hoc")

        # There are thirtyeight compartments and the following are chosen as
        # attributes to this python class for potential recording
        self.soma = h.Soma
        self.dend = h.MainDendrite      # len(h.MainDendrite) -> 1
        #self.dend_sm_distalshort = h.SmoothDistalDendriteshort # len() -> 3
        #self.dend_sm_distallong = h.SmoothDistalDendritelong  # len() -> 3
        #self.dend_sp_distal = h.SpinyDistalDendrite # len() -> 3
        #self.dend_adj = h.AdjacentDendrite # len() -> 15
        #self.spine_neck = h.SpineNeck # len() -> 1
        self.spine = h.Spine # len() -> 1

