# ~/managers/operatorsTranscribe/fabricator.py
from datetime import datetime

import pynwb
from pynwb import NWBFile
from pynwb import TimeSeries
#from pynwb.icephys import IntracellularElectrode
from pynwb.icephys import CurrentClampSeries, CurrentClampStimulusSeries
from pynwb.icephys import VoltageClampSeries, VoltageClampStimulusSeries
#from pynwb import get_manager
#from pynwb.form.backends.hdf5 import HDF5IO


class Fabricator(object):
    """Operators working under TranscribeManager

    Available methods:
    forfile
    """

    def build_nwbfile( self, filemd ):
        """method for building the nwbfile

        Argument:
        filemd -- dictionary such that
                  { "source": "Where is the data from?",
                    "session_description": "How was the data generated?",
                    "identifier": "a unique ID",
                    "session_start_time": str(time when recording began),
                    "experimenter": "name of the experimenter",
                    "experiment_description": "described experiment",
                    "session_id": "collab ID",
                    "institution": "name of the institution",
                    "lab": "name of the lab" }
        file_to_write = build_nwbfile( file_metadata )

        Returned Value:
        nwbfile with the attributes
               nwbfile.source, nwbfile.session_description, nwbfile.identifier,
               nwbfile.session_start_time, nwbfile.experimenter,
               nwbfile.experiment_description, nwbfile.session_id, nwbfile.lab,
               nwbfile.institution

        Availablle attributes:
        pynwb.file.NWBFile(source, session_description, identifier, session_start_time,
                file_create_date=None, experimenter=None, experiment_description=None,
                session_id=None, institution=None, notes=None, pharmacology=None,
                protocol=None, related_publications=None, slices=None,
                source_script=None, source_script_file_name=None, data_collection=None,
                surgery=None, virus=None, stimulus_notes=None, lab=None,
                acquisition=None, stimulus=None, stimulus_template=None, epochs=None,
                epoch_tags=set(), trials=None, modules=None, ec_electrodes=None,
                ec_electrode_groups=None, ic_electrodes=None, imaging_planes=None,
                ogen_sites=None, devices=None, subject=None)

        Note:
            - call an nwbfile.attribute
            - http://pynwb.readthedocs.io/en/latest/pynwb.file.html#pynwb.file.NWBFile
        """
        return NWBFile( source = filemd["source"],
                        session_description = filemd["session_description"],
                        identifier = filemd["identifier"],
                        session_start_time = filemd["session_start_time"],
                        file_create_date = str(datetime.now()),                   # additions
                        experimenter = filemd["experimenter"],
                        experiment_description = filemd["experiment_description"],
                        session_id = filemd["session_id"],
                        lab = filemd["lab"],
                        institution = filemd["institution"] )

    @staticmethod
    def generic_timeseries(metadata):
        """static method called by construct_nwbseries

        Arguments:
        metadata -- 

        Returned Value:
        nwbts with the attributes
               nwbts.name, nwbts.source, nwbts.data, nwbts.timestamps, nwbts.unit,
               nwbts.resolution, nwbts.converstion, #nwbts.starting_time, #nwbts.rate,
               nwbts.comment, nwbts.description

        Available attributes:
        pynwb.base.TimeSeries(name, source, data=None, unit=None, resolution=0.0,
                              conversion=1.0, timestamps=None, starting_time=None,
                              rate=None, comments='no comments',
                              description='no description', control=None,
                              control_description=None, parent=None)

        NOTE:
            - https://pynwb.readthedocs.io/en/latest/pynwb.base.html#pynwb.base.TimeSeries
            - due to the bug I reported https://github.com/NeurodataWithoutBorders/pynwb/issues/579
              starting_time and rate attributes are not included thus defaults to None
            - pynwb developer says
              's is because you either enter timestamps or rate+starting_time, not all three. We should catch this and raise an error.'
            - so to avoid error in future pynwb version the two attributes are taken out.
        """
        return TimeSeries( metadata["name"],
                           metadata["source"],
                           data = metadata["data"],
                           unit = metadata["unit"],
                           resolution = metadata["resolution"],
                           conversion = metadata["conversion"],
                           timestamps = metadata["timestamps"],
                           #starting_time = metadata["starting_time"],
                           #rate = metadata["rate"],
                           comments = metadata["comment"],
                           description = metadata["description"] )

    @classmethod
    def construct_nwbseries_nostimulus(cls, chosenmodel, tsmd):
        """class method called by build_nwbseries

        Returned Value:
        nwbts with the attributes
               nwbts[key].name, nwbts[key].source, nwbts[key].data,
               nwbts[key].timestamps, nwbts[key].unit,
               nwbts[key].resolution, nwbts[key].converstion,
               nwbts[key].starting_time, nwbts[key].rate,
               nwbts[key].comment, nwbts[key].description
        keys are the keys in chosemodel.regions = {'soma':0.0, 'axon':0.0}

        Available attributes:
        pynwb.base.TimeSeries(name, source, data=None, unit=None, resolution=0.0,
                              conversion=1.0, timestamps=None, starting_time=None,
                              rate=None, comments='no comments',
                              description='no description', control=None,
                              control_description=None, parent=None)
        NOTE:
            - https://pynwb.readthedocs.io/en/latest/pynwb.base.html#pynwb.base.TimeSeries
        """
        nwbseries = {}
        for cellregion in chosenmodel.regions.keys():
            nwbseries.update( {cellregion:
                              cls.generic_timeseries(tsmd[cellregion])} )
        return nwbseries

    def build_nwbseries(self, chosenmodel=None, tsmd=None):
        """
        Returned Value:
        nwbts with the attributes
               nwbts[key].name, nwbts[key].source, nwbts[key].data,
               nwbts[key].timestamps, nwbts[key].unit,
               nwbts[key].resolution, nwbts[key].converstion,
               nwbts[key].starting_time, nwbts[key].rate,
               nwbts[key].comment, nwbts[key].description
        keys are the keys in chosemodel.regions and with or without 'stimulus' as a key.

        Available attributes:
        pynwb.base.TimeSeries(name, source, data=None, unit=None, resolution=0.0,
                              conversion=1.0, timestamps=None, starting_time=None,
                              rate=None, comments='no comments',
                              description='no description', control=None,
                              control_description=None, parent=None)
        NOTE:
            - https://pynwb.readthedocs.io/en/latest/pynwb.base.html#pynwb.base.TimeSeries
        """
        nwbseries = {}
        if "stimulus" in tsmd:
            nwbseries.update( {"stimulus": self.generic_timeseries(tsmd["stimulus"])} )
            nwbseries.update( self.construct_nwbseries_nostimulus(chosenmodel, tsmd) )
        else:
            nwbseries.update( self.construct_nwbseries_nostimulus(chosenmodel, tsmd) )
        return nwbseries

    @staticmethod
    def link_nwbseriesresponses_to_nwbfile(nwbseries, nwbfile):
        """static method only for adding response related timeseries NOT stimulus.
        This is called by affix_nwbseries_to_nwbfile

        Arguments:
        nwbseries -- dictorary; keys = keys in chosenmodel.regions = {"soma": 0.0, "axon", 0.0}
                                values for each key is
                                pynwb.base.TimeSeries, obtained using build_nwbseries method
        nwbfile -- pynwb.file.NWBFile, obtained using build_nwbfile method

        Returned value:
        updated_nwbfile with all the TimeSeries which can be extracted as
             ts_of_key = updated_nwbfile.get_acquisition(nwbseries[key].name)
             where key is the region
             Eg: 
                ts_soma = updated_nwbfile.get_acquisition(nwbseries["soma"].name)
                then you can get all the available attributes as usual
                    ts_soma.name, ts_soma.source, ts_soma.data,
                    ts_soma.timestamps, ts_soma.unit,
                    ts_soma.resolution, ts_soma.converstion,
                    ts_soma.starting_time, ts_soma.rate,
                    ts_soma.comment, ts_soma.description
              NOTE:
                 - unlike the returned value for build_nwbseries
                   the timeseries here are for a particular key
                   therefore it is no longer a dictionary.
        """
        for key in nwbseries.keys():
            nwbfile.add_acquisition(nwbseries[key])
        return nwbfile

    @staticmethod
    def strip_out_stimulus_from_nwbseries(nwbseries):
        """static method called by affix_nwbseries_to_nwbfile
        """
        return { x: nwbseries[x] for x in nwbseries
                                  if x not in {"stimulus"} }

    def affix_nwbseries_to_nwbfile(self, nwbseries=None, nwbfile=None):
        """method that adds nwbseries with or without stimulus

        Keyword Arguments:
        nwbseries -- dictorary; keys = keys in chosenmodel.regions = {"soma": 0.0, "axon", 0.0}
                                             with or without "stimulus" as key
                                values for each key is
                                pynwb.base.TimeSeries, obtained using build_nwbseries method
        nwbfile -- pynwb.file.NWBFile, obtained using build_nwbfile method

        Returned value:
        updated_nwbfile with all the TimeSeries which can be extracted as
             ts_of_key = updated_nwbfile.get_acquisition(nwbseries[key].name)
             where key is the region
             Eg: 
                ts_soma = updated_nwbfile.get_acquisition(nwbseries["soma"].name)
                then you can get all the available attributes as usual
                    ts_soma.name, ts_soma.source, ts_soma.data,
                    ts_soma.timestamps, ts_soma.unit,
                    ts_soma.resolution, ts_soma.converstion,
                    ts_soma.starting_time, ts_soma.rate,
                    ts_soma.comment, ts_soma.description
                But
                if "stimulus" is one of the key
                ts_stim = updated_nwbfile.get_stimulus(nwbseries["stimulus"].name)
                and get its attributes as usual.
        """
        if "stimulus" in nwbseries.keys():
            nwbfile.add_stimulus(nwbseries["stimulus"])
            stripped_nwbseries = self.strip_out_stimulus_from_nwbseries(nwbseries)
            nwbfile = self.link_nwbseriesresponses_to_nwbfile(stripped_nwbseries,
                                                              nwbfile)
        else:
            nwbfile = self.link_nwbseriesresponses_to_nwbfile(nwbseries,
                                                              nwbfile)
        return nwbfile

    @staticmethod
    def insert_a_nwbepoch( epoch_i_cellregion, epochmd, nwbfile, nwbts ):
        """static method called by construct_nwbepochs

        Arguments:
        epoch_i_cellregion -- string; eg, epoch1soma
        epochmd -- dictionary;
                   meta-data for case chosenmodel.regions = {'soma': 0.0, 'axon': 0.0} and no of epochs/region=2 with stimulation is of the form
                   {"epoch0soma": {"source": "soma", "start_time": float, "stop_time": float,
                                   "description": string, "tags": tuple}
                    "epoch1soma": {"source": "soma", "start_time": float, "stop_time": float,
                                   "description": string, "tags": tuple}
                    "epoch0axon": {"source": "axon", "start_time": float, "stop_time": float,
                                   "description": string, "tags": tuple}
                    "epoch1axon": {"source": "axon", "start_time": float, "stop_time": float,
                                   "description": string, "tags": tuple}}
                  for the case without stimulation
                   {"epoch0soma": {"source": "soma", "start_time": float, "stop_time": float,
                                   "description": string, "tags": tuple}
                    "epoch0axon": {"source": "axon", "start_time": float, "stop_time": float,
                                   "description": string, "tags": tuple}}
        nwbfile -- pynwb.file.NWBFile, obtained using build_nwbfile method
        nwbts -- pynwb.base.TimeSeries, obtained using build_nwbseries method

        NOTE:
            - the whole nwbts is not passed here
            - pass only time series that corresponds to this region

        Use case:
        epochmd = {"epoch0soma": {"source": "soma", "start_time": float, "stop_time": float,
                                  "description": string, "tags": tuple}
                   "epoch0axon": {"source": "axon", "start_time": float, "stop_time": float,
                                  "description": string, "tags": tuple}}
        updated_nwbfile = insert_a_nwbepoch( "epoch0soma", epochmd, nwbfile )

        Returned Value:
        nwbfile.epochs.epochs.data returns a list with tuple such that
                     [( 0.0, # => epochmd["epoch0soma"]["start_time"]
                       10.0, # => epochmd["epoch0soma"]["stop_time"]
                       '1_epoch_responses,0,axon,DummyTest,epoch0axon', # => epochmd["epoch0soma"]["tags"]
                       <pynwb.form.data_utils.ListSlicer object at 0x7ff5883a8450>, # EPOCH DATA
                       'first epoch')] # => epochmd["epoch0soma"]["description"]
        Since we are interested in the Epoch Date created, to access it
        nwbfile.epochs.epochs.data[0][3] returns
                     <pynwb.form.data_utils.ListSlicer object at 0x7ff5883a8450>
              NOTE:
                  - first index (here, 0) will vary with number of epochs inserted
                  - second index (3) will always be 3.
        Next nwbfile.epochs.epochs.data[0][3].data is a TimeSeries class.
        To get the TimeSeries object do
        nwbfile.epochs.epochs.data[0][3].data.data which returns a list with tuple
                     [( 0, # => 
                        1000, # => timeseries_metadata["soma"]["conversion"]
                        <pynwb.base.TimeSeries object at 0x7fabf68b8690>)] # => nwb TimeSeries object
        Finally to retrieve the TimeSeries data and timestamps associated with this epoch
        follow the same format as done for the returned values of build_nwbseries
        with some modifications as shown
        nwbfile.epochs.epochs.data[0][3].data.data[0][2].timestamps
        nwbfile.epochs.epochs.data[0][3].data.data[0][2].data

        NOTE:
            - for nwb epoch attributes see
              http://pynwb.readthedocs.io/en/latest/pynwb.epoch.html#pynwb.epoch.Epochs
              https://github.com/AllenInstitute/nwb-api/blob/master/ainwb/nwb/nwbep.py
              https://pynwb.readthedocs.io/en/latest/pynwb.file.html#pynwb.file.NWBFile.create_epoch
        """
        nwbfile.create_epoch( epochmd[epoch_i_cellregion]["source"],
                              start_time = epochmd[epoch_i_cellregion]["start_time"],
                              stop_time = epochmd[epoch_i_cellregion]["stop_time"],
                              timeseries = nwbts,
                              tags = epochmd[epoch_i_cellregion]["tags"],
                              description = epochmd[epoch_i_cellregion]["description"] )
        return nwbfile

    def build_nwbepochs( self, epochmd=None, nwbfile=None, nwbts=None ):
        """method for contructing epochs into the built nwbfile

        Keyword arguments:
        epochmd -- dictionary;
                   meta-data for case chosenmodel.regions = {'soma': 0.0, 'axon': 0.0} and no of epochs/region=2 with stimulation is of the form
                   {"epoch0soma": {"source": "soma", "start_time": float, "stop_time": float,
                                   "description": string, "tags": tuple}
                    "epoch1soma": {"source": "soma", "start_time": float, "stop_time": float,
                                   "description": string, "tags": tuple}
                    "epoch0axon": {"source": "axon", "start_time": float, "stop_time": float,
                                   "description": string, "tags": tuple}
                    "epoch1axon": {"source": "axon", "start_time": float, "stop_time": float,
                                   "description": string, "tags": tuple}}
                  for the case without stimulation
                   {"epoch0soma": {"source": "soma", "start_time": float, "stop_time": float,
                                   "description": string, "tags": tuple}
                    "epoch0axon": {"source": "axon", "start_time": float, "stop_time": float,
                                   "description": string, "tags": tuple}}
        nwbfile -- pynwb.file.NWBFile, obtained using build_nwbfile method
        nwbts -- pynwb.base.TimeSeries, obtained using build_nwbseries method

        Use case:
        epoch_meta_data = { "epoch0soma": {"source": "soma",
                                           "start_time": 0.0, "stop_time": 10.0,
                                           "description": "first epoch",
                                           "tags": ('1_epoch_responses', '0', 'soma', 'DummyTest', "epoch0soma")},
                            "epoch0axon": {"source": "axon",
                                           "start_time": 0.0, "stop_time": 10.0,
                                           "description": "first epoch",
                                           "tags": ('1_epoch_responses', '0', 'axon', 'DummyTest', "epoch0axon")} }
        updated_nwbfile = build_nwbepochs( nwbfile=nwbfile, epochmd=epoch_meta_data,
                                           nwbts=nwbts )
        """
        for epoch_i_region in epochmd.keys():
            region = epochmd[epoch_i_region]["source"]
            updated_nwbfile = self.insert_a_nwbepoch( epoch_i_region, epochmd, nwbfile,
                                                      nwbts[region]  )
        return updated_nwbfile

    @staticmethod
    def insert_an_intracell_electrode( elecmd_of_a_region, nwbfile ):
        """static method called by insert_intracell_electrodes

        Arguments:
        elecmd_of_a_region -- dictionary;
                  for cellregion 'soma' and  with stimulation it is of the form
                  {"name": 'electrode_IClamp_soma',
                   "source": 'from neuron import h >> h.IClamp',
                   "location": 'soma', "slice": 'sec=0.5',
                   "seal": 'no seal', "filtering": 'no filter function',
                   "resistance": '0 Ohm', "initial_access_resistance": '0 Ohm',
                   "description": 'virtual patch-clamp electrode in soma with stimulation',
                   "device": 'NEURON 7.4 version'}
                 for the case without stimulation
                  {"name": 'electrode_soma',
                   "source": 'from neuron import h',
                   "location": 'soma', "slice": 'sec=0.5',
                   "seal": 'no seal', "filtering": 'no filter function',
                   "resistance": '0 Ohm', "initial_access_resistance": '0 Ohm',
                   "description": 'virtual patch-clamp electrode in soma without stimulation',
                   "device": 'NEURON 7.4 version'}
        nwbfile -- pynwb.file.NWBFile, obtained using build_nwbfile method

        Use case:
        elecmd = {"name": 'electrode_soma',
                  "source": 'from neuron import h',
                  "location": 'soma', "slice": 'sec=0.5',
                  "seal": 'no seal', "filtering": 'no filter function',
                  "resistance": '0 Ohm', "initial_access_resistance": '0 Ohm',
                  "description": 'virtual patch-clamp electrode in soma without stimulation',
                  "device": 'NEURON 7.4 version'}
        updated_nwbfile = insert_an_intracell_electrode( elecmd, nwbfile )

        NOTE:
            - for nwb intracellular electrode attributes see
              https://pynwb.readthedocs.io/en/latest/pynwb.icephys.html
        """
        anelectrode = nwbfile.create_intracellular_electrode(
                          name = elecmd_of_a_region["name"],
                          source = elecmd_of_a_region["source"],
                          location = elecmd_of_a_region["location"],
                          slice = elecmd_of_a_region["slice"],
                          seal = elecmd_of_a_region["seal"],
                          description = elecmd_of_a_region["description"],
                          resistance = elecmd_of_a_region["resistance"],
                          filtering = elecmd_of_a_region["filtering"],
                          initial_access_resistance = elecmd_of_a_region["initial_access_resistance"],
                          device = elecmd_of_a_region["device"] )
        return nwbfile, anelectrode

    @classmethod
    def insert_intracell_electrodes( cls, chosenmodel, elecmd, nwbfile ):
        """class method called by construct_nwbelectrodes

        Arguments:
        chosenmodel -- instantiated model
        elecmd -- dictionary;
                  meta-data for case chosenmodel.regions = {'soma': 0.0, 'axon': 0.0} and no of epochs/region=2 with stimulation is of the form
                  {"soma": {"name": 'electrode_IClamp_soma',
                            "source": 'from neuron import h >> h.IClamp',
                            "location": 'soma', "slice": 'sec=0.5',
                            "seal": 'no seal', "filtering": 'no filter function',
                            "resistance": '0 Ohm', "initial_access_resistance": '0 Ohm',
                            "description": 'virtual patch-clamp electrode in soma with stimulation',
                            "device": 'NEURON 7.4 version'},
                   "axon": {"name": 'electrode_IClamp_axon',
                            "source": 'from neuron import h >> h.IClamp',
                            "location": 'axon', "slice": 'sec=0.5',
                            "seal": 'no seal', "filtering": 'no filter function',
                            "resistance": '0 Ohm', "initial_access_resistance": '0 Ohm',
                            "description": 'virtual patch-clamp electrode in axon with stimulation',
                            "device": 'NEURON 7.4 version'}}
                 for the case without stimulation
                  {"soma": {"name": 'electrode_soma',
                            "source": 'from neuron import h',
                            "location": 'soma', "slice": 'sec=0.5',
                            "seal": 'no seal', "filtering": 'no filter function',
                            "resistance": '0 Ohm', "initial_access_resistance": '0 Ohm',
                            "description": 'virtual patch-clamp electrode in soma without stimulation',
                            "device": 'NEURON 7.4 version'},
                   "axon": {"name": 'electrode_axon',
                            "source": 'from neuron import h',
                            "location": 'axon', "slice": 'sec=0.5',
                            "seal": 'no seal', "filtering": 'no filter function',
                            "resistance": '0 Ohm', "initial_access_resistance": '0 Ohm',
                            "description": 'virtual patch-clamp electrode in axon without stimulation',
                            "device": 'NEURON 7.4 version'}}
        nwbfile -- pynwb.file.NWBFile, obtained using build_nwbfile method

        Use case:
        elecmd = {"soma":
                    {"name": 'electrode_soma',
                     "source": 'from neuron import h',
                     "location": 'soma', "slice": 'sec=0.5',
                     "seal": 'no seal', "filtering": 'no filter function',
                     "resistance": '0 Ohm', "initial_access_resistance": '0 Ohm',
                     "description": 'virtual patch-clamp electrode in soma without stimulation',
                     "device": 'NEURON 7.4 version'}}
        updated_nwbfile = insert_intracell_electrodes( chosenmodel, elecmd, nwbfile )
        """
        electrodes = {}
        for cellregion in chosenmodel.regions.keys():
            updated_nwbfile, anelectrode = cls.insert_an_intracell_electrode(
                                                          elecmd[cellregion], nwbfile)
            electrodes.update( {cellregion: anelectrode} )
        return updated_nwbfile, electrodes

    def construct_nwbelectrodes( self, chosenmodel=None, electype=None, elecmd=None, nwbfile=None ):
        """method for contructing electrodes into the built nwbfile

        Keyword arguments:
        chosenmodel -- instantiated model
        electype -- string; 'intracell', 'extracell'
        elecmd -- dictionary;
                  meta-data for case chosenmodel.regions = {'soma': 0.0, 'axon': 0.0} and no of epochs/region=2 with stimulation is of the form
                  {"soma": {"name": 'electrode_IClamp_soma',
                            "source": 'from neuron import h >> h.IClamp',
                            "location": 'soma', "slice": 'sec=0.5',
                            "seal": 'no seal', "filtering": 'no filter function',
                            "resistance": '0 Ohm', "initial_access_resistance": '0 Ohm',
                            "description": 'virtual patch-clamp electrode in soma with stimulation',
                            "device": 'NEURON 7.4 version'},
                   "axon": {"name": 'electrode_IClamp_axon',
                            "source": 'from neuron import h >> h.IClamp',
                            "location": 'axon', "slice": 'sec=0.5',
                            "seal": 'no seal', "filtering": 'no filter function',
                            "resistance": '0 Ohm', "initial_access_resistance": '0 Ohm',
                            "description": 'virtual patch-clamp electrode in axon with stimulation',
                            "device": 'NEURON 7.4 version'}}
                 for the case without stimulation
                  {"soma": {"name": 'electrode_soma',
                            "source": 'from neuron import h',
                            "location": 'soma', "slice": 'sec=0.5',
                            "seal": 'no seal', "filtering": 'no filter function',
                            "resistance": '0 Ohm', "initial_access_resistance": '0 Ohm',
                            "description": 'virtual patch-clamp electrode in soma without stimulation',
                            "device": 'NEURON 7.4 version'},
                   "axon": {"name": 'electrode_axon',
                            "source": 'from neuron import h',
                            "location": 'axon', "slice": 'sec=0.5',
                            "seal": 'no seal', "filtering": 'no filter function',
                            "resistance": '0 Ohm', "initial_access_resistance": '0 Ohm',
                            "description": 'virtual patch-clamp electrode in axon without stimulation',
                            "device": 'NEURON 7.4 version'}}
        nwbfile -- pynwb.file.NWBFile, obtained using build_nwbfile method

        Use case:
        elecmd = {"soma":
                    {"name": 'electrode_soma',
                     "source": 'from neuron import h',
                     "location": 'soma', "slice": 'sec=0.5',
                     "seal": 'no seal', "filtering": 'no filter function',
                     "resistance": '0 Ohm', "initial_access_resistance": '0 Ohm',
                     "description": 'virtual patch-clamp electrode in soma without stimulation',
                     "device": 'NEURON 7.4 version'}}
        updated_nwbfile = construct_nwbelectrodes( chosenmodel=chosenmodel, electype='intracell',
                                                   elecmd=elecmd, nwbfile=nwbfile )
        """
        if electype=='intracell':
            updated_nwbfile, electrodes_list = self.insert_intracell_electrodes(
                                                                chosenmodel, elecmd, nwbfile )
        return updated_nwbfile, electrodes_list

