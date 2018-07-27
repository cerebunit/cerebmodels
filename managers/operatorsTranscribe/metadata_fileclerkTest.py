 #/managers/operatorsTranscribe/metadata_fileclerkTest.py
import unittest

import os
import sys
# import modules for other directories
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
# this is required for
from models.cells.modelDummyTest import DummyCell

from metadata_fileclerk import FileClerk

class MetadataClerkTest(unittest.TestCase):

    def setUp(self):
        self.fc = FileClerk()
        self.pwd = os.getcwd()
        self.chosenmodel = DummyCell()

    #@unittest.skip("reason for skipping")
    def test_1_forfile_without_model(self):
        self.assertRaises(ValueError, self.fc.forfile,)

    #@unittest.skip("reason for skipping")
    def test_2_forfile_with_model(self):
        filemd = self.fc.forfile(chosenmodel = self.chosenmodel)
        compare1 = [ "no_model_uuid", "anonymous",
                     "raw simulation without running any CerebUnit test",
                     "no lab name was provided",
                     "no institution was provided" ]
        compare2 = [ filemd["identifier"], filemd["experimenter"],
                     filemd["experiment_description"],
                     filemd["lab"], filemd["institution"] ]
        self.assertEqual( compare2, compare1 )

if __name__ == '__main__':
    unittest.main()
