# ../managers/managerSimulateTest.py
import unittest
import os
import shutil

from managerSimulate import SimManager

class SimManagerTest(unittest.TestCase):

    def setUp(self):
        self.sm = SimManager() #instance for non: static & class methods.
        self.pwd = os.getcwd()

    def test_1_available_modelscales_nomodelscales(self):
        # modelscales are under models/
        # this test is under managers/ Thus mimicking case when there
        # are no modelscales 
        self.assertRaises(ValueError, self.sm.available_modelscales)

    def test_2_available_modelscales_modelscales_exists(self):
        os.chdir("..") # move up one directory
        x = len(self.sm.available_modelscales()) != 0
        self.assertEqual(x, True)
        os.chdir(self.pwd) # come back to where this .py resides
 
if __name__ == '__main__':
    unittest.main()
