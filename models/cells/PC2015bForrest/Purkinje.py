#Template of the Purkinje cell model, Forrest 2015
#This are two templates:
#Template 1: 1088 compartment (full)
#Templating by Lungsi 2019 based on ~/PC2015Genet/full_morph.hoc
#Template 2: 2 compartments (reduced)
#Templating by Lungsi 2019 based on ~/PC2015Genet/2_compartment.hoc
#PC2015bForrest -> Template 2
from neuron import h
#from pdb import set_trace as breakpoint

class Purkinje(object):
    """Multi-compartment cell
    """
    def __init__(self):
        h("proc set_ra() {}") # this step is needed otherwise there is RuntimeError
        # for the undefined function when loading 2_compartment.hoc where this
        # function is called at line 34. The above step defines the function set_ra()
        h.xopen("2_compartment.hoc")

        # The 1087 out of 1088 compartments are the compartment of dendites,
        # smooth and spiny. These 1087 are reduced to a compartment. Thus,
        # attributes to this python class for potential recording are
        self.soma = h.soma
        self.dend = h.Couple # h.Couple.nseg -> 1

