# ~#/managers/managerTranscribeTest.py
import unittest

import platform
import datetime
import shutil
import os
import sys
# import modules for other directories
sys.path.append(os.path.dirname(os.getcwd()))
# this is required for

pwd = os.getcwd()
os.chdir("..") # this moves you up to ~/cerebmodels
rootwd = os.getcwd()
from models.cells.modelDummyTest import DummyCell
os.chdir(pwd)

from managers.transcribe import TranscribeManager

import numpy
from managers.operatorsTranscribe.fabricator import Fabricator as fab
from managers.operatorsFiling.crawler import Crawler as cr
from pynwb import NWBHDF5IO

from pdb import set_trace as breakpoint

class TranscribeManagerTest(unittest.TestCase):

    def setUp(self):
        os.chdir(rootwd)
        self.chosenmodel = DummyCell()
        self.simtime = datetime.datetime.now()
        os.chdir(pwd)
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        self.runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 200, "v_init": 65}
        self.stimparameters = {"type": ["current", "IClamp"],
                               "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                             {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                               "tstop": self.runtimeparam["tstop"]}
        rec_t = [ t*self.runtimeparam["dt"]
                  for t in range( 1 + int( self.runtimeparam["tstop"]/self.runtimeparam["dt"] ) ) ]
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
        tm.load_metadata( chosenmodel = self.chosenmodel, simtime = self.simtime,
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
        tm.load_metadata( chosenmodel = self.chosenmodel, simtime = self.simtime,
                          recordings = self.recordings_nostimulus,
                          runtimeparameters = self.runtimeparam,
                          stimparameters = self.stimparameters )
        tm.compile_nwbfile()
        #
        region_0 = tm.nwbfile.epochs[0][3][2]
        region_1 = tm.nwbfile.epochs[1][3][2]
        region_2 = tm.nwbfile.epochs[2][3][2]
        region_3 = tm.nwbfile.epochs[3][3][2]
        #
        a = all( boolean == True for boolean in
                 tm.nwbfile.epochs[0][4][0][2].data #== ts_md_0 )
                 == tm.respmd[region_0]["data"] )
        b = all( boolean == True for boolean in
                 tm.nwbfile.epochs[1][4][0][2].timestamps #== ts_md_1 )
                 == tm.respmd[region_1]["timestamps"] )
        c = all( boolean == True for boolean in
                 tm.nwbfile.epochs[2][4][0][2].timestamps #== ts_md_2 )
                 == tm.respmd[region_2]["timestamps"] )
        d = all( boolean == True for boolean in
                 tm.nwbfile.epochs[3][4][0][2].data #== ts_md_3 )
                 == tm.respmd[region_3]["data"] )
        compare1 = [ a, b, c, d,
                     tm.nwbfile.epochs[0][4][0][2].unit,
                     tm.nwbfile.epochs[3][4][0][2].description ]
        compare2 = [ True, True, True, True,
                     tm.respmd[region_0]["unit"], tm.respmd[region_3]["description"] ]
        self.assertEqual( compare1, compare2 )

    #@unittest.skip("reason for skipping")
    def test_3_save_nwbfile_nostimulus(self):
        os.chdir("..") # move up to ~/cerebmodels
        tm = TranscribeManager()
        tm.load_metadata( chosenmodel = self.chosenmodel, simtime = self.simtime,
                          recordings = self.recordings_nostimulus,
                          runtimeparameters = self.runtimeparam )
        tm.compile_nwbfile()
        fullname = tm.save_nwbfile()
        #
        sesstime = str(tm.nwbfile.session_start_time).replace(" ", "_")[0:-6]
        filename_shouldbe = tm.nwbfile.session_id + "_" + sesstime.replace(":", "-") + ".h5"
        #
        path = os.getcwd() + os.sep + "responses" + os.sep + self.chosenmodel.modelscale + os.sep + self.chosenmodel.modelname
        shutil.rmtree( path )
        os.chdir(pwd) # reset to the location of this managerTranscriberTest.py
        #
        fullname_shouldbe = path + os.sep + filename_shouldbe
        #print(fullname_shouldbe)
        #breakpoint()
        self.assertEqual( fullname, fullname_shouldbe )

    #@unittest.skip("reason for skipping")
    def test_4_save_nwbfile_stimulus(self):
        os.chdir("..") # move up to ~/cerebmodels
        tm = TranscribeManager()
        tm.load_metadata( chosenmodel = self.chosenmodel, simtime = self.simtime,
                          recordings = self.recordings_stimulus,
                          runtimeparameters = self.runtimeparam,
                          stimparameters = self.stimparameters )
        tm.compile_nwbfile()
        fullname = tm.save_nwbfile()
        #
        io = NWBHDF5IO(fullname, mode="r")
        nwbfile = io.read()
        stimulus = nwbfile.get_stimulus(self.chosenmodel.modelname+"_stimulus")
        #
        #print(type(stimulus.data))                        # <class 'h5py._hl.dataset.Dataset'>
        #print(type(self.recordings_stimulus['stimulus'])) # <type 'numpy.ndarray'>
        #print(len(stimulus.data))
        #print(len(numpy.array(stimulus.data)))
        #breakpoint()
        #
        a = all(boolean == True for boolean in
                                numpy.array(stimulus.data) == self.recordings_stimulus['stimulus'])
        b = all(boolean == False for boolean in
                                numpy.array(stimulus.timestamps) == self.recordings_stimulus['time'])
        self.assertTrue( a is True and b is False)
        io.close()
        #
        path = os.getcwd() + os.sep + "responses" + os.sep + self.chosenmodel.modelscale + os.sep + self.chosenmodel.modelname
        shutil.rmtree( path )
        os.chdir(pwd) # reset to the location of this managerTranscriberTest.py

if __name__ == '__main__':
    unittest.main()
