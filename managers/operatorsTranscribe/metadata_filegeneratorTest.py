 #/managers/operatorsTranscribe/metadata_filegeneratorTest.py
import unittest

import os
import sys
# import modules for other directories
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
# this is required for
from models.cells.modelDummyTest import DummyCell

from metadata_filegenerator import FileGenerator

class FileGeneratoryTest(unittest.TestCase):

    def setUp(self):
        self.fg = FileGenerator()
        self.pwd = os.getcwd()
        self.chosenmodel = DummyCell()

    #@unittest.skip("reason for skipping")
    def test_1_forfile_without_model(self):
        self.assertRaises(ValueError, self.fg.forfile,)

    #@unittest.skip("reason for skipping")
    def test_2_forfile_with_model(self):
        filemd = self.fg.forfile(chosenmodel = self.chosenmodel)
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
