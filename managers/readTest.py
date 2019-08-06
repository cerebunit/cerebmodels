# ~/managers/readTest.py
import unittest
from pdb import set_trace as breakpoint

import datetime
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
#from managers.operatorsTranscribe.fabricator import Fabricator as fab
from managers.transcribe import TranscribeManager
os.chdir(pwd)

from managers.read import ReadManager as rm

import numpy

from pynwb import NWBHDF5IO

from random import randint

class ReadManagerTest(unittest.TestCase):

    def setUp(self):
        os.chdir(rootwd)
        self.chosenmodel = DummyCell()
        self.simtime = datetime.datetime.now()
        os.chdir(pwd)
        # self.chosenmodel.regions ->
        # {"soma": ["v", "i_cap"], "axon": ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        # Voltage clamp
        self.sec_runtimeparam = {"dt": 0.1, "celsius": 30, "tstop": 35, "v_init": 65}
        self.sec_stimparameters = {"type": ["voltage", "SEClamp"],
                               "stimlist": [ {'amp1': 0., 'dur1': 10.0},
                                        {'amp2': -70.0, 'dur2': 20.0} ],
                               "tstop": self.sec_runtimeparam["tstop"]}
        self.sec_rec_t = [ t*self.sec_runtimeparam["dt"] for t in
                   range( int( self.sec_runtimeparam["tstop"]/self.sec_runtimeparam["dt"] ) ) ]
        self.sec_rec_stim = numpy.random.rand(1,len(self.sec_rec_t))[0]
        self.sec_rec_resp = numpy.random.rand(7,len(self.sec_rec_t))
        self.sec_recordings = {"time": self.sec_rec_t,
           "response": {"soma": [self.sec_rec_resp[0], self.sec_rec_resp[1]],
                        "axon": [ self.sec_rec_resp[2] ],
           "channels": {"soma": {"hh": [self.sec_rec_resp[3], self.sec_rec_resp[4]],
                                 "pas":[ self.sec_rec_resp[5] ]},
                        "axon": {"pas":[ self.sec_rec_resp[3] ]}}},
           "stimulus": self.sec_rec_stim}
        #
        tm = TranscribeManager()
        tm.load_metadata( chosenmodel = self.chosenmodel, simtime = self.simtime,
                          recordings = self.sec_recordings,
                          runtimeparameters = self.sec_runtimeparam,
                          stimparameters = self.sec_stimparameters )
        tm.compile_nwbfile()
        self.fullname = tm.save_nwbfile()

    #@unittest.skip("reason for skipping")
    def test_1_load_nwbfile(self):
        nwbfile = rm.load_nwbfile(self.fullname)
        self.assertTrue( (str(type(nwbfile))[8:-2]=="pynwb.file.NWBFile") is True )
        os.remove( self.fullname )

    #@unittest.skip("reason for skipping")
    def test_2_timestamps_and_data_for_epoch(self):
        #  <---10--->  <----20---->
        # 0----------10-----------20------------35
        # ep0        ep1          ep2
        # {"soma": ["v", "i_cap"], "axon": ["v"], 
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        # notice 7 measuring regions times three points above = 21 epochs in total
        nwbfile = rm.load_nwbfile(self.fullname)
        times = rm.timestamps_for_epoch( nwbfile.epochs[0] )
        data = rm.data_for_epoch( nwbfile.epochs[0] )
        #a = all(boolean == True for boolean in times!=data)
        self.assertEqual( len(times), len(data) )
        os.remove( self.fullname )

    #@unittest.skip("reason for skipping")
    def test_3_get_total_epochIDs(self):
        #  <---10--->  <----20---->
        # 0----------10-----------20------------35
        # ep0        ep1          ep2
        # {"soma": ["v", "i_cap"], "axon": ["v"], 
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        # notice 7 measuring regions times three points above = 21 epochs in total
        nwbfile = rm.load_nwbfile(self.fullname)
        self.assertEqual( rm.total_epochIDs( nwbfile ), 3 )
        os.remove( self.fullname )

    #@unittest.skip("reason for skipping")
    def test_4_order_all_epocs_for_region(self):
        #  <---10--->  <----20---->
        # 0----------10-----------20------------35
        # ep0        ep1          ep2
        # {"soma": ["v", "i_cap"], "axon": ["v"], 
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        # notice 7 measuring regions times three points above = 21 epochs in total
        nwbfile = rm.load_nwbfile(self.fullname)
        chosenreg = "soma v"
        orderedepochs = rm.order_all_epochs_for_region(nwbfile=nwbfile, region=chosenreg)
        #print(len(orderedepochs))
        epoch0 = orderedepochs[0]
        epoch1 = orderedepochs[1]
        epoch2 = orderedepochs[2]
        #print( epoch1[0] )
        #print( epoch1[1] )
        #print( epoch1[2] )
        #print( epoch1[3] )
        #print( epoch0[4] )
        a = len(orderedepochs) == 3
        b = epoch0[1] < epoch1[1]
        c = epoch1[1] < epoch2[1]
        #print(a, b, c)
        #print( epoch0[1], epoch1[1], epoch2[1] )
        self.assertEqual( [a, b, c], [True, True, True] )
        #self.assertTrue( a and b and c is True )
        os.remove( self.fullname )

if __name__ == '__main__':
    unittest.main()
