#Template of the Granule cell model (multi-compartment), Diwakar et al. 2009
#Templating by Lungsi 2019 based on ~/GrC2009Diwakar/Start.hoc & Grc_Cell.hoc
from neuron import h
#from pdb import set_trace as breakpoint

class Granule(object):
    """Multi-compartment cell
    """
    def __init__(self):
        nsg = 4    # hillock
        ndend = 5  # dendrite
        naxon = 30 # axon
        # Construct parts
        self.soma = h.Section(name="soma")
        self.hillock = [h.Section(name="hillock"+str(i)) for i in range(nsg)]
        self.axon = [h.Section(name="axon"+str(i)) for i in range(naxon)]
        self.dend_1 = [h.Section(name="dend"+str(i)) for i in range(ndend)]
        self.dend_2 = [h.Section(name="dend"+str(i)) for i in range(ndend)]
        self.dend_3 = [h.Section(name="dend"+str(i)) for i in range(ndend)]
        self.dend_4 = [h.Section(name="dend"+str(i)) for i in range(ndend)]
        self.branch0 = h.Section(name="branch0")
        self.branch1 = h.Section(name="branch1")
        self.branch2 = h.Section(name="branch2")
        self.branch3 = h.Section(name="branch3")

        # Soma definition
        self.soma.nseg = 1
        self.soma.diam = 5.8 # 6.06
        self.soma.L = 5.8 # 6.16
        self.soma.cm = 1
        self.soma.Ra = 100

        self.soma.insert("GRC_LKG1")
        self.soma.insert("GRC_LKG2")
        [setattr(seg.GRC_LKG2,"ggaba", 3e-05) for seg in self.soma]
        self.soma.insert("GRC_KIR")
        self.soma.insert("GRC_KA")
        self.soma.insert("GRC_KM")
        self.soma.insert("GRC_NA")
        self.soma.insert("GRC_KV")
        
        h.usetable_GRC_KA = 0
        h.usetable_GRC_KIR = 0
        h.usetable_GRC_KM = 0

        self.soma.insert("GRC_NA")
        self.soma.insert("GRC_KV")

        #h.usetable_GRC_NA = 0 not defined in mod file
        h.usetable_GRC_KV = 0

        self.soma.insert("GRC_KCA")
        [setattr(seg.GRC_KCA,"gkbar", 0) for seg in self.soma]
        h.usetable_GRC_KCA = 0

        self.soma.insert("GRC_CA")
        [setattr(seg.GRC_CA,"gcabar", 0) for seg in self.soma]
        h.usetable_GRC_CA = 0

        self.soma.insert("GRC_CALC")
        [setattr(seg.GRC_CALC,"beta", 1.5) for seg in self.soma]

        self.soma.ena = 87.39
        self.soma.ek = -84.69
        self.soma.eca = 129.33
        #self.soma.ecl = -65 # not defined in any of the above mod files

        # Hillock definition
        for w1 in range(nsg):
                self.hillock[w1].nseg = 1
                self.hillock[w1].diam = 2.3 - (0.5*w1)
                self.hillock[w1].L = 0.5
                self.hillock[w1].cm = 1
                self.hillock[w1].Ra = 100

                self.hillock[w1].insert("GRC_LKG1")
                self.hillock[w1].insert("GRC_NA")
                self.hillock[w1].insert("GRC_KV")

                #h.usetable_GRC_NA = 0 # not defined in mod file
                h.usetable_GRC_KV = 0

                self.hillock[w1].ena = 87.39
                self.hillock[w1].ek = -84.69

        # Axon definition
        for w3 in range(naxon):
                self.axon[w3].nseg = 1
                self.axon[w3].diam = 0.3
                self.axon[w3].L = 2.3367
                self.axon[w3].cm = 1
                self.axon[w3].Ra = 100

                self.axon[w3].insert("GRC_LKG1")
                self.axon[w3].insert("GRC_NA")
                self.axon[w3].insert("GRC_KV")

                #h.usetable_GRC_NA = 0 # not defined in mod file
                h.usetable_GRC_KV = 0

                self.axon[w3].ena = 87.39
                self.axon[w3].ek = -84.69
        # Dendrite definition
        self.synG = [i for i in range(ndend)] # synapse for dend_3 compartment
        self.synA = [i for i in range(ndend)] # synapse for dend_4 compartment
        self.synNS = [i for i in range(ndend)]# synapse for dend_4 compartment
        for w2 in range(ndend):
                # First compartment
                self.dend_1[w2].nseg = 1
                self.dend_1[w2].diam = 0.75
                self.dend_1[w2].L = 5
                self.dend_1[w2].cm = 1
                self.dend_1[w2].Ra = 100

                self.dend_1[w2].insert("GRC_LKG1")
                self.dend_1[w2].insert("GRC_LKG2")
                [setattr(seg.GRC_LKG2,"ggaba", 3e-05) for seg in self.dend_1[w2]]

                self.dend_1[w2].insert("GRC_KIR")
                h.usetable_GRC_KIR = 0
                [setattr(seg.GRC_KIR,"gkbar", 0) for seg in self.dend_1[w2]]

                self.dend_1[w2].insert("GRC_KA")
                h.usetable_GRC_KA = 0
                [setattr(seg.GRC_KA,"gkbar", 0) for seg in self.dend_1[w2]]

                self.dend_1[w2].insert("GRC_KCA")
                h.usetable_GRC_KCA = 0
                [setattr(seg.GRC_KCA,"gkbar", 0) for seg in self.dend_1[w2]]

                self.dend_1[w2].insert("GRC_CA")
                h.usetable_GRC_CA = 0
                [setattr(seg.GRC_CA,"gcabar", 0) for seg in self.dend_1[w2]]

                self.dend_1[w2].insert("GRC_CALC")
                [setattr(seg.GRC_CALC,"beta", 1.5) for seg in self.dend_1[w2]]

                self.dend_1[w2].eca = 129.33
                self.dend_1[w2].ek = -84.69

                # Second compartment
                self.dend_2[w2].nseg = 1
                self.dend_2[w2].diam = 0.75
                self.dend_2[w2].L = 5
                self.dend_2[w2].cm = 1
                self.dend_2[w2].Ra = 100

                self.dend_2[w2].insert("GRC_LKG1")
                self.dend_2[w2].insert("GRC_LKG2")
                [setattr(seg.GRC_LKG2,"ggaba", 3e-05) for seg in self.dend_2[w2]]

                self.dend_2[w2].insert("GRC_KIR")
                h.usetable_GRC_KIR = 0
                [setattr(seg.GRC_KIR,"gkbar", 0) for seg in self.dend_2[w2]]

                self.dend_2[w2].insert("GRC_KA")
                h.usetable_GRC_KA = 0
                [setattr(seg.GRC_KA,"gkbar", 0) for seg in self.dend_2[w2]]

                self.dend_2[w2].insert("GRC_KCA")
                h.usetable_GRC_KCA = 0
                [setattr(seg.GRC_KCA,"gkbar", 0) for seg in self.dend_2[w2]]

                self.dend_2[w2].insert("GRC_CA")
                h.usetable_GRC_CA = 0
                [setattr(seg.GRC_CA,"gcabar", 0) for seg in self.dend_2[w2]]

                self.dend_2[w2].insert("GRC_CALC")
                [setattr(seg.GRC_CALC,"beta", 1.5) for seg in self.dend_2[w2]]

                self.dend_2[w2].eca = 129.33
                self.dend_2[w2].ek = -84.69

                # Third compartment
                self.dend_3[w2].nseg = 1
                self.dend_3[w2].diam = 0.75
                self.dend_3[w2].L = 2.5 # different from above two
                self.dend_3[w2].cm = 1
                self.dend_3[w2].Ra = 100

                self.dend_3[w2].insert("GRC_LKG1")
                self.dend_3[w2].insert("GRC_LKG2")
                [setattr(seg.GRC_LKG2,"ggaba", 3e-05) for seg in self.dend_3[w2]]

                self.dend_3[w2].insert("GRC_KIR")
                h.usetable_GRC_KIR = 0
                [setattr(seg.GRC_KIR,"gkbar", 0) for seg in self.dend_3[w2]]

                self.dend_3[w2].insert("GRC_KA")
                h.usetable_GRC_KA = 0
                [setattr(seg.GRC_KA,"gkbar", 0) for seg in self.dend_3[w2]]

                self.dend_3[w2].insert("GRC_KCA")
                h.usetable_GRC_KCA = 0
                [setattr(seg.GRC_KCA,"gkbar", 0) for seg in self.dend_3[w2]]

                self.dend_3[w2].insert("GRC_CA")
                h.usetable_GRC_CA = 0
                [setattr(seg.GRC_CA,"gcabar", 0) for seg in self.dend_3[w2]]

                self.dend_3[w2].insert("GRC_CALC")
                [setattr(seg.GRC_CALC,"beta", 1.5) for seg in self.dend_3[w2]]

                self.dend_3[w2].eca = 129.33
                self.dend_3[w2].ek = -84.69

                h("objref sG")
                h("sG = new GRC_GABA(0.5)")
                self.synG[w2] = h.sG

                # Fourth compartment
                self.dend_4[w2].nseg = 1
                self.dend_4[w2].diam = 0.75
                self.dend_4[w2].L = 2.5 # same as third compartment
                self.dend_4[w2].cm = 1
                self.dend_4[w2].Ra = 100

                self.dend_4[w2].insert("GRC_LKG1")
                self.dend_4[w2].insert("GRC_LKG2")
                [setattr(seg.GRC_LKG2,"ggaba", 3e-05) for seg in self.dend_4[w2]]

                self.dend_4[w2].insert("GRC_KIR")
                h.usetable_GRC_KIR = 0
                [setattr(seg.GRC_KIR,"gkbar", 0) for seg in self.dend_4[w2]]

                self.dend_4[w2].insert("GRC_KA")
                h.usetable_GRC_KA = 0
                [setattr(seg.GRC_KA,"gkbar", 0) for seg in self.dend_4[w2]]

                self.dend_4[w2].insert("GRC_KCA")
                h.usetable_GRC_KCA = 0

                self.dend_4[w2].insert("GRC_CA")
                h.usetable_GRC_CA = 0

                self.dend_4[w2].insert("GRC_CALC")
                [setattr(seg.GRC_CALC,"beta", 1.5) for seg in self.dend_4[w2]]

                self.dend_4[w2].eca = 129.33
                self.dend_4[w2].ek = -84.69

                h("objref sA, sNS")
                h("sA = new AmpaCOD(0.5)")
                h("sNS = new NMDAS(0.5)")
                self.synA[w2] = h.sA
                self.synNS[w2] = h.sNS

        # Definitions for passive compartments (maintains propagation delay)
        self.branch0.nseg = 1
        self.branch0.diam = 0.3
        self.branch0.L = 3
        self.branch0.cm = 0.5
        self.branch0.Ra = 100
        #self.branch0.celsius = 30 # celsius not section variable instead its h.celsius
        h.celsius = 30
        self.branch0.insert("GRC_LKG1")

        self.branch1.nseg = 1
        self.branch1.diam = 0.2
        self.branch1.L = 5
        self.branch1.cm = 0.45
        self.branch1.Ra = 100
        #self.branch1.celsius = 30 # celsius not section variable instead its h.celsius
        self.branch1.insert("GRC_LKG1")

        self.branch2.nseg = 1
        self.branch2.diam = 0.1
        self.branch2.L = 10
        self.branch2.cm = 1
        self.branch2.Ra = 90
        #self.branch3.celsius = 30 # celsius not section variable instead its h.celsius
        self.branch2.insert("GRC_LKG1")

        self.branch3.nseg = 1
        self.branch3.diam = 0.1
        self.branch3.L = 200
        self.branch3.cm = 1
        self.branch3.Ra = 100
        #self.branch3.celsius = 30 # celsius not section variable instead its h.celsius
        self.branch3.insert("GRC_LKG1")

        # Connection
        for i in range(ndend):
                self.dend_4[i].connect( self.dend_3[i], 1, 0 )
                self.dend_3[i].connect( self.dend_2[i], 1, 0 )
                self.dend_2[i].connect( self.dend_1[i], 1, 0 )
                self.dend_1[i].connect( self.soma, 1, 0 )

        self.soma.connect( self.hillock[0], 1, 0 )

        [ self.hillock[i].connect( self.hillock[i+1], 1, 0 ) for i in range(nsg-1) ]

        self.hillock[nsg-1].connect( self.axon[0], 1, 0 )

        [ self.axon[i].connect( self.axon[i+1], 1, 0 ) for i in range(naxon-1) ]

        self.axon[naxon-1].connect( self.branch0, 1, 0 )

        self.branch0.connect( self.branch1, 1, 0 )
        self.branch1.connect( self.branch2, 1, 0 )
        self.branch2.connect( self.branch3, 1, 0 )
