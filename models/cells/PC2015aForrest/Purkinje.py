#Template of the Purkinje cell model, Forrest 2015
#There are two templates:
#Template 1: 1088 compartment (full)
#Templating by Lungsi 2019 based on ~/PC2015Genet/full_morph.hoc
#Template 2: 2 compartments (reduced)
#Templating by Lungsi 2019 based on ~/PC2015Genet/2_compartment.hoc
#PC2015aForrest -> Template 1
from neuron import h
#from pdb import set_trace as breakpoint

class Purkinje(object):
    """Multi-compartment cell
    """
    def __init__(self):
        h("proc set_ra() {}") # this step is needed otherwise there is RuntimeError
        # for the undefined function when loading full_morph.hoc where this function
        # is called at line 3676. The above step defines the function set_ra()
        h.xopen("full_morph.hoc")

        # There are 1088 compartments and the following are chosen as
        # attributes to this python class for potential recording
        self.soma = h.soma
        self.dend_sm = h.SmoothDendrite # len(h.SmoothDendrite) -> 85
        self.dend_sp = h.SpinyDendrite # len(h.SpinyDendrite) -> 1002

