# ~/managers/operatorsFiling/pathspawnerTest.py
import unittest
import os
import shutil

from pathspawner import PathSpawner

class PathSpawnerTest(unittest.TestCase):

    def setUp(self):
        self.ps = PathSpawner() #instance for non: static & class methods.
        self.pwd = os.getcwd()

    def test_1_hatch_path_to_model(self):
        mod_path, lib_path = self.ps.hatch_path_to_nmodl(modelscale="cells",
                                                         modelname="XY2000Author")
        self.assertEqual(os.path.dirname(mod_path),
                         os.path.dirname(os.path.dirname(os.path.dirname(lib_path))))

    def test_2_exception_hatch_path_to_model(self):
        self.assertRaises(ValueError, self.ps.hatch_path_to_nmodl, )
 
if __name__ == '__main__':
    unittest.main()
