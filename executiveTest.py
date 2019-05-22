# ../executiveTest.py
import unittest
import os
import shutil
import importlib

from executive import ExecutiveControl

from pdb import set_trace as breakpoint

class ExecutiveControlTest(unittest.TestCase):

    def setUp(self):
        self.ec = ExecutiveControl() #instance for non: static & class methods.
        self.pwd = os.getcwd()

    #@unittest.skip("reason for skipping")
    def test_1_list_modelscales(self):
        x = len(self.ec.list_modelscales()) != 0
        self.assertEqual(x, True)

    #@unittest.skip("reason for skipping")
    def test_2_list_models(self):
        dummyscale_path = self.pwd+os.sep+"models"+os.sep+"dummyscale"
        for i in range(3): # create three dummymodels
            os.makedirs(dummyscale_path+os.sep+"dummymodel"+str(i+1))
        self.assertEqual(
            len(self.ec.list_models(modelscale="dummyscale")),
            3)
        shutil.rmtree(dummyscale_path)

    #@unittest.skip("reason for skipping")
    def test_3_choose_model(self):
        # NOTE: this only works if the 'minimal' script
        # ~/models/cells/model2015Masoli.py exists
        # 'minimal' => a class with __init__ method with
        # self.modelname = "PC2015Masoli.py"
        x = self.ec.choose_model( modelscale="cells",
                                  modelname="PC2015Masoli" ) #"DummyTest"
        self.assertEqual( x.modelname, "PC2015Masoli" )

    #@unittest.skip("reason for skipping")
    def test_4_launch_model_NEURON_nostimulus_with_capability(self):
        pickedmodel = self.ec.choose_model( modelscale="cells",
                                            modelname="DummyTest" )
        parameters = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        self.assertEqual( self.ec.launch_model (
                              parameters = parameters,
                              onmodel = pickedmodel,
                              capabilities = {'model': None,
                                              'vtest': None} ),
                          pickedmodel )

    #@unittest.skip("reason for skipping")
    def test_5_launch_model_NEURON_nostimulus_raw(self):
        pickedmodel = self.ec.choose_model( modelscale="cells",
                                            modelname="PC2015Masoli" )
        parameters = {"dt": 0.1, "celsius": 30, "tstop": 10, "v_init": 65}
        self.assertEqual( self.ec.launch_model (
                              parameters = parameters,
                              onmodel = pickedmodel),
                          pickedmodel )

    #@unittest.skip("reason for skipping")
    def test_6_save_response(self):
        pickedmodel = self.ec.choose_model( modelscale="cells",
                                            modelname="PC2015Masoli" )
        parameters = {"dt": 0.1, "celsius": 30, "tstop": 10, "v_init": 65}
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 5.0, "delay": 1.0},
                                        {"amp": 1.0, "dur": 5.0, "delay": 0.0+5.0} ],
                          "tstop": parameters["tstop"]}
        model = self.ec.launch_model( parameters = parameters, onmodel = pickedmodel,
                                      stimparameters = stimparameters, stimloc = pickedmodel.cell.soma )
        fullname = self.ec.save_response()
        #
        sesstime = str(self.ec.tm.nwbfile.session_start_time).replace(" ", "_")[0:-6]
        filename_shouldbe = self.ec.tm.nwbfile.session_id + "_" + sesstime.replace(":", "-") + ".h5"
        #
        path = os.getcwd() + os.sep + "responses" + os.sep + model.modelscale + os.sep + model.modelname
        shutil.rmtree( path )
        #
        fullname_shouldbe = path + os.sep + filename_shouldbe
        #
        self.assertEqual( fullname, fullname_shouldbe )
        

if __name__ == '__main__':
    unittest.main()
