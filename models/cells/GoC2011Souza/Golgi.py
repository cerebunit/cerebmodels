#Template of the Golgi cell (31 compartments), Souza & Schutter 2011
#Templating by Lungsi 2019 based 0n ~/GoC2011Souza/Golgi_template.hoc,
from neuron import h


class Golgi(object):
    """Multi-compartment cell
    """
    def __init__(self):
        ############################# MORPHOLOGY ##############################
        h.xopen("Golgi_template.hoc") # Within it is the function Goc() which
        # creates a soma (1 section, 1 segment = 1 compartment) and
        # three dendrites (3 section, each with 10 compartments = 10 segments)
        # notice the absence of axon
        h("objref GoC")      # this will make available: h.GoC.soma
        h("GoC = new Goc(0,0,0)") # h.GoC.axon and h.GoC.dend
        # Notice three arguments vs GoC2007Solinas, this is because here the
        # the template by Souza & Schutter are meant for the network.
        # The arguments are basically the x,y,z-coordinates.

        # below are the regions set as attribute to this python class
        self.soma = h.GoC.soma
        self.dend = h.GoC.dend # len(h.GoC.dend) -> 3

        ############################# PARAMETERS ##############################
        # using the parameters given in network.hoc (under Golgi cell layer)
        #self.soma.el_Golgi_lkg = -55. # already by default
        self.soma.ko = 5
        #self.soma.ki = 140 # already by default
        self.soma.nao = 145
        #self.soma.nai = 5 # already by default
        #
        # Based on the paper http://dx.doi.org/10.1186/2042-1001-1-7
        # under Methods section, Model GoC's sub-section
        # "We adopted a resting membrane potential of -60 mV and a
        # passive leakage current with reversal porential at -44.5 mV."
        h("v_init = -60.")
        self.soma.el_Golgi_lkg = -44.5
        [ setattr(d, "el_Golgi_lkg", -44.5) for d in self.dend ]
        
