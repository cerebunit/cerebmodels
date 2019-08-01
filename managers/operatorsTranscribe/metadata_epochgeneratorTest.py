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

from metadata_epochgenerator import EpochGenerator as eg

from collections import Counter

class EpochGeneratorTest(unittest.TestCase):

    def setUp(self):
        os.chdir(rootwd)
        self.chosenmodel = DummyCell()
        os.chdir(pwd)
        # No stimulus
        self.no_runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        # IClamp
        self.ic_runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 200, "v_init": 65}
        self.ic_stimparameters = {"type": ["current", "IClamp"],
                              "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                            {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                                 "tstop": self.ic_runtimeparam["tstop"]}
        # SEClamp
        self.sec_runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 35, "v_init": 65}
        self.sec_stimparameters = {"type": ["voltage", "SEClamp"],
                               "stimlist": [ {'amp1': 0., 'dur1': 10.0},
                                             {'amp2': -70.0, 'dur2': 20.0} ],
                                  "tstop": self.sec_runtimeparam["tstop"]}

    #@unittest.skip("reason for skipping")
    def test_1_compute_totalepochs_per_cellregion_without_stimulus(self):
        self.assertEqual( eg.compute_totalepochs_per_cellregion(self.no_runtimeparam),
                          1 )

    #@unittest.skip("reason for skipping")
    def test_2_compute_totalepochs_per_cellregion_with_currentstimulus(self):
        self.assertEqual( eg.compute_totalepochs_per_cellregion(self.ic_stimparameters),
                          1 + len(self.ic_stimparameters["stimlist"]) )

    #@unittest.skip("reason for skipping")
    def test_3_compute_totalepochs_per_cellregion_with_voltagestimulus(self):
        self.assertEqual( eg.compute_totalepochs_per_cellregion(self.sec_stimparameters),
                          len(self.sec_stimparameters["stimlist"]) )
        
    #@unittest.skip("reason for skipping")
    def test_4_epochcontainer_for_regionbodies_nostimulus(self):
        no_of_epochs = eg.compute_totalepochs_per_cellregion(self.no_runtimeparam)
        filler = eg.epochcontainer_for_regionbodies(self.chosenmodel, no_of_epochs)
        compare2 = len(filler)
        # self.chosenmodel.regions ->
        # {"soma": ["v", "i_cap"], "axon": ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        no_of_regions = 2
        compare1 = no_of_regions * no_of_epochs
        #print filler # how does the epochcontainer metadata look?
        self.assertEqual( compare2, compare1 )

    #@unittest.skip("reason for skipping")
    def test_5_epochcontainer_for_regionbodies_currentstimulus(self):
        no_of_epochs = eg.compute_totalepochs_per_cellregion(self.ic_stimparameters)
        filler = eg.epochcontainer_for_regionbodies(self.chosenmodel, no_of_epochs)
        #print(filler) # how does the epochcontainer metadata look?
        # self.chosenmodel.regions ->
        # {"soma": ["v", "i_cap"], "axon": ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        compare1a = filler["epoch0soma"]["v"]["tags"][0] # number of epochs
        compare1b = filler["epoch0soma"]["v"]["tags"][1] # epochID
        compare1c = filler["epoch0soma"]["v"]["tags"][2][-1] # recsite
        compare1d = filler["epoch0soma"]["v"]["tags"][3] # all recsites
        compare1e = filler["epoch0soma"]["v"]["tags"][4] # modelname
        compare1f = filler["epoch0soma"]["v"]["tags"][5] # modelscale
        compare1g = filler["epoch0soma"]["v"]["tags"][6][-1] # key for recsite
        compare2a = filler["epoch0axon"]["v"]["tags"][0]
        compare2b = filler["epoch0axon"]["v"]["tags"][1]
        compare2c = filler["epoch0axon"]["v"]["tags"][2][-1]
        compare2d = filler["epoch1soma"]["v"]["tags"][3] # all recsites
        compare2e = filler["epoch0axon"]["v"]["tags"][4]
        compare2f = filler["epoch0axon"]["v"]["tags"][5]
        compare2g = filler["epoch1soma"]["v"]["tags"][6][-1]
        #
        compare1 = [compare1a, compare1b, compare1c, compare1d, compare1e, compare1f, compare1g]
        compare2 = [compare2a, compare2b, compare2c, compare2d, compare2e, compare2f, compare2g]
        a = Counter(compare1) == Counter(compare2)
        #
        compare3a = filler["epoch0soma"]["v"]["tags"][1] # epochID
        compare3b = filler["epoch0soma"]["v"]["tags"][2][-1] # [ region, recsite ]
        compare3c = filler["epoch0soma"]["v"]["tags"][3] # all recsites
        compare4a = filler["epoch1soma"]["v"]["tags"][1]
        compare4b = filler["epoch1soma"]["i_cap"]["tags"][2][-1]
        compare4c = filler["epoch0axon"]["v"]["tags"][3]
        #
        compare3 = [compare3a, compare3b, compare3c]
        compare4 = [compare4a, compare4b, compare4c]
        b = Counter(compare3) != Counter(compare4)
        #
        self.assertEqual( [a, b], [True, True] )

    #@unittest.skip("reason for skipping")
    def test_6_epochcontainer_for_components_currentstimulus(self):
        no_of_epochs = eg.compute_totalepochs_per_cellregion(self.ic_stimparameters)
        filler = eg.epochcontainer_for_components(self.chosenmodel, no_of_epochs)
        #print(filler) # how does the epochcontainer metadata look?
        # self.chosenmodel.regions ->
        # {"soma": ["v", "i_cap"], "axon": ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        compare1a = filler["epoch0channels"]["soma"]["pas"]["i"]["tags"][0] # number of epochs
        compare1b = filler["epoch0channels"]["soma"]["pas"]["i"]["tags"][1] # epochID
        compare1c = filler["epoch0channels"]["soma"]["pas"]["i"]["tags"][2][-1] # recsite
        compare1d = filler["epoch0channels"]["soma"]["pas"]["i"]["tags"][3] # all recsites
        compare1e = filler["epoch0channels"]["soma"]["pas"]["i"]["tags"][4] # modelname
        compare1f = filler["epoch0channels"]["soma"]["pas"]["i"]["tags"][5] # modelscale
        compare1g = filler["epoch0channels"]["soma"]["pas"]["i"]["tags"][6][-1] # key for recsite
        compare2a = filler["epoch0channels"]["axon"]["pas"]["i"]["tags"][0] # number of epochs
        compare2b = filler["epoch0channels"]["axon"]["pas"]["i"]["tags"][1] # epochID
        compare2c = filler["epoch0channels"]["axon"]["pas"]["i"]["tags"][2][-1] # recsite
        compare2d = filler["epoch0channels"]["axon"]["pas"]["i"]["tags"][3] # all recsites
        compare2e = filler["epoch0channels"]["axon"]["pas"]["i"]["tags"][4] # modelname
        compare2f = filler["epoch0channels"]["axon"]["pas"]["i"]["tags"][5] # modelscale
        compare2g = filler["epoch0channels"]["axon"]["pas"]["i"]["tags"][6][-1] # key for recsite
        #
        compare1 = [compare1a, compare1b, compare1c, compare1d, compare1e, compare1f, compare1g]
        compare2 = [compare2a, compare2b, compare2c, compare2d, compare2e, compare2f, compare2g]
        a = Counter(compare1) == Counter(compare2)
        #
        compare3a = filler["epoch0channels"]["soma"]["hh"]["il"]["tags"][0] # number of epochs
        compare3b = filler["epoch0channels"]["soma"]["hh"]["il"]["tags"][1] # epochID
        compare3c = filler["epoch0channels"]["soma"]["hh"]["il"]["tags"][2][-1] # recsite
        compare3d = filler["epoch0channels"]["soma"]["hh"]["il"]["tags"][3] # all recsites
        compare3e = filler["epoch0channels"]["soma"]["hh"]["il"]["tags"][6][-1] # key for recsite
        compare4a = filler["epoch1channels"]["axon"]["pas"]["i"]["tags"][0] # number of epochs
        compare4b = filler["epoch1channels"]["soma"]["hh"]["il"]["tags"][1] # epochID
        compare4c = filler["epoch0channels"]["axon"]["pas"]["i"]["tags"][2][-1] # recsite
        compare4d = filler["epoch0channels"]["soma"]["pas"]["i"]["tags"][3] # all recsites
        compare4e = filler["epoch0channels"]["soma"]["hh"]["el"]["tags"][6][-1] # key for recsite
        #
        compare3 = [compare3a, compare3b, compare3c, compare3d, compare3e]
        compare4 = [compare4a, compare4b, compare4c, compare4d, compare4e]
        b = Counter(compare3) != Counter(compare4)
        #
        self.assertEqual( [a, b], [True, True] )
        
    #@unittest.skip("reason for skipping")
    def test_7_epochcontainer_without_stimulus(self):
        no_of_regions = len(list(self.chosenmodel.regions.keys()))
        filler = eg.epochcontainer(self.chosenmodel, self.no_runtimeparam)
        no_of_epochs = filler["epoch0soma"]["v"]["tags"][0]
        #print filler # how does the epochcontainer metadata look?
        self.assertEqual( int(no_of_epochs[0]), 1 )

    #@unittest.skip("reason for skipping")
    def test_8_epochcontainer_with_voltagestimulus(self):
        filler = eg.epochcontainer(self.chosenmodel, self.sec_stimparameters)
        #print(filler) # how does the epochcontainer metadata look?
        #print(filler.keys())
        #print(filler["epoch0soma"].keys())
        # self.chosenmodel.regions ->
        # {"soma": ["v", "i_cap"], "axon": ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        compare1a = filler["epoch0soma"]["v"]["tags"][0] # number of epochs
        compare1b = filler["epoch0soma"]["v"]["tags"][1] # epochID
        compare1c = filler["epoch0soma"]["v"]["tags"][2][-1] # recsite
        compare1d = filler["epoch0soma"]["v"]["tags"][3] # all recsites
        compare1e = filler["epoch0soma"]["v"]["tags"][4] # modelname
        compare1f = filler["epoch0soma"]["v"]["tags"][5] # modelscale
        compare1g = filler["epoch0soma"]["v"]["tags"][6][-1] # key for recsite
        compare2a = filler["epoch0axon"]["v"]["tags"][0]
        compare2b = filler["epoch0axon"]["v"]["tags"][1]
        compare2c = filler["epoch0axon"]["v"]["tags"][2][-1]
        compare2d = filler["epoch1soma"]["v"]["tags"][3] # all recsites
        compare2e = filler["epoch0axon"]["v"]["tags"][4]
        compare2f = filler["epoch0axon"]["v"]["tags"][5]
        compare2g = filler["epoch1soma"]["v"]["tags"][6][-1]
        #
        compare1 = [compare1a, compare1b, compare1c, compare1d, compare1e, compare1f, compare1g]
        compare2 = [compare2a, compare2b, compare2c, compare2d, compare2e, compare2f, compare2g]
        a = Counter(compare1) == Counter(compare2)
        #
        compare3a = filler["epoch0soma"]["v"]["tags"][1] # epochID
        compare3b = filler["epoch0soma"]["v"]["tags"][2][-1] # [ region, recsite ]
        compare3c = filler["epoch0soma"]["v"]["tags"][3] # all recsites
        compare4a = filler["epoch1soma"]["v"]["tags"][1]
        compare4b = filler["epoch1soma"]["i_cap"]["tags"][2][-1]
        compare4c = filler["epoch0axon"]["v"]["tags"][3]
        #
        compare3 = [compare3a, compare3b, compare3c]
        compare4 = [compare4a, compare4b, compare4c]
        b = Counter(compare3) != Counter(compare4)
        #
        compare5a = filler["epoch0channels"]["soma"]["pas"]["i"]["tags"][0] # number of epochs
        compare5b = filler["epoch0channels"]["soma"]["pas"]["i"]["tags"][1] # epochID
        compare5c = filler["epoch0channels"]["soma"]["pas"]["i"]["tags"][2][-1] # recsite
        compare5d = filler["epoch0channels"]["soma"]["pas"]["i"]["tags"][3] # all recsites
        compare5e = filler["epoch0channels"]["soma"]["pas"]["i"]["tags"][4] # modelname
        compare5f = filler["epoch0channels"]["soma"]["pas"]["i"]["tags"][5] # modelscale
        compare5g = filler["epoch0channels"]["soma"]["pas"]["i"]["tags"][6][-1] # key for recsite
        compare6a = filler["epoch0channels"]["axon"]["pas"]["i"]["tags"][0] # number of epochs
        compare6b = filler["epoch0channels"]["axon"]["pas"]["i"]["tags"][1] # epochID
        compare6c = filler["epoch0channels"]["axon"]["pas"]["i"]["tags"][2][-1] # recsite
        compare6d = filler["epoch0channels"]["axon"]["pas"]["i"]["tags"][3] # all recsites
        compare6e = filler["epoch0channels"]["axon"]["pas"]["i"]["tags"][4] # modelname
        compare6f = filler["epoch0channels"]["axon"]["pas"]["i"]["tags"][5] # modelscale
        compare6g = filler["epoch0channels"]["axon"]["pas"]["i"]["tags"][6][-1] # key for recsite
        #
        compare5 = [compare5a, compare5b, compare5c, compare5d, compare5e, compare5f, compare5g]
        compare6 = [compare6a, compare6b, compare6c, compare6d, compare6e, compare6f, compare6g]
        c = Counter(compare5) == Counter(compare6)
        #
        compare7a = filler["epoch0channels"]["soma"]["hh"]["il"]["tags"][0] # number of epochs
        compare7b = filler["epoch0channels"]["soma"]["hh"]["il"]["tags"][1] # epochID
        compare7c = filler["epoch0channels"]["soma"]["hh"]["il"]["tags"][2][-1] # recsite
        compare7d = filler["epoch0channels"]["soma"]["hh"]["il"]["tags"][3] # all recsites
        compare7e = filler["epoch0channels"]["soma"]["hh"]["il"]["tags"][6][-1] # key for recsite
        compare8a = filler["epoch1channels"]["axon"]["pas"]["i"]["tags"][0] # number of epochs
        compare8b = filler["epoch1channels"]["soma"]["hh"]["il"]["tags"][1] # epochID
        compare8c = filler["epoch0channels"]["axon"]["pas"]["i"]["tags"][2][-1] # recsite
        compare8d = filler["epoch0channels"]["soma"]["pas"]["i"]["tags"][3] # all recsites
        compare8e = filler["epoch0channels"]["soma"]["hh"]["el"]["tags"][6][-1] # key for recsite
        #
        compare7 = [compare7a, compare7b, compare7c, compare7d, compare7e]
        compare8 = [compare8a, compare8b, compare8c, compare8d, compare8e]
        d = Counter(compare7) != Counter(compare8)
        #
        self.assertEqual( [a, b, c, d], [True, True, True, True] )

    @unittest.skip("reason for skipping")
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

    @unittest.skip("reason for skipping")
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

    @unittest.skip("reason for skipping")
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

    @unittest.skip("reason for skipping")
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

    @unittest.skip("reason for skipping")
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

    @unittest.skip("reason for skipping")
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

    @unittest.skip("reason for skipping")
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

    @unittest.skip("reason for skipping")
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

    @unittest.skip("reason for skipping")
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

    @unittest.skip("reason for skipping")
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
