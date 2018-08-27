# ~/models/cells/modelDummyTest.py

#from managers.managerRecord import RecordManager
#from managers.managerSimulation import SimulationManager

from models.cells.DummyTest.Dummy import Dummy

class DummyCell(object):

    def __init__(self):
        self.cell = Dummy()
        self.regions = {'soma': 0.0, # refer Dummy.py to choose regions
                        'axon': 0.0}
        self.modelscale = "cells"
        self.modelname = "DummyTest"
        #
        self.name = "Dummy Test"
        self.description = "This is a dummy model for testing out the managers and their operators."
        # instantiate
        #self.rc = RecordManager()

    def produce_voltage_response(self):
        return "DummyTest model just finished run for produce_voltage_response"

    def produce_spike_train(self):
        return "DummyTest model just finished run for produce_spike_train"
