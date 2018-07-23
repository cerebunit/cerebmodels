# ~/models/cells/modelDummyTest.py

#from managers.managerRecord import RecordManager
#from managers.managerSimulation import SimulationManager

from models.cells.DummyTest.Dummy import Dummy

class DummyTest(object):

    def __init__(self):
        self.cell = Dummy()
        self.regions = {self.cell.soma: 0.0, # refer Dummy.py to choose regions
                        self.cell.axon: 0.0}
        self.modelscale = "cells"
        self.modelname = "DummyTest"
        # instantiate
        #self.rc = RecordManager()

    def produce_voltage_response(self):
        return "DummyTest model just finished run for produce_voltage_response"

    def produce_spike_train(self):
        return "DummyTest model just finished run for produce_spike_train"
