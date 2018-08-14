# ~#/managers/managerTranscribeTest.py
import unittest

import shutil
import os
import sys
# import modules for other directories
sys.path.append(os.path.dirname(os.getcwd()))
# this is required for
from models.cells.modelDummyTest import DummyCell

from managerTranscribe import TranscribeManager

import numpy
from managers.operatorsFiling.crawler import Crawler
from pynwb import NWBHDF5IO

class TranscribeManagerTest(unittest.TestCase):

    def setUp(self):
        self.pwd = os.getcwd()
        self.chosenmodel = DummyCell()
        self.cr = Crawler()
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        self.runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 200, "v_init": 65}
        self.stimparameters = {"type": ["current", "IClamp"],
                               "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                             {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                               "tstop": self.runtimeparam["tstop"]}
        rec_t = [ t*self.runtimeparam["dt"]
                  for t in range( int( self.runtimeparam["tstop"]/self.runtimeparam["dt"] ) ) ]
        rec_i = numpy.random.rand(1,len(rec_t))[0]
        rec_v = numpy.random.rand(2,len(rec_t))
        self.recordings_stimulus = {"time": rec_t,
                                    "response": {"soma": rec_v[0], "axon": rec_v[1]},
                                    "stimulus": rec_i}
        self.recordings_nostimulus = {"time": rec_t,
                                     "response": {"soma": rec_v[0], "axon": rec_v[1]},
                                     "stimulus": "Model is not stimulated"}

    #@unittest.skip("reason for skipping")
    def test_1_load_metadata_nostimulus(self):
        tm = TranscribeManager()
        tm.load_metadata( chosenmodel = self.chosenmodel,
                          recordings = self.recordings_nostimulus,
                          runtimeparameters = self.runtimeparam )
        compare1 = [ tm.filemd["identifier"], tm.filemd["experimenter"],
                     tm.respmd["soma"]["name"], tm.respmd["axon"]["data"],
                     tm.epochmd["epoch0soma"]["stop_time"] ]
        compare2 = [ "no_model_uuid", "anonymous",
                     "DummyTest_soma", self.recordings_nostimulus["response"]["axon"],
                     tm.epochmd["epoch0axon"]["stop_time"] ]
        self.assertEqual( compare1, compare2 )

    #@unittest.skip("reason for skipping")
    def test_2_compile_nwbfile_stimulus(self):
        tm = TranscribeManager()
        tm.load_metadata( chosenmodel = self.chosenmodel,
                          recordings = self.recordings_nostimulus,
                          runtimeparameters = self.runtimeparam,
                          stimparameters = self.stimparameters )
        tm.compile_nwbfile()
        compare1 = [ tm.nwbfile.epochs.epochs.data[0][3].data.data[0][2].data,
                     tm.nwbfile.epochs.epochs.data[1][3].data.data[1][2].timestamps,
                     tm.nwbfile.epochs.epochs.data[2][3].data.data[2][2].unit,
                     tm.nwbfile.epochs.epochs.data[3][3].data.data[3][2].description ]

        compare2 = [ tm.respmd[ tm.nwbfile.epochs.epochs.data[0][2][-4:] ]["data"],
                     tm.respmd[ tm.nwbfile.epochs.epochs.data[1][2][-4:] ]["timestamps"],
                     tm.respmd[ tm.nwbfile.epochs.epochs.data[2][2][-4:] ]["unit"],
                     tm.respmd[ tm.nwbfile.epochs.epochs.data[3][2][-4:] ]["description"] ]
        self.assertEqual( compare1, compare2 )

    #@unittest.skip("reason for skipping")
    def test_3_save_nwbfile_nostimulus(self):
        os.chdir("..") # move up to ~/cerebmodels
        tm = TranscribeManager()
        tm.load_metadata( chosenmodel = self.chosenmodel,
                          recordings = self.recordings_nostimulus,
                          runtimeparameters = self.runtimeparam )
        tm.compile_nwbfile()
        tm.save_nwbfile()
        #
        x = self.cr.show_files(dir_names=['responses', self.chosenmodel.modelscale,
                                          self.chosenmodel.modelname])
        #print x
        for key in x.keys():
            compare1 = key
        #print compare1
        #
        sesstime = str(tm.nwbfile.session_start_time).replace(" ", "_")[0:-6]
        compare2 = tm.nwbfile.session_id + "_" + sesstime.replace(":", "-") + ".h5"
        #print compare2
        #
        path = os.getcwd() + os.sep + "responses" + os.sep + self.chosenmodel.modelscale + os.sep + self.chosenmodel.modelname
        shutil.rmtree( path )
        os.chdir(self.pwd) # reset to the location of this managerTranscriberTest.py
        self.assertEqual( compare1, compare2 )

    #@unittest.skip("reason for skipping")
    def test_4_save_nwbfile_stimulus(self):
        os.chdir("..") # move up to ~/cerebmodels
        tm = TranscribeManager()
        tm.load_metadata( chosenmodel = self.chosenmodel,
                          recordings = self.recordings_stimulus,
                          runtimeparameters = self.runtimeparam,
                          stimparameters = self.stimparameters )
        tm.compile_nwbfile()
        tm.save_nwbfile()
        #
        x = self.cr.show_files(dir_names=['responses', self.chosenmodel.modelscale,
                                          self.chosenmodel.modelname])
        #
        for key in x.keys():
            k = key
        #
        io = NWBHDF5IO(x[k])
        nwbfile = io.read()
        stimulus = nwbfile.get_stimulus(self.chosenmodel.modelname+"_stimulus")
        a = all(boolean == True for boolean in
                                (stimulus.data.value == self.recordings_stimulus['stimulus']))
        b = all(boolean == False for boolean in
                                (stimulus.timestamps.value == self.recordings_stimulus['stimulus']))
        self.assertTrue( a and b is True)
        io.close()
        #
        path = os.getcwd() + os.sep + "responses" + os.sep + self.chosenmodel.modelscale + os.sep + self.chosenmodel.modelname
        shutil.rmtree( path )
        os.chdir(self.pwd) # reset to the location of this managerTranscriberTest.py

if __name__ == '__main__':
    unittest.main()
