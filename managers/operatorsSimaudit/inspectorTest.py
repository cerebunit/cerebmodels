# ~/managers/operatorsSimaudit/inspectorTest.py
import unittest
import os
import shutil
import sys

from inspector import SimInspector

class SimInspectorTest(unittest.TestCase):

    def setUp(self):
        self.si = SimInspector() # instance for non: static & class methods
        self.pwd = os.getcwd()

    def test_1_lock_and_load_nmodl_compile_libnrnmech(self):
        modelscale = "cells"
        modelname = "PC2015Masoli"
        os.chdir("..") # this moves you up to ~/managers
        os.chdir("..") # you are now in root
        compile_path = os.getcwd() + os.sep + "models" + os.sep + modelscale + os.sep + modelname
        try:
            # try deleting previous compiled files
            shutil.rmtree(compile_path + os.sep + "x86_64")
        except:
            pass
        self.assertEqual(self.si.lock_and_load_nmodl(modelscale=modelscale,
                                                     modelname=modelname),
                         "nmodl has just been compiled")
        os.chdir(self.pwd) # reset to the location of this inspectorTest.py

    def test_2_lock_and_load_nmodl_alreadycompiled(self):
        modelscale = "cells"
        modelname = "PC2015Masoli"
        os.chdir("..") # this moves you up to ~/managers
        os.chdir("..") # you are now in root
        compile_path = os.getcwd() + os.sep + "models" + os.sep + modelscale + os.sep + modelname
        self.assertEqual(self.si.lock_and_load_nmodl(modelscale=modelscale,
                                                     modelname=modelname),
                         "nmodl was already compiled")
        os.chdir(self.pwd) # reset to the location of this inspectorTest.py

if __name__ == '__main__':
    unittest.main()
