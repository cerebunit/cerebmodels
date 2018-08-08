#/managers/operatorsTranscribe/readerTest.py
import unittest

import StringIO #import io for Python3

import uuid
import os
import sys
# import modules for other directories
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
# this is required for
from models.cells.modelDummyTest import DummyCell
import numpy
from fabricator import Fabricator # to generate NWBFile
from pynwb import NWBHDF5IO

from reader import Reader


class ReaderTest(unittest.TestCase):

    def setUp(self):
        self.pwd = os.getcwd()
        # Create two files with/without stimulus
        fab = Fabricator() # NOTE: Reader() is an exception for not instantiating
        chosenmodel = DummyCell()
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
        mynwbfile_nostimulus = fab.build_nwbfile(file_metadata) # file with no stimulus
        mynwbfile_stimulus = fab.build_nwbfile(file_metadata)   # file with stimulus
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
        nwbts_nostimulus = fab.build_nwbseries(chosenmodel = chosenmodel,
                                               tsmd = self.ts_metadata_nostimulus)
        nwbts_stimulus = fab.build_nwbseries(chosenmodel = chosenmodel,
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
                    "tags": ('1_epoch_responses', '0', 'soma', 'DummyTest',  'cells', "epoch0soma")},
             "epoch0axon": {"source": "axon", "start_time": 0.0, "stop_time": runtimeparam["tstop"],
                    "description": "first epoch",
                    "tags": ('1_epoch_responses', '0', 'axon', 'DummyTest', 'cells', "epoch0axon")}}
        epoch_metadata_stimulus = \
            {"epoch0soma": {"source": "soma", "start_time": 0.0,
                    "stop_time": 0.0 + stimparameters['stimlist'][0]['delay'],
                    "description": "first epoch",
                    "tags": ('2_epoch_responses', '0', 'soma', 'DummyTest', 'cells', "epoch0soma")},
             "epoch1soma": {"source": "soma", "start_time": stimparameters['stimlist'][1]['delay'],
                    "stop_time": stimparameters['stimlist'][1]['delay'] + stimparameters['stimlist'][1]['dur'],
                    "description": "second epoch",
                    "tags": ('2_epoch_responses', '1', 'soma', 'DummyTest', 'cells', "epoch1soma")},
             "epoch0axon": {"source": "axon", "start_time": 0.0,
                    "stop_time": 0.0 + stimparameters['stimlist'][0]['delay'],
                    "description": "first epoch",
                    "tags": ('2_epoch_responses', '0', 'axon', 'DummyTest', 'cells', "epoch0axon")},
             "epoch1axon": {"source": "axon", "start_time": stimparameters['stimlist'][1]['delay'],
                    "stop_time": stimparameters['stimlist'][1]['delay'] + stimparameters['stimlist'][1]['dur'],
                    "description": "second epoch",
                    "tags": ('2_epoch_responses', '1', 'axon', 'DummyTest', 'cells', "epoch1axon")}}
        updated_mynwbfile_nostimulus = fab.build_nwbepochs(nwbfile=updated_mynwbfile_nostimulus,
                                                           epochmd=epoch_metadata_nostimulus,
                                                           nwbts=nwbts_nostimulus)
        updated_mynwbfile_stimulus = fab.build_nwbepochs(nwbfile=updated_mynwbfile_stimulus,
                                                         epochmd=epoch_metadata_stimulus,
                                                         nwbts=nwbts_stimulus)
        # Write for nostimulus
        write_io_nostimulus = NWBHDF5IO('mynwbfile_nostimulus.h5', mode='w')
        write_io_nostimulus.write(updated_mynwbfile_nostimulus)
        write_io_nostimulus.close()
        # Write for stimulus
        write_io_stimulus = NWBHDF5IO('mynwbfile_stimulus.h5', mode='w')
        write_io_stimulus.write(updated_mynwbfile_stimulus)
        write_io_stimulus.close()
        # Read the files
        #self.reader = Reader()
        #self.read_io_nostimulus = Reader('mynwbfile_nostimulus.h5')
        #self.read_io_stimulus = Reader('mynwbfile_stimulus.h5')

    #@unittest.skip("reason for skipping")
    def test_1_init(self):
        reader_io_nostimulus = Reader('mynwbfile_nostimulus.h5')
        reader_io_stimulus = Reader('mynwbfile_stimulus.h5')
        # this tests extract_modelname_modelscale & load_model
        compare1 = [ reader_io_nostimulus.modelname,  # output of 
                     reader_io_nostimulus.modelscale ]# extract_modelname_modelscale()
        compare2 = [ reader_io_stimulus.chosenmodel.modelname,  # output of
                     reader_io_stimulus.chosenmodel.modelscale ]# load_model()
        self.assertEqual( compare1, compare2 )
        reader_io_nostimulus.closefile()
        reader_io_stimulus.closefile()

    #@unittest.skip("reason for skipping")
    def test_2_visualizetable(self):
        reader_io_nostimulus = Reader('mynwbfile_nostimulus.h5')
        reader_io_nostimulus.session_info() # pretty prints table
        reader_io_nostimulus.closefile()

    #@unittest.skip("reason for skipping")
    def test_3_get_epochindices_chosenregion(self):
        reader_io_stimulus = Reader('mynwbfile_stimulus.h5')
        epoch_indices_soma = reader_io_stimulus.get_epochindices_chosenregion('soma')
        epoch_indices_axon = reader_io_stimulus.get_epochindices_chosenregion('axon')
        self.assertNotEqual( epoch_indices_soma, epoch_indices_axon )
        reader_io_stimulus.closefile()

    #@unittest.skip("reason for skipping")
    def test_4_get_epochids_chosenregion(self):
        reader_io_stimulus = Reader('mynwbfile_stimulus.h5')
        epoch_ids_soma = reader_io_stimulus.get_epochids_chosenregion('soma')
        epoch_ids_axon = reader_io_stimulus.get_epochids_chosenregion('axon')
        self.assertEqual( epoch_ids_soma, epoch_ids_axon )
        reader_io_stimulus.closefile()

    #@unittest.skip("reason for skipping")
    def test_5_extract_orderedepochs(self):
        reader_io_stimulus = Reader('mynwbfile_stimulus.h5')
        orderedepochs_soma = reader_io_stimulus.extract_orderedepochs('soma')
        #print orderedepochs_soma
        #print len(orderedepochs_soma)
        #to compare
        epoch_indices_soma = reader_io_stimulus.get_epochindices_chosenregion('soma')
        compare1 = [ orderedepochs_soma[0][0], orderedepochs_soma[1][0] ]
        self.assertEqual( compare1, epoch_indices_soma )
        reader_io_stimulus.closefile()

    #@unittest.skip("reason for skipping")
    def test_6_extract_epoch(self):
        reader_io_stimulus = Reader('mynwbfile_stimulus.h5')
        orderedepochs_soma = reader_io_stimulus.extract_orderedepochs('soma')
        epochs = []
        epoch_ids_soma = reader_io_stimulus.get_epochids_chosenregion('soma')
        for epoch_id in epoch_ids_soma:
            epochs.append( reader_io_stimulus.extract_epoch(epoch_id, orderedepochs_soma) )
        #print epoch_ids_soma
        #print epochs[0]
        #print epochs[1]
        self.assertNotEqual( epochs[0], epochs[1] )
        reader_io_stimulus.closefile()

    #@unittest.skip("reason for skipping")
    def test_7_get_epoch_start_stop_times(self):
        reader_io_nostimulus = Reader('mynwbfile_nostimulus.h5')
        orderedepochs_soma = reader_io_nostimulus.extract_orderedepochs('soma')
        orderedepochs_axon = reader_io_nostimulus.extract_orderedepochs('axon')
        epochtuple_soma = reader_io_nostimulus.extract_epoch(0, orderedepochs_soma)
        epochtuple_axon = reader_io_nostimulus.extract_epoch(0, orderedepochs_axon)
        #
        #print epochtuple_soma
        strt_soma, stop_soma = reader_io_nostimulus.get_epoch_start_stop_times(epochtuple_soma)
        strt_axon, stop_axon = reader_io_nostimulus.get_epoch_start_stop_times(epochtuple_axon)
        #print strt_soma, stop_soma
        #print strt_axon, stop_axon
        self.assertEqual( [ strt_soma, stop_soma ], [ strt_axon, stop_axon ] )
        reader_io_nostimulus.closefile()

    #@unittest.skip("reason for skipping")
    def test_8_get_epochdescription(self):
        reader_io_stimulus = Reader('mynwbfile_stimulus.h5')
        orderedepochs_soma = reader_io_stimulus.extract_orderedepochs('soma')
        epochtuple_0soma = reader_io_stimulus.extract_epoch(0, orderedepochs_soma)
        epochtuple_1soma = reader_io_stimulus.extract_epoch(1, orderedepochs_soma)
        #
        #print epochtuple_0soma
        descrip0 = reader_io_stimulus.get_epochdescription(epochtuple_0soma)
        descrip1 = reader_io_stimulus.get_epochdescription(epochtuple_1soma)
        #print descrip0, descrip1
        self.assertNotEqual( descrip0, descrip1 )
        reader_io_stimulus.closefile()

    @unittest.skip("reason for skipping")
    def test_6_get_timeseries_slicer_from_epoch(self):
        a_pickedepoch = self.read.pick_an_epoch( epoch_id="epoch0soma",
                                                 nwbfile=self.mynwbfile_nostimulus)
        x = Reader.get_timeseries_slicer_from_epoch(a_pickedepoch)
        #print x
        # "<class '__main__.ClassA'>" 1st"_"is 8 & last"'"is -2
        self.assertEqual ( str(type(x))[8:-2],
                           "pynwb.form.data_utils.ListSlicer" )

    @unittest.skip("reason for skipping")
    def test_7_pull_whole_datatable(self):
        a_pickedepoch = self.read.pick_an_epoch( epoch_id="epoch0axon",
                                                 nwbfile=self.mynwbfile_stimulus)
        table_whole_timeseriesdata = self.read.pull_whole_datatable(a_pickedepoch)
        print table_whole_timeseriesdata
        self.assertEqual ( len(table_whole_timeseriesdata),
                           Reader.get_totalno_epochs(self.mynwbfile_stimulus) )

    @unittest.skip("reason for skipping")
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
