#/managers/operatorsVisualize/readerTest.py
import unittest

import StringIO #import io for Python3

import uuid
import os
import sys
# import modules for other directories
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
# this is required for

pwd = os.getcwd()
os.chdir(os.path.dirname(os.path.dirname(pwd))) # this moves you up to ~/cerebmodels
rootwd = os.getcwd() # save the path ~/cerebmodels
from models.cells.modelDummyTest import DummyCell
os.chdir(pwd)

import numpy
from managers.operatorsTranscribe.fabricator import Fabricator as fab
from pynwb import NWBHDF5IO

from reader import Reader


class ReaderTest(unittest.TestCase):

    def setUp(self):
        self.pwd = os.getcwd()
        # Create two files with/without stimulus
        #fab = Fabricator() # NOTE: Reader() is an exception for not instantiating
        os.chdir(rootwd)
        chosenmodel = DummyCell()
        os.chdir(pwd)
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
        updated_mynwbfile_nostimulus = fab.affix_nwbseries_to_nwbfile(nwbts=nwbts_nostimulus,
                                                                      nwbfile=mynwbfile_nostimulus)
        updated_mynwbfile_stimulus = fab.affix_nwbseries_to_nwbfile(nwbts=nwbts_stimulus,
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
        # loads nwbfile, extracts modelname, modelscale & instantiate model
        os.chdir(rootwd)
        reader_io_nostimulus = Reader(pwd+os.sep+"mynwbfile_nostimulus.h5")
        reader_io_stimulus = Reader(pwd+os.sep+"mynwbfile_stimulus.h5")
        os.chdir(pwd)
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
        # gives you session of the nwbfile
        os.chdir(rootwd)
        reader_io_nostimulus = Reader(pwd+os.sep+"mynwbfile_nostimulus.h5")
        os.chdir(pwd)
        reader_io_nostimulus.session_info() # pretty prints table
        reader_io_nostimulus.closefile()

    #@unittest.skip("reason for skipping")
    def test_3_pull_epochindices_chosenregion(self):
        os.chdir(rootwd)
        reader_io_stimulus = Reader(pwd+os.sep+"mynwbfile_stimulus.h5")
        os.chdir(pwd)
        epoch_indices_soma = reader_io_stimulus.pull_epochindices_chosenregion('soma')
        epoch_indices_axon = reader_io_stimulus.pull_epochindices_chosenregion('axon')
        #print epoch_indices_soma
        #print epoch_indices_axon
        self.assertNotEqual( epoch_indices_soma, epoch_indices_axon )
        reader_io_stimulus.closefile()

    #@unittest.skip("reason for skipping")
    def test_4_pull_epochid(self):
        os.chdir(rootwd)
        reader_io_stimulus = Reader(pwd+os.sep+"mynwbfile_stimulus.h5")
        os.chdir(pwd)
        epoch_indices_soma = reader_io_stimulus.pull_epochindices_chosenregion('soma')
        epoch_indices_axon = reader_io_stimulus.pull_epochindices_chosenregion('axon')
        epoch_id_soma = reader_io_stimulus.pull_epochid(epoch_indices_soma[0])
        epoch_id_axon = reader_io_stimulus.pull_epochid(epoch_indices_axon[0])
        #print epoch_indices_soma, epoch_id_soma
        #print epoch_indices_soma, reader_io_stimulus.pull_epochid(epoch_indices_soma[1])
        #print epoch_indices_axon, epoch_id_axon
        #print reader_io_stimulus.nwbfile.epochs.epochs.data
        #print reader_io_stimulus.nwbfile.epochs.epochs.data[0]
        #print reader_io_stimulus.nwbfile.epochs.epochs.data[1][2]
        self.assertNotEqual( epoch_id_soma, epoch_id_axon )
        reader_io_stimulus.closefile()

    #@unittest.skip("reason for skipping")
    def test_5_drawout_orderedepochs(self):
        os.chdir(rootwd)
        reader_io_stimulus = Reader(pwd+os.sep+"mynwbfile_stimulus.h5")
        os.chdir(pwd)
        orderedepochs_soma = reader_io_stimulus.drawout_orderedepochs('soma')
        #print orderedepochs_soma
        #print len(orderedepochs_soma)
        #to compare
        compare1 = [ orderedepochs_soma[0][1], orderedepochs_soma[1][1] ]
        self.assertEqual( compare1, [0, 1] )
        reader_io_stimulus.closefile()

    #@unittest.skip("reason for skipping")
    def test_6_get_epoch(self):
        # To get an epoch
        os.chdir(rootwd)
        reader_io_stimulus = Reader(pwd+os.sep+"mynwbfile_stimulus.h5")
        os.chdir(pwd)
        orderedepochs_soma = reader_io_stimulus.drawout_orderedepochs('soma') # drawout orderedepochs
        epochs = []
        for i in range(len(orderedepochs_soma)):
            epoch_id = orderedepochs_soma[i][1]
            epochs.append( Reader.get_epoch(epoch_id, orderedepochs_soma) ) # get epoch
        #print epoch_ids_soma
        #print epochs
        #print epochs[0]
        #print epochs[1]
        self.assertNotEqual( epochs[0], epochs[1] )
        reader_io_stimulus.closefile()

    #@unittest.skip("reason for skipping")
    def test_7_get_epoch_start_stop_times(self):
        os.chdir(rootwd)
        reader_io_nostimulus = Reader(pwd+os.sep+"mynwbfile_nostimulus.h5")
        os.chdir(pwd)
        orderedepochs_soma = reader_io_nostimulus.drawout_orderedepochs('soma') #drawout orderedepoch
        orderedepochs_axon = reader_io_nostimulus.drawout_orderedepochs('axon')
        epochtuple_soma = Reader.get_epoch(0, orderedepochs_soma) # get epoch
        epochtuple_axon = Reader.get_epoch(0, orderedepochs_axon)
        #
        #print epochtuple_soma
        strt_soma, stop_soma = Reader.get_epoch_start_stop_times(epochtuple_soma) #get epoch t0, tend
        strt_axon, stop_axon = Reader.get_epoch_start_stop_times(epochtuple_axon)
        #print strt_soma, stop_soma
        #print strt_axon, stop_axon
        self.assertEqual( [ strt_soma, stop_soma ], [ strt_axon, stop_axon ] )
        reader_io_nostimulus.closefile()

    #@unittest.skip("reason for skipping")
    def test_8_get_epoch_start_stop_times(self):
        os.chdir(rootwd)
        reader_io_stimulus = Reader(pwd+os.sep+"mynwbfile_stimulus.h5")
        os.chdir(pwd)
        orderedepochs_soma = reader_io_stimulus.drawout_orderedepochs('soma') #drawout orderedepoch
        epochtuple_soma0 = Reader.get_epoch(0, orderedepochs_soma) # get epoch
        epochtuple_soma1 = Reader.get_epoch(1, orderedepochs_soma)
        #
        #print epochtuple_soma
        strt_soma0, stop_soma0 = Reader.get_epoch_start_stop_times(epochtuple_soma0) #epoch t0, tend
        strt_soma1, stop_soma1 = Reader.get_epoch_start_stop_times(epochtuple_soma1)
        print orderedepochs_soma
        print strt_soma0, stop_soma0
        print strt_soma1, stop_soma1
        self.assertNotEqual( [ strt_soma0, stop_soma0 ], [ strt_soma1, stop_soma1 ] )
        reader_io_stimulus.closefile()

    @unittest.skip("reason for skipping")
    def test_8_get_epochdescription(self):
        os.chdir(rootwd)
        reader_io_stimulus = Reader(pwd+os.sep+"mynwbfile_stimulus.h5")
        os.chdir(pwd)
        orderedepochs_soma = reader_io_stimulus.drawout_orderedepochs('soma') #drawout ordered epoch
        epochtuple_0soma = Reader.get_epoch(0, orderedepochs_soma) # get epoch
        epochtuple_1soma = Reader.get_epoch(1, orderedepochs_soma)
        #
        #print epochtuple_0soma
        descrip0 = Reader.get_epoch_description(epochtuple_0soma) # get epoch description
        descrip1 = Reader.get_epoch_description(epochtuple_1soma)
        #print descrip0, descrip1
        self.assertNotEqual( descrip0, descrip1 )
        reader_io_stimulus.closefile()

    @unittest.skip("reason for skipping")
    def test_9_get_epoch_data_timestamps(self):
        # also tests get_timeseries_stage1, get_timeseries_object
        os.chdir(rootwd)
        reader_io_nostimulus = Reader(pwd+os.sep+"mynwbfile_nostimulus.h5")
        os.chdir(pwd)
        #
        orderedepochs_soma = reader_io_nostimulus.drawout_orderedepochs('soma')#drawout ordered epoch
        epoch_id_soma = 0
        epochtuple_soma = Reader.get_epoch(epoch_id_soma, orderedepochs_soma) # get epoch
        #
        orderedepochs_axon = reader_io_nostimulus.drawout_orderedepochs('axon')#drawout ordered epoch
        epoch_id_axon = 0
        epochtuple_axon = Reader.get_epoch(epoch_id_axon, orderedepochs_axon) # get epoch
        #
        ts_soma = reader_io_nostimulus.pull_epoch_nwbts(epochtuple_soma)
        ts_axon = reader_io_nostimulus.pull_epoch_nwbts(epochtuple_axon)
        #
        a = all(boolean == True for boolean in 
                                (ts_soma.timestamps.value == ts_axon.timestamps.value) )
        b = all(boolean == True for boolean in 
                                (ts_soma.data.value != ts_axon.data.value) )
        self.assertTrue( a and b is True )
        reader_io_nostimulus.closefile()

    @unittest.skip("reason for skipping")
    def test_10_pull_whole_datatable(self):
        os.chdir(rootwd)
        reader_io_nostimulus = Reader(pwd+os.sep+"mynwbfile_nostimulus.h5")
        reader_io_stimulus = Reader(pwd+os.sep+"mynwbfile_stimulus.h5")
        os.chdir(pwd)
        #
        stimulus_nwbts = reader_io_stimulus.pull_stimulus_nwbts()
        nostimulus_nwbts = reader_io_nostimulus.pull_stimulus_nwbts()
        #print stimulus_nwbts
        a = all(boolean == False for boolean in
                                 (stimulus_nwbts.data.value == stimulus_nwbts.timestamps.value) )
        b = (nostimulus_nwbts == "Model is not stimulated")
        #
        self.assertTrue( a and b is True )
        reader_io_stimulus.closefile()
        reader_io_nostimulus.closefile()

if __name__ == '__main__':
    unittest.main()
