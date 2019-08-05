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

from collections import Counter

class TranscribeManagerTest(unittest.TestCase):

    def setUp(self):
        os.chdir(rootwd)
        self.chosenmodel = DummyCell()
        self.simtime = datetime.datetime.now()
        os.chdir(pwd)
        # self.chosenmodel.regions ->
        # {"soma": ["v", "i_cap"], "axon": ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        # No stimulus
        self.no_runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        self.no_rec_t = [ t*self.no_runtimeparam["dt"] for t in
                     range( int( self.no_runtimeparam["tstop"]/self.no_runtimeparam["dt"] ) ) ]
        self.no_rec_resp = numpy.random.rand(7,len(self.no_rec_t))
        self.no_rec_stim = "Model is not stimulated" # response["stimulus"]
        #self.no_stimtype = None # stimparameters["type"] = ["current", "IClamp"]
        self.no_recordings = {"time": self.no_rec_t,
           "response": {"soma": [self.no_rec_resp[0], self.no_rec_resp[1]],
                        "axon": [ self.no_rec_resp[2] ],
           "channels": {"soma": {"hh": [self.no_rec_resp[3], self.no_rec_resp[4]],
                                 "pas":[ self.no_rec_resp[5] ]},
                        "axon": {"pas":[ self.no_rec_resp[3] ]}}},
           "stimulus": "Model is not stimulated"}
        #self.no_respmd = tg.forrecording( chosenmodel = self.chosenmodel,
        #                                  recordings = self.no_recordings,
        #                                  runtimeparameters = self.no_runtimeparam )
        #self.no_epochmd = eg.epochcontainer( chosenmodel = self.chosenmodel,
        #                                     parameters = self.no_runtimeparam )
        # IClamp
        self.ic_runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        self.ic_stimparameters = {"type": ["current", "IClamp"],
                              "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                            {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                              "tstop": self.ic_runtimeparam["tstop"]}
        self.ic_rec_t = [ t*self.ic_runtimeparam["dt"] for t in
                  range( int( self.ic_runtimeparam["tstop"]/self.ic_runtimeparam["dt"] ) ) ]
        self.ic_rec_stim = numpy.random.rand(1,len(self.ic_rec_t))[0]
        self.ic_rec_resp = numpy.random.rand(7,len(self.ic_rec_t))
        self.ic_recordings = {"time": self.ic_rec_t,
           "response": {"soma": [self.ic_rec_resp[0], self.ic_rec_resp[1]],
                        "axon": [ self.ic_rec_resp[2] ],
           "channels": {"soma": {"hh": [self.ic_rec_resp[3], self.ic_rec_resp[4]],
                                 "pas":[ self.ic_rec_resp[5] ]},
                        "axon": {"pas":[ self.ic_rec_resp[6] ]}}},
           "stimulus": self.ic_rec_stim}
        #self.ic_respmd = tg.forrecording( chosenmodel = self.chosenmodel,
        #                                  recordings = self.ic_recordings,
        #                                  runtimeparameters = self.ic_runtimeparam,
        #                                  stimparameters = self.ic_stimparameters )
        #self.ic_epochmd = eg.epochcontainer( chosenmodel = self.chosenmodel,
        #                                     parameters = self.ic_stimparameters )
        # Voltage clamp
        self.sec_runtimeparam = {"dt": 0.1, "celsius": 30, "tstop": 35, "v_init": 65}
        self.sec_stimparameters = {"type": ["voltage", "SEClamp"],
                               "stimlist": [ {'amp1': 0., 'dur1': 10.0},
                                        {'amp2': -70.0, 'dur2': 20.0} ],
                               "tstop": self.sec_runtimeparam["tstop"]}
        self.sec_rec_t = [ t*self.sec_runtimeparam["dt"] for t in
                   range( int( self.sec_runtimeparam["tstop"]/self.sec_runtimeparam["dt"] ) ) ]
        self.sec_rec_stim = numpy.random.rand(1,len(self.sec_rec_t))[0]
        self.sec_rec_resp = numpy.random.rand(7,len(self.sec_rec_t))
        self.sec_recordings = {"time": self.sec_rec_t,
           "response": {"soma": [self.sec_rec_resp[0], self.sec_rec_resp[1]],
                        "axon": [ self.sec_rec_resp[2] ],
           "channels": {"soma": {"hh": [self.sec_rec_resp[3], self.sec_rec_resp[4]],
                                 "pas":[ self.sec_rec_resp[5] ]},
                        "axon": {"pas":[ self.sec_rec_resp[3] ]}}},
           "stimulus": self.sec_rec_stim}
        #self.sec_respmd = tg.forrecording( chosenmodel = self.chosenmodel,
        #                                   recordings = self.sec_recordings,
        #                                   runtimeparameters = self.sec_runtimeparam,
        #                                   stimparameters = self.sec_stimparameters )
        #self.sec_epochmd = eg.epochcontainer( chosenmodel = self.chosenmodel,
        #                                      parameters = self.sec_stimparameters )
        # parameters for generating NWBFile
        #now = datetime.datetime.now()
        #self.file_metadata = {
        #        "source": "Where is the data from?, i.e, platform",
        #        "session_description": "How was the data generated?, i.e, simulation of __",
        #        "identifier": "a unique modelID, uuid",
        #        "session_start_time": datetime(now.year, now.month, now.day, now.hour, now.minute,
        #                                       now.second, now.microsecond, tzinfo=tzlocal()),
        #        "experimenter": "name of the experimenter/username",
        #        "experiment_description": "described experiment/test description",
        #        "session_id": str(hash(str(uuid.uuid1()))).replace('-',''),
        #        "lab": "name of the lab",
        #        "institution": "name of the institution" }
        # parameters for generating TimeSeries nwb object
        #self.no_ts_metadata = {

    #@unittest.skip("reason for skipping")
    def test_1_load_metadata_nostimulus(self):
        # self.chosenmodel.regions ->
        # {"soma": ["v", "i_cap"], "axon": ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        tm = TranscribeManager()
        tm.load_metadata( chosenmodel = self.chosenmodel, simtime = self.simtime,
                          recordings = self.no_recordings,
                          runtimeparameters = self.no_runtimeparam )
        compare1 = [ tm.filemd["identifier"], tm.filemd["experimenter"],
                     tm.respmd["soma"][0]["name"],
                     tm.epochmd["epoch0soma"]["v"]["stop_time"] ]
        compare2 = [ "no_model_uuid", "anonymous",
                     "DummyTest_soma_v",
                     tm.epochmd["epoch0axon"]["v"]["stop_time"] ]
        a = Counter( compare1 ) == Counter( compare2 )
        b = all(boolean == True for boolean in tm.respmd["axon"][0]["data"] ==
                                               self.no_recordings["response"]["axon"][0])
        self.assertTrue( a and b is True )

    @unittest.skip("reason for skipping")
    def test_2_compile_nwbfile_currentstimulus(self):
        tm = TranscribeManager()
        tm.load_metadata( chosenmodel = self.chosenmodel, simtime = self.simtime,
                          recordings = self.recordings_nostimulus,
                          runtimeparameters = self.runtimeparam,
                          stimparameters = self.stimparameters )
        tm.compile_nwbfile()
        #
        compare1 = tm.nwbfile.epochs[0][3][0] # 4_no_of_epochs
        compare2 = tm.nwbfile.epochs[1][3][0] # 4_no_of_epochs
        #
        compare3 = tm.nwbfile.epochs[0][1] # start_time
        compare4 = tm.nwbfile.epochs[1][1] # start_time
        #
        compare5 = tm.nwbfile.epochs[0][3][1] # epochID
        compare6 = tm.nwbfile.epochs[1][3][1] # epochID
        #
        a = compare1 == compare2
        b = compare3 != compare4
        c = compaer5 != compare6
        self.assertTrue( a and b and c is True )

    #@unittest.skip("reason for skipping")
    def test_3_save_nwbfile_nostimulus(self):
        os.chdir("..") # move up to ~/cerebmodels
        tm = TranscribeManager()
        tm.load_metadata( chosenmodel = self.chosenmodel, simtime = self.simtime,
                          recordings = self.no_recordings,
                          runtimeparameters = self.no_runtimeparam )
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
    def test_4_save_nwbfile_voltagestimulus(self):
        os.chdir("..") # move up to ~/cerebmodels
        tm = TranscribeManager()
        tm.load_metadata( chosenmodel = self.chosenmodel, simtime = self.simtime,
                          recordings = self.sec_recordings,
                          runtimeparameters = self.sec_runtimeparam,
                          stimparameters = self.sec_stimparameters )
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
                                numpy.array(stimulus.data) == self.sec_recordings['stimulus'])
        b = all(boolean == False for boolean in
                                numpy.array(stimulus.timestamps) == self.sec_recordings['time'])
        self.assertTrue( a is True and b is False)
        io.close()
        #
        path = os.getcwd() + os.sep + "responses" + os.sep + self.chosenmodel.modelscale + os.sep + self.chosenmodel.modelname
        shutil.rmtree( path )
        os.chdir(pwd) # reset to the location of this managerTranscriberTest.py

if __name__ == '__main__':
    unittest.main()
