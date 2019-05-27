#/managers/operatorsTranscribe/fabricatorTest.py
import unittest

from datetime import datetime
from dateutil.tz import tzlocal
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

from managers.operatorsTranscribe.fabricator import Fabricator as fab

import numpy

from pynwb import NWBHDF5IO

from pdb import set_trace as breakpoint

class FabricatorTest(unittest.TestCase):

    def setUp(self):
        os.chdir(rootwd)
        self.chosenmodel = DummyCell()
        os.chdir(pwd)
        # parameters for generating NWBFile
        now = datetime.now()
        self.file_metadata = {
                "source": "Where is the data from?, i.e, platform",
                "session_description": "How was the data generated?, i.e, simulation of __",
                "identifier": "a unique modelID, uuid",
                "session_start_time": datetime(now.year, now.month, now.day, now.hour, now.minute,
                                               now.second, now.microsecond, tzinfo=tzlocal()),
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
              {"name": "DummyTest_soma", #"source": "soma",
               "data": rec_v_soma, "unit": "mV",
               "resolution": runtimeparam["dt"],
               "conversion": 1000.0,
               "timestamps": rec_t, "starting_time": 0.0,
               "rate": 1/runtimeparam["dt"],
               "comments": "voltage response without stimulation",
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
        a = all(boolean == True for boolean in nwbts.data==rec_v_soma)
        b = all(boolean == True for boolean in nwbts.timestamps==rec_t)
        self.assertTrue( a and b is True )

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
              {"soma": {"name": "DummyTest_soma", #"source": "soma",
                        "data": recordings["response"]["soma"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comments": "voltage response without stimulation",
                        "description": "whole single array of voltage response from soma of DummyTest"},
               "axon": {"name": "DummyTest_axon", #"source": "axon",
                        "data": recordings["response"]["axon"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comments": "voltage response without stimulation",
                        "description": "whole single array of voltage response from axon of DummyTest"} }
        nwbts = fab.construct_nwbseries_nostimulus(self.chosenmodel,
                                                        ts_metadata)
        #print nwbts['soma'].name # what does this return
        #print [nwbts.name, nwbts.source, nwbts.data, nwbts.unit, nwbts.resolution, nwbts.conversion, nwbts.timestamps, nwbts.starting_time, nwbts.rate, nwbts.comments, nwbts.description, nwbts.control, nwbts.control_description, nwbts.parent] # available attributes
        a = all(boolean == True for boolean in
                                nwbts['soma'].data==recordings['response']['soma'])
        b = all(boolean == True for boolean in
                                nwbts['axon'].data==recordings['response']['axon'])
        c = all(boolean == True for boolean in
                                nwbts['soma'].timestamps==recordings['time'])
        self.assertTrue( a and b and c is True )

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
              {"soma": {"name": "DummyTest_soma",
                        "data": recordings["response"]["soma"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comments": "voltage response without stimulation",
                        "description": "whole single array of voltage response from soma of DummyTest"},
               "axon": {"name": "DummyTest_axon",
                        "data": recordings["response"]["axon"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comments": "voltage response without stimulation",
                        "description": "whole single array of voltage response from axon of DummyTest"} }
        nwbts = fab.build_nwbseries(chosenmodel = self.chosenmodel,
                                    tsmd = ts_metadata)
        #print nwbts['soma'].name # what does this return
        #print [nwbts.name, nwbts.source, nwbts.data, nwbts.unit, nwbts.resolution, nwbts.conversion, nwbts.timestamps, nwbts.starting_time, nwbts.rate, nwbts.comments, nwbts.description, nwbts.control, nwbts.control_description, nwbts.parent] # available attributes
        a = all(boolean == True for boolean in
                                nwbts['soma'].data==recordings['response']['soma'])
        b = all(boolean == True for boolean in
                                nwbts['axon'].data==recordings['response']['axon'])
        c = all(boolean == True for boolean in
                                nwbts['soma'].timestamps==recordings['time'])
        self.assertTrue( a and b and c is True )

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
              {"soma": {"name": "DummyTest_soma",
                        "data": recordings["response"]["soma"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comments": "voltage response without stimulation",
                        "description": "whole single array of voltage response from soma of DummyTest"},
               "axon": {"name": "DummyTest_axon",
                        "data": recordings["response"]["axon"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comments": "voltage response without stimulation",
                        "description": "whole single array of voltage response from axon of DummyTest"},
               "stimulus": {"name": "DummyTest_stimulus",
                            "data": recordings["stimulus"], "unit": "nA",
                            "resolution": runtimeparam["dt"],
                            "conversion": 1000.0,
                            "timestamps": recordings["time"],
                            "comments": "current injection, "+stimparameters["type"][1],
                            "description": "whole single array of stimulus"} }
        nwbts = fab.build_nwbseries(chosenmodel = self.chosenmodel,
                                    tsmd = ts_metadata)
        #print nwbts['soma'].name # what does this return
        #print [nwbts.name, nwbts.source, nwbts.data, nwbts.unit, nwbts.resolution, nwbts.conversion, nwbts.timestamps, nwbts.starting_time, nwbts.rate, nwbts.comments, nwbts.description, nwbts.control, nwbts.control_description, nwbts.parent] # available attributes
        a = all(boolean == True for boolean in
                                nwbts['soma'].data==recordings['response']['soma'])
        b = all(boolean == True for boolean in
                                nwbts['axon'].data==recordings['response']['axon'])
        c = all(boolean == True for boolean in
                                nwbts['soma'].timestamps==recordings['time'])
        self.assertTrue( a and b and c is True )

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
              {"soma": {"name": "DummyTest_soma",
                        "data": recordings["response"]["soma"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comments": "voltage response without stimulation",
                        "description": "whole single array of voltage response from soma of DummyTest"},
               "axon": {"name": "DummyTest_axon",
                        "data": recordings["response"]["axon"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comments": "voltage response without stimulation",
                        "description": "whole single array of voltage response from axon of DummyTest"} }
        nwbts = fab.build_nwbseries(chosenmodel = self.chosenmodel,
                                    tsmd = ts_metadata)
        # Insert
        updated_mynwbfile = fab.link_nwbseriesresponses_to_nwbfile(nwbts, mynwbfile)
        # what does the insertion lead to?
        extracted_nwbts_soma =  updated_mynwbfile.get_acquisition(nwbts["soma"].name)
        extracted_nwbts_axon =  updated_mynwbfile.get_acquisition(nwbts["axon"].name)
        #
        a = all(boolean == True for boolean in
                                extracted_nwbts_soma.data==nwbts['soma'].data)
        b = all(boolean == True for boolean in
                                extracted_nwbts_axon.data==nwbts['axon'].data)
        c = all(boolean == True for boolean in
                                extracted_nwbts_soma.timestamps==nwbts['soma'].timestamps)
        d = ( str(type(updated_mynwbfile))[8:-2] == "pynwb.file.NWBFile" )
        self.assertTrue( a and b and c and d is True )

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
              {"soma": {"name": "DummyTest_soma",
                        "data": recordings["response"]["soma"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comments": "voltage response without stimulation",
                        "description": "whole single array of voltage response from soma of DummyTest"},
               "axon": {"name": "DummyTest_axon",
                        "data": recordings["response"]["axon"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comments": "voltage response without stimulation",
                        "description": "whole single array of voltage response from axon of DummyTest"},
               "stimulus": {"name": "DummyTest_stimulus",
                            "data": recordings["stimulus"], "unit": "nA",
                            "resolution": runtimeparam["dt"],
                            "conversion": 1000.0,
                            "timestamps": recordings["time"],
                            "comments": "current injection, "+stimparameters["type"][1],
                            "description": "whole single array of stimulus"} }
        nwbts = fab.build_nwbseries(chosenmodel = self.chosenmodel,
                                    tsmd = ts_metadata)
        stripped_nwbts = fab.strip_out_stimulus_from_nwbseries(nwbts)
        #print stripped_nwbts
        #print help(stripped_nwbts['soma'])
        #print stripped_nwbts['soma'].data
        #print stripped_nwbts['soma'].timestamps
        #print stripped_nwbts['soma'].starting_time
        #print stripped_nwbts['soma'].description
        #print stripped_nwbts['soma'].unit
        #print stripped_nwbts['soma'].timestamps_unit
        #print ts_metadata["stimulus"]["data"]
        #print nwbts["stimulus"].data
        #print type(stripped_nwbts["soma"])
        #print type(stripped_nwbts["axon"])
        #print nwbts['soma'].name # what does this return
        #print [nwbts.name, nwbts.source, nwbts.data, nwbts.unit, nwbts.resolution, nwbts.conversion, nwbts.timestamps, nwbts.starting_time, nwbts.rate, nwbts.comments, nwbts.description, nwbts.control, nwbts.control_description, nwbts.parent] # available attributes
        a = all(boolean == True for boolean in
                                stripped_nwbts["soma"].data==nwbts['soma'].data)
        b = all(boolean == True for boolean in
                                stripped_nwbts["axon"].data==nwbts['axon'].data)
        compare1 = [len(nwbts), len(stripped_nwbts), a, b]
        compare2 = [3, 2, True, True]
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
              {"soma": {"name": "DummyTest_soma",
                        "data": recordings["response"]["soma"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comments": "voltage response without stimulation",
                        "description": "whole single array of voltage response from soma of DummyTest"},
               "axon": {"name": "DummyTest_axon",
                        "data": recordings["response"]["axon"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comments": "voltage response without stimulation",
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
        a = all(boolean == True for boolean in
                                extracted_nwbts_soma.data==nwbts['soma'].data)
        b = all(boolean == True for boolean in
                                extracted_nwbts_axon.data==nwbts['axon'].data)
        c = all(boolean == True for boolean in
                                extracted_nwbts_soma.timestamps==nwbts['soma'].timestamps)
        d = ( str(type(updated_mynwbfile))[8:-2] == "pynwb.file.NWBFile" )
        self.assertTrue( a and b and c and d is True )

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
              {"soma": {"name": "DummyTest_soma",
                        "data": recordings["response"]["soma"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comments": "voltage response without stimulation",
                        "description": "whole single array of voltage response from soma of DummyTest"},
               "axon": {"name": "DummyTest_axon",
                        "data": recordings["response"]["axon"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comments": "voltage response without stimulation",
                        "description": "whole single array of voltage response from axon of DummyTest"},
               "stimulus": {"name": "DummyTest_stimulus",
                            "data": recordings["stimulus"], "unit": "nA",
                            "resolution": runtimeparam["dt"],
                            "conversion": 1000.0,
                            "timestamps": recordings["time"],
                            "comments": "current injection, "+stimparameters["type"][1],
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
        #io = NWBHDF5IO('updated_mynwbfile.nwb', mode='r')
        #nwbfile = io.read()
        #print("breakpoint")
        #breakpoint()
        #
        # what does the insertion lead to?
        extracted_nwbts_soma =  updated_mynwbfile.get_acquisition(nwbts["soma"].name)
        extracted_nwbts_axon =  updated_mynwbfile.get_acquisition(nwbts["axon"].name)
        extracted_nwbts_stim =  updated_mynwbfile.get_stimulus(nwbts["stimulus"].name)
        #
        a = all(boolean == True for boolean in
                                extracted_nwbts_soma.data==nwbts['soma'].data)
        b = all(boolean == True for boolean in
                                extracted_nwbts_axon.data==nwbts['axon'].data)
        c = all(boolean == True for boolean in
                                extracted_nwbts_soma.timestamps==nwbts['soma'].timestamps)
        d = ( str(type(updated_mynwbfile))[8:-2] == "pynwb.file.NWBFile" )
        self.assertTrue( a and b and c and d is True )

    #@unittest.skip("reason for skipping")
    def test_10_insert_a_nwbepoch(self):
        # Build NWBFile
        mynwbfile = fab.build_nwbfile(self.file_metadata)
        # since self.chosenmodel.regions = {'soma': 0.0, 'axon': 0.0}
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10.0, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( 1 + int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                      "stimulus": "Model is not stimulated"}
        ts_metadata = \
              {"soma": {"name": "DummyTest_soma", #"source": "soma",
                        "data": recordings["response"]["soma"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comments": "voltage response without stimulation",
                        "description": "whole single array of voltage response from soma of DummyTest"},
               "axon": {"name": "DummyTest_axon", #"source": "axon",
                        "data": recordings["response"]["axon"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comments": "voltage response without stimulation",
                        "description": "whole single array of voltage response from axon of DummyTest"} }
        nwbts = fab.build_nwbseries(chosenmodel = self.chosenmodel,
                                    tsmd = ts_metadata)
        epoch_metadata_nostimulus = \
              {"epoch0soma": {"source": "soma", "start_time": 0.0, "stop_time": 10.0, "source":"soma", 
                      "description": "first epoch",
                      "tags": ('1_epoch_responses', '0', 'soma', 'DummyTest', 'cells', "epoch0soma",
                               "soma axon")},
               "epoch0axon": {"start_time": 0.0, "stop_time": 10.0, "source":"axon", 
                      "description": "first epoch",
                      "tags": ('1_epoch_responses', '0', 'axon', 'DummyTest', 'cells' "epoch0axon",
                               "soma axon")}}
        pickedepoch = "epoch0axon" # choose just one
        updated_mynwbfile = fab.insert_a_nwbepoch(pickedepoch,
                                                  epoch_metadata_nostimulus,
                                                  mynwbfile, nwbts["axon"])
        # what does the output look like?
        #updated_mynwbfile = Fabricator.insert_a_nwbepoch("epoch0soma",
        #                                        epoch_metadata_nostimulus,
        #                                        mynwbfile, nwbts["soma"])
        #print(dir(updated_mynwbfile.epochs)) # all the epochs
        #print(updated_mynwbfile.epochs.colnames)
        #print(updated_mynwbfile.epochs)
        #print(len(updated_mynwbfile.epochs))
        #print(updated_mynwbfile.epochs[0])
        #print(len(updated_mynwbfile.epochs[0]))
        #print(updated_mynwbfile.epochs[0][0])
        #print(updated_mynwbfile.epochs[0][1])
        #print(updated_mynwbfile.epochs[0][2])
        #print(updated_mynwbfile.epochs[0][3])
	#print(updated_mynwbfile.epochs[0][4])
	#print(updated_mynwbfile.epochs[0][4][0])
        #print(updated_mynwbfile.epochs[0][4][0][2])
        #print(updated_mynwbfile.epochs[0][4][0][2].timestamps)
        #print(type(updated_mynwbfile.epochs[0][4][0][2].timestamps))
        #print([ i for i in range(updated_mynwbfile.epochs[0][4][0][2].num_samples)
        #        if updated_mynwbfile.epochs[0][4][0][2].timestamps[i]==0.0])
        #breakpoint()
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
        # write test
        # Insert
        #updated_mynwbfile = fab.affix_nwbseries_to_nwbfile(nwbts=nwbts,
        #                                                   nwbfile=mynwbfile)
        #io = NWBHDF5IO('updated_mynwbfile.nwb', mode='w')
        #io.write(updated_mynwbfile)
        #io.close()
        #io = NWBHDF5IO('updated_mynwbfile.nwb', mode='r')
        #nwbfile = io.read()
        #print("breakpoint")
        #breakpoint()
        # "<class '__main__.ClassA'>" 1st"_"is 8 & last"'"is -2
        a = all( boolean == True for boolean in
                 updated_mynwbfile.epochs[0][4][0][2].timestamps
                 == ts_metadata[pickedepoch[-4:]]["timestamps"] )
        b = all( boolean == True for boolean in
                 updated_mynwbfile.epochs[0][4][0][2].data
                 == ts_metadata[pickedepoch[-4:]]["data"] )
        c = ( str(type(updated_mynwbfile))[8:-2] == "pynwb.file.NWBFile" )
        self.assertTrue( a and b and c is True )
        #compare1 = [str(type(updated_mynwbfile))[8:-2], #"<class '__main__.ClassA'>" 1st"_"is 8 & last"'"is -2
        #            updated_mynwbfile.epochs[0][4][0][2].timestamps,
        #            updated_mynwbfile.epochs[0][4][0][2].data]
        #indices = fab.indices_tseries_for_epoch(epoch_metadata_nostimulus[pickedepoch], nwbts["axon"])
        #compare2 = [ "pynwb.file.NWBFile",
        #             numpy.array([ts_metadata[pickedepoch[-4:]]["timestamps"] for i in indices]),
        #             numpy.array([ts_metadata[pickedepoch[-4:]]["data"] for i in indices]) ]
        #print(type(updated_mynwbfile.epochs[0][4][0][2].timestamps))
        #print(type([ts_metadata[pickedepoch[-4:]]["timestamps"] for i in indices]))
        #breakpoint()
        #self.assertEqual( compare1, compare2 )

    #@unittest.skip("reason for skipping")
    def test_11_insert_a_nwbepoch_twice(self):
        # Build NWBFile
        mynwbfile = fab.build_nwbfile(self.file_metadata)
        # since self.chosenmodel.regions = {'soma': 0.0, 'axon': 0.0}
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10.0, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( 1 + int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
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
                        "comments": "voltage response without stimulation",
                        "description": "whole single array of voltage response from soma of DummyTest"},
               "axon": {"name": "DummyTest_axon", "source": "axon",
                        "data": recordings["response"]["axon"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comments": "voltage response without stimulation",
                        "description": "whole single array of voltage response from axon of DummyTest"} }
        nwbts = fab.build_nwbseries(chosenmodel = self.chosenmodel,
                                    tsmd = ts_metadata)
        epoch_metadata_nostimulus = \
              {"epoch0soma": {"start_time": 0.0, "stop_time": 5.0, "source": "soma",
                      "description": "first epoch",
                      "tags": ('1_epoch_responses', '0', 'soma', 'DummyTest', 'cells', "epoch0soma",
                               "soma axon")},
               "epoch0axon": {"start_time": 5.0, "stop_time": 10.0, "source": "axon",
                      "description": "first epoch",
                      "tags": ('1_epoch_responses', '0', 'axon', 'DummyTest', 'cells' "epoch0axon",
                               "soma axon")}}
        pickedepoch1 = "epoch0soma"
        pickedepoch2 = "epoch0axon"
        updated_mynwbfile = fab.insert_a_nwbepoch(pickedepoch1,
                                                  epoch_metadata_nostimulus,
                                                  mynwbfile, nwbts["soma"])
        updated_mynwbfile = fab.insert_a_nwbepoch(pickedepoch2,
                                                  epoch_metadata_nostimulus,
                                                  mynwbfile, nwbts["axon"])
        # Insert
        #updated_mynwbfile = fab.affix_nwbseries_to_nwbfile(nwbts=nwbts,
        #                                                   nwbfile=mynwbfile)
        #io = NWBHDF5IO('updated_mynwbfile.h5', mode='w')
        #io.write(updated_mynwbfile)
        #io.close()
        #io = NWBHDF5IO('updated_mynwbfile.h5', mode='r')
        #nwbfile = io.read()
        #print("breakpoint")
        #breakpoint()
        # what does the output look like?
        #updated_mynwbfile = Fabricator.insert_a_nwbepoch("epoch0soma",
        #                                        epoch_metadata_nostimulus,
        #                                        mynwbfile, nwbts["soma"])
        #print(dir(updated_mynwbfile.epochs)) # all the epochs
        #print(updated_mynwbfile.epochs.colnames)
        #print(updated_mynwbfile.epochs)
        #print(len(updated_mynwbfile.epochs))
        #print(len(updated_mynwbfile.epochs[0][4]))
        #print(updated_mynwbfile.epochs[0])
        #print(updated_mynwbfile.epochs[1])
        #print(len(updated_mynwbfile.epochs[0][4]))
        #print(updated_mynwbfile.epochs[0][4])
        #print(updated_mynwbfile.epochs[1][4])
        #print(updated_mynwbfile.epochs[0][4][0])
        #print(updated_mynwbfile.epochs[0][4][0][2])
        #print(updated_mynwbfile.epochs[0][4][0][2].timestamps)
        #print(updated_mynwbfile.epochs[0][4][0][2].data)
        #other attributes: comments, conversion, resolution, interval, unit, description, num_samples
        # "<class '__main__.ClassA'>" 1st"_"is 8 & last"'"is -2
        #indices1=fab.indices_tseries_for_epoch(epoch_metadata_nostimulus[pickedepoch1], nwbts["soma"])
        #indices2=fab.indices_tseries_for_epoch(epoch_metadata_nostimulus[pickedepoch2], nwbts["axon"])
        #ts_md1 = [ ts_metadata[pickedepoch1[-4:]]["timestamps"][i] for i in indices1 ]
        #ts_md2 = [ ts_metadata[pickedepoch2[-4:]]["timestamps"][i] for i in indices2 ]
        #print(type(ts_metadata[pickedepoch1[-4:]]["timestamps"]))
        #print(type(ts_md1))
        #print(type(updated_mynwbfile.epochs[0][4][0][2].timestamps))
        a = all( boolean == True for boolean in
                 updated_mynwbfile.epochs[0][4][0][2].timestamps #== ts_md1 )
                 == ts_metadata[pickedepoch1[-4:]]["timestamps"] )
        b = all( boolean == True for boolean in
                 updated_mynwbfile.epochs[1][4][0][2].data #== ts_md2 )
                 == ts_metadata[pickedepoch2[-4:]]["data"] )
        ab = ( #all( boolean == True for boolean in
                 updated_mynwbfile.epochs[0][1]      # start_time
                 != updated_mynwbfile.epochs[1][1] ) # start_time
        c = ( str(type(updated_mynwbfile))[8:-2] == "pynwb.file.NWBFile" )
        self.assertTrue( a and b and ab and c is True )

    #@unittest.skip("reason for skipping")
    def test_12_build_nwbepoch(self):
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
              {"soma": {"name": "DummyTest_soma", 
                        "data": recordings["response"]["soma"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comments": "voltage response with stimulation",
                        "description": "whole single array of voltage response from soma of DummyTest"},
               "axon": {"name": "DummyTest_axon",
                        "data": recordings["response"]["axon"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comments": "voltage response with stimulation",
                        "description": "whole single array of voltage response from axon of DummyTest"},
               "stimulus": {"name": "DummyTest_stimulus", #"source": stimparameters["type"][1],
                            "data": recordings["stimulus"], "unit": "nA",
                            "resolution": runtimeparam["dt"],
                            "conversion": 1000.0,
                            "timestamps": recordings["time"],
                            "comments": "current injection, "+stimparameters["type"][1],
                            "description": "whole single array of stimulus"} }
        nwbts = fab.build_nwbseries(chosenmodel = self.chosenmodel,
                                    tsmd = ts_metadata)
        # Insert For Write Test
        #updated_mynwbfile = self.fab.affix_nwbseries_to_nwbfile(nwbts=nwbts,
        #                                                        nwbfile=mynwbfile)
        # Now Epocs
        epoch_metadata_stimulus = \
              {"epoch0soma": {"start_time": 0.0, "stop_time": 10.0, "source": "soma",
                     "description": "first epoch",
                     "tags": ('2_epoch_responses', '0', 'soma', 'DummyTest', 'cells', "epoch0soma",
                              "soma axon")},
               "epoch1soma": {"start_time": 10.0, "stop_time": 20.0, "source": "soma",
                     "description": "second epoch",
                     "tags": ('2_epoch_responses', '1', 'soma', 'DummyTest', 'cells', "epoch1soma",
                              "soma axon")},
               "epoch0axon": {"start_time": 0.0, "stop_time": 10.0, "source": "axon",
                     "description": "first epoch",
                     "tags": ('2_epoch_responses', '0', 'axon', 'DummyTest', 'cells', "epoch0axon",
                              "soma axon")},
               "epoch1axon": {"start_time": 10.0, "stop_time": 20.0, "source": "axon",
                     "description": "second epoch",
                     "tags": ('2_epoch_responses', '1', 'axon', 'DummyTest', 'cells', "epoch1axon",
                              "soma axon")}}
        updated_mynwbfile = fab.build_nwbepochs(nwbfile=mynwbfile,
                                                epochmd=epoch_metadata_stimulus,
                                                nwbts=nwbts)
        #
        #print("start_time")
        #print(updated_mynwbfile.epochs[0][1], updated_mynwbfile.epochs[0][4][0][0])
        #print(updated_mynwbfile.epochs[1][1], updated_mynwbfile.epochs[1][4][0][0])
        #print(updated_mynwbfile.epochs[2][1], updated_mynwbfile.epochs[2][4][0][0])
        #print(updated_mynwbfile.epochs[3][1], updated_mynwbfile.epochs[3][4][0][0])
        #print("stop_time")
        #print(updated_mynwbfile.epochs[0][2], updated_mynwbfile.epochs[0][4][0][1])
        #print(updated_mynwbfile.epochs[1][2], updated_mynwbfile.epochs[1][4][0][1])
        #print(updated_mynwbfile.epochs[2][2], updated_mynwbfile.epochs[2][4][0][1])
        #print(updated_mynwbfile.epochs[3][2], updated_mynwbfile.epochs[3][4][0][1])
        #print(updated_mynwbfile.epochs[0][4][0])
        #breakpoint()
        # Insert
        #updated_mynwbfile = fab.affix_nwbseries_to_nwbfile(nwbts=nwbts,
        #                                                   nwbfile=mynwbfile)
        #io = NWBHDF5IO('updated_mynwbfile.h5', mode='w')
        #io.write(updated_mynwbfile)
        #io.close()
        #io = NWBHDF5IO('updated_mynwbfile.h5', mode='r')
        #nwbfile = io.read()
        #print("breakpoint")
        #breakpoint()
        # what does the output look like?
        #print updated_mynwbfile.epochs.epochs.data # all the epochs
        #emd_key_0 = updated_mynwbfile.epochs[0][3][5]
        region_0 = updated_mynwbfile.epochs[0][3][2]
        #indices_0 = fab.indices_tseries_for_epoch(epoch_metadata_stimulus[emd_key_0],nwbts[region_0])
        #
        #emd_key_1 = updated_mynwbfile.epochs[1][3][5]
        region_1 = updated_mynwbfile.epochs[1][3][2]
        #indices_1 = fab.indices_tseries_for_epoch(epoch_metadata_stimulus[emd_key_1],nwbts[region_1])
        #
        #emd_key_2 = updated_mynwbfile.epochs[2][3][5]
        region_2 = updated_mynwbfile.epochs[2][3][2]
        #indices_2 = fab.indices_tseries_for_epoch(epoch_metadata_stimulus[emd_key_2],nwbts[region_2])
        #
        #emd_key_3 = updated_mynwbfile.epochs[3][3][5]
        region_3 = updated_mynwbfile.epochs[3][3][2]
        #indices_3 = fab.indices_tseries_for_epoch(epoch_metadata_stimulus[emd_key_3],nwbts[region_3])
        #
        #ts_md_0 = [ ts_metadata[region_0]["data"][i] for i in indices_0 ]
        #ts_md_1 = [ ts_metadata[region_1]["timestamps"][i] for i in indices_1 ]
        #ts_md_2 = [ ts_metadata[region_2]["timestamps"][i] for i in indices_2 ]
        #ts_md_3 = [ ts_metadata[region_3]["data"][i] for i in indices_3 ]
        #print(len(ts_md_0s))
        #print(len(updated_mynwbfile.epochs[0][4][0][2].data))
        #print(updated_mynwbfile.epochs[0][1], updated_mynwbfile.epochs[0][2])
        #print(updated_mynwbfile.epochs[0][3])
        #breakpoint()
        a = all( boolean == True for boolean in
                 updated_mynwbfile.epochs[0][4][0][2].data #== ts_md_0 )
                 == ts_metadata[region_0]["data"] )
        b = all( boolean == True for boolean in
                 updated_mynwbfile.epochs[1][4][0][2].timestamps #== ts_md_1 )
                 == ts_metadata[region_1]["timestamps"] )
        #compare1 = [ a, b,
        #            updated_mynwbfile.epochs[2][4][0][2].unit,
        #            updated_mynwbfile.epochs[3][4][0][2].description]
        #compare2 = \
        #   [ True, True,
        #    ts_metadata[ updated_mynwbfile.epochs[2][3][2] ]["unit"],
        #    ts_metadata[ updated_mynwbfile.epochs[3][3][2] ]["description"]]
        #self.assertEqual( compare1, compare2 )
        c = all( boolean == True for boolean in
                 updated_mynwbfile.epochs[2][4][0][2].timestamps #== ts_md_2 )
                 == ts_metadata[region_2]["timestamps"] )
        d = all( boolean == True for boolean in
                 updated_mynwbfile.epochs[3][4][0][2].data #== ts_md_3 )
                 == ts_metadata[region_3]["data"] )
        self.assertTrue( a and b and c and d is True )

    #@unittest.skip("reason for skipping")
    def test_13_write_nwbfile(self):
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
              {"soma": {"name": "DummyTest_soma",
                        "data": recordings["response"]["soma"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comments": "voltage response with stimulation",
                        "description": "whole single array of voltage response from soma of DummyTest"},
               "axon": {"name": "DummyTest_axon",
                        "data": recordings["response"]["axon"], "unit": "mV",
                        "resolution": runtimeparam["dt"],
                        "conversion": 1000.0,
                        "timestamps": recordings["time"],
                        "comments": "voltage response with stimulation",
                        "description": "whole single array of voltage response from axon of DummyTest"},
               "stimulus": {"name": "DummyTest_stimulus",
                            "data": recordings["stimulus"], "unit": "nA",
                            "resolution": runtimeparam["dt"],
                            "conversion": 1000.0,
                            "timestamps": recordings["time"],
                            "comments": "current injection, "+stimparameters["type"][1],
                            "description": "whole single array of stimulus"} }
        nwbts = fab.build_nwbseries(chosenmodel = self.chosenmodel,
                                    tsmd = ts_metadata)
        # Insert For Write Test
        updated_mynwbfile = fab.affix_nwbseries_to_nwbfile(nwbts=nwbts,
                                                           nwbfile=mynwbfile)
        # Now Epocs
        epoch_metadata_stimulus = \
              {"epoch0soma": {"source": "soma", "start_time": 0.0, "stop_time": 10.0,
                     "description": "first epoch",
                     "tags": ('2_epoch_responses', '0', 'soma', 'DummyTest', 'cells', "epoch0soma",
                              "soma axon")},
               "epoch1soma": {"source": "soma", "start_time": 10.0, "stop_time": 20.0,
                     "description": "second epoch",
                     "tags": ('2_epoch_responses', '1', 'soma', 'DummyTest', 'cells', "epoch1soma",
                              "soma axon")},
               "epoch0axon": {"source": "axon", "start_time": 0.0, "stop_time": 10.0,
                     "description": "first epoch",
                     "tags": ('2_epoch_responses', '0', 'axon', 'DummyTest', 'cells', "epoch0axon",
                              "soma axon")},
               "epoch1axon": {"source": "axon", "start_time": 10.0, "stop_time": 20.0,
                     "description": "second epoch",
                     "tags": ('2_epoch_responses', '1', 'axon', 'DummyTest', 'cells', "epoch1axon",
                              "soma axon")}}
        updated_mynwbfile = fab.build_nwbepochs(
                                                nwbfile=updated_mynwbfile,
                                                epochmd=epoch_metadata_stimulus,
                                                nwbts=nwbts)
        # Write Test
        fullname = fab.write_nwbfile(nwbfile=updated_mynwbfile)
        # Read
        io = NWBHDF5IO(fullname, mode="r")
        nwbfile = io.read()
        # what does the output look like?
        #print(dir(nwbfile.epochs)) # all the epochs
        #print(nwbfile.epochs.colnames)
        #print(updated_mynwbfile.epochs)
        #print(len(updated_mynwbfile.epochs))
        #print(len(updated_mynwbfile.epochs[0][4]))
        #print(updated_mynwbfile.epochs[0])
        #print(updated_mynwbfile.epochs[1])
        #print(len(updated_mynwbfile.epochs[0][4]))
        #print(updated_mynwbfile.epochs[0][4])
        #print(updated_mynwbfile.epochs[1][4])
        #print(updated_mynwbfile.epochs[0][4][0])
        #print(updated_mynwbfile.epochs[0][4][0][2])
        #print(updated_mynwbfile.epochs[0][4][0][2].timestamps)
        #print(updated_mynwbfile.epochs[0][4][0][2].data)
        #other attributes: comments, conversion, resolution, interval, unit, description, num_samples
        # "<class '__main__.ClassA'>" 1st"_"is 8 & last"'"is -2
        region_0 = updated_mynwbfile.epochs[0][3][2]
        region_1 = updated_mynwbfile.epochs[1][3][2]
        region_2 = updated_mynwbfile.epochs[2][3][2]
        region_3 = updated_mynwbfile.epochs[3][3][2]
        #
        a = all( boolean == True for boolean in
                 updated_mynwbfile.epochs[0][4][0][2].data #== ts_md_0 )
                 == ts_metadata[region_0]["data"] )
        b = all( boolean == True for boolean in
                 updated_mynwbfile.epochs[1][4][0][2].timestamps #== ts_md_1 )
                 == ts_metadata[region_1]["timestamps"] )
        c = all( boolean == True for boolean in
                 updated_mynwbfile.epochs[2][4][0][2].timestamps #== ts_md_2 )
                 == ts_metadata[region_2]["timestamps"] )
        d = all( boolean == True for boolean in
                 updated_mynwbfile.epochs[3][4][0][2].data #== ts_md_3 )
                 == ts_metadata[region_3]["data"] )
        self.assertTrue( a and b and c and d is True )
        os.remove(fullname)

if __name__ == '__main__':
    unittest.main()
