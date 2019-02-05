# ~/models/cells/DummyTest/Dummy.py

from neuron import h
h.load_file("stdrun.hoc")

class Dummy(object):
    def __init__(self):
        self.soma = h.Section(name='soma')
        self.soma.nseg = 1 # compartmentalized parameter
        self.soma.diam = 30.0 # um
        self.soma.L = 30.0    # um same as diam => sphere
        self.soma.cm = 1.0
        self.soma.Ra = 120
        self.soma.insert('hh')
        #
        self.axon = h.Section(name='axon')
        self.axon.nseg = 20 # compartmentalized parameter
        self.axon.diam = 1.0  # um
        self.soma.L = 1000.0 # um long
        self.axon.insert('hh')
        self.axon.connect(self.soma,1,0)
        
        ### ====== STANDARDIZED FOR cerebmodels =======
        ### ===== mandatory for all NEURON models =====
	#self.rec_t = h.Vector()
	#self.rec_t.record(h._ref_t)
        # ------- this will be the cell-regions -------
	#self.vm_soma = h.Vector()
	#self.vm_soma.record(self.soma(0.5)._ref_v)
