 #/managers/operatorsTranscribe/metadata_epochgeneratorTest.py
import unittest

import os
import sys
# import modules for other directories
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
# this is required for

pwd = os.getcwd()
os.chdir("..") # this moves you up to ~/managers
os.chdir("..") # you are now in parent /cerebmodels
rootwd = os.getcwd()
from models.cells.modelDummyTest import DummyCell
os.chdir(pwd)

from managers.operatorsTranscribe.metadata_epochgenerator import EpochGenerator as eg

class EpochGeneratorTest(unittest.TestCase):

    def setUp(self):
        os.chdir(rootwd)
        self.chosenmodel = DummyCell()
        os.chdir(pwd)

    #@unittest.skip("reason for skipping")
    def test_1_compute_totalepochs_per_cellregion_without_stimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        self.assertEqual( eg.compute_totalepochs_per_cellregion(runtimeparam),
                          1 )

    #@unittest.skip("reason for skipping")
    def test_2_compute_totalepochs_per_cellregion_with_stimulus(self):
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                          "tstop": 10.0+100.0+50.0}
        self.assertEqual( eg.compute_totalepochs_per_cellregion(stimparameters),
                          1 + len(stimparameters["stimlist"]) )
        
    #@unittest.skip("reason for skipping")
    def test_3_epochcontainer_without_stimulus(self):
        no_of_regions = len(list(self.chosenmodel.regions.keys()))
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        filler = eg.epochcontainer(self.chosenmodel, runtimeparam)
        compare2 = len(filler)
        no_of_epochs_per_region = 1
        compare1 = no_of_regions * no_of_epochs_per_region 
        #print filler # how does the epochcontainer metadata look?
        self.assertEqual( compare2, compare1 )

    #@unittest.skip("reason for skipping")
    def test_4_epochcontainer_with_stimulus(self):
        no_of_regions = len(list(self.chosenmodel.regions.keys()))
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                          "tstop": 10.0+100.0+50.0}
        filler = eg.epochcontainer(self.chosenmodel, stimparameters)
        compare2 = len(filler)
        no_of_epochs_per_region = 1 + len(stimparameters["stimlist"])
        compare1 = no_of_regions * no_of_epochs_per_region
        #print filler # how does the epochcontainer metadata look?
        self.assertEqual( compare2, compare1 )

    #@unittest.skip("reason for skipping")
    def test_5_an_epoch_stimulus_window_firststimulus(self):
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},       #1
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],#2
                          "tstop": 10.0+100.0+50.0}
        epoch_value = eg.an_epoch_stimulus_window( 1, "soma", stimparameters)
        compare2 = epoch_value["start_time"] + epoch_value["stop_time"]
        compare1 = stimparameters["stimlist"][0]["delay"] + \
              stimparameters["stimlist"][0]["delay"]+stimparameters["stimlist"][0]["dur"]
        #print epoch_value # how does an epoch metadata look?
        self.assertEqual( compare2, compare1 )

    #@unittest.skip("reason for skipping")
    def test_6_an_epoch_stimulus_window_laststimulus(self):
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},       #1
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],#2
                          "tstop": 10.0+100.0+50.0}
        epoch_value = eg.an_epoch_stimulus_window( 2, "soma", stimparameters)
        compare2 = epoch_value["start_time"] + epoch_value["stop_time"]
        compare1 = stimparameters["stimlist"][1]["delay"] + \
              stimparameters["stimlist"][1]["delay"]+stimparameters["stimlist"][1]["dur"]
        #print epoch_value # how does an epoch metadata look?
        self.assertEqual( compare2, compare1 )

    #@unittest.skip("reason for skipping")
    def test_7_an_epoch_prestimulus(self):
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                          "tstop": 10.0+100.0+50.0}
        epoch_value = eg.an_epoch( 0, "soma", stimparameters)
        compare2 = epoch_value["start_time"] + epoch_value["stop_time"]
        compare1 = 0.0 + stimparameters["stimlist"][0]["delay"]
        #print epoch_value # how does an epoch metadata look?
        self.assertEqual( compare2, compare1 )

    #@unittest.skip("reason for skipping")
    def test_8_an_epoch_firststimulus(self):
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                          "tstop": 10.0+100.0+50.0}
        epoch_value = eg.an_epoch( 1, "axon", stimparameters)
        compare2 = epoch_value["description"]
        compare1 = "IClamp stimulation of model with amplitude = " + \
                       str(stimparameters["stimlist"][0]["amp"]) + " nA"
        #print epoch_value # hows does an epoch metadata look?
        self.assertEqual( compare2, compare1 )

    #@unittest.skip("reason for skipping")
    def test_9_an_epoch_laststimulus_equals_tstop(self):
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                          "tstop": 10.0+100.0+50.0}
        epoch_value = eg.an_epoch( 2, "axon", stimparameters)
        compare2 = epoch_value["description"]
        compare1 = "IClamp stimulation of model with amplitude = " + \
                       str(stimparameters["stimlist"][1]["amp"]) + " nA"
        #print epoch_value # hows does an epoch metadata look?
        self.assertEqual( compare2, compare1 )

    #@unittest.skip("reason for skipping")
    def test_10_an_epoch_laststimulus_notequals_tstop(self):
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                          "tstop": 200.0}
        epoch_value = eg.an_epoch( 2, "axon", stimparameters)
        compare2 = epoch_value["description"]
        compare1 = "IClamp stimulation of model with amplitude = " + \
                       str(stimparameters["stimlist"][1]["amp"]) + " nA"
        #print epoch_value # hows does an epoch metadata look?
        self.assertEqual( compare2, compare1 )

    #@unittest.skip("reason for skipping")
    def test_11_an_epoch_poststimulus(self):
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                          "tstop": 200.0}
        epoch_value = eg.an_epoch( 3, "axon", stimparameters)
        compare2 = epoch_value["description"]
        compare1 = "last, no stimulus"
        #print epoch_value # hows does an epoch metadata look?
        self.assertEqual( compare2, compare1 )

    #@unittest.skip("reason for skipping")
    def test_12_forepoch_without_stimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        epochmd = eg.forepoch( chosenmodel = self.chosenmodel,
                                    parameters = runtimeparam )
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        no_of_stimulus_epochs_per_region = 0 
        compare2 = epochmd["epoch"+str(no_of_stimulus_epochs_per_region)+"soma"]["stop_time"]
        compare1 = epochmd["epoch"+str(no_of_stimulus_epochs_per_region)+"axon"]["stop_time"]
        #print epochmd # hows does the main epoch metadata look?
        self.assertEqual( compare2, compare1 )

    #@unittest.skip("reason for skipping")
    def test_13_forepoch_with_stimulus(self):
        stimparameters = {"type": ["current", "IRamp"],
           "stimlist": [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0, "delay": 5.0},
                         {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0, "delay": 10.0},
                         {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0, "delay": 15.0},
                         {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0, "delay": 20.0} ],
           "tstop": 20.0+5.0}
        epochmd = eg.forepoch( chosenmodel = self.chosenmodel,
                               parameters = stimparameters )
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        no_of_stimulus_epochs_per_region = len(stimparameters["stimlist"])
        compare2 = epochmd["epoch"+str(no_of_stimulus_epochs_per_region)+"soma"]["stop_time"]
        compare1 = epochmd["epoch"+str(no_of_stimulus_epochs_per_region)+"axon"]["stop_time"]
        #print epochmd # how does the main epoch metadata look?
        self.assertEqual( compare2, compare1 )

    #@unittest.skip("reason for skipping")
    def test_14_forepoch_with_stimulus_laststimulus_notequals_tstop(self):
        stimparameters = {"type": ["current", "IRamp"],
           "stimlist": [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0, "delay": 5.0},
                         {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0, "delay": 10.0},
                         {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0, "delay": 15.0},
                         {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0, "delay": 20.0} ],
           "tstop": 20.0+10.0}
        epochmd = eg.forepoch( chosenmodel = self.chosenmodel,
                               parameters = stimparameters )
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        no_of_stimulus_epochs_per_region = len(stimparameters["stimlist"])
        compare2 = [ epochmd["epoch"+str(0)+"soma"]["stop_time"],
                     epochmd["epoch"+str(no_of_stimulus_epochs_per_region)+"soma"]["stop_time"],
                     epochmd["epoch"+str(no_of_stimulus_epochs_per_region+1)+"soma"]["stop_time"] ]
        compare1 = [ epochmd["epoch"+str(0)+"axon"]["stop_time"],
                     epochmd["epoch"+str(no_of_stimulus_epochs_per_region)+"axon"]["stop_time"],
                     stimparameters["tstop"] ]
        #print epochmd # how does the main epoch metadata look?
        self.assertEqual( compare2, compare1 )

if __name__ == '__main__':
    unittest.main()
