# ~/managers/operatorsVisualize/reader.py
import os
import sys
import importlib
from collections import namedtuple

#import modules from other directories
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
# this is required for
from utilities import UsefulUtils as uu

from pynwb import NWBHDF5IO
import numpy

class Reader(object):
    """Operators working under VisualizeManager

    Useful methods:
    load_model # if the model is not already loaded (see use case, below)
    drawout_orderedepochs
    get_tuple_for_epoch
    get_timestamps_for_epoch
    get_datavalues_for_epoch
    get_stimulus
    get_timestamps

    Use Cases:
    loading the file
        loadedfile = Reader("path/to/HDF5file")
    not necessary but recommended is
        loadedfile.chosenmodel = instantiated model
     or loadedfile.load_model()
    visualize high-level metadata
        loadedfile.session_info()
    get 'all' epochs for a particular 'cell region'
        x = loadedfile.drawout_orderedepochs('soma')
    get timestamp values for 'an epoch'
        loadedfile.get_timestamps_for_epoch(epoch_id, x)
    get data values for 'an epoch'
        loadedfile.get_datavalues_for_epoch(epoch_id, x)
    get stimulus values
        stim = loadedfile.get_stimulus()
        stim.data.value
    get timestamp value (not just for an epoch)
        tstamps = loadedfile.get_timestamps()
        tstamps.value
    get additional metadata
        for timestamps and data values
            epochtuple = loadedfile.get_tuple_for_epoch(epoch_id, x)
            then,
            epochtuple[2].description
            epochtuple[2].unit
            epochtuple[2].timestamps_unit
        for stimulus
            stim.source
            stim.comment
            stim.unit (also stim.timestamps_unit)

    NOTE:
    For x = loadedfile.drawout_orderedepochs('soma')
        x[epoch_id][1] = epoch_id
        x[epoch_id][0] = its index in list of epochs for all regions (not just soma)
    Thus,
        x[epoch_id][1] = loadedfile.nwbfile.epochs.epochs.data[ x[epoch_id][0] ]
    Notice that,
        x[epoch_id][0] returns index of this epoch in list of all region epochs
        x[epoch_id][1] returns index of this epoch in list of a region epochs
    Therefore to differentiate them
        x[epoch_id][0] is referred to as index
        x[epoch_id][1] is referred to as epoch id
    """

    def __init__(self,filepath):
        self.io = NWBHDF5IO(filepath)
        self.nwbfile = self.io.read()
        self.extract_modelname_modelscale()
        #self.load_model()

    def closefile(self):
        self.io.close()

    def extract_modelname_modelscale(self):
        """method called by __init__
        """
        # in cerebmodels the tag of each epoch is a string of the form
        # 'No_epoch_responses, index, cellregion, modelname, modelscale, epoch<index>cellregion'
        epoch_tags_list = self.nwbfile.epochs.epochs.data[0][2].split(",")
        self.modelname = epoch_tags_list[3]
        self.modelscale = epoch_tags_list[4]
        
    def load_model(self):
        """method called by __init__
        """
        modelmodule = importlib.import_module("models."+self.modelscale+".model"+self.modelname)
        pickedmodel = getattr(modelmodule,
                              uu.classesinmodule(modelmodule)[0].__name__)
        self.chosenmodel = pickedmodel()

    def compute_total_epoch_id(self):                             
        self.total_epoch_no = len(self.nwbfile.epochs.epochs.data)
        self.total_regions = len(self.chosenmodel.regions)
        self.total_epoch_id = self.total_epoch_no/self.total_regions

    def session_info(self):
        """method displaying the session of loaded nwbfile as table
        """
        Row = namedtuple('Row', ['metadata_background', 'metadata'])
        data1 = Row("Where is the data from?", self.nwbfile.source)
        data2 = Row("How was the data generated?", self.nwbfile.session_description)
        data3 = Row("When did the simulation start?", self.nwbfile.session_start_time)
        data4 = Row("What is the session id?", self.nwbfile.session_id)
        uu.pprinttable([data1, data2, data3, data4])

    def pull_epochindices_chosenregion(self, chosenregion):
        """method returns the list of ascending indices for all epochs OF MODEL.
        This is called by extract_orderedepochs(chosenregion).
        """
        indices = []
        for i in range(len(self.nwbfile.epochs.epochs.data)):
            a_taglist = self.nwbfile.epochs.epochs.data[i][2].split(",")
            a_region = a_taglist[2]
            if a_region == chosenregion:
                indices.append(i)
        return sorted(indices) # ascending order

    def pull_epochid(self, epochindx):
        """method returns the list of ascending id for all epochs OF model REGION.
        """
        a_taglist = self.nwbfile.epochs.epochs.data[epochindx][2].split(",")
        return int(a_taglist[1])

    def drawout_orderedepochs(self, chosenregion):
        """method returns all the epochs for a desired model-region as ordered list.
        
        Returned value:
        [ [0, 0, desiredregion_epoch_0_in_allepochsofmodel],
          [3, 1, desiredregion_epoch_3_in_allepochsofmodel],
          [5, 2, desiredregion_epoch_5_in_allepochsofmodel] ]

        NOTE:
           - most methods in Reader() extracts nwb objects AS-IS
           - this method is an exception where returned value includes index of
             the epoch of the desiredregion; index in all epochs of the model.
           - for each element notice that the first two numbers are integers such that:
             * first number is the index of the epoch in question of desired region
             * index => index in list of epochs from all the regions
             * second number is the epoch_id, thus ordering is based on this.
        """
        # https://stackoverflow.com/questions/2177590/how-can-i-reorder-a-list
        indxlist = self.pull_epochindices_chosenregion(chosenregion)
        #return [ [i, self.pull_epochid(i), self.nwbfile.epochs.epochs.data[i]]
        #                                                     for i in indxlist ]
        orderedepochs = []
        i = 0
        while len(orderedepochs) < len(indxlist):
            for indx in indxlist:
                if self.pull_epochid(indx)==i:
                    orderedepochs.append(
                          [indx, i, self.nwbfile.epochs.epochs.data[indx]] )
            i += 1
        return orderedepochs

    @staticmethod
    def get_tuple_for_epoch(epoch_id, orderedepochs):
        """method returns array which is of the form
        (tstartindex, counts, TimeSeriesObject)

        orderedepoch[0]          first, ie, epoch
        orderedepoch[0][2]       returns root tuple
        orderedepoch[0][2][3]    return array
        orderedepoch[0][2][3][0] returns final/only tuple in the array
        """
        return orderedepochs[epoch_id][2][3][0]

    @classmethod
    def get_timestamps_for_epoch(cls, epoch_id, orderedepochs):
        """method returns timestamp values for desired epoch_id
        This is done by stripping from the whole timestamps.
        """
        epochtuple = cls.get_tuple_for_epoch(epoch_id, orderedepochs)
        return [ epochtuple[2].timestamps.value[i]
                 for i in numpy.arange( epochtuple[0], # index for tstart
                                        epochtuple[0]+epochtuple[1] ) ] # to total counts

    @classmethod
    def get_datavalues_for_epoch(cls, epoch_id, orderedepochs):
        """method returns data values for desired epoch_id
        This is done by stripping from the whole data.
        """
        epochtuple = cls.get_tuple_for_epoch(epoch_id, orderedepochs)
        return [ epochtuple[2].data.value[i]
                 for i in numpy.arange( epochtuple[0], # index for tstart
                                        epochtuple[0]+epochtuple[1] ) ] # to total counts

    def get_datavalues(self):
        """method returns data values from t0 till end of simulation

        print reader_io.nwbfile.epochs.epochs.data # all epochs
        print reader_io.nwbfile.epochs.epochs.data[i][3][0] # tuple of i'th epoch
        print reader_io.nwbfile.epochs.epochs.data[i][3][0][2] # timeseries object

        Usecase:
        x = reader_io.get_datavalues()
        """
        epoch_id = 0 # does not matter as long as its an id that exists
        return self.nwbfile.epochs.epochs.data[epoch_id][3][0][2].data.value

    def get_stimulus(self):
        """method returns stimulus in the first one out the three below
        
        print reader_io_stim.nwbfile.stimulus["DummyTest_stimulus"]
        print reader_io_stim.nwbfile.stimulus["DummyTest_stimulus"].data
        print reader_io_stim.nwbfile.stimulus["DummyTest_stimulus"].data.value

        Usecase:
        x = reader_io_stim.get_stimulus()
        x.data
        x.data.value
        """
        nospacename = self.chosenmodel.name.replace(" ", "")
        return self.nwbfile.stimulus[nospacename+"_stimulus"]

    def get_timestamps(self):
        """method returns timestamps

        No epoch_id, cell_region and stimulus/nostimulus is needed to get timestamps
        """
        return self.nwbfile.epochs.epochs.data[0][3][0][2].timestamps #epoch_id=0

    @staticmethod
    def get_epoch(epoch_id, orderedepochs):
        """method returns all the epochs for a desired model-region as ordered list.
        
        Argument:
        [ [0, 0, desiredregion_epoch_0_in_allepochsofmodel],
          [3, 1, desiredregion_epoch_3_in_allepochsofmodel],
          [5, 2, desiredregion_epoch_5_in_allepochsofmodel] ]

        NOTE:
           - [<epoch_indx>, <epoch_id>, <epoch>]
        """
        for i in range(len(orderedepochs)):
            an_epochtuple = orderedepochs[i][2]
            # ('start_time', 'stop_time', 'tags', 'timeseries', 'description')
            a_taglist = an_epochtuple[2].split(",")
            # 'X_epoch_responses, P, region, modelname, modelscale, epoch<P><region>'
            a_id = int(a_taglist[1])
            if a_id==epoch_id:
                # ('start_time', 'stop_time', 'tags', 'timeseries', 'description')
                return an_epochtuple # epochtuple

    @staticmethod
    def get_description_epoch(epoch_id, orderedepochs):
        """method returns array which is of the form
        (tstartindex, counts, TimeSeriesObject)

        orderedepoch[0]          first, ie, epoch
        orderedepoch[0][2]       returns root tuple
        orderedepoch[0][2][3]    return array
        orderedepoch[0][2][3][0] returns final/only tuple in the array
        """
        return orderedepochs[epoch_id][2][4]
