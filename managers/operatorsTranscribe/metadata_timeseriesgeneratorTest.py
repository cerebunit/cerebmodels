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
        specific_rec_i = "not stimulated" # != response["stimulus"]
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        ts_response = tg.cellrecordings_response(self.chosenmodel,
                              "axon", rec_t, specific_rec_i, rec_v_axon, runtimeparam)
        self.assertEqual( [ts_response["name"], ts_response["data"], ts_response["comment"]],
                          ["DummyTest_axon", rec_v_axon, "voltage response without stimulation"] )

    #@unittest.skip("reason for skipping")
    def test_2_cellrecordings_response_stimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v_soma = numpy.random.rand(1,len(rec_t))[0]
        rec_i = numpy.random.rand(1,len(rec_t))[0] # = response["stimulus"]
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        ts_response = tg.cellrecordings_response(self.chosenmodel,
                              "soma", rec_t, rec_i, rec_v_soma, runtimeparam)
        self.assertNotEqual( [ts_response["name"], ts_response["data"], ts_response["comment"]],
                             ["DummyTest_soma", rec_v_soma, "voltage response without stimulation"] )

    #@unittest.skip("reason for skipping")
    def test_3_recordings_cell_current_stimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                          "tstop": runtimeparam["tstop"]}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_i = numpy.random.rand(1,len(rec_t))[0]
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        ts_stimulus = tg.recordings_cell_currentstimulus(self.chosenmodel,
                                       rec_t, rec_i, runtimeparam, stimparameters)
        self.assertEqual( [ts_stimulus["name"], ts_stimulus["comment"]],
                          ["DummyTest_stimulus", "current injection, IClamp"] )

    #@unittest.skip("reason for skipping")
    def test_4_recordings_cellstimulus_current(self):
        # this is basically the same as test_3_recordings_cell_current_stimulus
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                          "tstop": runtimeparam["tstop"]}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_i = numpy.random.rand(1,len(rec_t))[0]
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        ts_stimulus = tg.recordings_cellstimulus(self.chosenmodel,
                                       rec_t, rec_i, runtimeparam, stimparameters)
        self.assertEqual( [ts_stimulus["name"], ts_stimulus["comment"]],
                          ["DummyTest_stimulus", "current injection, IClamp"] )

    #@unittest.skip("reason for skipping")
    def test_5_forcellrecordings_nostimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]}}
                     #"stimulus": "Model is not stimulated"} not needed for this test
        response = tg.forcellrecordings_nostimulus(self.chosenmodel,
                                                         recordings, runtimeparam)
        self.assertEqual( [response["soma"]["name"], response["axon"]["name"],
                           response["soma"]["comment"]],
                          ["DummyTest_soma", "DummyTest_axon",
                           "voltage response without stimulation"] )

    #@unittest.skip("reason for skipping")
    def test_6_forcellrecordings_stimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                          "tstop": runtimeparam["tstop"]}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_i = numpy.random.rand(1,len(rec_t))[0]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                      "stimulus": rec_i}
        response = tg.forcellrecordings_stimulus(self.chosenmodel, recordings,
                                                       runtimeparam, stimparameters)
        self.assertEqual( [response["soma"]["name"], response["axon"]["data"],
                           response["soma"]["comment"]],
                          ["DummyTest_soma", recordings["response"]["axon"],
                           "voltage response with stimulation"] )

    #@unittest.skip("reason for skipping")
    def test_7_forcellrecording_None(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        #stimparameters = {"type": ["current", "IClamp"],
        #                  "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
        #                                {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
        #                  "tstop": runtimeparam["tstop"]}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_i = numpy.random.rand(1,len(rec_t))[0]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                      "stimulus": rec_i}
        self.assertRaises(ValueError, tg.forcellrecording,
                          chosenmodel=self.chosenmodel, recordings=recordings,
                          runtimeparameters=runtimeparam)

    #@unittest.skip("reason for skipping")
    def test_8_forcellrecording_nostimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                     "stimulus": "Model is not stimulated"}
        respmd = tg.forcellrecording(chosenmodel=self.chosenmodel,
                                           recordings=recordings,
                                           runtimeparameters=runtimeparam)
        self.assertEqual( [respmd["soma"]["name"], respmd["axon"]["name"],
                           respmd["soma"]["comment"]],
                          ["DummyTest_soma", "DummyTest_axon",
                           "voltage response without stimulation"] )

    #@unittest.skip("reason for skipping")
    def test_9_forcellrecording_stimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                          "tstop": runtimeparam["tstop"]}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_i = numpy.random.rand(1,len(rec_t))[0]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                      "stimulus": rec_i}
        respmd = tg.forcellrecording(chosenmodel=self.chosenmodel,
                                           recordings=recordings,
                                           runtimeparameters=runtimeparam,
                                           stimparameters=stimparameters)
        self.assertEqual( [respmd["soma"]["name"], respmd["axon"]["data"],
                           respmd["axon"]["comment"]],
                          ["DummyTest_soma", recordings["response"]["axon"],
                           "voltage response with stimulation"] )

    #@unittest.skip("reason for skipping")
    def test_10_forrecording_None(self):
        self.assertRaises(ValueError, tg.forrecording,)

    #@unittest.skip("reason for skipping")
    def test_11_forrecording_cellular_nostimulus(self):
        runtimeparam = {"dt": 0.1, "celsius": 30, "tstop": 1, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                     "stimulus": "Model is not stimulated"}
        respmd = tg.forrecording(chosenmodel=self.chosenmodel,
                                      recordings=recordings,
                                      runtimeparameters=runtimeparam)
        #print respmd # what does it looke like?
        self.assertEqual( [respmd["soma"]["name"], respmd["axon"]["name"]],
                          ["DummyTest_soma", "DummyTest_axon"] )

    #@unittest.skip("reason for skipping")
    def test_12_forrecording_cellular_stimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                          "tstop": runtimeparam["tstop"]}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_i = numpy.random.rand(1,len(rec_t))[0]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                      "stimulus": rec_i}
        respmd = tg.forrecording(chosenmodel=self.chosenmodel,
                                       recordings=recordings,
                                       runtimeparameters=runtimeparam,
                                       stimparameters=stimparameters)
        self.assertEqual( [respmd["soma"]["name"], respmd["axon"]["data"]],
                          ["DummyTest_soma", recordings["response"]["axon"]] )

if __name__ == '__main__':
    unittest.main()
