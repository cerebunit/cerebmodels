#Template of the excitatory DCN projection neuron (517 compartments), Luthman et al. 2011
#Templating by Lungsi 2019 based 0n ~/DCN2011Luthman/DCN_simulation.hoc, DCN_morph.hoc,
#DCN_mechs.hoc, DCN_run.hoc and DCN_recording.hoc
from neuron import h


class ExcitatoryDCNneuron(object):
    """Multi-compartment cell
    """
    def __init__(self):
        h.xopen("DCN_simulation.hoc") # Within it, after defining the parameters
        # it loads: DCN_morph.hoc, DCN_mechs.hoc and DCN_run.hoc
        # (inside DCN_run.hoc, DCN_recording.hoc is loaded)
        # NOTE: for our application none of the functions within DCN_run.hoc and
        # DCN_recording.hoc will be invoked and hence are of direct interest.

        # since there are 517 compartments with the following reference groups:
        # h.soma, h.axHillock, h.axIniSeg, h.axNode,
        # h.proxDend, h.distDend, h.excSynapseComps, h.inhSynapseComps
        # only those used in DCN_recording.hoc have its attribute to this python class
        self.soma = h.soma
        self.gaba = h.gaba # len(h.gaba) -> 450
