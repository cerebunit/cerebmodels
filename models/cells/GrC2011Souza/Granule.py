#Template of the Granule cell, Souza & Schutter 2011
#Templating by Lungsi 2019 based 0n ~/GrC2011Souza/granule_template.hoc,
from neuron import h


class Granule(object):
    """Single-compartment cell
    """
    def __init__(self):
        ############################# MORPHOLOGY ##############################
        h.xopen("granule_template.hoc") # Within it is the function grc() which
        # creates a soma (1 section, 1 segment = 1 compartment)
        h("objref GrC")      # this will make available: h.GrC.soma
        h("GrC = new grc(0,0,0)")
        # Notice three arguments, this is because here the
        # the template by Souza & Schutter are meant for the network.
        # The arguments are basically the x,y,z-coordinates.

        # below are the regions set as attribute to this python class
        self.soma = h.GrC.soma
