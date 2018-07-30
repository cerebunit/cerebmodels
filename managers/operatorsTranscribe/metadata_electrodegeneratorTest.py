 #/managers/operatorsTranscribe/metadata_electrodegeneratorTest.py
import unittest

import os
import sys
# import modules for other directories
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
# this is required for
from models.cells.modelDummyTest import DummyCell

from metadata_electrodegenerator import ElectrodeGenerator

class ElectrodeGeneratorTest(unittest.TestCase):

    def setUp(self):
        self.eg = ElectrodeGenerator()
        self.pwd = os.getcwd()
        self.chosenmodel = DummyCell()

    #@unittest.skip("reason for skipping")
    def test_1_cellelectrode_stimulus(self):
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}
        elec = ElectrodeGenerator.cellelectrode_stimulus("soma", stimparameters)
        self.assertEqual( elec["name"], "electrode_IClamp_soma" )

    #@unittest.skip("reason for skipping")
    def test_2_cellelectrode_nostimulus(self):
        elec = ElectrodeGenerator.cellelectrode_nostimulus("axon")
        self.assertEqual( elec["name"], "electrode_axon" )

    #@unittest.skip("reason for skipping")
    def test_3_forcellelectrode_stimulus(self):
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        elecmd = self.eg.forcellelectrode( chosenmodel = self.chosenmodel,
                                           parameters = stimparameters )
        self.assertEqual( elecmd["soma"]["name"]+" and "+elecmd["axon"]["name"],
                          "electrode_IClamp_soma and electrode_IClamp_axon" )

    #@unittest.skip("reason for skipping")
    def test_4_forelectrode_stimulus(self):
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        elecmd = self.eg.forelectrode( chosenmodel = self.chosenmodel,
                                       parameters = stimparameters )
        self.assertEqual( elecmd["soma"]["name"]+" and "+elecmd["axon"]["name"],
                          "electrode_IClamp_soma and electrode_IClamp_axon" )

    #@unittest.skip("reason for skipping")
    def test_5_forelectrode_nostimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        elecmd = self.eg.forelectrode( chosenmodel = self.chosenmodel,
                                       parameters = runtimeparam )
        self.assertEqual( elecmd["soma"]["name"]+" and "+elecmd["axon"]["name"],
                          "electrode_soma and electrode_axon" )

if __name__ == '__main__':
    unittest.main()
