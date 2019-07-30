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
        # self.chosenmodel.regions ->
        # {"soma": ["v", "i_cap"], "axon": ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        #
        # The following are generated via RegionParser in operatorsTranscribe/regionparser.py
        self.regionlist = ["soma", "axon"]
        self.componentgrouplist = ["channels"]
        self.regionlist_of_of_componentgroup = ["soma", "axon"]
        self.soma_componentlist = ["hh", "pas"]
        self.axon_componentlist = ["pas"]
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
                        "axon": {"pas":[ self.ic_rec_resp[3] ]}}},
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
        self.sec_rec_resp = numpy.random.rand(7,len(self.sec_rec_t))
        self.sec_recordings = {"time": self.sec_rec_t,
           "response": {"soma": [self.sec_rec_resp[0], self.sec_rec_resp[1]],
                        "axon": [ self.sec_rec_resp[2] ],
           "channels": {"soma": {"hh": [self.sec_rec_resp[3], self.sec_rec_resp[4]],
                                 "pas":[ self.sec_rec_resp[5] ]},
                        "axon": {"pas":[ self.sec_rec_resp[3] ]}}},
           "stimulus": self.sec_rec_stim}

    #@unittest.skip("reason for skipping")
    def test_1_cellrecordings_response_regionbodies_nostimulus(self):
        stimtype = None # stimparameters["type"] = ["current", "IClamp"]
        # self.chosenmodel.regions = {'soma': ["v", "i_cap"], 'axon': ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        ts_response = tg.cellrecordings_response_regionbodies(self.chosenmodel,
                                        self.no_recordings, stimtype, self.no_runtimeparam)
        a = all(boolean == True for boolean in
                                           ts_response["axon"][0]["data"] ==
                        self.no_recordings["response"]["axon"][0])
        b = all(boolean == True for boolean in
                                           ts_response["axon"][0]["data"] !=
                                           ts_response["soma"][0]["data"])
        self.assertEqual( [ts_response["axon"][0]["name"], a, b, ts_response["soma"][1]["name"],
                           ts_response["axon"][0]["comments"]],
                          ["DummyTest_axon_v", True, True, "DummyTest_soma_i_cap",
                           "voltage response without stimulation"] )

    #@unittest.skip("reason for skipping")
    def test_2_cellrecordings_response_regionbodies_currentstimulus(self):
        stimtype = self.ic_stimparameters["type"] #["current", "IClamp"]
        # self.chosenmodel.regions = {'soma': ["v", "i_cap"], 'axon': ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        ts_response = tg.cellrecordings_response_regionbodies(self.chosenmodel,
                                        self.ic_recordings, stimtype, self.ic_runtimeparam)
        a = all(boolean == True for boolean in
                                      ts_response["axon"][0]["data"] ==
                   self.ic_recordings["response"]["axon"][0])
        self.assertEqual( [ts_response["soma"][0]["name"], a, ts_response["soma"][0]["comments"],
                           ts_response["soma"][1]["comments"]],
                          ["DummyTest_soma_v", True, "voltage response with IClamp",
                           "current response with IClamp"] )

    #@unittest.skip("reason for skipping")
    def test_3_cellrecordings_response_regionbodies_voltagestimulus(self):
        stimtype = self.sec_stimparameters["type"] #["voltage", "SEClamp"]
        # self.chosenmodel.regions = {'soma': ["v", "i_cap"], 'axon': ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        ts_response = tg.cellrecordings_response_regionbodies(self.chosenmodel,
                                        self.sec_recordings, stimtype, self.sec_runtimeparam)
        a = all(boolean == True for boolean in
                                      ts_response["soma"][0]["data"] ==
                   self.sec_recordings["response"]["soma"][0])
        b = all(boolean == True for boolean in
                                      ts_response["soma"][0]["data"] !=
                                      ts_response["soma"][1]["data"])
        self.assertEqual( [ts_response["soma"][0]["name"], a, b, ts_response["soma"][1]["name"],
                           ts_response["soma"][0]["comments"], ts_response["soma"][1]["comments"]],
                          ["DummyTest_soma_v", True, True, "DummyTest_soma_i_cap",
                           "voltage response with SEClamp", "current response with SEClamp"] )

    #@unittest.skip("reason for skipping")
    def test_4_cellrecordings_response_components_nostimulus(self):
        stimtype = None # stimparameters["type"] = ["current", "IClamp"]
        # self.chosenmodel.regions = {'soma': ["v", "i_cap"], 'axon': ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        ts_response = tg.cellrecordings_response_components(self.chosenmodel,
                                        self.no_recordings, stimtype, self.no_runtimeparam)
        a = all(boolean == True for boolean in
                        ts_response["channels"]["soma"]["pas"][0]["data"] ==
                        self.no_recordings["response"]["channels"]["soma"]["pas"][0])
        b = all(boolean == True for boolean in
                        ts_response["channels"]["soma"]["pas"][0]["data"] !=
                        ts_response["channels"]["axon"]["pas"][0])
        self.assertEqual( [ts_response["channels"]["soma"]["pas"][0]["name"], a, b,
                           ts_response["channels"]["axon"]["pas"][0]["name"],
                           ts_response["channels"]["soma"]["pas"][0]["comments"]],
                          ["DummyTest_soma_pas_i", True, True, "DummyTest_axon_pas_i",
                           "current response without stimulation"] )

    #@unittest.skip("reason for skipping")
    def test_5_cellrecordings_response_components_voltagestimulus(self):
        stimtype = self.sec_stimparameters["type"] #["voltage", "SEClamp"]
        # self.chosenmodel.regions = {'soma': ["v", "i_cap"], 'axon': ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        ts_response = tg.cellrecordings_response_components(self.chosenmodel,
                                        self.sec_recordings, stimtype, self.sec_runtimeparam)
        a = all(boolean == True for boolean in
                   ts_response["channels"]["soma"]["hh"][0]["data"] ==
                   self.sec_recordings["response"]["channels"]["soma"]["hh"][0])
        b = all(boolean == True for boolean in
                   ts_response["channels"]["soma"]["hh"][0]["data"] !=
                   ts_response["channels"]["soma"]["hh"][1]["data"])
        self.assertEqual( [ts_response["channels"]["soma"]["hh"][0]["name"], a, b,
                           ts_response["channels"]["axon"]["pas"][0]["name"],
                           ts_response["channels"]["soma"]["hh"][1]["comments"],
                           ts_response["channels"]["soma"]["pas"][0]["comments"]],
                          ["DummyTest_soma_hh_il", True, True, "DummyTest_axon_pas_i",
                           "voltage response with SEClamp", "current response with SEClamp"] )

    #@unittest.skip("reason for skipping")
    def test_6_recordings_cellstimulus_current(self):
        stimtype = self.ic_stimparameters["type"] #["current", "IClamp"]
        # self.chosenmodel.regions = {'soma': ["v", "i_cap"], 'axon': ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        ts_stimulus = tg.recordings_cell_stimulus(self.chosenmodel, self.ic_recordings,
                                                 self.ic_runtimeparam, self.ic_stimparameters)
        a = all(boolean == True for boolean in
                                ts_stimulus["data"]==self.ic_recordings["stimulus"])
        self.assertEqual( [ts_stimulus["name"], a, ts_stimulus["comments"]],
                          ["DummyTest_stimulus", True, "current injection, IClamp"] )

    #@unittest.skip("reason for skipping")
    def test_7_recordings_cellstimulus_voltage(self):
        stimtype = self.sec_stimparameters["type"] #["voltage", "SEClamp"]
        # self.chosenmodel.regions = {'soma': ["v", "i_cap"], 'axon': ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        ts_stimulus = tg.recordings_cell_stimulus(self.chosenmodel, self.sec_recordings,
                                                 self.sec_runtimeparam, self.sec_stimparameters)
        a = all(boolean == True for boolean in
                                ts_stimulus["data"] == self.sec_recordings["stimulus"])
        self.assertEqual( [ts_stimulus["name"], a, ts_stimulus["comments"]],
                          ["DummyTest_stimulus", True, "voltage injection, SEClamp"] )

    #@unittest.skip("reason for skipping")
    def test_8_forcellrecording_nostimulus(self):
        stimtype = None # stimparameters["type"] = ["current", "IClamp"]
        # self.chosenmodel.regions = {'soma': ["v", "i_cap"], 'axon': ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        respmd = tg.forcellrecording(chosenmodel = self.chosenmodel,
                                     recordings = self.no_recordings,
                                     runtimeparameters = self.no_runtimeparam)
        a = all(boolean == True for boolean in
                        respmd["channels"]["soma"]["pas"][0]["data"] ==
                        self.no_recordings["response"]["channels"]["soma"]["pas"][0])
        b = all(boolean == True for boolean in
                        respmd["channels"]["soma"]["pas"][0]["data"] !=
                        respmd["channels"]["axon"]["pas"][0])
        self.assertEqual( [respmd["channels"]["soma"]["pas"][0]["name"], a, b,
                           respmd["channels"]["axon"]["pas"][0]["name"],
                           respmd["channels"]["soma"]["pas"][0]["comments"]],
                          ["DummyTest_soma_pas_i", True, True, "DummyTest_axon_pas_i",
                           "current response without stimulation"] )

    #@unittest.skip("reason for skipping")
    def test_9_forcellrecording_stimulus(self):
        stimtype = self.ic_stimparameters["type"] #["current", "IClamp"]
        # self.chosenmodel.regions = {'soma': ["v", "i_cap"], 'axon': ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        respmd = tg.forcellrecording(chosenmodel = self.chosenmodel,
                                     recordings = self.ic_recordings,
                                     runtimeparameters = self.ic_runtimeparam,
                                     stimparameters = self.ic_stimparameters)
        a = all(boolean == True for boolean in
                                      respmd["axon"][0]["data"] ==
                   self.ic_recordings["response"]["axon"][0])
        self.assertEqual( [respmd["soma"][0]["name"], a, respmd["soma"][0]["comments"],
                           respmd["soma"][1]["comments"]],
                          ["DummyTest_soma_v", True, "voltage response with IClamp",
                           "current response with IClamp"] )

    #@unittest.skip("reason for skipping")
    def test_10_forrecording_None(self):
        self.assertRaises(ValueError, tg.forrecording,)

    #@unittest.skip("reason for skipping")
    def test_11_forrecording_cellular_nostimulus(self):
        stimtype = None # stimparameters["type"] = ["current", "IClamp"]
        # self.chosenmodel.regions = {'soma': ["v", "i_cap"], 'axon': ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        respmd = tg.forrecording(chosenmodel = self.chosenmodel,
                                 recordings = self.no_recordings,
                                 runtimeparameters = self.no_runtimeparam)
        a = all(boolean == True for boolean in
                        respmd["channels"]["soma"]["pas"][0]["data"] ==
                        self.no_recordings["response"]["channels"]["soma"]["pas"][0])
        b = all(boolean == True for boolean in
                        respmd["channels"]["soma"]["pas"][0]["data"] !=
                        respmd["channels"]["axon"]["pas"][0])
        self.assertEqual( [respmd["channels"]["soma"]["pas"][0]["name"], a, b,
                           respmd["channels"]["axon"]["pas"][0]["name"],
                           respmd["channels"]["soma"]["pas"][0]["comments"]],
                          ["DummyTest_soma_pas_i", True, True, "DummyTest_axon_pas_i",
                           "current response without stimulation"] )

    #@unittest.skip("reason for skipping")
    def test_12_forrecording_cellular_stimulus(self):
        stimtype = self.sec_stimparameters["type"] #["voltage", "SEClamp"]
        # self.chosenmodel.regions = {'soma': ["v", "i_cap"], 'axon': ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        respmd = tg.forrecording( chosenmodel = self.chosenmodel,
                                  recordings = self.sec_recordings,
                                  runtimeparameters = self.sec_runtimeparam,
                                  stimparameters = self.sec_stimparameters)
        a = all(boolean == True for boolean in
                   respmd["channels"]["soma"]["hh"][0]["data"] ==
                   self.sec_recordings["response"]["channels"]["soma"]["hh"][0])
        b = all(boolean == True for boolean in
                   respmd["channels"]["soma"]["hh"][0]["data"] !=
                   respmd["channels"]["soma"]["hh"][1]["data"])
        c = all(boolean == True for boolean in
                   respmd["soma"][0]["data"] != respmd["axon"][0]["data"])
        self.assertEqual( [respmd["channels"]["soma"]["hh"][0]["name"], a, b, c,
                           respmd["channels"]["axon"]["pas"][0]["name"],
                           respmd["channels"]["soma"]["hh"][1]["comments"],
                           respmd["channels"]["soma"]["pas"][0]["comments"]],
                          ["DummyTest_soma_hh_il", True, True, True, "DummyTest_axon_pas_i",
                           "voltage response with SEClamp", "current response with SEClamp"] )

if __name__ == '__main__':
    unittest.main()
