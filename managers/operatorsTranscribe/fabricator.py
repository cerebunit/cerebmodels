# ~/managers/operatorsTranscribe/fabricator.py
from datetime import datetime
import pkg_resources

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
        """
        return NWBFile( source = filemd["source"],
                        session_description = filemd["session_description"],
                        identifier = filemd["identifier"],
                        session_start_time = filemd["session_start_time"],
                        file_create_date = str(datetime.now()),                   # additions
                        version = pkg_resources.get_distribution("pynwb").version,# additions
                        experimenter = filemd["experimenter"],
                        experiment_description = filemd["experiment_description"],
                        session_id = filemd["session_id"],
                        lab = filemd["lab"],
                        institution = filemd["institution"] )

    @staticmethod
    def insert_a_nwbepoch( epoch_i_cellregion, epochmd, nwbfile ):
        """static method called by construct_nwbepochs

        Arguments:
        epoch_i_cellregion -- string; eg, epoch1soma
        epochmd -- dictionary;
                   meta-data for case chosenmodel.regions = {'soma': 0.0, 'axon': 0.0} and no of epochs/region=2 with stimulation is of the form
                   {"epoch0soma": {"source": "soma", "start_time": float, "stop_time": float,
                                   "description": string}
                    "epoch1soma": {"source": "soma", "start_time": float, "stop_time": float,
                                   "description": string}
                    "epoch0axon": {"source": "axon", "start_time": float, "stop_time": float,
                                   "description": string}
                    "epoch1axon": {"source": "axon", "start_time": float, "stop_time": float,
                                   "description": string}
                    "epoch_tags": ('2_epoch_responses',)}
                  for the case without stimulation
                   {"epoch0soma": {"source": "soma", "start_time": float, "stop_time": float,
                                   "description": string}
                    "epoch0axon": {"source": "axon", "start_time": float, "stop_time": float,
                                   "description": string}
        nwbfile -- pynwb.file.NWBFile, obtained using build_nwbfile method

        Use case:
        epochmd = {"epoch0soma": {"source": "soma", "start_time": float, "stop_time": float,
                                  "description": string}
                   "epoch0axon": {"source": "axon", "start_time": float, "stop_time": float,
                                  "description": string}
                   "epoch_tags": ('1_epoch_responses',)}
        updated_nwbfile = insert_a_nwbepoch( "epoch0soma", epochmd, nwbfile )

        NOTE:
            - for nwb epoch attributes see
              https://github.com/AllenInstitute/nwb-api/blob/master/ainwb/nwb/nwbep.py
              https://pynwb.readthedocs.io/en/latest/pynwb.file.html#pynwb.file.NWBFile.create_epoch
        """
        nwbfile.create_epoch( name = epoch_i_cellregion,
                              source = epochmd[epoch_i_cellregion]["source"],
                              start = epochmd[epoch_i_cellregion]["start_time"], # start_time
                              stop = epochmd[epoch_i_cellregion]["stop_time"],   # stop_time
                              tags = epochmd["epoch_tags"],
                              description = epochmd[epoch_i_cellregion]["description"] )
        return nwbfile

    def construct_nwbepochs( self, epochmd=None, nwbfile=None ):
        """method for contructing epochs into the built nwbfile

        Keyword arguments:
        epochmd -- dictionary;
                   meta-data for case chosenmodel.regions = {'soma': 0.0, 'axon': 0.0} and no of epochs/region=2 with stimulation is of the form
                   {"epoch0soma": {"source": "soma", "start_time": float, "stop_time": float,
                                   "description": string}
                    "epoch1soma": {"source": "soma", "start_time": float, "stop_time": float,
                                   "description": string}
                    "epoch0axon": {"source": "axon", "start_time": float, "stop_time": float,
                                   "description": string}
                    "epoch1axon": {"source": "axon", "start_time": float, "stop_time": float,
                                   "description": string}
                    "epoch_tags": ('2_epoch_responses',)}
                  for the case without stimulation
                   {"epoch0soma": {"source": "soma", "start_time": float, "stop_time": float,
                                   "description": string}
                    "epoch0axon": {"source": "axon", "start_time": float, "stop_time": float,
                                   "description": string}
        nwbfile -- pynwb.file.NWBFile, obtained using build_nwbfile method

        Use case:
        epoch_meta_data = { "epoch0soma": {"source": "soma",
                                           "start_time": 0.0, "stop_time": 10.0,
                                           "description": "first epoch"},
                            "epoch0axon": {"source": "axon",
                                           "start_time": 0.0, "stop_time": 10.0,
                                           "description": "first epoch"}
                            "epoch_tags": ("1_epoch_responses",) }
        nwbfile, epoch_list = construct_nwbepochs( nwbfile=nwbfile, epochmd=epoch_meta_data )
        """
        md_no_tags = { x: epochmd[x] for x in epochmd
                                      if x not in {"epoch_tags"} }
        #nwb_epochs_list = []
        for epoch_i_region in md_no_tags.keys():
            updated_nwbfile = self.insert_a_nwbepoch( epoch_i_region, epochmd, nwbfile )
        return updated_nwbfile
