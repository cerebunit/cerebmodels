# ~/managers/managerReadTest.py
import unittest
from pdb import set_trace as breakpoint

from datetime import datetime
from dateutil.tz import tzlocal
import uuid
import os
import sys

# import modules in other directories
sys.path.append(os.path.dirname(os.getcwd()))
pwd = os.getcwd()
os.chdir("..") # you are now in parent /cerebmodels
rootwd = os.getcwd()
from models.cells.modelDummyTest import DummyCell
from managers.operatorsTranscribe.fabricator import Fabricator as fab
os.chdir(pwd)

from managerRead import ReadManager as rm

import numpy

from pynwb import NWBHDF5IO

class ReadManagerTest(unittest.TestCase):

    def setUp(self):
        os.chdir(rootwd)
        self.chosenmodel = DummyCell()
        os.chdir(pwd)
        now = datetime.now()
        file_metadata = {
                 "source": "Where is the data from?, i.e, platform",
                 "session_description": "How was the data generated?, i.e, simulation of __",
                 "identifier": "a unique modelID, uuid",
                 "session_start_time": datetime(now.year, now.month, now.day, now.hour, now.minute,
                                                now.second, now.microsecond, tzinfo=tzlocal()),
                 "experimenter": "name of the experimenter/username",
                 "experiment_description": "described experiment/test description",
                 "session_id": str(hash(str(uuid.uuid1()))).replace('-',''),
                 "lab": "name of the lab",
                 "institution": "name of the institution" }
        mynwbfile = fab.build_nwbfile(file_metadata)
        # generate data
        self.runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 200, "v_init": 65}
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                          "tstop": self.runtimeparam["tstop"]}
        rec_t = [ t*self.runtimeparam["dt"]
                  for t in range( int( self.runtimeparam["tstop"]/self.runtimeparam["dt"] ) ) ]
        rec_i = numpy.random.rand(1,len(rec_t))[0]
        rec_v = numpy.random.rand(2,len(rec_t))
        # self.chosenmodel.regions = {'soma':0.0, 'axon':0.0}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                      "stimulus": rec_i}
        # create TimeSeries nwb object
        self.ts_metadata = \
         {"soma": {"name": "DummyTest_soma",
                   "data": recordings["response"]["soma"], "unit": "mV",
                   "resolution": self.runtimeparam["dt"],
                   "conversion": 1000.0,
                   "timestamps": recordings["time"],
                   "comments": "voltage response with stimulation",
                   "description": "whole single array of voltage response from soma of DummyTest"},
          "axon": {"name": "DummyTest_axon",
                   "data": recordings["response"]["axon"], "unit": "mV",
                   "resolution": self.runtimeparam["dt"],
                   "conversion": 1000.0,
                   "timestamps": recordings["time"],
                   "comments": "voltage response with stimulation",
                   "description": "whole single array of voltage response from axon of DummyTest"},
          "stimulus": {"name": "DummyTest_stimulus",
                       "data": recordings["stimulus"], "unit": "nA",
                       "resolution": self.runtimeparam["dt"],
                       "conversion": 1000.0,
                       "timestamps": recordings["time"],
                       "comments": "current injection, "+stimparameters["type"][1],
                       "description": "whole single array of stimulus"} }
        nwbts = fab.build_nwbseries(chosenmodel = self.chosenmodel, tsmd = self.ts_metadata)
        updated_mynwbfile = fab.affix_nwbseries_to_nwbfile(nwbts=nwbts, nwbfile=mynwbfile)
        # Now epochs
        self.epoch_metadata = \
            {"epoch0soma": {"source": "soma", "start_time": 0.0, "stop_time": 10.0,
                   "description": "first epoch",
                   "tags": ('2_epoch_responses', '0', 'soma', 'DummyTest', 'cells', "epoch0soma",
                            "soma axon")},
             "epoch1soma": {"source": "soma", "start_time": 10.0, "stop_time": 20.0,
                   "description": "second epoch",
                   "tags": ('2_epoch_responses', '1', 'soma', 'DummyTest', 'cells', "epoch1soma",
                            "soma axon")},
             "epoch0axon": {"source": "axon", "start_time": 0.0, "stop_time": 10.0,
                   "description": "first epoch",
                   "tags": ('2_epoch_responses', '0', 'axon', 'DummyTest', 'cells', "epoch0axon",
                            "soma axon")},
             "epoch1axon": {"source": "axon", "start_time": 10.0, "stop_time": 20.0,
                   "description": "second epoch",
                   "tags": ('2_epoch_responses', '1', 'axon', 'DummyTest', 'cells', "epoch1axon",
                            "soma axon")}}
        updated_mynwbfile = fab.build_nwbepochs(nwbfile=updated_mynwbfile, nwbts=nwbts,
                                                epochmd=self.epoch_metadata)
        self.fullname = fab.write_nwbfile(nwbfile=updated_mynwbfile)

    #@unittest.skip("reason for skipping")
    def test_1_load_nwbfile(self):
        nwbfile = rm.load_nwbfile(self.fullname)
        self.assertTrue( (str(type(nwbfile))[8:-2]=="pynwb.file.NWBFile") is True )
        os.remove( self.fullname )

    #@unittest.skip("reason for skipping")
    def test_2_timestamps_and_data_for_epoch(self):
        nwbfile = rm.load_nwbfile(self.fullname)
        times = rm.timestamps_for_epoch( nwbfile.epochs[0] )
        data = rm.data_for_epoch( nwbfile.epochs[0] )
        #a = all(boolean == True for boolean in times!=data)
        self.assertEqual( len(times), len(data) )
        os.remove( self.fullname )

    @unittest.skip("reason for skipping")
    def test_3_get_total_epochIDs(self):
        nwbfile = rm.load_nwbfile(self.fullname)
        self.assertEqual( rm.total_epochIDs( nwbfile ), 2 ) # two epochs per region
        os.remove( self.fullname )

    @unittest.skip("reason for skipping")
    def test_4_order_all_epocs_for_region(self):
        nwbfile = rm.load_nwbfile(self.fullname)
        chosenreg = "soma"
        orderedepochs = rm.order_all_epochs_for_region(nwbfile=nwbfile, region=chosenreg)
        #print(len(orderedepochs))
        epoch0 = orderedepochs[0]
        epoch1 = orderedepochs[1]
        #print(epoch0[1], epoch1[1])
        #print(epoch0[2], epoch1[2])
        a0_md = ( epoch0[1] == self.epoch_metadata["epoch0"+chosenreg]["start_time"] )
        a0_a1 = ( epoch0[1] != epoch1[1] )
        b1_md = ( epoch1[2] == self.epoch_metadata["epoch1"+chosenreg]["stop_time"] )
        #print(a0_md, a0_a1, b1_md)
        self.assertTrue( a0_md and a0_a1 and b1_md )
        os.remove( self.fullname )

if __name__ == '__main__':
    unittest.main()
