#Template of Purkinje (-) & Mossy Fiber (+) to Deep Cerebellar neuron, Sudhakar et al. 2015
#Templating by Lungsi 2010 based on ~/PCDCNnMFDCN2015aSudhakar/model1.hoc
#model1.hoc has been converted from the original DCN_init_model1.hoc
#model1.hoc does not authomatically start the simulation and start recording.
from neuron import h
#from pdb import set_trace as breakpoint

class PurkinjeAndMossyToDeepCerebellar(object):
    """Multi-compartment (517) Deep Cerebellar Nuclei neuron with
    inhibitory connection from 200 Purkinje and
    excitatory connection from 100 Mossy fiber.
    There are NO connections with Climbing fiber.
    """
    def __init__(self):
        h.xopen("model1.hoc")

        # The following compartments of the Deep Cerebellar Neuron if available
        # as attributes
        self.soma = h.soma # 1 compartment
        # there is also only 1 compartment for axon hillock but it is a SectionList
        self.axon_hillock = [ sec for sec in h.axHillock ][0]
        # there are 10 compartments of axon initial segment
        self.axon_initial = [ sec for sec in h.axIniSeg ]
        # there are 20 compartments for axon node
        self.axon_node = [ sec for sec in h.axNode ]
        # there are 83 compartments for the proximal dendrite
        self.dend_proximal = [ sec for sec in h.proxDend ]
        # there are 402 compartments for the distal dendrite
        self.dend_distal = [ sec for sec in h.distDend ]
