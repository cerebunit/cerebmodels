#/managers/operatorsTranscribe/fabricatorTest.py
import unittest

import uuid
import collections # for comparing unordered lists
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

from fabricator import Fabricator as fab

import numpy

from pynwb import NWBHDF5IO

class FabricatorTest(unittest.TestCase):

    def setUp(self):
        os.chdir(rootwd)
        self.chosenmodel = DummyCell()
        os.chdir(pwd)
        # parameters for generating NWBFile
        self.file_metadata = {
                "source": "Where is the data from?, i.e, platform",
                "session_description": "How was the data generated?, i.e, simulation of __",
                "identifier": "a unique modelID, uuid",
                "session_start_time": '01-12-2017 00:00:00', #"when simulation starts"
                "experimenter": "name of the experimenter/username",
                "experiment_description": "described experiment/test description",
                "session_id": str(hash(str(uuid.uuid1()))).replace('-',''),
                "lab": "name of the lab",
                "institution": "name of the institution" }
        # parameters for generating TimeSeries nwb object

    #@unittest.skip("reason for skipping")
    def test_1_build_nwbfile(self):
        nwbfile = fab.build_nwbfile(self.file_metadata)
        #print [nwbfile.source, nwbfile.session_description, nwbfile.identifier,
        #       nwbfile.session_start_time, nwbfile.experimenter,
        #       nwbfile.experiment_description, nwbfile.session_id, nwbfile.lab,
        #       nwbfile.institution] # what does this nwbfile have?

        # "<class '__main__.ClassA'>" 1st"_"is 8 & last"'"is -2
        typestr = str(type(nwbfile))[8:-2]
        self.assertEqual( typestr, "pynwb.file.NWBFile" )
        #sesstime = str(nwbfile.session_start_time).replace(" ", "_")
        #print( nwbfile.session_id + "_" + sesstime.replace(":", "-") ) 

    #@unittest.skip("reason for skipping")
    def test_2_generic_timeseries(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v_soma = numpy.random.rand(1,len(rec_t))[0]
        ts_metadata = \
              {"name": "DummyTest_soma", "source": "soma",
               "data": rec_v_soma, "unit": "mV",
               "resolution": runtimeparam["dt"],
               "conversion": 1000.0,
               "timestamps": rec_t, "starting_time": 0.0,
               "rate": 1/runtimeparam["dt"],
               "comment": "voltage response without stimulation",
               "description": "whole single array of voltage response from soma of DummyTest"}
        nwbts = fab.generic_timeseries(ts_metadata)
        # Bug with pynwb (reported by me on 1/7/2018)
        # https://github.com/NeurodataWithoutBorders/pynwb/issues/579 
        #print nwbts.resolution # float
        #print type(nwbts.conversion) # float
        #print nwbts.starting_time # None but should be float
        #print type(nwbts.rate) # None but should be float
          
        #print [nwbts.name, nwbts.source, nwbts.data, nwbts.unit, nwbts.resolution, nwbts.conversion, nwbts.timestamps, nwbts.starting_time, nwbts.rate, nwbts.comments, nwbts.description, nwbts.control, nwbts.control_description, nwbts.parent] # what does this return
        #
        # write test
        #updated_mynwbfile = self.fab.build_nwbfile(self.file_metadata)
        #updated_mynwbfile.add_acquisition(nwbts)
        #io = NWBHDF5IO('updated_mynwbfile.nwb', mode='w')
        #io.write(updated_mynwbfile)
        #io.close()
        #io = NWBHDF5IO('updated_mynwbfile.nwb')
        #nwbfile = io.read()
        #
        self.assertEqual( [nwbts.data, nwbts.timestamps],
                          [rec_v_soma, rec_t] )

    #@unittest.skip("reason for skipping")
    def test_3_construct_nwbseries_nostimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                      "stimulus": "Model is not stimulated"}
        ts_metadata = \
              {"soma": {"name": "DummyTest_soma", "source": "soma",
                        "data": recordings["response"]["soma"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comment": "voltage response without stimulation",
                        "description": "whole single array of voltage response from soma of DummyTest"},
               "axon": {"name": "DummyTest_axon", "source": "axon",
                        "data": recordings["response"]["axon"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comment": "voltage response without stimulation",
                        "description": "whole single array of voltage response from axon of DummyTest"} }
        nwbts = fab.construct_nwbseries_nostimulus(self.chosenmodel,
                                                        ts_metadata)
        #print nwbts['soma'].name # what does this return
        #print [nwbts.name, nwbts.source, nwbts.data, nwbts.unit, nwbts.resolution, nwbts.conversion, nwbts.timestamps, nwbts.starting_time, nwbts.rate, nwbts.comments, nwbts.description, nwbts.control, nwbts.control_description, nwbts.parent] # available attributes
        compare1 = [nwbts['soma'].data, nwbts['axon'].data, nwbts['soma'].timestamps]
        compare2 = [recordings['response']['soma'], recordings['response']['axon'],
                    recordings['time']]
        self.assertEqual( compare1, compare2 )

    #@unittest.skip("reason for skipping")
    def test_4_build_nwbseries_nostimulus(self):
        # basically the same as test_3_construct_nwbseries_nostimulus
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                      "stimulus": "Model is not stimulated"}
        ts_metadata = \
              {"soma": {"name": "DummyTest_soma", "source": "soma",
                        "data": recordings["response"]["soma"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comment": "voltage response without stimulation",
                        "description": "whole single array of voltage response from soma of DummyTest"},
               "axon": {"name": "DummyTest_axon", "source": "axon",
                        "data": recordings["response"]["axon"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comment": "voltage response without stimulation",
                        "description": "whole single array of voltage response from axon of DummyTest"} }
        nwbts = fab.build_nwbseries(chosenmodel = self.chosenmodel,
                                    tsmd = ts_metadata)
        #print nwbts['soma'].name # what does this return
        #print [nwbts.name, nwbts.source, nwbts.data, nwbts.unit, nwbts.resolution, nwbts.conversion, nwbts.timestamps, nwbts.starting_time, nwbts.rate, nwbts.comments, nwbts.description, nwbts.control, nwbts.control_description, nwbts.parent] # available attributes
        compare1 = [nwbts['soma'].data, nwbts['axon'].data,
                    nwbts['soma'].timestamps]
        compare2 = [recordings['response']['soma'], recordings['response']['axon'],
                    recordings['time']]
        self.assertEqual( compare1, compare2 )

    #@unittest.skip("reason for skipping")
    def test_5_build_nwbseries_stimulus(self):
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 200, "v_init": 65}
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
        ts_metadata = \
              {"soma": {"name": "DummyTest_soma", "source": "soma",
                        "data": recordings["response"]["soma"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comment": "voltage response without stimulation",
                        "description": "whole single array of voltage response from soma of DummyTest"},
               "axon": {"name": "DummyTest_axon", "source": "axon",
                        "data": recordings["response"]["axon"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comment": "voltage response without stimulation",
                        "description": "whole single array of voltage response from axon of DummyTest"},
               "stimulus": {"name": "DummyTest_stimulus", "source": stimparameters["type"][1],
                            "data": recordings["stimulus"], "unit": "nA",
                            "resolution": runtimeparam["dt"],
                            "conversion": 1000.0,
                            "timestamps": recordings["time"],
                            "comment": "current injection, "+stimparameters["type"][1],
                            "description": "whole single array of stimulus"} }
        nwbts = fab.build_nwbseries(chosenmodel = self.chosenmodel,
                                    tsmd = ts_metadata)
        #print nwbts['soma'].name # what does this return
        #print [nwbts.name, nwbts.source, nwbts.data, nwbts.unit, nwbts.resolution, nwbts.conversion, nwbts.timestamps, nwbts.starting_time, nwbts.rate, nwbts.comments, nwbts.description, nwbts.control, nwbts.control_description, nwbts.parent] # available attributes
        compare1 = [nwbts['soma'].data, nwbts['axon'].data, nwbts['stimulus'].data,
                    nwbts['stimulus'].timestamps]
        compare2 = [recordings['response']['soma'], recordings['response']['axon'],
                    recordings['stimulus'], recordings['time']]
        self.assertEqual( compare1, compare2 )

    #@unittest.skip("reason for skipping")
    def test_6_link_nwbseriesresponses_to_nwbfile(self):
        # Build NWBFile
        mynwbfile = fab.build_nwbfile(self.file_metadata)
        # generate data
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                      "stimulus": "Model is not stimulated"}
        # create TimeSeries nwb object
        ts_metadata = \
              {"soma": {"name": "DummyTest_soma", "source": "soma",
                        "data": recordings["response"]["soma"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comment": "voltage response without stimulation",
                        "description": "whole single array of voltage response from soma of DummyTest"},
               "axon": {"name": "DummyTest_axon", "source": "axon",
                        "data": recordings["response"]["axon"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comment": "voltage response without stimulation",
                        "description": "whole single array of voltage response from axon of DummyTest"} }
        nwbts = fab.build_nwbseries(chosenmodel = self.chosenmodel,
                                    tsmd = ts_metadata)
        # Insert
        updated_mynwbfile = fab.link_nwbseriesresponses_to_nwbfile(nwbts, mynwbfile)
        # what does the insertion lead to?
        extracted_nwbts_soma =  updated_mynwbfile.get_acquisition(nwbts["soma"].name)
        extracted_nwbts_axon =  updated_mynwbfile.get_acquisition(nwbts["axon"].name)
        #
        compare1 = [extracted_nwbts_soma.data, extracted_nwbts_axon.data,
                    extracted_nwbts_soma.timestamps, str(type(updated_mynwbfile))[8:-2]]
        compare2 = [nwbts['soma'].data, nwbts['axon'].data,
                    nwbts['soma'].timestamps, "pynwb.file.NWBFile"]
        self.assertEqual( compare1, compare2 )

    #@unittest.skip("reason for skipping")
    def test_7_strip_out_stimulus_from_nwbseries(self):
        # very similar to test_5_build_nwbseries_stimulus but stripping off created stimulus series
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 200, "v_init": 65}
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
        ts_metadata = \
              {"soma": {"name": "DummyTest_soma", "source": "soma",
                        "data": recordings["response"]["soma"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comment": "voltage response without stimulation",
                        "description": "whole single array of voltage response from soma of DummyTest"},
               "axon": {"name": "DummyTest_axon", "source": "axon",
                        "data": recordings["response"]["axon"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comment": "voltage response without stimulation",
                        "description": "whole single array of voltage response from axon of DummyTest"},
               "stimulus": {"name": "DummyTest_stimulus", "source": stimparameters["type"][1],
                            "data": recordings["stimulus"], "unit": "nA",
                            "resolution": runtimeparam["dt"],
                            "conversion": 1000.0,
                            "timestamps": recordings["time"],
                            "comment": "current injection, "+stimparameters["type"][1],
                            "description": "whole single array of stimulus"} }
        nwbts = fab.build_nwbseries(chosenmodel = self.chosenmodel,
                                    tsmd = ts_metadata)
        stripped_nwbts = fab.strip_out_stimulus_from_nwbseries(nwbts)
        #print type(stripped_nwbts["soma"])
        #print type(stripped_nwbts["axon"])
        #print nwbts['soma'].name # what does this return
        #print [nwbts.name, nwbts.source, nwbts.data, nwbts.unit, nwbts.resolution, nwbts.conversion, nwbts.timestamps, nwbts.starting_time, nwbts.rate, nwbts.comments, nwbts.description, nwbts.control, nwbts.control_description, nwbts.parent] # available attributes
        compare1 = [len(nwbts), len(stripped_nwbts), stripped_nwbts["soma"].data,
                                                     stripped_nwbts["axon"].data]
        compare2 = [3, 2, nwbts['soma'].data, nwbts['axon'].data]
        self.assertEqual( compare1, compare2 )

    #@unittest.skip("reason for skipping")
    def test_8_affix_nwbseries_to_nwbfilei_nostimulus(self):
        # similar to test_6_link_nwbseriesresponses_to_nwbfile
        # output should be same as test_6_link_nwbseriesresponses_to_nwbfile
        # Build NWBFile
        mynwbfile = fab.build_nwbfile(self.file_metadata)
        # generate data
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                      "stimulus": "Model is not stimulated"}
        # create TimeSeries nwb object
        ts_metadata = \
              {"soma": {"name": "DummyTest_soma", "source": "soma",
                        "data": recordings["response"]["soma"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comment": "voltage response without stimulation",
                        "description": "whole single array of voltage response from soma of DummyTest"},
               "axon": {"name": "DummyTest_axon", "source": "axon",
                        "data": recordings["response"]["axon"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comment": "voltage response without stimulation",
                        "description": "whole single array of voltage response from axon of DummyTest"} }
        nwbts = fab.build_nwbseries(chosenmodel = self.chosenmodel,
                                             tsmd = ts_metadata)
        # Insert
        updated_mynwbfile = fab.affix_nwbseries_to_nwbfile(nwbts=nwbts,
                                                           nwbfile=mynwbfile)
        # what does the insertion lead to?
        extracted_nwbts_soma =  updated_mynwbfile.get_acquisition(nwbts["soma"].name)
        extracted_nwbts_axon =  updated_mynwbfile.get_acquisition(nwbts["axon"].name)
        #
        compare1 = [extracted_nwbts_soma.data, extracted_nwbts_axon.data,
                    extracted_nwbts_soma.timestamps, str(type(updated_mynwbfile))[8:-2]]
        compare2 = [nwbts['soma'].data, nwbts['axon'].data,
                    nwbts['soma'].timestamps, "pynwb.file.NWBFile"]
        self.assertEqual( compare1, compare2 )

    #@unittest.skip("reason for skipping")
    def test_9_affix_nwbseries_to_nwbfile_stimulus(self):
        # Build NWBFile
        mynwbfile = fab.build_nwbfile(self.file_metadata)
        # generate data
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 200, "v_init": 65}
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
        # create TimeSeries nwb object
        ts_metadata = \
              {"soma": {"name": "DummyTest_soma", "source": "soma",
                        "data": recordings["response"]["soma"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comment": "voltage response without stimulation",
                        "description": "whole single array of voltage response from soma of DummyTest"},
               "axon": {"name": "DummyTest_axon", "source": "axon",
                        "data": recordings["response"]["axon"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comment": "voltage response without stimulation",
                        "description": "whole single array of voltage response from axon of DummyTest"},
               "stimulus": {"name": "DummyTest_stimulus", "source": stimparameters["type"][1],
                            "data": recordings["stimulus"], "unit": "nA",
                            "resolution": runtimeparam["dt"],
                            "conversion": 1000.0,
                            "timestamps": recordings["time"],
                            "comment": "current injection, "+stimparameters["type"][1],
                            "description": "whole single array of stimulus"} }
        nwbts = fab.build_nwbseries(chosenmodel = self.chosenmodel,
                                    tsmd = ts_metadata)
        # Insert
        updated_mynwbfile = fab.affix_nwbseries_to_nwbfile(nwbts=nwbts,
                                                           nwbfile=mynwbfile)
        # write test
        #io = NWBHDF5IO('updated_mynwbfile.nwb', mode='w')
        #io.write(updated_mynwbfile)
        #io.close()
        #io = NWBHDF5IO('updated_mynwbfile.nwb')
        #nwbfile = io.read()
        #
        # what does the insertion lead to?
        extracted_nwbts_soma =  updated_mynwbfile.get_acquisition(nwbts["soma"].name)
        extracted_nwbts_axon =  updated_mynwbfile.get_acquisition(nwbts["axon"].name)
        extracted_nwbts_stim =  updated_mynwbfile.get_stimulus(nwbts["stimulus"].name)
        #
        compare1 = [extracted_nwbts_soma.data, extracted_nwbts_axon.data,
                    extracted_nwbts_stim.timestamps, str(type(updated_mynwbfile))[8:-2]]
        compare2 = [nwbts['soma'].data, nwbts['axon'].data,
                    nwbts['stimulus'].timestamps, "pynwb.file.NWBFile"]
        self.assertEqual( compare1, compare2 )

    #@unittest.skip("reason for skipping")
    def test_10_insert_a_nwbepoch(self):
        # Build NWBFile
        mynwbfile = fab.build_nwbfile(self.file_metadata)
        # since self.chosenmodel.regions = {'soma': 0.0, 'axon': 0.0}
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                      "stimulus": "Model is not stimulated"}
        ts_metadata = \
              {"soma": {"name": "DummyTest_soma", "source": "soma",
                        "data": recordings["response"]["soma"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comment": "voltage response without stimulation",
                        "description": "whole single array of voltage response from soma of DummyTest"},
               "axon": {"name": "DummyTest_axon", "source": "axon",
                        "data": recordings["response"]["axon"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comment": "voltage response without stimulation",
                        "description": "whole single array of voltage response from axon of DummyTest"} }
        nwbts = fab.build_nwbseries(chosenmodel = self.chosenmodel,
                                    tsmd = ts_metadata)
        epoch_metadata_nostimulus = \
              {"epoch0soma": {"source": "soma", "start_time": 0.0, "stop_time": 10.0,
                      "description": "first epoch",
                      "tags": ('1_epoch_responses', '0', 'soma', 'DummyTest', 'cells', "epoch0soma")},
               "epoch0axon": {"source": "axon", "start_time": 0.0, "stop_time": 10.0,
                      "description": "first epoch",
                      "tags": ('1_epoch_responses', '0', 'axon', 'DummyTest', 'cells' "epoch0axon")}}
        pickedepoch = "epoch0axon" # choose just one
        updated_mynwbfile = fab.insert_a_nwbepoch(pickedepoch,
                                                  epoch_metadata_nostimulus,
                                                  mynwbfile, nwbts["axon"])
        # what does the output look like?
        #updated_mynwbfile = Fabricator.insert_a_nwbepoch("epoch0soma",
        #                                        epoch_metadata_nostimulus,
        #                                        mynwbfile, nwbts["soma"])
        #print updated_mynwbfile.epochs.epochs.data # all the epochs
        #print updated_mynwbfile.epochs.epochs.data[0] # first epoch
        #print updated_mynwbfile.epochs.epochs.data[0][3].data # class
        #print updated_mynwbfile.epochs.epochs.data[0][3].data.data # data for all epochs
        #print updated_mynwbfile.epochs.epochs.data[0][3].data.data[0][2] # data for first epoch
        #print updated_mynwbfile.epochs.epochs.data[0][3].data.data[0][2].timestamps
        #print updated_mynwbfile.epochs.epochs.data[0][3].data.data[0][2].data
        # making sure that each data correspond to respective epochs
        #print updated_mynwbfile.epochs.epochs.data[0]
        #print updated_mynwbfile.epochs.epochs.data[0][3].data.data[0][2].description
        #print updated_mynwbfile.epochs.epochs.data[1]
        #print updated_mynwbfile.epochs.epochs.data[1][3].data.data[1][2].description
        #print nwbts["soma"].description
        #print nwbts["axon"].description
        # "<class '__main__.ClassA'>" 1st"_"is 8 & last"'"is -2
        compare1 = [str(type(updated_mynwbfile))[8:-2], #"<class '__main__.ClassA'>" 1st"_"is 8 & last"'"is -2
                    updated_mynwbfile.epochs.epochs.data[0][3].data.data[0][2].timestamps,
                    updated_mynwbfile.epochs.epochs.data[0][3].data.data[0][2].data]
        compare2 = ["pynwb.file.NWBFile",
                    ts_metadata[pickedepoch[-4:]]["timestamps"],
                    ts_metadata[pickedepoch[-4:]]["data"]]
        self.assertEqual( compare1, compare2 )

    #@unittest.skip("reason for skipping")
    def test_11_build_nwbepoch(self):
        # Build NWBFile
        mynwbfile = fab.build_nwbfile(self.file_metadata)
        # generate data
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 200, "v_init": 65}
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
        # create TimeSeries nwb object
        ts_metadata = \
              {"soma": {"name": "DummyTest_soma", "source": "soma",
                        "data": recordings["response"]["soma"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comment": "voltage response with stimulation",
                        "description": "whole single array of voltage response from soma of DummyTest"},
               "axon": {"name": "DummyTest_axon", "source": "axon",
                        "data": recordings["response"]["axon"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comment": "voltage response with stimulation",
                        "description": "whole single array of voltage response from axon of DummyTest"},
               "stimulus": {"name": "DummyTest_stimulus", "source": stimparameters["type"][1],
                            "data": recordings["stimulus"], "unit": "nA",
                            "resolution": runtimeparam["dt"],
                            "conversion": 1000.0,
                            "timestamps": recordings["time"],
                            "comment": "current injection, "+stimparameters["type"][1],
                            "description": "whole single array of stimulus"} }
        nwbts = fab.build_nwbseries(chosenmodel = self.chosenmodel,
                                    tsmd = ts_metadata)
        # Insert For Write Test
        #updated_mynwbfile = self.fab.affix_nwbseries_to_nwbfile(nwbts=nwbts,
        #                                                        nwbfile=mynwbfile)
        # Now Epocs
        epoch_metadata_stimulus = \
              {"epoch0soma": {"source": "soma", "start_time": 0.0, "stop_time": 10.0,
                     "description": "first epoch",
                     "tags": ('2_epoch_responses', '0', 'soma', 'DummyTest', 'cells', "epoch0soma")},
               "epoch1soma": {"source": "soma", "start_time": 10.0, "stop_time": 20.0,
                     "description": "second epoch",
                     "tags": ('2_epoch_responses', '1', 'soma', 'DummyTest', 'cells', "epoch1soma")},
               "epoch0axon": {"source": "axon", "start_time": 0.0, "stop_time": 10.0,
                     "description": "first epoch",
                     "tags": ('2_epoch_responses', '0', 'axon', 'DummyTest', 'cells', "epoch0axon")},
               "epoch1axon": {"source": "axon", "start_time": 10.0, "stop_time": 20.0,
                     "description": "second epoch",
                     "tags": ('2_epoch_responses', '1', 'axon', 'DummyTest', 'cells', "epoch1axon")}}
        updated_mynwbfile = fab.build_nwbepochs(
                                                nwbfile=mynwbfile,
                                                epochmd=epoch_metadata_stimulus,
                                                nwbts=nwbts)
        # Write Test
        #io = NWBHDF5IO('updated_mynwbfile.h5', mode='w')
        #io.write(updated_mynwbfile)
        #io.close()
        #io = NWBHDF5IO('updated_mynwbfile.h5')
        #nwbfile = io.read()
        # what does the output look like?
        #print updated_mynwbfile.epochs.epochs.data # all the epochs
        #print updated_mynwbfile.epochs.epochs.data[0][3] # 1st epoch
        #print updated_mynwbfile.epochs.epochs.data[0][3].data.data[0][2].description # its data
        #print updated_mynwbfile.epochs.epochs.data[1][3] # 2nd epoch
        #print updated_mynwbfile.epochs.epochs.data[1][3].data.data[1][2].description # its data
        #print updated_mynwbfile.epochs.epochs.data[2][3] # 3rd epoch
        #print updated_mynwbfile.epochs.epochs.data[2][3].data.data[2][2].description # its data
        #print updated_mynwbfile.epochs.epochs.data[3][3] # 4th epoch
        #print updated_mynwbfile.epochs.epochs.data[3][3].data.data[3][2].description # its data
        #
        # Here because all the tags have the form
        # 2_epoch_responses,1,soma,DummyTest,epoch1soma extract the last 4 characters
        # the last 4 characters corresponds to source of TimeSeries object
        #print updated_mynwbfile.epochs.epochs.data[0][2]#[-4:]
        compare1 = [updated_mynwbfile.epochs.epochs.data[0][3].data.data[0][2].data,
                    updated_mynwbfile.epochs.epochs.data[1][3].data.data[1][2].timestamps,
                    updated_mynwbfile.epochs.epochs.data[2][3].data.data[2][2].unit,
                    updated_mynwbfile.epochs.epochs.data[3][3].data.data[3][2].description]
        compare2 = \
           [ts_metadata[ updated_mynwbfile.epochs.epochs.data[0][2][-4:] ]["data"],
            ts_metadata[ updated_mynwbfile.epochs.epochs.data[1][2][-4:] ]["timestamps"],
            ts_metadata[ updated_mynwbfile.epochs.epochs.data[2][2][-4:] ]["unit"],
            ts_metadata[ updated_mynwbfile.epochs.epochs.data[3][2][-4:] ]["description"]]
        self.assertEqual( compare1, compare2 )

if __name__ == '__main__':
    unittest.main()
