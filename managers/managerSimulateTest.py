# ../managers/managerAccountTest.py
import unittest
import os
import shutil

from managerSimulate import AccountManager

class AccountManagerTest(unittest.TestCase):

    def setUp(self):
        self.am = AccountManager() #instance for non: static & class methods.
        self.pwd = os.getcwd()

    def test_1_available_modelscales_nomodelscales(self):
        # modelscales are under models/
        # this test is under managers/ Thus mimicking case when there
        # are no modelscales 
        self.assertRaises(ValueError, self.am.available_modelscales)

    def test_2_available_modelscales_modelscales_exists(self):
        os.chdir("..") # move up one directory
        x = len(self.am.available_modelscales()) != 0
        self.assertEqual(x, True)
        os.chdir(self.pwd) # come back to where this .py resides

    def test_3_modelscale_inventory_nomodelscales(self):
        self.assertRaises(ValueError, self.am.modelscale_inventory,
                          model_scale="molecules")

    def test_4_modelscale_inventory_nomodels(self):
        os.chdir("..") # move up one directory
        self.assertRaises(ValueError, self.am.modelscale_inventory,
                          model_scale="cell")
        os.chdir(self.pwd) # come back to where this .py resides

    def test_5_modelscale_inventory_model_exists(self):
        os.chdir("..") # move up one directory
        dummyscale_path = os.getcwd()+os.sep+"models"+os.sep+"dummyscale"
        for i in range(3): # create three dummymodels
            os.makedirs(dummyscale_path+os.sep+"dummymodel"+str(i+1))
        self.assertEqual(
            len(self.am.modelscale_inventory(model_scale="dummyscale")),
            3)
        shutil.rmtree(dummyscale_path)           
        os.chdir(self.pwd) # come back to where this .py resides
 
if __name__ == '__main__':
    unittest.main()
