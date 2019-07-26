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

    #@unittest.skip("reason for skipping")
    def test_1_cellrecordings_response_nostimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v_axon = numpy.random.rand(1,len(rec_t))[0]
        rec_stim = "Model is not stimulated" # response["stimulus"]
        stimtype = None # stimparameters["type"] = ["current", "IClamp"]
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0,
        #                             'channels': {'soma': ['pas'], 'axon': ['pas']}}
        ts_response = tg.cellrecordings_response(self.chosenmodel, "axon", rec_t,
                                                 rec_v_axon, rec_stim, stimtype, runtimeparam)
        self.assertEqual( [ts_response["name"], ts_response["data"], ts_response["comments"]],
                          ["DummyTest_axon", rec_v_axon, "voltage response without stimulation"] )

    #@unittest.skip("reason for skipping")
    def test_2_cellrecordings_response_currentstimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v_soma = numpy.random.rand(1,len(rec_t))[0]
        rec_stim = numpy.random.rand(1,len(rec_t))[0] # = response["stimulus"]
        stimtype = ["current", "IClamp"]
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0,
        #                             'channels': {'soma': ['pas'], 'axon': ['pas']}}
        ts_response = tg.cellrecordings_response(self.chosenmodel, "soma", rec_t,
                                                 rec_v_soma, rec_stim, stimtype, runtimeparam)
        self.assertNotEqual( [ts_response["name"], ts_response["data"], ts_response["comments"]],
                             ["DummyTest_soma", rec_v_soma, "voltage response without stimulation"] )

    #@unittest.skip("reason for skipping")
    def test_3_cellrecordings_response_voltagestimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_i_channel_soma_pas = numpy.random.rand(1,len(rec_t))[0]
        rec_stim = numpy.random.rand(1,len(rec_t))[0] # = response["stimulus"]
        stimtype = ["voltage", "SEClamp"]
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0,
        #                             'channels': {'soma': ['pas'], 'axon': ['pas']}}
        ts_response = tg.cellrecordings_response(self.chosenmodel, "channel_soma_pas", rec_t,
                                                 rec_i_channel_soma_pas, rec_stim, stimtype,
                                                 runtimeparam)
        self.assertEqual( [ts_response["name"], ts_response["data"], ts_response["comments"]],
                          ["DummyTest_channel_soma_pas", rec_i_channel_soma_pas,
                           "current response with SEClamp"] )

    #@unittest.skip("reason for skipping")
    def test_4_recordings_cellstimulus_current(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                          "tstop": runtimeparam["tstop"]}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_i_stim = numpy.random.rand(1,len(rec_t))[0]
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0,
        #                             'channels': {'soma': ['pas'], 'axon': ['pas']}}
        ts_stimulus = tg.recordings_cell_stimulus(self.chosenmodel, rec_t, rec_i_stim,
                                                 runtimeparam, stimparameters)
        self.assertEqual( [ts_stimulus["name"], ts_stimulus["comments"]],
                          ["DummyTest_stimulus", "current injection, IClamp"] )

    #@unittest.skip("reason for skipping")
    def test_5_recordings_cellstimulus_voltage(self):
        runtimeparam = {"dt": 0.1, "celsius": 30, "tstop": 35, "v_init": 65}
        stimparameters = {"type": ["voltage", "SEClamp"],
                          "stimlist": [ {'amp1': 0., 'dur1': 10.0},
                                        {'amp2': -70.0, 'dur2': 20.0} ],
                          "tstop": runtimeparam["tstop"]}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v_stim = numpy.random.rand(1,len(rec_t))[0]
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0,
        #                             'channels': {'soma': ['pas'], 'axon': ['pas']}}
        ts_stimulus = tg.recordings_cell_stimulus(self.chosenmodel, rec_t, rec_v_stim,
                                                 runtimeparam, stimparameters)
        self.assertEqual( [ts_stimulus["name"], ts_stimulus["comments"]],
                          ["DummyTest_stimulus", "voltage injection, SEClamp"] )

    #@unittest.skip("reason for skipping")
    def test_6_forcellrecording_nostimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v = numpy.random.rand(4,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0,
        #                             'channels': {'soma': ['pas'], 'axon': ['pas']}}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1],
                                                  "channels": {"soma":[rec_v[2]],
                                                               "axon":[rec_v[3]]}},
                     "stimulus": "Model is not stimulated"}
        respmd = tg.forcellrecording(chosenmodel=self.chosenmodel,
                                           recordings=recordings,
                                           runtimeparameters=runtimeparam)
        self.assertEqual( [respmd["soma"]["name"], respmd["axon"]["name"],
                           respmd["soma"]["comments"]],
                          ["DummyTest_soma", "DummyTest_axon",
                           "voltage response without stimulation"] )

    #@unittest.skip("reason for skipping")
    def test_7_forcellrecording_stimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                          "tstop": runtimeparam["tstop"]}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_stim = numpy.random.rand(1,len(rec_t))[0]
        rec_v = numpy.random.rand(4,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0,
        #                             'channels': {'soma': ['pas'], 'axon': ['pas']}}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1],
                                                  "channels": {"soma":[rec_v[2]],
                                                               "axon":[rec_v[3]]}},
                     "stimulus": rec_stim}
        respmd = tg.forcellrecording(chosenmodel=self.chosenmodel,
                                           recordings=recordings,
                                           runtimeparameters=runtimeparam,
                                           stimparameters=stimparameters)
        a = all(boolean == True for boolean in
                                respmd["axon"]["data"]==recordings["response"]["axon"])
        self.assertEqual( [respmd["soma"]["name"], a, respmd["axon"]["comments"]],
                          ["DummyTest_soma", True, "voltage response with IClamp"] )

    #@unittest.skip("reason for skipping")
    def test_8_forrecording_None(self):
        self.assertRaises(ValueError, tg.forrecording,)

    #@unittest.skip("reason for skipping")
    def test_9_forrecording_cellular_nostimulus(self):
        runtimeparam = {"dt": 0.1, "celsius": 30, "tstop": 1, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v = numpy.random.rand(4,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0,
        #                             'channels': {'soma': ['pas'], 'axon': ['pas']}}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1],
                                                  "channels": {"soma":[rec_v[2]],
                                                               "axon":[rec_v[3]]}},
                     "stimulus": "Model is not stimulated"}
        respmd = tg.forrecording(chosenmodel=self.chosenmodel,
                                      recordings=recordings,
                                      runtimeparameters=runtimeparam)
        #print respmd # what does it looke like?
        self.assertEqual( [respmd["soma"]["name"], respmd["axon"]["name"],
                           respmd["soma"]["comments"]],
                          ["DummyTest_soma", "DummyTest_axon",
                           "voltage response without stimulation"] )

    #@unittest.skip("reason for skipping")
    def test_10_forrecording_cellular_stimulus(self):
        runtimeparam = {"dt": 0.1, "celsius": 30, "tstop": 35, "v_init": 65}
        stimparameters = {"type": ["voltage", "SEClamp"],
                          "stimlist": [ {'amp1': 0., 'dur1': 10.0},
                                        {'amp2': -70.0, 'dur2': 20.0} ],
                          "tstop": runtimeparam["tstop"]}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_stim = numpy.random.rand(1,len(rec_t))[0]
        rec_v = numpy.random.rand(4,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0,
        #                             'channels': {'soma': ['pas'], 'axon': ['pas']}}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1],
                                                  "channels": {"soma":[rec_v[2]],
                                                               "axon":[rec_v[3]]}},
                     "stimulus": rec_stim}
        respmd = tg.forrecording( chosenmodel=self.chosenmodel,
                                  recordings=recordings,
                                  runtimeparameters=runtimeparam,
                                  stimparameters=stimparameters)
        #print(respmd.keys())
        print(self.chosenmodel.regions.keys())
        #a = all(boolean == True for boolean in
        #                        respmd["soma"]["data"] == recordings["response"]["soma"])
        #b = all(boolean == True for boolean in
        #                        respmd["channel_soma_pas"]["data"] ==
        #                        recordings["response"]["channels"]["soma"][0])
        #c = all(boolean == False for boolean in
        #                         respmd["channel_soma_pas"]["data"] ==
        #                         recordings["response"]["soma"])
        #self.assertEqual( [respmd["soma"]["name"], respmd["channel_soma_pas"]["name"], a, b, c,
        #                   respmd["axon"]["comments"]],
        #                  ["DummyTest_soma", "DummyTest_channel_soma_pas", True, True, False,
        #                   "current response with SEClamp"] )

if __name__ == '__main__':
    unittest.main()
