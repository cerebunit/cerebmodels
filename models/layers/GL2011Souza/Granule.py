#Template of the Granule Layer (GrC + GoC + MF), Souza & Schutter 2011
#Templating by Lungsi 2019 based 0n ~/GL2011Souza/network.hoc,
from neuron import h


class Granule(object):
    """Granule layer with 8100 GrCs, 225 GoCs and 900 MFs.
    """
    def __init__(self):
        ############################# MORPHOLOGY ##############################
        h("GJ = 1") # 0 for no gap-junctions between GoCs
        # 0 or 1, GJ must be set prior to loading network.hoc
        h.xopen("network.hoc") # Within it is the function Goc() which

        # below are the components set as attribute to this python class
        self.GrC = h.GrC # len(h.GrC) -> 8100
        self.GoC = h.GoC # len(h.GoC) -> 225
        self.MF = h.fiber # len(h.fiber) -> 900

        # to extract spiketimes WHICH ARE ALREADY VECTORS
        # self.GrC[i].spiketimes
        # self.GoC[i].spiketimes
        # self.MF[i].spiketimes
        #
        # to extract voltages
        # self.GrC[i].soma.v
        # self.GoC[i].soma.v
