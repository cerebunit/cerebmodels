 #/managers/operatorsTranscribe/metadata_timeseriesgeneratorTest.py
import unittest

import os
import sys
# import modules for other directories
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
# this is required for

pwd = os.getcwd()
os.chdir("..") # this moves you up to ~/managers
os.chdir("..") # you are now in parent /cerebmodels
rootwd = os.getcwd()
from models.cells.modelDummyTest import DummyCell
os.chdir(pwd)

from metadata_timeseriesgenerator import TimeseriesGenerator as tg

import numpy

class TimeseriesGeneratorTest(unittest.TestCase):

    def setUp(self):
        #self.tg = TimeseriesGenerator()
        #self.pwd = os.getcwd()
        os.chdir(rootwd)
        self.chosenmodel = DummyCell()
        os.chdir(pwd)
        #
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0,
        #                             'channels': {'soma': ['pas'], 'axon': ['pas']}}
        self.regionkeylist = ["soma", "axon", "channels_soma_pas", "channels_axon_pas"]
        # No stimulus
        self.no_runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        self.no_rec_t = [ t*self.no_runtimeparam["dt"] for t in
                     range( int( self.no_runtimeparam["tstop"]/self.no_runtimeparam["dt"] ) ) ]
        self.no_rec_resp = numpy.random.rand(4,len(self.no_rec_t))
        self.no_rec_stim = "Model is not stimulated" # response["stimulus"]
        #self.no_stimtype = None # stimparameters["type"] = ["current", "IClamp"]
        self.no_recordings = {"time": self.no_rec_t,
                              "response": {"soma": self.no_rec_resp[0],
                                           "axon": self.no_rec_resp[1],
                                           "channels": {"soma": {"pas": self.no_rec_resp[2]},
                                                        "axon": {"pas": self.no_rec_resp[3]}}},
                              "stimulus": "Model is not stimulated"}
        # IClamp
        self.ic_runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        self.ic_stimparameters = {"type": ["current", "IClamp"],
                              "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                            {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                              "tstop": self.ic_runtimeparam["tstop"]}
        self.ic_rec_t = [ t*self.ic_runtimeparam["dt"] for t in
                  range( int( self.ic_runtimeparam["tstop"]/self.ic_runtimeparam["dt"] ) ) ]
        self.ic_rec_stim = numpy.random.rand(1,len(self.ic_rec_t))[0]
        self.ic_rec_resp = numpy.random.rand(4,len(self.ic_rec_t))
        self.ic_recordings = {"time": self.ic_rec_t,
                              "response": {"soma": self.ic_rec_resp[0],
                                            "axon": self.ic_rec_resp[1],
                                            "channels": {"soma": {"pas": self.ic_rec_resp[2]},
                                                         "axon": {"pas": self.ic_rec_resp[3]}}},
                               "stimulus": self.ic_rec_stim}
        # Voltage clamp
        self.sec_runtimeparam = {"dt": 0.1, "celsius": 30, "tstop": 35, "v_init": 65}
        self.sec_stimparameters = {"type": ["voltage", "SEClamp"],
                               "stimlist": [ {'amp1': 0., 'dur1': 10.0},
                                        {'amp2': -70.0, 'dur2': 20.0} ],
                               "tstop": self.sec_runtimeparam["tstop"]}
        self.sec_rec_t = [ t*self.sec_runtimeparam["dt"] for t in
                   range( int( self.sec_runtimeparam["tstop"]/self.sec_runtimeparam["dt"] ) ) ]
        self.sec_rec_stim = numpy.random.rand(1,len(self.sec_rec_t))[0]
        self.sec_rec_resp = numpy.random.rand(4,len(self.sec_rec_t))
        self.sec_recordings = {"time": self.sec_rec_t,
                               "response": {"soma": self.sec_rec_resp[0],
                                            "axon": self.sec_rec_resp[1],
                                            "channels": {"soma": {"pas": self.sec_rec_resp[2]},
                                                         "axon": {"pas": self.sec_rec_resp[3]}}},
                               "stimulus": self.sec_rec_stim}

    #@unittest.skip("reason for skipping")
    def test_1_cellrecordings_response_nostimulus(self):
        stimtype = None # stimparameters["type"] = ["current", "IClamp"]
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0,
        #                             'channels': {'soma': ['pas'], 'axon': ['pas']}}
        ts_response = tg.cellrecordings_response(self.chosenmodel, "axon", self.no_recordings,
                                                 stimtype, self.no_runtimeparam)
        a = all(boolean == True for boolean in
                                ts_response["data"]==self.no_recordings["response"]["axon"])
        self.assertEqual( [ts_response["name"], a, ts_response["comments"]],
                          ["DummyTest_axon", True, "voltage response without stimulation"] )

    #@unittest.skip("reason for skipping")
    def test_2_cellrecordings_response_currentstimulus(self):
        stimtype = self.ic_stimparameters["type"] #["current", "IClamp"]
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0,
        #                             'channels': {'soma': ['pas'], 'axon': ['pas']}}
        ts_response = tg.cellrecordings_response(self.chosenmodel, "soma", self.ic_recordings,
                                                 stimtype, self.ic_runtimeparam)
        a = all(boolean == True for boolean in
                                ts_response["data"]==self.ic_recordings["response"]["soma"])
        self.assertNotEqual( [ts_response["name"], a, ts_response["comments"]],
                             ["DummyTest_soma", True, "voltage response without stimulation"] )

    #@unittest.skip("reason for skipping")
    def test_3_cellrecordings_response_voltagestimulus(self):
        stimtype = self.sec_stimparameters["type"] #["voltage", "SEClamp"]
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0,
        #                             'channels': {'soma': ['pas'], 'axon': ['pas']}}
        ts_response = tg.cellrecordings_response(self.chosenmodel, "channels_soma_pas",
                                                 self.sec_recordings, stimtype,
                                                 self.sec_runtimeparam)
        #print( len(self.sec_recordings["response"]["channels"]["soma"]["pas"]) )
        #print( len(ts_response["data"]) )
        a = all(boolean == True for boolean in
                                ts_response["data"] ==
                                self.sec_recordings["response"]["channels"]["soma"]["pas"])
        self.assertEqual( [ts_response["name"], a, ts_response["comments"]],
                          ["DummyTest_channels_soma_pas", True, "current response with SEClamp"] )

    #@unittest.skip("reason for skipping")
    def test_4_recordings_cellstimulus_current(self):
        stimtype = self.ic_stimparameters["type"] #["current", "IClamp"]
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0,
        #                             'channels': {'soma': ['pas'], 'axon': ['pas']}}
        ts_stimulus = tg.recordings_cell_stimulus(self.chosenmodel, self.ic_recordings,
                                                 self.ic_runtimeparam, self.ic_stimparameters)
        a = all(boolean == True for boolean in
                                ts_stimulus["data"]==self.ic_recordings["stimulus"])
        self.assertEqual( [ts_stimulus["name"], a, ts_stimulus["comments"]],
                          ["DummyTest_stimulus", True, "current injection, IClamp"] )

    #@unittest.skip("reason for skipping")
    def test_5_recordings_cellstimulus_voltage(self):
        stimtype = self.sec_stimparameters["type"] #["voltage", "SEClamp"]
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0,
        #                             'channels': {'soma': ['pas'], 'axon': ['pas']}}
        ts_stimulus = tg.recordings_cell_stimulus(self.chosenmodel, self.sec_recordings,
                                                 self.sec_runtimeparam, self.sec_stimparameters)
        a = all(boolean == True for boolean in
                                ts_stimulus["data"] == self.sec_recordings["stimulus"])
        self.assertEqual( [ts_stimulus["name"], a, ts_stimulus["comments"]],
                          ["DummyTest_stimulus", True, "voltage injection, SEClamp"] )

    #@unittest.skip("reason for skipping")
    def test_6_forcellrecording_nostimulus(self):
        stimtype = None # stimparameters["type"] = ["current", "IClamp"]
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0,
        #                             'channels': {'soma': ['pas'], 'axon': ['pas']}}
        self.no_recordings["regions"] = self.regionkeylist
        respmd = tg.forcellrecording(chosenmodel = self.chosenmodel,
                                     recordings = self.no_recordings,
                                     runtimeparameters = self.no_runtimeparam)
        a = all(boolean == True for boolean in
                                respmd["axon"]["data"]==self.no_recordings["response"]["axon"])
        self.assertEqual( [respmd["soma"]["name"], respmd["axon"]["name"], a,
                           respmd["soma"]["comments"]],
                          ["DummyTest_soma", "DummyTest_axon", True,
                           "voltage response without stimulation"] )

    #@unittest.skip("reason for skipping")
    def test_7_forcellrecording_stimulus(self):
        stimtype = self.ic_stimparameters["type"] #["current", "IClamp"]
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0,
        #                             'channels': {'soma': ['pas'], 'axon': ['pas']}}
        self.ic_recordings["regions"] = self.regionkeylist
        ts_stimulus = tg.recordings_cell_stimulus(self.chosenmodel, self.ic_recordings,
                                                 self.ic_runtimeparam, self.ic_stimparameters)
        respmd = tg.forcellrecording(chosenmodel = self.chosenmodel,
                                     recordings = self.ic_recordings,
                                     runtimeparameters = self.ic_runtimeparam,
                                     stimparameters = self.ic_stimparameters)
        a = all(boolean == True for boolean in
                                respmd["axon"]["data"]==self.ic_recordings["response"]["axon"])
        self.assertEqual( [respmd["soma"]["name"], a, respmd["axon"]["comments"]],
                          ["DummyTest_soma", True, "voltage response with IClamp"] )

    #@unittest.skip("reason for skipping")
    def test_8_forrecording_None(self):
        self.assertRaises(ValueError, tg.forrecording,)

    #@unittest.skip("reason for skipping")
    def test_9_forrecording_cellular_nostimulus(self):
        stimtype = None # stimparameters["type"] = ["current", "IClamp"]
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0,
        #                             'channels': {'soma': ['pas'], 'axon': ['pas']}}
        self.no_recordings["regions"] = self.regionkeylist
        respmd = tg.forrecording(chosenmodel = self.chosenmodel,
                                 recordings = self.no_recordings,
                                 runtimeparameters = self.no_runtimeparam)
        a = all(boolean == True for boolean in
                                respmd["axon"]["data"] == self.no_recordings["response"]["axon"])
        b = all(boolean == True for boolean in
                                respmd["axon"]["data"] != respmd["soma"]["data"])
        #print respmd # what does it looke like?
        #print(respmd["soma"]["comments"])
        self.assertEqual( [respmd["soma"]["name"], respmd["axon"]["name"], a, b,
                           respmd["soma"]["comments"]],
                          ["DummyTest_soma", "DummyTest_axon", True, True,
                           "voltage response without stimulation"] )

    @unittest.skip("reason for skipping")
    def test_10_forrecording_cellular_stimulus(self):
        stimtype = self.sec_stimparameters["type"] #["voltage", "SEClamp"]
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0,
        #                             'channels': {'soma': ['pas'], 'axon': ['pas']}}
        self.sec_recordings["regions"] = self.regionkeylist
        respmd = tg.forrecording( chosenmodel = self.chosenmodel,
                                  recordings = self.sec_recordings,
                                  runtimeparameters = self.sec_runtimeparam,
                                  stimparameters = self.sec_stimparameters)
        #print(self.chosenmodel.regions.keys())
        a = all(boolean == True for boolean in
                                respmd["soma"]["data"] == self.sec_recordings["response"]["soma"])
        b = all(boolean == True for boolean in
                                respmd["channels"]["soma"]["pas"]["data"] ==
                                self.sec_recordings["response"]["channels"]["soma"]["pas"])
        c = all(boolean == True for boolean in
                                 respmd["channels"]["soma"]["pas"]["data"] !=
                                 self.sec_recordings["response"]["axon"]["pas"])
        self.assertEqual( [respmd["soma"]["name"], respmd["channels"]["soma"]["pas"]["name"],
                           a, b, c, respmd["axon"]["comments"]],
                          ["DummyTest_soma", "DummyTest_channels_soma_pas", True, True, True,
                           "current response with SEClamp"] )

if __name__ == '__main__':
    unittest.main()
