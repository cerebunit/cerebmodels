#Template of the Purkinje cell model (single compartment), Akemann and Knöpfel 2061
#Templating by Lungsi 2019 based on ~/PC2006Akemann/morphology_mechanisms.hoc
from neuron import h
#from pdb import set_trace as breakpoint

class Purkinje(object):
    """Single compartment cell
    """
    def __init__(self):
        h.xopen("morphology_mechanisms.hoc")

        # Being a single compartment the class has the attribute soma
        self.soma = h.soma

