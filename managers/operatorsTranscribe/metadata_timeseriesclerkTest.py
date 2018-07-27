 #/managers/operatorsTranscribe/metadata_timeseriesclerkTest.py
import unittest

import os
import sys
# import modules for other directories
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
# this is required for
from models.cells.modelDummyTest import DummyCell

from metadata_timeseriesclerk import TimeseriesClerk

import numpy

class TimeseriesClerkTest(unittest.TestCase):

    def setUp(self):
        self.tsc = TimeseriesClerk()
        self.pwd = os.getcwd()
        self.chosenmodel = DummyCell()

    #@unittest.skip("reason for skipping")
    def test_1_cellrecordings_response_nostimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v_soma = numpy.random.rand(1,len(rec_t))[0]
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        response = TimeseriesClerk.cellrecordings_response_nostimulus(self.chosenmodel,
                                             "soma", rec_t, rec_v_soma, runtimeparam)
        self.assertEqual( [response["name"], response["data"]],
                          ["DummyTest_nostim_Vm_soma", rec_v_soma] )

    #@unittest.skip("reason for skipping")
    def test_2_cellrecordings_response_stimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v_axon = numpy.random.rand(1,len(rec_t))[0]
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        response = TimeseriesClerk.cellrecordings_response_stimulus(self.chosenmodel,
                                             "soma", rec_t, rec_v_axon, runtimeparam)
        self.assertNotEqual( [response["name"], response["data"]],
                             ["DummyTest_nostim_Vm_soma", rec_v_axon] )

    #@unittest.skip("reason for skipping")
    def test_3_cellrecordings_stimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_i = numpy.random.rand(1,len(rec_t))[0]
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        response = TimeseriesClerk.cellrecordings_stimulus(self.chosenmodel, rec_t, rec_i,
                                       runtimeparam, stimparameters)
        self.assertEqual( [response["name"], response["comment"]],
                          ["DummyTest_stimulus", "current injection, IClamp"] )

    #@unittest.skip("reason for skipping")
    def test_4_forcellrecordings_nostimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]}}
                     #"stimulus": "Model is not stimulated"} not needed for this test
        response = self.tsc.forcellrecordings_nostimulus(self.chosenmodel,
                                                         recordings, runtimeparam)
        self.assertEqual( [response["soma"]["name"], response["axon"]["name"]],
                          ["DummyTest_nostim_Vm_soma", "DummyTest_nostim_Vm_axon"] )

    #@unittest.skip("reason for skipping")
    def test_5_forcellrecordings_stimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_i = numpy.random.rand(1,len(rec_t))[0]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                      "stimulus": rec_i}
        response = self.tsc.forcellrecordings_stimulus(self.chosenmodel, recordings,
                                                       runtimeparam, stimparameters)
        self.assertEqual( [response["soma"]["name"], response["axon"]["data"]],
                          ["DummyTest_stim_Vm_soma", recordings["response"]["axon"]] )

    #@unittest.skip("reason for skipping")
    def test_6_forcellrecording_None(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        #stimparameters = {"type": ["current", "IClamp"],
        #                  "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
        #                                {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_i = numpy.random.rand(1,len(rec_t))[0]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                      "stimulus": rec_i}
        self.assertRaises(ValueError, self.tsc.forcellrecording,
                          chosenmodel=self.chosenmodel, recordings=recordings,
                          runtimeparameters=runtimeparam)

    #@unittest.skip("reason for skipping")
    def test_7_forcellrecording_nostimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                     "stimulus": "Model is not stimulated"}
        respmd = self.tsc.forcellrecording(chosenmodel=self.chosenmodel,
                                           recordings=recordings,
                                           runtimeparameters=runtimeparam)
        self.assertEqual( [respmd["soma"]["name"], respmd["axon"]["name"]],
                          ["DummyTest_nostim_Vm_soma", "DummyTest_nostim_Vm_axon"] )

    #@unittest.skip("reason for skipping")
    def test_8_forcellrecording_stimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_i = numpy.random.rand(1,len(rec_t))[0]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                      "stimulus": rec_i}
        respmd = self.tsc.forcellrecording(chosenmodel=self.chosenmodel,
                                           recordings=recordings,
                                           runtimeparameters=runtimeparam,
                                           stimparameters=stimparameters)
        self.assertEqual( [respmd["soma"]["name"], respmd["axon"]["data"]],
                          ["DummyTest_stim_Vm_soma", recordings["response"]["axon"]] )

    #@unittest.skip("reason for skipping")
    def test_9_forrecording_None(self):
        self.assertRaises(ValueError, self.tsc.forrecording,)

    #@unittest.skip("reason for skipping")
    def test_10_forrecording_cellular_nostimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                     "stimulus": "Model is not stimulated"}
        respmd = self.tsc.forrecording(chosenmodel=self.chosenmodel,
                                      recordings=recordings,
                                      runtimeparameters=runtimeparam)
        self.assertEqual( [respmd["soma"]["name"], respmd["axon"]["name"]],
                          ["DummyTest_nostim_Vm_soma", "DummyTest_nostim_Vm_axon"] )

    #@unittest.skip("reason for skipping")
    def test_11_forrecording_cellular_stimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_i = numpy.random.rand(1,len(rec_t))[0]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                      "stimulus": rec_i}
        respmd = self.tsc.forrecording(chosenmodel=self.chosenmodel,
                                       recordings=recordings,
                                       runtimeparameters=runtimeparam,
                                       stimparameters=stimparameters)
        self.assertEqual( [respmd["soma"]["name"], respmd["axon"]["data"]],
                          ["DummyTest_stim_Vm_soma", recordings["response"]["axon"]] )

if __name__ == '__main__':
    unittest.main()
