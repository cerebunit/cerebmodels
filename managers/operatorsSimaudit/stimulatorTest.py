# ~/managers/operatorsSimaudit/stimulatorTest.py
import unittest

import os
import sys
# import modules from other directories
# set to ~/cerebmodels
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
# this is required for
from models.cells.modelDummyTest import DummyTest

# because IRamp is not by default its nmodl files need to be loaded
# testing for inject_IRamp requires SimInspector
from managers.operatorsSimaudit.inspector import SimInspector
#from managers.managerSimulation import SimulationManager

from stimulator import Stimulator

from neuron import h
h.load_file("stdrun.hoc")

class StimulatorTest(unittest.TestCase):

    def setUp(self):
        self.st = Stimulator()
        self.pwd = os.getcwd()
        self.chosenmodel = DummyTest()
        self.si = SimInspector()
        #self.sm = SimulationManager()

    def test_1_inject_IClamp_wrong_key_in_parameter(self):
        os.chdir("..") # this moves you up to ~/managers
        os.chdir("..") # you are now in root
        #parameters = {"dt": 0.1, "celsius": 20, "tstop": 15, "v_init": 65}
        #injparam = [ {"amp": 0.5, "dur": 5.0, "delay": 5.0},
        #             {"amp": 1.0, "dur": 5.0, "delay": parameters["tstop"]-5.0} ]
        #                    this last duration is subtracted from tstop
        #self.sm.prepare_model_NEURON(parameters, self.chosenmodel)
        injparam = [ {"amplitude": 0.5, "dur": 5.0, "delay": 5.0},
                     {"amp": 1.0, "dur": 5.0, "delay": 10.0} ]
        self.assertRaises( AttributeError,
                           Stimulator.inject_IClamp,
                           injparam,
                           self.chosenmodel.cell.soma )
        os.chdir(self.pwd) # reset to the location of this stimulatorTest.py

    def test_2_inject_IClamp(self):
        os.chdir("..") # this moves you up to ~/managers
        os.chdir("..") # you are now in root
        injparam = [ {"amp": 0.5, "dur": 5.0, "delay": 5.0},
                     {"amp": 1.0, "dur": 5.0, "delay": 10.0} ]
        curr_stimuli = Stimulator.inject_IClamp(injparam, self.chosenmodel.cell.soma)
        self.assertEqual( len(curr_stimuli ), len(injparam) )
        os.chdir(self.pwd) # reset to the location of this stimulatorTest.py

    def test_3_inject_IRamp(self):
        os.chdir("..") # this moves you up to ~/managers
        os.chdir("..") # you are now in root
        # load nmodl file for using the custom IRamp
        self.si.lock_and_load_nmodl(modelscale="cells", modelname="DummyTest")
        #
        injparam = [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0, "delay": 5.0},
                     {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0, "delay": 10.0},
                     {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0, "delay": 15.0},
                     {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0, "delay": 20.0} ]
        curr_stimuli = Stimulator.inject_IRamp(injparam, self.chosenmodel.cell.soma)
        # here based on the injparm
        # increasing ramp is from injparam[0] to injparam[1] while
        # decreading ramp if from injparam[2] to injparam[3]. Thus,
        slopes = [ 0.5, 0.5, -0.5, -0.5 ]
        # NOTE: the magnitude for each slope is |amp_final - amp_initial| respectively.
        #
        curr_slopes = []
        for i in range(len(curr_stimuli)):
            curr_slopes.append( curr_stimuli[i].amp_final )
        #
        self.assertEqual( curr_slopes, slopes )
        os.chdir(self.pwd) # reset to the location of this stimulatorTest.py

    def test_4_inject_current_NEURON_without_currenttype(self):
        os.chdir("..") # this moves you up to ~/managers
        os.chdir("..") # you are now in root
        injparam = [ {"amp": 0.5, "dur": 5.0, "delay": 5.0},
                     {"amp": 1.0, "dur": 5.0, "delay": 10.0} ]
        self.assertRaises( ValueError,
                           self.st.inject_current_NEURON,
                           injparameters = injparam,
                           neuronsection = self.chosenmodel.cell.soma )
        os.chdir(self.pwd) # reset to the location of this stimulatorTest.py

    def test_5_inject_current_NEURON_wrong_currenttype(self):
        os.chdir("..") # this moves you up to ~/managers
        os.chdir("..") # you are now in root
        injparam = [ {"amp": 0.5, "dur": 5.0, "delay": 5.0},
                     {"amp": 1.0, "dur": 5.0, "delay": 10.0} ]
        self.assertRaises( ValueError,
                           self.st.inject_current_NEURON,
                           currenttype = "xyz",
                           injparameters = injparam,
                           neuronsection = self.chosenmodel.cell.soma )
        os.chdir(self.pwd) # reset to the location of this stimulatorTest.py

    def test_6_inject_current_NEURON_IClamp(self):
        os.chdir("..") # this moves you up to ~/managers
        os.chdir("..") # you are now in root
        injparam = [ {"amp": 0.5, "dur": 5.0, "delay": 5.0},
                     {"amp": 1.0, "dur": 5.0, "delay": 10.0} ]
        self.assertEqual( len( self.st.inject_current_NEURON(
                                       currenttype = "IClamp",
                                       injparameters = injparam,
                                       neuronsection = self.chosenmodel.cell.soma)),
                          len(injparam) )
        os.chdir(self.pwd) # reset to the location of this stimulatorTest.py

    def test_7_inject_current_NEURON_IRamp(self):
        os.chdir("..") # this moves you up to ~/managers
        os.chdir("..") # you are now in root
        # load nmodl file for using the custom IRamp
        self.si.lock_and_load_nmodl(modelscale="cells", modelname="DummyTest")
        #
        injparam = [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0, "delay": 5.0},
                     {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0, "delay": 10.0},
                     {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0, "delay": 15.0},
                     {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0, "delay": 20.0} ]
        curr_stimuli = self.st.inject_current_NEURON(
                                       currenttype = "IRamp",
                                       injparameters = injparam,
                                       neuronsection = self.chosenmodel.cell.soma)
        self.assertEqual( len(curr_stimuli ), len(injparam) )
        os.chdir(self.pwd) # reset to the location of this stimulatorTest.py

if __name__ == '__main__':
    unittest.main()