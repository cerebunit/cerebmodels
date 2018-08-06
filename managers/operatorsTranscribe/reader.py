# ~/managers/operatorsTranscribe/reader.py
from collections import namedtuple

import modules from other directories
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
    def __init__(self,filepath):
        io = NWBHDF5IO(filepath)
        self.nwbfile = io.read()

    def show_filemd(self):
        Row = namedtuple('Row', ['metadata detail', 'metadata'])
        data1 = Row("Where is the data from?", self.nwbfile.source)
        data2 = Row("How was the data generated?", self.nwbfile.session_description)
        data3 = Row("When did the simulation start?", self.nwbfile.session_start_time)
        data4 = Row("What is the session id?", self.nwbfile.session_id)
        uu.pprinttable([data1, data2, data3, data4])
