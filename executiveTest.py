# ../executiveTest.py
import unittest
import os
import shutil

from executive import ExecutiveControl

class ExecutiveControlTest(unittest.TestCase):

    def setUp(self):
        self.ec = ExecutiveControl() #instance for non: static & class methods.
        self.pwd = os.getcwd()

    def test_1_list_modelscales(self):
        x = len(self.ec.list_modelscales()) != 0
        self.assertEqual(x, True)

    def test_2_list_models(self):
        dummyscale_path = self.pwd+os.sep+"models"+os.sep+"dummyscale"
        for i in range(3): # create three dummymodels
            os.makedirs(dummyscale_path+os.sep+"dummymodel"+str(i+1))
        self.assertEqual(
            len(self.ec.list_models(modelscale="dummyscale")),
            3)
        shutil.rmtree(dummyscale_path)

    def test_3_choose_model(self):
        # NOTE: this only works if the 'minimal' script
        # ~/models/cells/model2015Masoli.py exists
        # 'minimal' => a class with __init__ method with
        # self.modelname = "PC2015Masoli.py"
        x = self.ec.choose_model( modelscale="cells",
                                  modelname="PC2015Masoli" )
        self.assertEqual( x().modelname, "PC2015Masoli" )
 
if __name__ == '__main__':
    unittest.main()
