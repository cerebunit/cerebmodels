# ../managers/managerSimulationTest.py
import unittest
import os
import importlib

import sys
# import modules from other directories
# set to ~/cerebmodels
sys.path.append(os.path.dirname(os.getcwd()))
# this is required for
# from managers.operatorsSimaudit.inspector import SimInspector
# from managers.operatorsSimaudit.hardware import HardwareConfigurator
# from managers.operatorsSimaudit.assembler import SimAssembler
# called in managerSimulation.py
# and also for the utilities
from utilities import UsefulUtils

from managerSimulation import SimulationManager


class SimulationManagerTest(unittest.TestCase):

    def setUp(self):
        self.sm = SimulationManager() #instance for non: static & class methods.
        self.uu = UsefulUtils() #for alternative approach see managerRecordTest.py
        self.pwd = os.getcwd()

    def test_1_prepare_model_NEURON(self):
        os.chdir("..") # move up to load the model
        #from utilities import UsefulUtils as uu
        # pick the model
        modelmodule = importlib.import_module("models.cells.modelDummyTest")
        pickedmodel = getattr(modelmodule,
                              self.uu.classesinmodule(modelmodule)[0].__name__)
        chosenmodel = pickedmodel()
        #
        parameters = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        self.assertEqual(self.sm.prepare_model_NEURON(parameters, chosenmodel),
                         "NEURON model is ready")
        os.chdir(self.pwd) # return to the location of this test file

    def test_2_lock_and_load_capability(self):
        os.chdir("..") # move up to load the model
        #from utilities import UsefulUtils as uu
        # pick the model
        modelmodule = importlib.import_module("models.cells.modelDummyTest")
        pickedmodel = getattr(modelmodule,
                              self.uu.classesinmodule(modelmodule)[0].__name__)
        chosenmodel = pickedmodel()
        #
        self.assertEqual(SimulationManager.lock_and_load_capability(
                                              chosenmodel,
                                              modelcapability="produce_spike_train"),
                         "DummyTest model just finished run for produce_spike_train")
        os.chdir(self.pwd) # return to the location of this test file

    def test_3_trigger_NEURON_with_capability(self):
        os.chdir("..") # move up to load the model
        # pick the model
        modelmodule = importlib.import_module("models.cells.modelDummyTest")
        pickedmodel = getattr(modelmodule,
                              self.uu.classesinmodule(modelmodule)[0].__name__)
        chosenmodel = pickedmodel()
        #
        parameters = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        self.sm.prepare_model_NEURON(parameters, chosenmodel)
        self.assertEqual( self.sm.trigger_NEURON (
                                          chosenmodel,
                                          modelcapability="produce_spike_train"),
                          "model was successfully triggered via NEURON" )
        os.chdir(self.pwd) # return to the location of this test file

    def test_4_trigger_NEURON_raw(self):
        os.chdir("..") # move up to load the model
        # pick the model
        modelmodule = importlib.import_module("models.cells.modelDummyTest")
        pickedmodel = getattr(modelmodule,
                              self.uu.classesinmodule(modelmodule)[0].__name__)
        chosenmodel = pickedmodel()
        #
        parameters = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        self.sm.prepare_model_NEURON(parameters, chosenmodel)
        self.assertEqual( self.sm.trigger_NEURON ( chosenmodel ),
                          "model was successfully triggered via NEURON" )
        os.chdir(self.pwd) # return to the location of this test file

    def test_5_stimulate_model_NEURON_parameter_None(self):
        os.chdir("..") # move up to load the model
        # pick the model
        modelmodule = importlib.import_module("models.cells.modelDummyTest")
        pickedmodel = getattr(modelmodule,
                              self.uu.classesinmodule(modelmodule)[0].__name__)
        chosenmodel = pickedmodel()
        #
        parameters = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        self.sm.prepare_model_NEURON(parameters, chosenmodel)
        self.assertEqual( self.sm.stimulate_model_NEURON(),
                          "Model is not stimulated" )
        os.chdir(self.pwd) # return to the location of this test file

    def test_6_stimulate_model_NEURON_parameter_error(self):
        os.chdir("..") # move up to load the model
        # pick the model
        modelmodule = importlib.import_module("models.cells.modelDummyTest")
        pickedmodel = getattr(modelmodule,
                              self.uu.classesinmodule(modelmodule)[0].__name__)
        chosenmodel = pickedmodel()
        #
        parameters = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        #currparameters = {"type": ["current", "IClamp"]} # default
        currparameters = {"type": "current"} # alternative
        self.sm.prepare_model_NEURON(parameters, chosenmodel)
        self.assertRaises( ValueError,
                           self.sm.stimulate_model_NEURON,
                           stimparameters = currparameters,
                           modelsite = chosenmodel.cell.soma )
        os.chdir(self.pwd) # return to the location of this test file

    def test_7_stimulate_model_NEURON_current(self):
        os.chdir("..") # move up to load the model
        # pick the model
        modelmodule = importlib.import_module("models.cells.modelDummyTest")
        pickedmodel = getattr(modelmodule,
                              self.uu.classesinmodule(modelmodule)[0].__name__)
        chosenmodel = pickedmodel()
        #
        parameters = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        currparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {'amp': 0.5, 'dur': 100.0, 'delay': 10.0},
                                        {'amp': 1.0, 'dur': 50.0, 'delay': 10.0+100.0} ] }
        self.sm.prepare_model_NEURON(parameters, chosenmodel)
        self.assertEqual( len( self.sm.stimulate_model_NEURON(
                                                stimparameters = currparameters,
                                                modelsite = chosenmodel.cell.soma ) ),
                          len(currparameters["stimlist"]) )
        os.chdir(self.pwd) # return to the location of this test file


if __name__ == '__main__':
    unittest.main()
