# ~/models/cells/modelDummyTest.py
import os
pwd = os.getcwd()

#from managers.managerRecord import RecordManager
#from managers.managerSimulation import SimulationManager

from managers.managerSimulation import SimulationManager
from models.cells.DummyTest.Dummy import Dummy

class DummyCell(object):

    def __init__(self):
        self.regions = {'soma': 0.0, # refer Dummy.py to choose regions
                        'axon': 0.0}
        self.modelscale = "cells"
        self.modelname = "DummyTest"
        #
        self.name = "Dummy Test"
        self.description = "This is a dummy model for testing out the managers and their operators."
        #
        self.sm = SimulationManager()
        # instantiate
        self.sm.si.lock_and_load_nmodl(modelscale=self.modelscale, modelname=self.modelname)
        self.cell = Dummy()
        #self.rc = RecordManager()

    def produce_voltage_response(self):
        return "DummyTest model just finished run for produce_voltage_response"

    def produce_spike_train(self):
        return "DummyTest model just finished run for produce_spike_train"
