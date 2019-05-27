 #/managers/operatorsTranscribe/metadata_filegeneratorTest.py
import unittest

import platform
import datetime
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

from managers.operatorsTranscribe.metadata_filegenerator import FileGenerator as fg

class FileGeneratoryTest(unittest.TestCase):

    def setUp(self):
        os.chdir(rootwd)
        self.chosenmodel = DummyCell()
        self.simtime = datetime.datetime.now()
        os.chdir(pwd)

    #@unittest.skip("reason for skipping")
    def test_1_forfile_without_model(self):
        self.assertRaises(ValueError, fg.forfile,)

    #@unittest.skip("reason for skipping")
    def test_2_forfile_with_model(self):
        filemd = fg.forfile(chosenmodel = self.chosenmodel, simtime = self.simtime)
        compare1 = [ "no_model_uuid", "anonymous",
                     "raw simulation without running any CerebUnit test",
                     platform.platform(),
                     "no institution was provided" ]
        compare2 = [ filemd["identifier"], filemd["experimenter"],
                     filemd["experiment_description"],
                     filemd["lab"], filemd["institution"] ]
        self.assertEqual( compare2, compare1 )

if __name__ == '__main__':
    unittest.main()
