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
from utilities import UsefulUtils as uu

pwd = os.getcwd()
os.chdir("..") # this moves you up to ~/cerebmodels
rootwd = os.getcwd()
os.chdir(pwd)

from managerSimulation import SimulationManager as sm


class SimulationManagerTest(unittest.TestCase):

    def setUp(self):
        #self.sm = SimulationManager() #instance for non: static & class methods.
        pass

    #@unittest.skip("reason for skipping")
    def test_1_lock_and_load_model_libraries_error(self):
        self.assertRaises( ValueError, sm.lock_and_load_model_libraries, )

    #@unittest.skip("reason for skipping")
    def test_2_lock_and_load_model_libraries(self):
        os.chdir(rootwd) # move up to ~/cerebmodels
        self.assertEqual( sm.lock_and_load_model_libraries(
                                     modelscale="cells", modelname="DummyTest"),
                          "Model libraries area loaded" )
        os.chdir(pwd)

    #@unittest.skip("reason for skipping")
    def test_3_prepare_model_NEURON_nomodel(self):
        self.assertRaises( ValueError, sm.prepare_model_NEURON, )

    #@unittest.skip("reason for skipping")
    def test_4_prepare_model_NEURON(self):
        os.chdir(rootwd) # move up to load the model
        #from utilities import UsefulUtils as uu
        # pick the model
        modelmodule = importlib.import_module("models.cells.modelDummyTest")
        pickedmodel = getattr(modelmodule,
                              uu.classesinmodule(modelmodule)[0].__name__)
        chosenmodel = pickedmodel()
        #
        parameters = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        self.assertEqual(sm.prepare_model_NEURON(
                                parameters=parameters, chosenmodel=chosenmodel),
                         "NEURON model is ready")
        os.chdir(pwd) # return to the location of this test file

    #@unittest.skip("reason for skipping")
    def test_5_lock_and_load_capability(self):
        os.chdir(rootwd) # move up to load the model
        #from utilities import UsefulUtils as uu
        # pick the model
        modelmodule = importlib.import_module("models.cells.modelDummyTest")
        pickedmodel = getattr(modelmodule,
                              uu.classesinmodule(modelmodule)[0].__name__)
        chosenmodel = pickedmodel()
        #
        self.assertEqual(sm.lock_and_load_capability(
                                 chosenmodel, modelcapability="produce_spike_train"),
                         "DummyTest model just finished run for produce_spike_train")
        os.chdir(pwd) # return to the location of this test file

    #@unittest.skip("reason for skipping")
    def test_6_trigger_NEURON_with_capability(self):
        os.chdir(rootwd) # move up to load the model
        # pick the model
        modelmodule = importlib.import_module("models.cells.modelDummyTest")
        pickedmodel = getattr(modelmodule,
                              uu.classesinmodule(modelmodule)[0].__name__)
        chosenmodel = pickedmodel()
        #
        parameters = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        sm.prepare_model_NEURON(parameters=parameters, chosenmodel=chosenmodel)
        self.assertEqual( sm.trigger_NEURON (
                                 chosenmodel, modelcapability="produce_spike_train"),
                          "model was successfully triggered via NEURON" )
        os.chdir(pwd) # return to the location of this test file

    #@unittest.skip("reason for skipping")
    def test_7_trigger_NEURON_raw(self):
        os.chdir(rootwd) # move up to load the model
        # pick the model
        modelmodule = importlib.import_module("models.cells.modelDummyTest")
        pickedmodel = getattr(modelmodule,
                              uu.classesinmodule(modelmodule)[0].__name__)
        chosenmodel = pickedmodel()
        #
        parameters = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        sm.prepare_model_NEURON(parameters=parameters, chosenmodel=chosenmodel)
        self.assertEqual( sm.trigger_NEURON ( chosenmodel ),
                          "model was successfully triggered via NEURON" )
        os.chdir(pwd) # return to the location of this test file

    #@unittest.skip("reason for skipping")
    def test_8_stimulate_model_NEURON_parameter_None(self):
        os.chdir(rootwd) # move up to load the model
        # pick the model
        modelmodule = importlib.import_module("models.cells.modelDummyTest")
        pickedmodel = getattr(modelmodule,
                              uu.classesinmodule(modelmodule)[0].__name__)
        chosenmodel = pickedmodel()
        #
        parameters = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        sm.prepare_model_NEURON(parameters=parameters, chosenmodel=chosenmodel)
        self.assertEqual( sm.stimulate_model_NEURON(),
                          "Model is not stimulated" )
        os.chdir(pwd) # return to the location of this test file

    #@unittest.skip("reason for skipping")
    def test_9_stimulate_model_NEURON_parameter_error(self):
        os.chdir(rootwd) # move up to load the model
        # pick the model
        modelmodule = importlib.import_module("models.cells.modelDummyTest")
        pickedmodel = getattr(modelmodule,
                              uu.classesinmodule(modelmodule)[0].__name__)
        chosenmodel = pickedmodel()
        #
        parameters = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        #currparameters = {"type": ["current", "IClamp"]} # default
        currparameters = {"type": "current"} # alternative
        sm.prepare_model_NEURON(parameters=parameters, chosenmodel=chosenmodel)
        self.assertRaises( ValueError,
                           sm.stimulate_model_NEURON,
                           stimparameters = currparameters,
                           modelsite = chosenmodel.cell.soma )
        os.chdir(pwd) # return to the location of this test file

    #@unittest.skip("reason for skipping")
    def test_10_stimulate_model_NEURON_current(self):
        os.chdir(rootwd) # move up to load the model
        # pick the model
        modelmodule = importlib.import_module("models.cells.modelDummyTest")
        pickedmodel = getattr(modelmodule,
                              uu.classesinmodule(modelmodule)[0].__name__)
        chosenmodel = pickedmodel()
        #
        parameters = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        currparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {'amp': 0.5, 'dur': 100.0, 'delay': 10.0},
                                        {'amp': 1.0, 'dur': 50.0, 'delay': 10.0+100.0} ] }
        sm.prepare_model_NEURON(parameters=parameters, chosenmodel=chosenmodel)
        self.assertEqual( len( sm.stimulate_model_NEURON(
                                                stimparameters = currparameters,
                                                modelsite = chosenmodel.cell.soma ) ),
                          len(currparameters["stimlist"]) )
        os.chdir(pwd) # return to the location of this test file


if __name__ == '__main__':
    unittest.main()
