#Template of the Granue cell model (multi-compartment), Gabbiani et al. 1994)
#Templating by Lungsi 2019 based on ~/GrC1994Gabbiani/granule2.oc granule2.proto & granule.nrn
from neuron import h
#from pdb import set_trace as breakpoint

class Granule(object):
    """Multi-compartment cell
    """
    def __init__(self):
        ndend = 4
        nbulb = 4
        coord = {"soma": {"D1": [   0., 0., 0., 6.76], # x, y, z, diameter
                          "D2": [14.55, 0., 0., 6.76]},
                 "dend0":{"D1": [  5., 0., 0., 1.24],
                          "D2": [93.1, 0., 0., 1.24],},
                 "dend1":{"D1": [   -5, 0., 0., 1.24],
                          "D2": [-93.1, 0., 0., 1.24],},
                 "dend2":{"D1": [  5., 0., 0., 1.24],
                          "D2": [93.1, 0., 0., 1.24],},
                 "dend3":{"D1": [   -5, 0., 0., 1.24],
                          "D2": [-93.1, 0., 0., 1.24],},
                 "bulb0":{"D1": [ 93.1, 0., 0., 3.6],
                          "D2": [100.3, 0., 0., 3.6],},
                 "bulb1":{"D1": [ -93.1, 0., 0., 3.6],
                          "D2": [-100.3, 0., 0., 3.6],},
                 "bulb2":{"D1": [ 93.1, 0., 0., 3.6],
                          "D2": [100.3, 0., 0., 3.6],},
                 "bulb3":{"D1": [ -93.1, 0., 0., 3.6],
                          "D2": [-100.3, 0., 0., 3.6],},}
        # Construct parts
        self.soma = h.Section(name="soma")
        self.dend = [h.Section(name="dend"+str(i)) for i in range(ndend)]
        self.bulb = [h.Section(name="bulb"+str(i)) for i in range(nbulb)]

        # Soma definition
        self.soma.nseg = 1

        self.soma.insert("naf_chan")
        [setattr(seg.naf_chan, "gbar", 0.07) for seg in self.soma]

        self.soma.insert("kdr_chan")

        self.soma.insert("ka_chan")
        [setattr(seg.ka_chan, "gbar", 0.00367) for seg in self.soma]
        #[setattr(seg.ka_chan, "tauh_min", 12) for seg in self.soma]
        h.tauh_min_ka_chan = 12. # since global variable

        self.soma.insert("h_chan")
        [setattr(seg.h_chan, "gbar", 9e-5) for seg in self.soma]
        #[setattr(seg.h_chan, "am", 0.0008) for seg in self.soma]
        h.am_h_chan = 0.0008 # since global variable

        self.soma.insert("cahva_chan")
        self.soma.insert("nacaexch")

        self.soma.insert("cagrcdifus")
        #[setattr(seg.cagrcdifus, "CaRest", 7.55e-5) for seg in self.soma]
        h.CaRest_cagrcdifus = 7.55e-5 # since global variable
        #[setattr(seg.cagrcdifus, "k1buf", 30) for seg in self.soma]
        #[setattr(seg.cagrcdifus, "k2buf", 0.03) for seg in self.soma]
        h.k1buf_cagrcdifus = 30. # since PARAMETER
        h.k2buf_cagrcdifus = 0.03 # since PARAMETER
        [setattr(seg.cagrcdifus, "Buffer0", 0.025) for seg in self.soma]

        self.soma.insert("Ic")
        [setattr(seg.Ic, "gbar", 0.08) for seg in self.soma]

        self.soma.insert("caleak")
        [setattr(seg.caleak, "gbar", 4e-6) for seg in self.soma]

        self.soma.insert("naleak")
        [setattr(seg.naleak, "gbar", 7.6e-6) for seg in self.soma]

        self.soma.eca = 80
        self.soma.cao = 2
        self.soma.cai = 75.53-6

        # Soma coordinate
        self.soma.push()
        h.pt3dclear()
        h.pt3dadd( coord["soma"]["D1"][0], coord["soma"]["D1"][1], coord["soma"]["D1"][2],
                   coord["soma"]["D1"][3] )
        h.pt3dadd( coord["soma"]["D2"][0], coord["soma"]["D2"][1], coord["soma"]["D2"][2],
                   coord["soma"]["D2"][3] )
        h.pop_section()

        # Dendrite definition
        for i in range(ndend):
            self.dend[i].nseg = 2
            self.dend[i].insert("pas")
            [ setattr(seg.pas, "g", 0.000033) for seg in self.dend[i] ]
            [ setattr(seg.pas, "e", -65) for seg in self.dend[i] ]

            # Dendrite coordinate
            self.dend[i].push()
            h.pt3dclear()
            h.pt3dadd( coord["dend"+str(i)]["D1"][0], coord["dend"+str(i)]["D1"][1],
                       coord["dend"+str(i)]["D1"][2], coord["dend"+str(i)]["D1"][3] )
            h.pt3dadd( coord["dend"+str(i)]["D2"][0], coord["dend"+str(i)]["D2"][1],
                       coord["dend"+str(i)]["D2"][2], coord["dend"+str(i)]["D2"][3] )
            h.pop_section()

        # Bulb definition
        for i in range(nbulb):
            self.bulb[i].nseg = 1
            self.bulb[i].insert("pas")
            [ setattr(seg.pas, "g", 0.000033) for seg in self.bulb[i] ]
            [ setattr(seg.pas, "e", -65) for seg in self.bulb[i] ]

            # Dendrite coordinate
            self.bulb[i].push()
            h.pt3dclear()
            h.pt3dadd( coord["bulb"+str(i)]["D1"][0], coord["bulb"+str(i)]["D1"][1],
                       coord["bulb"+str(i)]["D1"][2], coord["bulb"+str(i)]["D1"][3] )
            h.pt3dadd( coord["bulb"+str(i)]["D2"][0], coord["bulb"+str(i)]["D2"][1],
                       coord["bulb"+str(i)]["D2"][2], coord["bulb"+str(i)]["D2"][3] )
            h.pop_section()

        h.Ra = 100. # Global Ra

        # Connection
        for i in range(ndend):
            # Dendrites to soma
            self.soma.connect( self.dend[i], 1, 0 )

        #  Blub to dendrites
        for i in range(nbulb):
            for j in range(ndend):
                self.dend[j].connect( self.bulb[i], 1, 0 )
