#Template of the Purkinje cell model, Forrest 2015
#There are two templates:
#Template 1: 1088 compartment (full)
#Templating by Lungsi 2019 based on ~/PC2015aForrest/full_morph.hoc
#Template 2: 2 compartments (reduced)
#Templating by Lungsi 2019 based on ~/PC2015bForrest/2_compartment.hoc
#PC2015aForrest -> Template 1
from neuron import h
#from pdb import set_trace as breakpoint
from random import randint

class Purkinje(object):
    """Multi-compartment cell
    """
    def __init__(self):
        h("load_file(\"nrngui.hoc\")") #h("proc set_ra() {}")
        # this step is needed otherwise there is RuntimeError
        # for the undefined function when loading full_morph.hoc where this function
        # is called at line 3676. The above step defines the function set_ra()
        h.xopen("full_morph.hoc")

        # There are 1088 compartments and the following are chosen as
        # attributes to this python class for potential recording
        self.soma = h.soma
        #
        dend_sm = h.SmoothDendrite # len(h.SmoothDendrite) -> 85
        dend_sp = h.SpinyDendrite # len(h.SpinyDendrite) -> 1002
        #
        self.dend_sm = dend_sm[ randint(0, len(dend_sm)-1) ]
        self.dend_sp = dend_sp[ randint(0, len(dend_sp)-1) ]

