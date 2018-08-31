# ../managers/managerFilingTest.py
import unittest
import os
import shutil

import sys
# import modules from other directories
# set to ~/cerebmodels
sys.path.append(os.path.dirname(os.getcwd()))
# this is required for
from models.cells.modelDummyTest import DummyCell
# called in managerAccount.py

from managerFiling import FilingManager as fm

class FilingManagerTest(unittest.TestCase):

    def setUp(self):
        #self.fm = FilingManager() #instance for non: static & class methods.
        self.pwd = os.getcwd()
        self.chosenmodel = DummyCell()

    #@unittest.skip("reason for skipping")
    def test_1_available_modelscales_nomodelscales(self):
        # modelscales are under models/
        # this test is under managers/ Thus mimicking case when there
        # are no modelscales 
        self.assertRaises(ValueError, fm.available_modelscales)

    #@unittest.skip("reason for skipping")
    def test_2_available_modelscales_modelscales_exists(self):
        os.chdir("..") # move up one directory
        x = len(fm.available_modelscales()) != 0
        self.assertEqual(x, True)
        os.chdir(self.pwd) # come back to where this .py resides

    #@unittest.skip("reason for skipping")
    def test_3_modelscale_inventory_nomodelscales(self):
        self.assertRaises(ValueError, fm.modelscale_inventory,
                          model_scale="molecules")

    #@unittest.skip("reason for skipping")
    def test_4_modelscale_inventory_nomodels(self):
        #os.chdir("..") # move up one directory
        os.mkdir(self.pwd+os.sep+"cells")
        self.assertRaises(ValueError, fm.modelscale_inventory,
                          model_scale="cells")
        os.rmdir("cells")
        #os.chdir(self.pwd) # come back to where this .py resides

    #@unittest.skip("reason for skipping")
    def test_5_modelscale_inventory_model_exists(self):
        os.chdir("..") # move up one directory
        dummyscale_path = os.getcwd()+os.sep+"models"+os.sep+"dummyscale"
        for i in range(3): # create three dummymodels
            os.makedirs(dummyscale_path+os.sep+"dummymodel"+str(i+1))
        self.assertEqual( len(fm.modelscale_inventory(model_scale="dummyscale")),
                          3 )
        shutil.rmtree(dummyscale_path)           
        os.chdir(self.pwd) # come back to where this .py resides
 
    #@unittest.skip("reason for skipping")
    def test_6_responsepath_check_create_argumenterror(self):
        self.assertRaises(ValueError,
                          fm.responsepath_check_create,
                          list_dir_names=['cells', 'DummyTest'])
 
    #@unittest.skip("reason for skipping")
    def test_7_get_responsepath_check_create(self):
        os.chdir("..") # move up one directory to ~/cerebmodels
        path = fm.get_responsepath_check_create(
                                    ['responses', 'cells', 'DummyTest'] )
        self.assertEqual( path,
             os.getcwd() + os.sep + 'responses' + os.sep + 'cells' + os.sep + 'DummyTest' )
        shutil.rmtree( os.path.dirname(os.path.dirname(path)) )
        os.chdir(self.pwd) # come back to where this .py resides

    #@unittest.skip("reason for skipping")
    def test_8_responsepath_check_create(self):
        # test similar to test_7_get_responsepath_check_create
        os.chdir("..") # move up one directory to ~/cerebmodels
        path = fm.responsepath_check_create(
                            list_dir_names=['responses', 'cells', 'DummyTest'])
        self.assertEqual( path,
             os.getcwd() + os.sep + 'responses' + os.sep + 'cells' + os.sep + 'DummyTest' )
        shutil.rmtree( os.path.dirname(os.path.dirname(path)) )
        os.chdir(self.pwd) # come back to where this .py resides
 
    #@unittest.skip("reason for skipping")
    def test_9_responsepath_check_create_chosenmodel(self):
        os.chdir("..") # move up one directory to ~/cerebmodels
        path = fm.responsepath_check_create(chosenmodel=self.chosenmodel)
        self.assertEqual( path,
             os.getcwd() + os.sep + 'responses' + os.sep + 'cells' + os.sep + 'DummyTest' )
        shutil.rmtree( os.path.dirname(os.path.dirname(path)) )
        os.chdir(self.pwd) # come back to where this .py resides
        shutil.rmtree("x86_64") # remove created dir ~/cerebmodels/managers/x86_64
 
if __name__ == '__main__':
    unittest.main()
