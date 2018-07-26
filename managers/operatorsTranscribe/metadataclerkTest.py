 #/managers/operatorsTranscribe/metadataclerkTest.py
import unittest

import os
import sys
# import modules for other directories
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
# this is required for
from models.cells.modelDummyTest import DummyCell

from metadataclerk import MetadataClerk

class MetadataClerkTest(unittest.TestCase):

    def setUp(self):
        self.md = MetadataClerk()
        self.pwd = os.getcwd()
        self.chosenmodel = DummyCell()

    #@unittest.skip("reason for skipping")
    def test_1_forfile_without_model(self):
        self.assertRaises(ValueError, self.md.forfile,)

    #@unittest.skip("reason for skipping")
    def test_1_forfile(self):
        filemd = self.md.forfile(chosenmodel = self.chosenmodel)
        compare1 = [ "no_model_uuid", "anonymous",
                     "raw simulation without running any CerebUnit test",
                     "no lab name was provided",
                     "no institution was provided" ]
        compare2 = [ filemd["identifier"], filemd["experimenter"],
                     filemd["experiment_description"],
                     filemd["lab"], filemd["institution"] ]
        self.assertEqual( compare2, compare1 )

    #@unittest.skip("reason for skipping")
    def test_2_compute_totalepochs_per_cellregion_without_stimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        self.assertEqual( MetadataClerk.compute_totalepochs_per_cellregion(runtimeparam),
                          1 )

    #@unittest.skip("reason for skipping")
    def test_3_compute_totalepochs_per_cellregion_with_stimulus(self):
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}
        self.assertEqual( MetadataClerk.compute_totalepochs_per_cellregion(stimparameters),
                          1 + len(stimparameters["stimlist"]) )
        
    #@unittest.skip("reason for skipping")
    def test_4_epochcontainer_without_stimulus(self):
        no_of_regions = len(list(self.chosenmodel.regions.keys()))
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        filler = self.md.epochcontainer(self.chosenmodel, runtimeparam)
        compare2 = len(filler) - 1 # exclude the key 'epoch_tags'
        no_of_epochs_per_region = 1
        compare1 = no_of_regions * no_of_epochs_per_region 
        self.assertEqual( compare2, compare1 )

    #@unittest.skip("reason for skipping")
    def test_5_epochcontainer_with_stimulus(self):
        no_of_regions = len(list(self.chosenmodel.regions.keys()))
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}
        filler = self.md.epochcontainer(self.chosenmodel, stimparameters)
        compare2 = len(filler) - 1 # exclude the key 'epoch_tags'
        no_of_epochs_per_region = 1 + len(stimparameters["stimlist"])
        compare1 = no_of_regions * no_of_epochs_per_region 
        self.assertEqual( compare2, compare1 )

    #@unittest.skip("reason for skipping")
    def test_4_an_epoch_prestimulus(self):
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}
        epoch_value = MetadataClerk.an_epoch( 0, "soma", stimparameters)
        compare2 = epoch_value["start"] + epoch_value["stop"]
        compare1 = 0.0 + stimparameters["stimlist"][0]["delay"]
        self.assertEqual( compare2, compare1 )

    #@unittest.skip("reason for skipping")
    def test_5_an_epoch_stimulus(self):
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}
        epoch_value = MetadataClerk.an_epoch( 1, "axon", stimparameters)
        compare2 = epoch_value["description"]
        compare1 = "IClamp stimulation of model with amplitude = " + \
                       str(stimparameters["stimlist"][0]["amp"]) + " nA"
        self.assertEqual( compare2, compare1 )

    #@unittest.skip("reason for skipping")
    def test_6_forepoch_without_stimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        epochmd = self.md.forepoch( chosenmodel = self.chosenmodel,
                                    parameters = runtimeparam )
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        no_of_stimulus_epochs_per_region = 0 
        compare2 = epochmd["epoch"+str(no_of_stimulus_epochs_per_region)+"soma"]["stop"]
        compare1 = epochmd["epoch"+str(no_of_stimulus_epochs_per_region)+"axon"]["stop"]
        self.assertEqual( compare2, compare1 )

    #@unittest.skip("reason for skipping")
    def test_7_forepoch_with_stimulus(self):
        stimparameters = {"type": ["current", "IRamp"],
           "stimlist": [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0, "delay": 5.0},
                         {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0, "delay": 10.0},
                         {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0, "delay": 15.0},
                         {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0, "delay": 20.0} ]}
        epochmd = self.md.forepoch( chosenmodel = self.chosenmodel,
                                    parameters = stimparameters )
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        no_of_stimulus_epochs_per_region = len(stimparameters["stimlist"])
        compare2 = epochmd["epoch"+str(no_of_stimulus_epochs_per_region)+"soma"]["stop"]
        compare1 = epochmd["epoch"+str(no_of_stimulus_epochs_per_region)+"axon"]["stop"]
        self.assertEqual( compare2, compare1 )

    #@unittest.skip("reason for skipping")
    def test_8_cellelectrode_stimulus(self):
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}
        elec = MetadataClerk.cellelectrode_stimulus("soma", stimparameters)
        self.assertEqual( elec["name"], "electrode_IClamp_soma" )

    #@unittest.skip("reason for skipping")
    def test_9_cellelectrode_nostimulus(self):
        elec = MetadataClerk.cellelectrode_nostimulus("axon")
        self.assertEqual( elec["name"], "electrode_axon" )

    #@unittest.skip("reason for skipping")
    def test_10_forelectrode_stimulus(self):
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        elecmd = self.md.forelectrode( chosenmodel = self.chosenmodel,
                                       parameters = stimparameters )
        self.assertEqual( elecmd["soma"]["name"]+" and "+elecmd["axon"]["name"],
                          "electrode_IClamp_soma and electrode_IClamp_axon" )

    #@unittest.skip("reason for skipping")
    def test_11_forelectrode_nostimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        elecmd = self.md.forelectrode( chosenmodel = self.chosenmodel,
                                       parameters = runtimeparam )
        self.assertEqual( elecmd["soma"]["name"]+" and "+elecmd["axon"]["name"],
                          "electrode_soma and electrode_axon" )


if __name__ == '__main__':
    unittest.main()
