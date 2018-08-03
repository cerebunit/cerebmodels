# ~/managers/operatorsTranscribe/fabricator.py

import pynwb

class Reader(object):
    """Operators working under TranscribeManager

    Available methods:
    pick_an_epoch
    extract_tsobject_of_pickedepoch

    Misc. but useful methods:
    pull_epoch_id
    get_epoch_no
    """
    @staticmethod
    def get_totalno_epochs(nwbfile):
        return len(nwbfile.epochs.epochs.data)

    @staticmethod
    def get_any_one_epoch(i, nwbfile):
        """static method called by pick_an_epoch
        """
        return nwbfile.epochs.epochs.data[i]

    @staticmethod
    def get_tags_an_epoch(epoch):
        """static method that returns tags

        Returned value:
        list of the form ['2_epoch_responses', '1', 'axon', 'DummyTest', 'epoch1axon']
        
        NOTE:
           - arrangement of the elements of the list is unique to cerebmodels
               '2_epoch_responses',
               '1',                  => \in {0, 1} of 2 responses FOR A GIVEN REGION
               'axon',               => region = keys in chosenmodel.regions
               'DummyTest',          => modelname
               'epoch1axon'          => epoch_id
        """
        tags = epoch[2]        # string
        return tags.split(",") # now a list

    @classmethod
    def pull_epoch_id(cls, an_epoch):
        """class method called by pick_an_epoch

        Returned value:
        string of the form epoch<i><region>
             i = 0 for first
             region = keys in chosenmodel.regions
                        eg: chosenmodel.regions={"soma":0.0, "axon":0.0}
        NOTE:
           - epoch tag form ('2_epoch_responses', '1', 'axon', 'DummyTest', "epoch1axon")       
           - arrangement of the elements of the list is unique to cerebmodels
               '2_epoch_responses',
               '1',                  => \in {0, 1} of 2 responses FOR A GIVEN REGION
               'axon',               => region = keys in chosenmodel.regions
               'DummyTest',          => modelname
               'epoch1axon'          => epoch_id
        """
        tags = cls.get_tags_an_epoch(an_epoch)
        return tags[-1]  #[int(tags[1]), tags[2]]

    def pick_an_epoch(self, epoch_id=None, nwbfile=None):
        """method that picks out the epoch of a given epoch<i><region> id from nwbfile

        Keyword arguments:
        epoch_id -- string of the form epoch<i><region>
        nwbfile -- a loaded pynwb.file.NWBFile

        Returned Value:
        tuple of the form ('start_time', 'stop_time', 'tags', 'timeseries', 'description')
          Eg:
             (0.0, 200.0,
              '1_epoch_responses,0,soma,DummyTest,epoch0soma',
              <pynwb.form.data_utils.ListSlicer object at 0x7f214a3da6d0>,
              'first epoch')
        NOTE:
           - epoch tag form ('2_epoch_responses', '1', 'axon', 'DummyTest', "epoch1axon")       
           - arrangement of the elements of the list is unique to cerebmodels
               '2_epoch_responses',
               '1',                  => \in {0, 1} of 2 responses FOR A GIVEN REGION
               'axon',               => region = keys in chosenmodel.regions
               'DummyTest',          => modelname
               'epoch1axon'          => epoch_id
        """
        for i in range(self.get_totalno_epochs(nwbfile)):
            epoch = self.get_any_one_epoch(i, nwbfile)
            ep_id = self.pull_epoch_id(epoch)
            if (ep_id==epoch_id): #and (ep_region == epoch_region):
                return epoch

    @staticmethod
    def get_epoch_number(epoch, nwbfile):
        """static method that returns no from overall epochs

        NOTE:
           - epoch_id => id out of X responses for a GIVEN REGION
           - epoch_no => no out of N epochs for a GIVEN MODEL
        """
        # https://stackoverflow.com/questions/176918/finding-the-index-of-an-item-given-a-list-containing-it-in-python
        # basis: ["foo", "bar", "baz"].index("bar")
        # nwbfile.epochs.epochs.data => list of all epochs of a GIVEN MODEL
        return nwbfile.epochs.epochs.data.index(epoch)

    @staticmethod
    def get_timeseries_slicer_from_epoch(epoch):
        """static method called by pull_whole_datatable

        Returned value:
        an object,  pynwb.form.data_utils.ListSlicer

        NOTE:
           - extracted from index labeled 'timeseries'
           - but it itself is not the nwb TimeSeries object
           - it contains the TimeSeries object corresponding to the particular epoch
           - this TimeSeries object is itself in a table
           - this table has TimeSeries objects for all the epochs of a GIVEN MODEL
        """
        # ('start_time', 'stop_time', 'tags', 'timeseries', 'description')
        return epoch[3]

    @classmethod
    def pull_whole_datatable(cls, any_epoch):
        """class method evoked by extract_tsobject_of_pickedepoch

        Returned value:
        list whose elements are tuples
              length of the list = total number of epochs of the GIVEN MODEL
              length of each tuple = 3
              last element of each tuple = TimeSeries object corresponds to a particular epoch
           Eg:
             [(1100, 500, <pynwb.base.TimeSeries object at 0x7f75a39143d0>),
              (0, 100, <pynwb.base.TimeSeries object at 0x7f75a3914410>),
              (1100, 500, <pynwb.base.TimeSeries object at 0x7f75a3914410>),
              (0, 100, <pynwb.base.TimeSeries object at 0x7f75a39143d0>)]

        NOTE:
           - the order of the list correspond to the order of nwbfile.epochs.epochs.data
             that is, 2nd element of the list correspond to 2nd epoch
           - here we are dealing with epoch_no NOT epoch_id
           - this only needs to be done once, any single epoch will do.
           - because all nwbepochs for a GIVEN NWBFile
                                   nwbfile.epochs.epochs.data[<any>][3]
             has the same
             data table, nwbfile.epochs.epochs.data[<any>][3].data.data
        """
        any_timeseries_slicer = cls.get_timeseries_slicer_from_epoch(any_epoch)
        return any_timeseries_slicer.data.data

    def extract_tsobject_of_pickedepoch(self, pickedepoch=None, nwbfile=None):
        """method that returns the TimeSeries nwb object for a particular epoch

        Keyword arguments:
        pickedepoch -- tuple of the form
                      ('start_time', 'stop_time', 'tags', 'timeseries', 'description')
                      Eg:  (0.0, 200.0,
                            '1_epoch_responses,0,soma,DummyTest,epoch0soma',
                            <pynwb.form.data_utils.ListSlicer object at 0x7f214a3da6d0>,
                            'first epoch')
        nwbfile -- a loaded pynwb.file.NWBFile

        Returned value:
        a nwb TimeSeries object, nwbts, with the attributes
                nwbts.name, nwbts.source, nwbts.data, nwbts.timestamps, nwbts.unit,
                nwbts.resolution, nwbts.converstion, #nwbts.starting_time, #nwbts.rate,
                nwbts.comment, nwbts.description
        NOTE:
           - due to the bug I reported https://github.com/NeurodataWithoutBorders/pynwb/issues/579 
             the attributes starting_time and rate should not be used
        """
        epoch_no = self.get_epoch_number(pickedepoch, nwbfile)
        ts_allepochs = self.pull_whole_datatable(pickedepoch)
        # ('start_time', 'conversion', 'timeseries') NOTE: ?1st two could change?
        return ts_allepochs[epoch_no][2] # but 3rd element is always ts
