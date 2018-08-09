# ~/managers/operatorsFiling/pathspawnerTest.py
import unittest
import os
import shutil

from pathspawner import PathSpawner

class PathSpawnerTest(unittest.TestCase):

    def setUp(self):
        self.ps = PathSpawner() #instance for non: static & class methods.
        self.pwd = os.getcwd()

    #@unittest.skip("reason for skipping")
    def test_1_hatch_path_to_nmodl(self):
        mod_path, lib_path = self.ps.hatch_path_to_nmodl(modelscale="cells",
                                                         modelname="XY2000Author")
        self.assertEqual(os.path.dirname(mod_path),
                         os.path.dirname(os.path.dirname(os.path.dirname(lib_path))))

    #@unittest.skip("reason for skipping")
    def test_2_exception_hatch_path_to_nmodl(self):
        self.assertRaises(ValueError, self.ps.hatch_path_to_nmodl, )
 
    #@unittest.skip("reason for skipping")
    def test_3_hatch_path_to_response(self):
        response_path = self.ps.hatch_path_to_response(modelscale="cells",
                                                       modelname="XY2000Author")
        self.assertEqual(
              os.path.dirname(os.path.dirname(os.path.dirname(response_path))),
              self.pwd )

    #@unittest.skip("reason for skipping")
    def test_4_exception_hatch_path_to_response(self):
        self.assertRaises(ValueError, self.ps.hatch_path_to_response, )
 
if __name__ == '__main__':
    unittest.main()
