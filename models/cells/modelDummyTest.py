# ~/models/cells/modelDummyTest.py
import os
pwd = os.getcwd()
path_to_files = pwd + os.sep + "models" + os.sep + "cells" + os.sep + \
                "DummyTest" + os.sep

#from managers.managerRecord import RecordManager
#from managers.managerSimulation import SimulationManager

from managers.simulation import SimulationManager as sm
from models.cells.DummyTest.Dummy import Dummy

class DummyCell(object):

    def __init__(self):
        self.regions = {'soma': 0.0, # refer Dummy.py to choose regions
                        'axon': 0.0,
                        'channels': {'soma': ['pas'],
                                     'axon': ['pas']}}
        self.modelscale = "cells"
        self.modelname = "DummyTest"
        #
        self.name = "Dummy Test"
        self.description = "This is a dummy model for testing out the managers and their operators."
        #
        # instantiate
        sm.lock_and_load_model_libraries(modelscale=self.modelscale,
                                         modelname=self.modelname)
        os.chdir(path_to_files)
        self.cell = Dummy()
        os.chdir(pwd)
        #self.rc = RecordManager()

    def produce_voltage_response(self):
        return "DummyTest model just finished run for produce_voltage_response"

    def produce_spike_train(self):
        return "DummyTest model just finished run for produce_spike_train"
