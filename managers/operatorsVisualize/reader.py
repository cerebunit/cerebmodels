# ~/managers/operatorsTranscribe/reader.py
import os
import sys
import importlib
from collections import namedtuple

#import modules from other directories
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
# this is required for
from utilities import UsefulUtils as uu

from pynwb import NWBHDF5IO

class Reader(object):
    """Operators working under TranscribeManager

    Available methods:
    pick_an_epoch
    extract_tsobject_of_pickedepoch

    Misc. but useful methods:
    pull_epoch_id
    get_epoch_no
    """
    #def __init__(self):
    #    pass

    def __init__(self,filepath):
        self.io = NWBHDF5IO(filepath)
        self.nwbfile = self.io.read()
        self.extract_modelname_modelscale()
        self.load_model()

    def closefile(self):
        self.io.close()

    def extract_modelname_modelscale(self):
        # in cerebmodels the tag of each epoch is a string of the form
        # 'No_epoch_responses, index, cellregion, modelname, modelscale, epoch<index>cellregion'
        epoch_tags_list = self.nwbfile.epochs.epochs.data[0][2].split(",")
        self.modelname = epoch_tags_list[3]
        self.modelscale = epoch_tags_list[4]
        
    def load_model(self):
        modelmodule = importlib.import_module("models."+self.modelscale+".model"+self.modelname)
        pickedmodel = getattr(modelmodule,
                              uu.classesinmodule(modelmodule)[0].__name__)
        self.chosenmodel = pickedmodel()

    def compute_total_epoch_id(self):                             
        self.total_epoch_no = len(self.nwbfile.epochs.epochs.data)
        self.total_regions = len(self.chosenmodel.regions)
        self.total_epoch_id = self.total_epoch_no/self.total_regions

    def session_info(self):
        Row = namedtuple('Row', ['metadata_background', 'metadata'])
        data1 = Row("Where is the data from?", self.nwbfile.source)
        data2 = Row("How was the data generated?", self.nwbfile.session_description)
        data3 = Row("When did the simulation start?", self.nwbfile.session_start_time)
        data4 = Row("What is the session id?", self.nwbfile.session_id)
        uu.pprinttable([data1, data2, data3, data4])

    #@classmethod
    def get_epochindices_chosenregion(self, chosenregion):
        indices = []
        for i in range(len(self.nwbfile.epochs.epochs.data)):
            a_taglist = self.nwbfile.epochs.epochs.data[i][2].split(",")
            a_region = a_taglist[2]
            if a_region == chosenregion:
                indices.append(i)
        return sorted(indices) # ascending order

    #@classmethod
    def extract_orderedepochs(self, chosenregion):
        # https://stackoverflow.com/questions/2177590/how-can-i-reorder-a-list
        indxlist = self.get_epochindices_chosenregion(chosenregion)
        return [ [i, self.nwbfile.epochs.epochs.data[i]] for i in indxlist ]

    def get_epochids_chosenregion(self, chosenregion):
        epoch_ids = []
        for i in range(len(self.nwbfile.epochs.epochs.data)):
            a_taglist = self.nwbfile.epochs.epochs.data[i][2].split(",")
            a_region = a_taglist[2]
            if a_region == chosenregion:
                epoch_ids.append( int(a_taglist[1]) )
        return sorted(epoch_ids) # ascending order

    @staticmethod
    def extract_epoch(epoch_id, orderedepochs):
        for i in range(len(orderedepochs)):
            # ('start_time', 'stop_time', 'tags', 'timeseries', 'description')
            a_taglist = orderedepochs[i][1][2].split(",")
            # 'X_epoch_responses, P, region, modelname, modelscale, epoch<P><region>'
            a_id = int(a_taglist[1])
            if a_id==epoch_id:
                # ('start_time', 'stop_time', 'tags', 'timeseries', 'description')
                return orderedepochs[i][1] # epochtuple

    @staticmethod
    def get_epoch_start_stop_times(epochtuple):
        # strt, stop = extract_epoch_start_stop_times(epochtuple)
        return [epochtuple[0], epochtuple[1]]

    @staticmethod
    def get_epochdescription(epochtuple):
        return epochtuple[4]

    @staticmethod
    def get_epoch_data_timestamps(epochindx, epochtuple):
        return [epochtuple[3].data.data[epochindx][2].data,
                epochtuple[3].data.data[epochindx][2].timestamps]
