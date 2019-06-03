#Template of the Granule cell model (single compartment), D'Angelo et al. 2001
#Templating by Lungsi 2018 based on ~/GrC2001DAngelo/grc.hoc
from neuron import h


class Granule(object):
    """Single compartment cell
    """
    def __init__(self):
        # Soma
        self.soma = h.Section(name="soma")
        self.soma.nseg = 1
        self.soma.diam = 9.76
        self.soma.L = 9.76
        self.soma.cm = 0.77
        self.soma.Ra = 100

        self.soma.insert("GrC_Lkg1")
        self.soma.insert("GrG_Na")
        self.soma.insert("GrG_Nar")
        self.soma.insert("GrG_KV")
        self.soma.insert("GrC_KA")
        self.soma.insert("GrC_Kir")
        self.soma.insert("GrC_KCa")
        self.soma.insert("GrC_CaHVA")
        self.soma.insert("Calc")
        self.soma.insert("GrC_pNa")
        self.soma.insert("GrG_KM")
        self.soma.insert("GrC_Lkg2")

        h.usetable_GrG_Na = 0
        h.usetable_GrC_pNa = 0
        h.usetable_GrC_CaHVA = 0
        h.usetable_GrG_KV = 0
        h.usetable_GrC_KA = 0
        h.usetable_GrC_Kir = 0
        h.usetable_GrC_KCa = 0
        h.usetable_GrG_KM = 0

        self.soma.ena = 87.39
        self.soma.ek = -84.69
        self.eca = 129.33
        self.ecl = -65
