#Template of the Purkinje cell model (1088 compartments), Genet et al. 2010)
#Templating by Lungsi 2019 based on ~/PC2010Genet/full_CP.hoc
from neuron import h
#from pdb import set_trace as breakpoint

class Purkinje(object):
    """Multi-compartment cell
    """
    def __init__(self):
        h.xopen("full_CP.hoc")

        # There are 1088 compartments and the following are chosen as
        # attributes to this python class for potential recording
        self.soma = h.soma
        self.dend_sm = h.sm      # len(h.sm) -> 85
        #self.dend_sp1 = h.spn1 # len() -> 1
        #but there are 86 such spiny dendrites and unlike h.sm they are separate
        self.dend_sp = []
        for i in range(1, 86+1):
            self.dend_sp.append( getattr(h,"spn"+str(i))[0] ) # since nseg = 1
        

