# ~/managers/operatorsReadNWB/epoch_unrevellerTest.py
import unittest
from pdb import set_trace as breakpoint

import datetime
from dateutil.tz import tzlocal
import uuid
import os
import sys

# import modules in other directories
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
pwd = os.getcwd()
os.chdir("..") # this moves you up to ~/managers
os.chdir("..") # you are now in parent /cerebmodels
rootwd = os.getcwd()
from models.cells.modelDummyTest import DummyCell
from managers.transcribe import TranscribeManager
os.chdir(pwd)

from epoch_unraveller import EpochUnraveller as eu

import numpy

from pynwb import NWBHDF5IO

class EpochUnraveller(unittest.TestCase):

    def setUp(self):
        os.chdir(rootwd)
        self.chosenmodel = DummyCell()
        self.simtime = datetime.datetime.now()
        os.chdir(pwd)
        # self.chosenmodel.regions ->
        # {"soma": ["v", "i_cap"], "axon": ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        # No stimulus
        self.no_runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        self.no_rec_t = [ t*self.no_runtimeparam["dt"] for t in
                     range( int( self.no_runtimeparam["tstop"]/self.no_runtimeparam["dt"] ) ) ]
        self.no_rec_resp = numpy.random.rand(7,len(self.no_rec_t))
        self.no_rec_stim = "Model is not stimulated" # response["stimulus"]
        #self.no_stimtype = None # stimparameters["type"] = ["current", "IClamp"]
        self.no_recordings = {"time": self.no_rec_t,
           "response": {"soma": [self.no_rec_resp[0], self.no_rec_resp[1]],
                        "axon": [ self.no_rec_resp[2] ],
           "channels": {"soma": {"hh": [self.no_rec_resp[3], self.no_rec_resp[4]],
                                 "pas":[ self.no_rec_resp[5] ]},
                        "axon": {"pas":[ self.no_rec_resp[3] ]}}},
           "stimulus": "Model is not stimulated"}
        # IClamp
        self.ic_runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        self.ic_stimparameters = {"type": ["current", "IClamp"],
                              "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                            {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                              "tstop": self.ic_runtimeparam["tstop"]}
        self.ic_rec_t = [ t*self.ic_runtimeparam["dt"] for t in
                  range( int( self.ic_runtimeparam["tstop"]/self.ic_runtimeparam["dt"] ) ) ]
        self.ic_rec_stim = numpy.random.rand(1,len(self.ic_rec_t))[0]
        self.ic_rec_resp = numpy.random.rand(7,len(self.ic_rec_t))
        self.ic_recordings = {"time": self.ic_rec_t,
           "response": {"soma": [self.ic_rec_resp[0], self.ic_rec_resp[1]],
                        "axon": [ self.ic_rec_resp[2] ],
           "channels": {"soma": {"hh": [self.ic_rec_resp[3], self.ic_rec_resp[4]],
                                 "pas":[ self.ic_rec_resp[5] ]},
                        "axon": {"pas":[ self.ic_rec_resp[6] ]}}},
           "stimulus": self.ic_rec_stim}
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
    def test_1_total_overall_epochs(self):
        #  <---10--->  <----20---->
        # 0----------10-----------20------------35
        # ep0        ep1          ep2
        # self.chosenmodel.regions ->
        # {"soma": ["v", "i_cap"], "axon": ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        # notice 7 measuring regions times three points above = 21 epochs in total
        io = NWBHDF5IO(self.fullname, mode="r")
        nwbfile = io.read()
        print(eu.total_overall_epochs( nwbfile ))
        self.assertEqual( eu.total_overall_epochs(nwbfile), 21 )
        os.remove( self.fullname )

    #@unittest.skip("reason for skipping")
    def test_2_pluck_epoch_row(self):
        io = NWBHDF5IO( self.fullname, mode="r")
        nwbfile = io.read()
        row = 2
        self.assertEqual( eu.pluck_epoch_row( nwbfile, row )[0], row )
        os.remove( self.fullname )

    #@unittest.skip("reason for skipping")
    def test_3_total_epochs_this_region(self):
        #  <---10--->  <----20---->
        # 0----------10-----------20------------35
        # ep0        ep1          ep2
        io = NWBHDF5IO( self.fullname, mode="r")
        nwbfile = io.read()
        row = 3
        an_epoch = eu.pluck_epoch_row( nwbfile, row )
        #if ( eu.total_epochs_this_region(an_epoch) == 4       # 4 for soma
        #     or eu.total_epochs_this_region(an_epoch) == 2 ): # 2 for axon
        #   say = True
        #else:
        #   say = False
        #self.assertTrue( say )
        a = eu.total_epochs_this_region(an_epoch) == 3
        self.assertTrue( a is True )
        os.remove( self.fullname )

    #@unittest.skip("reason for skipping")
    def test_4_pull_all_epochs_for_region(self):
        #  <---10--->  <----20---->
        # 0----------10-----------20------------35
        # ep0        ep1          ep2
        # self.chosenmodel.regions ->
        # {"soma": ["v", "i_cap"], "axon": ["v"],
        # "channels": {"soma": {"hh": ["il", "el"], "pas": ["i"]}, "axon": {"pas": ["i"]}}}
        # notice 7 measuring regions times three points above = 21 epochs in total
        io = NWBHDF5IO( self.fullname, mode="r")
        nwbfile = io.read()
        all_epochs_for_region1 = eu.pull_all_epochs_for_region( nwbfile=nwbfile, region="soma v" )
        all_epochs_for_region2 = eu.pull_all_epochs_for_region( nwbfile=nwbfile,
                                                                region="channels soma hh il" )
        a = len(all_epochs_for_region1) == 3
        b = eu.pluck_region( all_epochs_for_region2[0] ) == "channels soma hh il"
        c = len(all_epochs_for_region1) == len(all_epochs_for_region2)
        self.assertTrue( a and b and c is True )
        os.remove( self.fullname )

    #@unittest.skip("reason for skipping")
    def test_5_pull_indices_tseries_for_epoch(self):
        io = NWBHDF5IO( self.fullname, mode="r")
        nwbfile = io.read()
        row = 1
        an_epoch = eu.pluck_epoch_row( nwbfile, row )
        indices = eu.pull_indices_tseries_for_epoch( an_epoch )
        #
        # start_time to stop_time with dt resolution is t0 and t1 respectively
        # thus, divide real time by its resolution
        t0 = int(eu.pluck_start_time(an_epoch))#/self.sec_runtimeparam["dt"])
        t1 = int(eu.pluck_stop_time(an_epoch))#/self.sec_runtimeparam["dt"])
        #print(indices, len(indices), indices[0], indices[-1])
        #print(t0, t1) # corresponds with start_time and stop_time but scaled with dt
        #times = range( t0, t1+1 ) # to include t1
        times = numpy.arange( t0, t1, self.sec_runtimeparam["dt"] )
        #print(len(times), times[0], times[-1])
        #
        a = ( len(times) == len(indices) or len(times) == len(indices)+1 )
        #nwbts = eu.pluck_timeseries_object(an_epoch)
        #print( t0, t1, nwbts.timestamps[indices[0]], nwbts.timestamps[indices[-1]] )
        self.assertEqual( a, True )
        os.remove( self.fullname )

if __name__ == '__main__':
    unittest.main()
