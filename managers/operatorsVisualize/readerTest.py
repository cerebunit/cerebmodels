#/managers/operatorsVisualize/readerTest.py
import unittest

import StringIO #import io for Python3

import shutil
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
from executive import ExecutiveControl
from managers.managerFiling import FilingManager as fm
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
        self.chosenmodel = DummyCell()
        os.chdir(pwd)
        #
        self.ec = ExecutiveControl()
        #
        if os.path.isdir(pwd + os.sep + "responses"):
            shutil.rmtree("responses")
        #
        runtimeparam = {"dt": 0.1, "celsius": 30, "tstop": 200.0, "v_init": 65}
        stimparam = {"type": ["current", "IClamp"],
                     "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                   {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                     "tstop": runtimeparam["tstop"] }
        #
        # Write for stimulus
        self.ec.launch_model(parameters = runtimeparam,
                             stimparameters = stimparam,
                             stimloc = self.chosenmodel.cell.soma,
                             onmodel = self.chosenmodel)
        self.ec.save_response()
        # Get filename
        self.file_stim = fm.show_filenames_with_path(["responses", "cells", "DummyTest"])
        # save for comparison
        self.stimulus_for_comparison = numpy.array(self.ec.recordings["stimulus"])
        #
        # Write for nostimulus
        self.ec.launch_model(parameters = runtimeparam,
                             onmodel = self.chosenmodel)
        self.ec.save_response()
        # Get filename
        self.file_nostim = fm.show_filenames_with_path(["responses", "cells", "DummyTest"])
        for key in self.file_stim:
            del self.file_nostim[key]

    #@unittest.skip("reason for skipping")
    def test_1_init(self):
        # loads nwbfile, extracts modelname, modelscale & instantiate model
        os.chdir(rootwd)
        for key in self.file_nostim:
            reader_io_nostim = Reader(self.file_nostim[key])
        for key in self.file_stim:
            reader_io_stim = Reader(self.file_stim[key])
        os.chdir(pwd)
        #
        reader_io_nostim.chosenmodel = self.chosenmodel
        reader_io_stim.chosenmodel = self.chosenmodel
        #print self.chosenmodel.name
        # this tests extract_modelname_modelscale & load_model
        compare1 = [ reader_io_nostim.modelname,  # output of 
                     reader_io_nostim.modelscale ]# extract_modelname_modelscale()
        compare2 = [ reader_io_stim.chosenmodel.modelname,  # output of
                     reader_io_stim.chosenmodel.modelscale ]# load_model()
        self.assertEqual( compare1, compare2 )
        reader_io_nostim.closefile()
        reader_io_stim.closefile()

    #@unittest.skip("reason for skipping")
    def test_2_visualizetable(self):
        # gives you session of the nwbfile
        os.chdir(rootwd)
        for key in self.file_nostim:
            reader_io_nostim = Reader(self.file_nostim[key])
        os.chdir(pwd)
        reader_io_nostim.session_info() # pretty prints table
        reader_io_nostim.closefile()

    #@unittest.skip("reason for skipping")
    def test_3_pull_epochindices_chosenregion(self):
        os.chdir(rootwd)
        for key in self.file_stim:
            reader_io_stim = Reader(self.file_stim[key])
        os.chdir(pwd)
        epoch_indices_soma = reader_io_stim.pull_epochindices_chosenregion('soma')
        epoch_indices_axon = reader_io_stim.pull_epochindices_chosenregion('axon')
        #print epoch_indices_soma
        #print epoch_indices_axon
        self.assertNotEqual( epoch_indices_soma, epoch_indices_axon )
        reader_io_stim.closefile()
        #shutil.rmtree("responses")

    #@unittest.skip("reason for skipping")
    def test_4_pull_epochid(self):
        os.chdir(rootwd)
        for key in self.file_stim:
            reader_io_stim = Reader(self.file_stim[key])
        os.chdir(pwd)
        epoch_indices_soma = reader_io_stim.pull_epochindices_chosenregion('soma')
        epoch_indices_axon = reader_io_stim.pull_epochindices_chosenregion('axon')
        epoch_ids_soma = [ reader_io_stim.pull_epochid(epoch_indices_soma[0]),
                           reader_io_stim.pull_epochid(epoch_indices_soma[1]),
                           reader_io_stim.pull_epochid(epoch_indices_soma[2]),
                           reader_io_stim.pull_epochid(epoch_indices_soma[3]) ]
        epoch_ids_axon = [ reader_io_stim.pull_epochid(epoch_indices_axon[0]),
                           reader_io_stim.pull_epochid(epoch_indices_axon[1]),
                           reader_io_stim.pull_epochid(epoch_indices_axon[2]),
                           reader_io_stim.pull_epochid(epoch_indices_axon[3]) ]
        #print epoch_indices_soma
        #print epoch_indices_axon
        #print epoch_ids_soma
        #print epoch_ids_axon
        #print len(reader_io_stim.nwbfile.epochs.epochs.data)
        #print reader_io_stim.nwbfile.epochs.epochs.data[0]#[3][0]
        #print reader_io_stim.nwbfile.epochs.epochs.data[3]#[3][0]
        #print reader_io_stim.nwbfile.epochs.epochs.data[4]#[3][0]
        #print reader_io_stim.nwbfile.epochs.epochs.data[5]#[3][0]
        #print epoch_indices_soma, epoch_id_soma
        #print epoch_indices_soma, reader_io_stimulus.pull_epochid(epoch_indices_soma[1])
        #print epoch_indices_axon, epoch_id_axon
        #print reader_io_stimulus.nwbfile.epochs.epochs.data
        #print reader_io_stimulus.nwbfile.epochs.epochs.data[0]
        #print reader_io_stimulus.nwbfile.epochs.epochs.data[1][2]
        self.assertNotEqual( epoch_ids_soma, epoch_ids_axon )
        reader_io_stim.closefile()

    #@unittest.skip("reason for skipping")
    def test_5_drawout_orderedepochs(self):
        os.chdir(rootwd)
        for key in self.file_stim:
            reader_io_stim = Reader(self.file_stim[key])
        os.chdir(pwd)
        orderedepochs_soma = reader_io_stim.drawout_orderedepochs('soma')
        #print orderedepochs_soma
        #print len(orderedepochs_soma)
        #print orderedepochs_soma[0]          # first, i.e, epoch
        #print orderedepochs_soma[0][2]       # get root tuple
        #print orderedepochs_soma[0][2][3]    # get array
        #print orderedepochs_soma[0][2][3][0] # take out tuple from the array
        #print orderedepochs_soma[0][2][3][0][2] # take out timeseries object from tuple
        #print orderedepochs_soma[0][2][3][0][2].data.value
        #print type(orderedepochs_soma[0][2][3][0][2].data.value)
        #print orderedepochs_soma[0][2][3][0][2].timestamps.value
        #print len([ orderedepochs_soma[0][2][3][0][2].timestamps.value[i]
        #          for i in numpy.arange(orderedepochs_soma[0][2][3][0][0],
        #                                orderedepochs_soma[0][2][3][0][1]) ])
        #print orderedepochs_soma[0][1]
        #print orderedepochs_soma[0][0]
        #print reader_io_stim.nwbfile.epochs.epochs.data[orderedepochs_soma[0][0]]
        #to compare
        compare1 = [ orderedepochs_soma[0][1], orderedepochs_soma[1][1] ]
        self.assertEqual( compare1, [0, 1] )
        reader_io_stim.closefile()

    #@unittest.skip("reason for skipping")
    def test_6_get_tuple_for_epoch(self):
        # To get an epoch
        os.chdir(rootwd)
        for key in self.file_stim:
            reader_io_stim = Reader(self.file_stim[key])
        os.chdir(pwd)
        orderedepochs_soma = reader_io_stim.drawout_orderedepochs('soma') # drawout orderedepochs
        #epochs = []
        #for i in range(len(orderedepochs_soma)):
        #    epoch_id = orderedepochs_soma[i][1]
        #    epochs.append( Reader.get_array_for_epoch(epoch_id, orderedepochs_soma) ) # get epoch
        #print epochs
        #print epochs[0]
        #print epochs[1]
        epoch_id = 0
        epochtuple = Reader.get_tuple_for_epoch(epoch_id, orderedepochs_soma)
        #print epochtuple
        #print epochtuple[2].timestamps_unit #description/unit/time_unit/timestamps_unit
        self.assertNotEqual( epochtuple[0], # tstart index
                             epochtuple[1] )# counts
        #self.assertNotEqual( epochs[0], epochs[1] )
        reader_io_stim.closefile()

    #@unittest.skip("reason for skipping")
    def test_7_get_timestamps_for_epoch(self):
        os.chdir(rootwd)
        for key in self.file_nostim:
            reader_io_nostim = Reader(self.file_nostim[key])
        os.chdir(pwd)
        orderedepochs_soma = reader_io_nostim.drawout_orderedepochs('soma') #drawout orderedepoch
        orderedepochs_axon = reader_io_nostim.drawout_orderedepochs('axon')
        epoch_id = 0
        times_soma = reader_io_nostim.get_timestamps_for_epoch(epoch_id, orderedepochs_soma)
        times_axon = reader_io_nostim.get_timestamps_for_epoch(epoch_id, orderedepochs_axon)
        #
        self.assertEqual( [len(times_soma), times_soma],
                          [len(times_axon), times_axon] )
        reader_io_nostim.closefile()

    #@unittest.skip("reason for skipping")
    def test_8_get_datavalues_for_epoch(self):
        os.chdir(rootwd)
        for key in self.file_stim:
            reader_io_stim = Reader(self.file_stim[key])
        os.chdir(pwd)
        orderedepochs_soma = reader_io_stim.drawout_orderedepochs('soma') #drawout orderedepoch
        orderedepochs_axon = reader_io_stim.drawout_orderedepochs('axon')
        epoch_id = 1
        data_soma = reader_io_stim.get_datavalues_for_epoch(epoch_id, orderedepochs_soma)
        data_axon = reader_io_stim.get_datavalues_for_epoch(epoch_id, orderedepochs_axon)
        #
        self.assertNotEqual( data_soma, data_axon )
        reader_io_stim.closefile()

    #@unittest.skip("reason for skipping")
    def test_9_get_stimulus(self):
        os.chdir(rootwd)
        for key in self.file_stim:
            reader_io_stim = Reader(self.file_stim[key])
        os.chdir(pwd)
        #print help(reader_io_stim.nwbfile)
        #print reader_io_stim.nwbfile.get_stimulus["DummyTest_stimulus"]
        #print help(reader_io_stim.nwbfile)
        #print reader_io_stim.nwbfile.acquisition
        #print reader_io_stim.nwbfile.stimulus
        #print reader_io_stim.nwbfile
        #
        #print reader_io_stim.nwbfile.stimulus
        #print reader_io_stim.nwbfile.stimulus["DummyTest_stimulus"]
        #print reader_io_stim.nwbfile.stimulus["DummyTest_stimulus"].data
        #print reader_io_stim.nwbfile.stimulus["DummyTest_stimulus"].data.value
        reader_io_stim.chosenmodel = self.chosenmodel
        stimulus = reader_io_stim.get_stimulus()
        #print stimulus
        #print stimulus.data
        #print stimulus.timestamps
        a = all(boolean == True
                for boolean in stimulus.data.value == self.stimulus_for_comparison)
        self.assertTrue( a is True )
        reader_io_stim.closefile()

    #@unittest.skip("reason for skipping")
    def test_x_get_stimulus(self):
        os.chdir(rootwd)
        for key in self.file_nostim:
            reader_io_nostim = Reader(self.file_nostim[key])
        for key in self.file_stim:
            reader_io_stim = Reader(self.file_stim[key])
        os.chdir(pwd)
        reader_io_stim.chosenmodel = self.chosenmodel
        stimulus = reader_io_stim.get_stimulus()
        timestamps = reader_io_nostim.get_timestamps()
        #print stimulus
        #print stimulus.data
        #print stimulus.timestamps.value
        #print timestamps.value
        #print help(timestamps)
        a = all(boolean == True
                for boolean in stimulus.timestamps.value == timestamps.value)
        self.assertTrue( a is True )
        reader_io_stim.closefile()

    #@unittest.skip("reason for skipping")
    def test_xi_get_description_epoch(self):
        #print "test XI"
        os.chdir(rootwd)
        for key in self.file_stim:
            reader_io_stim = Reader(self.file_stim[key])
        os.chdir(pwd)
        orderedepochs_soma = reader_io_stim.drawout_orderedepochs('soma') #drawout ordered epoch
        descrip_0soma = Reader.get_description_epoch(0, orderedepochs_soma) # get epoch
        descrip_1soma = Reader.get_description_epoch(1, orderedepochs_soma)
        #
        #print descrip_0soma
        #print descrip_1soma
        self.assertNotEqual( descrip_0soma, descrip_1soma )
        reader_io_stim.closefile()
        shutil.rmtree("responses")

if __name__ == '__main__':
    unittest.main()
