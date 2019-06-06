#Template of the Golgi cell (131 compartments), Solinas et al. 2007
#Templating by Lungsi 2019 based 0n ~/GoC2007Solinas/Start_golgi.hoc, Golgi_template.hoc,
#Synapses.hoc
from neuron import h


class Golgi(object):
    """Multi-compartment cell
    """
    def __init__(self):
        ############################# MORPHOLOGY ##############################
        h.xopen("Golgi_template.hoc") # Within it is the function Goc() which
        # creates a soma (1 section, 1 segment = 1 compartment),
        # an axon (1 section, 100 segment = 100 compartments) and
        # three dendrites (3 section, each with 10 compartments = 10 segments)
        h("objref Golgi[1]")      # this will make available: h.Golgi[0].soma
        h("Golgi[0] = new Goc()") # h.Golgi[0].axon and h.Golgi[0].dend

        ############################# PARAMETERS ##############################
        h.xopen("Synapses.hoc") # synapse parameters are set on h.Golgi[0]

        # below are the regions set as attribute to this python class
        self.soma = h.Golgi[0].soma
        self.axon = h.Golgi[0].axon
        self.dend = h.Golgi[0].dend # len(h.Golgi[0].dend -> 3

        # ------------------------ Model Surface ------------------------------
        # Based on Start_golgi.hoc below are the settings for Model Surface

        # For soma
        #self.soma.push()
        #h("soma_surf = area(0.5)*1e-8")
        #h("cell_surf_cm = cell_surf_cm + area(0.5)*1e-8*nseg")
        #h.pop_section()

        # For axon
        #self.axon.push()
        #h("axon_surf = area(0.5)*1e-8")
        #h("cell_surf_cm = cell_surf_cm + area(0.5)*1e-8*nseg")
        #h.pop_section()

        # For dendrites
        #for i in range(len(self.dend)):
        #    self.dend[i].push()
        #    h("cell_surf_cm = cell_surf_cm + area(0.5)*1e-8*nseg")
        #    h("dend_surf = cell_surf_cm - soma_surf")
        #    h.pop_section()
