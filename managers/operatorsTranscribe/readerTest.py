#/managers/operatorsTranscribe/readerTest.py
import unittest

import uuid
import os
import sys
# import modules for other directories
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
# this is required for
from models.cells.modelDummyTest import DummyCell

from reader import Reader
from fabricator import Fabricator # to generate NWBFile

import numpy

class ReaderTest(unittest.TestCase):

    def setUp(self):
        self.read = Reader()
        fab = Fabricator() # NOTE: Reader() is an exception for not instantiating
        self.pwd = os.getcwd()
        self.chosenmodel = DummyCell()
        # Build NWBFile
        file_metadata = {
             "source": "Where is the data from?, i.e, platform",
             "session_description": "How was the data generated?, i.e, simulation of __",
             "identifier": "a unique modelID, uuid",
             "session_start_time": '01-12-2017 00:00:00', #"when simulation starts"
             "experimenter": "name of the experimenter/username",
             "experiment_description": "described experiment/test description",
             "session_id": str(hash(str(uuid.uuid1()))).replace('-',''),
             "lab": "name of the lab",
             "institution": "name of the institution" }
        mynwbfile_nostimulus = fab.build_nwbfile(file_metadata)
        mynwbfile_stimulus = fab.build_nwbfile(file_metadata)
        # Generate data
        runtimeparam = {"dt": 0.1, "celsius": 30, "tstop": 200.0, "v_init": 65}
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_i = numpy.random.rand(1,len(rec_t))[0]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings_nostimulus = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                                 "stimulus": "Model is not stimulated"}
        recordings_stimulus = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                               "stimulus": rec_i}
        # Build TimeSeries object
        self.ts_metadata_nostimulus = \
            {"soma": {"name": "DummyTest_soma", "source": "soma",
                      "data": recordings_nostimulus["response"]["soma"], "unit": "mV",
                      "resolution": runtimeparam["dt"],
                      "conversion": 1000.0,
                      "timestamps": recordings_nostimulus["time"],
                      "comment": "voltage response without stimulation",
                      "description": "whole single array of voltage response from soma of DummyTest"},
             "axon": {"name": "DummyTest_axon", "source": "axon",
                      "data": recordings_nostimulus["response"]["axon"], "unit": "mV",
                      "resolution": runtimeparam["dt"],
                      "conversion": 1000.0,
                      "timestamps": recordings_nostimulus["time"],
                      "comment": "voltage response without stimulation",
                      "description": "whole single array of voltage response from axon of DummyTest"}}
        self.ts_metadata_stimulus = \
            {"soma": {"name": "DummyTest_soma", "source": "soma",
                      "data": recordings_stimulus["response"]["soma"], "unit": "mV",
                      "resolution": runtimeparam["dt"],
                      "conversion": 1000.0,
                      "timestamps": recordings_stimulus["time"],
                      "comment": "voltage response with stimulation",
                      "description": "whole single array of voltage response from soma of DummyTest"},
             "axon": {"name": "DummyTest_axon", "source": "axon",
                      "data": recordings_stimulus["response"]["axon"], "unit": "mV",
                      "resolution": runtimeparam["dt"],
                      "conversion": 1000.0,
                      "timestamps": recordings_stimulus["time"],
                      "comment": "voltage response with stimulation",
                      "description": "whole single array of voltage response from axon of DummyTest"},
             "stimulus": {"name": "DummyTest_stimulus", "source": stimparameters["type"][1],
                          "data": recordings_stimulus["stimulus"], "unit": "nA",
                          "resolution": runtimeparam["dt"],
                          "conversion": 1000.0,
                          "timestamps": recordings_stimulus["time"],
                          "comment": "current injection, "+stimparameters["type"][1],
                          "description": "whole single array of stimulus"} }
        nwbts_nostimulus = fab.build_nwbseries(chosenmodel = self.chosenmodel,
                                               tsmd = self.ts_metadata_nostimulus)
        nwbts_stimulus = fab.build_nwbseries(chosenmodel = self.chosenmodel,
                                             tsmd = self.ts_metadata_stimulus)
        # Insert TimeSeries into NWBFile
        updated_mynwbfile_nostimulus = fab.affix_nwbseries_to_nwbfile(nwbseries=nwbts_nostimulus,
                                                                      nwbfile=mynwbfile_nostimulus)
        updated_mynwbfile_stimulus = fab.affix_nwbseries_to_nwbfile(nwbseries=nwbts_stimulus,
                                                                    nwbfile=mynwbfile_stimulus)
        # Build Epochs
        epoch_metadata_nostimulus = \
            {"epoch0soma": {"source": "soma", "start_time": 0.0, "stop_time": runtimeparam["tstop"],
                            "description": "first epoch",
                            "tags": ('1_epoch_responses', '0', 'soma', 'DummyTest', "epoch0soma")},
             "epoch0axon": {"source": "axon", "start_time": 0.0, "stop_time": runtimeparam["tstop"],
                            "description": "first epoch",
                            "tags": ('1_epoch_responses', '0', 'axon', 'DummyTest', "epoch0axon")}}
        epoch_metadata_stimulus = \
            {"epoch0soma": {"source": "soma", "start_time": 0.0,
                            "stop_time": 0.0 + stimparameters['stimlist'][0]['delay'],
                            "description": "first epoch",
                            "tags": ('2_epoch_responses', '0', 'soma', 'DummyTest', "epoch0soma")},
             "epoch1soma": {"source": "soma", "start_time": stimparameters['stimlist'][1]['delay'],
                            "stop_time": stimparameters['stimlist'][1]['delay'] + stimparameters['stimlist'][1]['dur'],
                            "description": "second epoch",
                            "tags": ('2_epoch_responses', '1', 'soma', 'DummyTest', "epoch1soma")},
             "epoch0axon": {"source": "axon", "start_time": 0.0,
                            "stop_time": 0.0 + stimparameters['stimlist'][0]['delay'],
                            "description": "first epoch",
                            "tags": ('2_epoch_responses', '0', 'axon', 'DummyTest', "epoch0axon")},
             "epoch1axon": {"source": "axon", "start_time": stimparameters['stimlist'][1]['delay'],
                            "stop_time": stimparameters['stimlist'][1]['delay'] + stimparameters['stimlist'][1]['dur'],
                            "description": "second epoch",
                            "tags": ('2_epoch_responses', '1', 'axon', 'DummyTest', "epoch1axon")}}
        self.mynwbfile_nostimulus = fab.build_nwbepochs(nwbfile=mynwbfile_nostimulus,
                                                        epochmd=epoch_metadata_nostimulus,
                                                        nwbts=nwbts_nostimulus)
        self.mynwbfile_stimulus = fab.build_nwbepochs(nwbfile=mynwbfile_stimulus,
                                                      epochmd=epoch_metadata_stimulus,
                                                      nwbts=nwbts_stimulus)

    #@unittest.skip("reason for skipping")
    def test_1_get_totalno_epochs(self):
        #print self.mynwbfile_stimulus.epochs.epochs.data
        self.assertEqual( Reader.get_totalno_epochs(self.mynwbfile_stimulus), 4 )

    #@unittest.skip("reason for skipping")
    def test_2_get_any_one_epoch(self):
        #print Reader.get_any_one_epoch(0, self.mynwbfile_stimulus)
        self.assertNotEqual( Reader.get_any_one_epoch(0, self.mynwbfile_nostimulus),
                             Reader.get_any_one_epoch(1, self.mynwbfile_nostimulus) )

    #@unittest.skip("reason for skipping")
    def test_3_get_tags_an_epoch(self):
        a_epoch = Reader.get_any_one_epoch(2, self.mynwbfile_stimulus)
        b_epoch = Reader.get_any_one_epoch(3, self.mynwbfile_stimulus)
        #print Reader.get_tags_an_epoch(a_epoch)
        self.assertNotEqual( Reader.get_tags_an_epoch(a_epoch),
                             Reader.get_tags_an_epoch(b_epoch) )

    #@unittest.skip("reason for skipping")
    def test_4_pull_epoch_id(self):
        a_epoch = Reader.get_any_one_epoch(1, self.mynwbfile_nostimulus)
        self.assertEqual( self.read.pull_epoch_id(a_epoch)[:-4], #strip out soma/axon
                          "epoch0" ) # nostimulus has epoch 0 for both soma & axon

    #@unittest.skip("reason for skipping")
    def test_5_pick_an_epoch(self):
        a_pickedepoch = self.read.pick_an_epoch( epoch_id= "epoch0soma",
                                                 nwbfile=self.mynwbfile_nostimulus)
        b_pickedepoch = self.read.pick_an_epoch( epoch_id= "epoch0axon",
                                                 nwbfile=self.mynwbfile_nostimulus)
        #print a_pickedepoch
        self.assertNotEqual( a_pickedepoch, b_pickedepoch )

    #@unittest.skip("reason for skipping")
    def test_6_get_timeseries_slicer_from_epoch(self):
        a_pickedepoch = self.read.pick_an_epoch( epoch_id="epoch0soma",
                                                 nwbfile=self.mynwbfile_nostimulus)
        x = Reader.get_timeseries_slicer_from_epoch(a_pickedepoch)
        #print x
        # "<class '__main__.ClassA'>" 1st"_"is 8 & last"'"is -2
        self.assertEqual ( str(type(x))[8:-2],
                           "pynwb.form.data_utils.ListSlicer" )

    #@unittest.skip("reason for skipping")
    def test_7_pull_whole_datatable(self):
        a_pickedepoch = self.read.pick_an_epoch( epoch_id="epoch0axon",
                                                 nwbfile=self.mynwbfile_stimulus)
        table_whole_timeseriesdata = self.read.pull_whole_datatable(a_pickedepoch)
        print table_whole_timeseriesdata
        self.assertEqual ( len(table_whole_timeseriesdata),
                           Reader.get_totalno_epochs(self.mynwbfile_stimulus) )

    #@unittest.skip("reason for skipping")
    def test_8_extract_tsobject_of_pickedepoch(self):
        a_pickedepoch = self.read.pick_an_epoch( epoch_id="epoch0soma",
                                                 nwbfile=self.mynwbfile_stimulus)
        b_pickedepoch = self.read.pick_an_epoch( epoch_id="epoch1soma",
                                                 nwbfile=self.mynwbfile_stimulus)
        c_pickedepoch = self.read.pick_an_epoch( epoch_id="epoch0axon",
                                                 nwbfile=self.mynwbfile_stimulus)
        d_pickedepoch = self.read.pick_an_epoch( epoch_id="epoch1axon",
                                                 nwbfile=self.mynwbfile_stimulus)
        ts_a_pickedepoch = self.read.extract_tsobject_of_pickedepoch(
                                 pickedepoch=a_pickedepoch, nwbfile=self.mynwbfile_stimulus)
        ts_b_pickedepoch = self.read.extract_tsobject_of_pickedepoch(
                                 pickedepoch=b_pickedepoch, nwbfile=self.mynwbfile_stimulus)
        ts_c_pickedepoch = self.read.extract_tsobject_of_pickedepoch(
                                 pickedepoch=c_pickedepoch, nwbfile=self.mynwbfile_stimulus)
        ts_d_pickedepoch = self.read.extract_tsobject_of_pickedepoch(
                                 pickedepoch=d_pickedepoch, nwbfile=self.mynwbfile_stimulus)
        #print ts_a_pickedepoch
        compare1 = [ ts_a_pickedepoch.data,
                     ts_b_pickedepoch.timestamps,
                     ts_c_pickedepoch.unit,
                     ts_d_pickedepoch.description ]
        compare2 = [ self.ts_metadata_stimulus["soma"]["data"],
                     self.ts_metadata_stimulus["soma"]["timestamps"],
                     self.ts_metadata_stimulus["axon"]["unit"],
                     self.ts_metadata_stimulus["axon"]["description"]]
        self.assertEqual( compare1, compare2 )

if __name__ == '__main__':
    unittest.main()
