#Template of the Purkinje cell model (38 compartments), Brown et al. 2011)
#Templating by Lungsi 2019 based on ~/PC2011Brown/purkinje_reduced_PPR model.hoc
from neuron import h
#from pdb import set_trace as breakpoint
from random import randint

class Purkinje(object):
    """Multi-compartment cell
    """
    def __init__(self):
        h.xopen("purkinje_reduced_PPR model.hoc")

        # There are thirtyeight compartments and the following are chosen as
        # attributes to this python class for potential recording
        self.soma = h.Soma
        #
        dend_root = h.MainDendrite      # len(h.MainDendrite) -> 1
        dend_sm_distalshort = h.SmoothDistalDendriteshort # len() -> 3
        dend_sm_distallong = h.SmoothDistalDendritelong  # len() -> 3
        dend_sp_distal = h.SpinyDistalDendrite # len() -> 3
        dend_adj = h.AdjacentDendrite # len() -> 15
        spine_neck = h.SpineNeck # len() -> 1
        spine = h.Spine # len() -> 1
        #
        self.dend_root = dend_root[0]
        self.dend_sm = [ dend_sm_distalshort[ randint(0, len(dend_sm_distalshort)-1) ],
                         dend_sm_distallong[ randint(0, len(dend_sm_distallong)-1) ] ][randint(0,1)]
        self.dend_sp = [ dend_sp_distal[ randint(0, len(dend_sp_distal)-1) ],
                         dend_adj[ randint(0, len(dend_adj)-1) ] ][randint(0,1)]
        self.spine_head = spine[0]
        self.spine_neck = spine_neck[0]
        
