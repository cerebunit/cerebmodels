#Template of the Mossy fiber to Granule cell (soma), Nieus et al. 2006
#Templating by Lungsi 2019 based on ~/MFGrC2006Nieus/Figure7_of_Nieus2006_Demo.hoc
from neuron import h
#from pdb import set_trace as breakpoint

class MossyGranule(object):
    """Single compartment Granule soma connected to Mossy fibre
    """
    def __init__(self):
        self.soma = h.Section(name="soma") # soma is the only compartment

        self.soma.push()

        h("objref synA, synN")
        h("objref stimfib, conMFnmda, conMFampa")

        h("stimfib = new SpikeGenerator2(0.5)")
        h("synA = new Ampa(0.5)")
        h("synN = new Nmda(0.5)")
        h("conMFampa = new NetCon(stimfib, synA,-20, 0.000, 1e-3)")
        h("conMFnmda = new NetCon(stimfib, synN,-20, 0.000, 1e-3)")

        h.pop_section()
