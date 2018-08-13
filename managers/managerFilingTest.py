# ../managers/managerFilingTest.py
import unittest
import os
import shutil

import sys
# import modules from other directories
# set to ~/cerebmodels
sys.path.append(os.path.dirname(os.getcwd()))
# this is required for
# from managers.operatorsFiling.crawler import Crawler
# called in managerAccount.py

from managerFiling import FilingManager

class FilingManagerTest(unittest.TestCase):

    def setUp(self):
        self.fm = FilingManager() #instance for non: static & class methods.
        self.pwd = os.getcwd()

    #@unittest.skip("reason for skipping")
    def test_1_available_modelscales_nomodelscales(self):
        # modelscales are under models/
        # this test is under managers/ Thus mimicking case when there
        # are no modelscales 
        self.assertRaises(ValueError, self.fm.available_modelscales)

    #@unittest.skip("reason for skipping")
    def test_2_available_modelscales_modelscales_exists(self):
        os.chdir("..") # move up one directory
        x = len(self.fm.available_modelscales()) != 0
        self.assertEqual(x, True)
        os.chdir(self.pwd) # come back to where this .py resides

    #@unittest.skip("reason for skipping")
    def test_3_modelscale_inventory_nomodelscales(self):
        self.assertRaises(ValueError, self.fm.modelscale_inventory,
                          model_scale="molecules")

    #@unittest.skip("reason for skipping")
    def test_4_modelscale_inventory_nomodels(self):
        #os.chdir("..") # move up one directory
        os.mkdir(self.pwd+os.sep+"cells")
        self.assertRaises(ValueError, self.fm.modelscale_inventory,
                          model_scale="cells")
        os.rmdir("cells")
        #os.chdir(self.pwd) # come back to where this .py resides

    #@unittest.skip("reason for skipping")
    def test_5_modelscale_inventory_model_exists(self):
        os.chdir("..") # move up one directory
        dummyscale_path = os.getcwd()+os.sep+"models"+os.sep+"dummyscale"
        for i in range(3): # create three dummymodels
            os.makedirs(dummyscale_path+os.sep+"dummymodel"+str(i+1))
        self.assertEqual(
            len(self.fm.modelscale_inventory(model_scale="dummyscale")),
            3)
        shutil.rmtree(dummyscale_path)           
        os.chdir(self.pwd) # come back to where this .py resides
 
if __name__ == '__main__':
    unittest.main()
