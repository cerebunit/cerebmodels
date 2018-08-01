#/managers/operatorsTranscribe/fabricatorTest.py
import unittest

import uuid
import collections # for comparing unordered lists
import os
import sys
# import modules for other directories
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
# this is required for
from models.cells.modelDummyTest import DummyCell

from fabricator import Fabricator

import numpy

class FabricatorTest(unittest.TestCase):

    def setUp(self):
        self.fab = Fabricator()
        self.pwd = os.getcwd()
        self.chosenmodel = DummyCell()

    #@unittest.skip("reason for skipping")
    def test_1_build_nwbfile(self):
        file_metadata = {
                "source": "Where is the data from?, i.e, platform",
                "session_description": "How was the data generated?, i.e, simulation of __",
                "identifier": "a unique modelID, uuid",
                "session_start_time": '01-12-2017 00:00:00', #"when simulation starts"
                "experimenter": "name of the experimenter/username",
                "experiment_description": "described experiment/test description",
                "session_id": str(hash(str(uuid.uuid1()))).replace('-',''),
                "lab": "name of the lab",
                "institution": "name of the institution" }
        nwbfile = self.fab.build_nwbfile(file_metadata)
        #print [nwbfile.source, nwbfile.session_description, nwbfile.identifier,
        #       nwbfile.session_start_time, nwbfile.experimenter,
        #       nwbfile.experiment_description, nwbfile.session_id, nwbfile.lab,
        #       nwbfile.institution] # what does this nwbfile have?

        # "<class '__main__.ClassA'>" 1st"_"is 8 & last"'"is -2
        typestr = str(type(nwbfile))[8:-2] 
        self.assertEqual( typestr, "pynwb.file.NWBFile" )

    #@unittest.skip("reason for skipping")
    def test_2_generictime_series(self):
        file_metadata = {
                "source": "Where is the data from?, i.e, platform",
                "session_description": "How was the data generated?, i.e, simulation of __",
                "identifier": "a unique modelID, uuid",
                "session_start_time": '01-12-2017 00:00:00', #"when simulation starts"
                "experimenter": "name of the experimenter/username",
                "experiment_description": "described experiment/test description",
                "session_id": str(hash(str(uuid.uuid1()))).replace('-',''),
                "lab": "name of the lab",
                "institution": "name of the institution" }
        # since self.chosenmodel.regions = {'soma': 0.0, 'axon': 0.0}
        #electrode_metadata_of_soma_stimulus = \
        #      {"name": 'electrode_soma', "source": 'from neuron import h',
        #       "location": 'soma', "slice": 'sec=0.5', "seal": 'no seal',
        #       "filtering": 'no filter function', "resistance": '0 Ohm',
        #       "initial_access_resistance": '0 Ohm', "device": 'NEURON 7.4 version',
        #       "description": 'virtual patch-clamp electrode in soma without stimulation'}
        #mynwbfile = self.fab.build_nwbfile(file_metadata)
        #updated_mynwbfile, anelectrode = Fabricator.insert_an_intracell_electrode(
        #                                           electrode_metadata_of_soma_stimulus,
        #                                           mynwbfile)
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v_soma = numpy.random.rand(1,len(rec_t))[0]
        ts_metadata = \
              {"type": "generictime_series", #"GenericTimeSeries"
               "name": "DummyTest_nostim_Vm_soma",
               "source": "soma",
               "data": rec_v_soma,
               "unit": "mV",
               "resolution": runtimeparam["dt"],
               "conversion": 1000.0,
               "timestamps": rec_t,
               "starting_time": 0.0,
               "rate": 1/runtimeparam["dt"],
               "comment": "voltage response without stimulation",
               "description": "whole single array of voltage response from soma of DummyTest"}
        nwbts = Fabricator.generictime_series(ts_metadata)
        # Bug with pynwb (reported by me on 1/7/2018) 
        #print nwbts.resolution # float
        #print type(nwbts.conversion) # float
        #print nwbts.starting_time # None but should be float
        #print type(nwbts.rate) # None but should be float
          
        #print [nwbts.name, nwbts.source, nwbts.data, nwbts.unit, nwbts.resolution, nwbts.conversion, nwbts.timestamps, nwbts.starting_time, nwbts.rate, nwbts.comments, nwbts.description, nwbts.control, nwbts.control_description, nwbts.parent] # what does this return
        self.assertEqual( [nwbts.data, nwbts.timestamps],
                          [rec_v_soma, rec_t] )

    #@unittest.skip("reason for skipping")
    def test_3_make_one_nwbseries(self):
        file_metadata = {
                "source": "Where is the data from?, i.e, platform",
                "session_description": "How was the data generated?, i.e, simulation of __",
                "identifier": "a unique modelID, uuid",
                "session_start_time": '01-12-2017 00:00:00', #"when simulation starts"
                "experimenter": "name of the experimenter/username",
                "experiment_description": "described experiment/test description",
                "session_id": str(hash(str(uuid.uuid1()))).replace('-',''),
                "lab": "name of the lab",
                "institution": "name of the institution" }
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v_soma = numpy.random.rand(1,len(rec_t))[0]
        ts_metadata = \
              {"type": "generictime_series", #"GenericTimeSeries"
               "name": "DummyTest_nostim_Vm_soma",
               "source": "soma",
               "data": rec_v_soma,
               "unit": "mV",
               "resolution": runtimeparam["dt"],
               "conversion": 1000.0,
               "timestamps": rec_t,
               "starting_time": 0.0,
               "rate": 1/runtimeparam["dt"],
               "comment": "voltage response without stimulation",
               "description": "whole single array of voltage response from soma of DummyTest"}
        nwbts = self.fab.make_one_nwbseries(ts_metadata)
        #print [nwbts.name, nwbts.source, nwbts.data, nwbts.unit, nwbts.resolution, nwbts.conversion, nwbts.timestamps, nwbts.starting_time, nwbts.rate, nwbts.comments, nwbts.description, nwbts.control, nwbts.control_description, nwbts.parent] # what does this return
        self.assertEqual( [nwbts.data, nwbts.timestamps],
                          [rec_v_soma, rec_t] )

    #@unittest.skip("reason for skipping")
    def test_3_construct_nwbseries(self):
        file_metadata = {
                "source": "Where is the data from?, i.e, platform",
                "session_description": "How was the data generated?, i.e, simulation of __",
                "identifier": "a unique modelID, uuid",
                "session_start_time": '01-12-2017 00:00:00', #"when simulation starts"
                "experimenter": "name of the experimenter/username",
                "experiment_description": "described experiment/test description",
                "session_id": str(hash(str(uuid.uuid1()))).replace('-',''),
                "lab": "name of the lab",
                "institution": "name of the institution" }
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_v_soma = numpy.random.rand(1,len(rec_t))[0]
        ts_metadata = \
              {"type": "generictime_series", #"GenericTimeSeries"
               "name": "DummyTest_nostim_Vm_soma",
               "source": "soma",
               "data": rec_v_soma,
               "unit": "mV",
               "resolution": runtimeparam["dt"],
               "conversion": 1000.0,
               "timestamps": rec_t,
               "starting_time": 0.0,
               "rate": 1/runtimeparam["dt"],
               "comment": "voltage response without stimulation",
               "description": "whole single array of voltage response from soma of DummyTest"}
        nwbts = self.fab.construct_nwbseries(chosenmodel=self.chosenmodel, ts_metadata)
        #print [nwbts.name, nwbts.source, nwbts.data, nwbts.unit, nwbts.resolution, nwbts.conversion, nwbts.timestamps, nwbts.starting_time, nwbts.rate, nwbts.comments, nwbts.description, nwbts.control, nwbts.control_description, nwbts.parent] # what does this return
        self.assertEqual( [nwbts.data, nwbts.timestamps],
                          [rec_v_soma, rec_t] )

    @unittest.skip("reason for skipping")
    def test_2_insert_a_nwbepoch_nostimulus(self):
        file_metadata = {
                "source": "Where is the data from?, i.e, platform",
                "session_description": "How was the data generated?, i.e, simulation of __",
                "identifier": "a unique modelID, uuid",
                "session_start_time": '01-12-2017 00:00:00', #"when simulation starts"
                "experimenter": "name of the experimenter/username",
                "experiment_description": "described experiment/test description",
                "session_id": "str(hash(str(uuid.uuid1())))",
                "lab": "name of the lab",
                "institution": "name of the institution" }
        # since self.chosenmodel.regions = {'soma': 0.0, 'axon': 0.0}
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 10, "v_init": 65}
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        epoch_metadata_nostimulus = \
              {"epoch0soma": {"source": "soma", "start_time": 0.0, "stop_time": 10.0,
                              "timeseries": rec_t, "description": "first epoch"},
               "epoch0axon": {"source": "axon", "start_time": 0.0, "stop_time": 10.0,
                              "timeseries": rec_t, "description": "first epoch"},
               "epoch_tags": ('1_epoch_responses','DummyTest','epoch0soma', 'epoch0axon')}
        mynwbfile = self.fab.build_nwbfile(file_metadata)
        updated_mynwbfile = Fabricator.insert_a_nwbepoch("epoch0axon",
                                                epoch_metadata_nostimulus,
                                                mynwbfile)
        # "<class '__main__.ClassA'>" 1st"_"is 8 & last"'"is -2
        #typestr = str(type(updated_mynwbfile))[8:-2] 
        #self.assertEqual( typestr, "pynwb.file.NWBFile" )

    @unittest.skip("reason for skipping")
    def test_3_insert_a_nwbepoch_stimulus(self):
        file_metadata = {
                "source": "Where is the data from?, i.e, platform",
                "session_description": "How was the data generated?, i.e, simulation of __",
                "identifier": "a unique modelID, uuid",
                "session_start_time": '01-12-2017 00:00:00', #"when simulation starts"
                "experimenter": "name of the experimenter/username",
                "experiment_description": "described experiment/test description",
                "session_id": "str(hash(str(uuid.uuid1())))",
                "lab": "name of the lab",
                "institution": "name of the institution" }
        # since self.chosenmodel.regions = {'soma': 0.0, 'axon': 0.0}
        epoch_metadata_stimulus = \
              {"epoch0soma": {"source": "soma", "start_time": 0.0, "stop_time": 10.0,
                              "description": "first epoch"},
               "epoch1soma": {"source": "soma", "start_time": 10.0, "stop_time": 20.0,
                              "description": "second epoch"},
               "epoch0axon": {"source": "axon", "start_time": 0.0, "stop_time": 10.0,
                              "description": "first epoch"},
               "epoch1axon": {"source": "axon", "start_time": 10.0, "stop_time": 20.0,
                              "description": "second epoch"},
               "epoch_tags": ('2_epoch_responses',)}
        mynwbfile = self.fab.build_nwbfile(file_metadata)
        updated_mynwbfile = Fabricator.insert_a_nwbepoch("epoch0axon",
                                                epoch_metadata_stimulus,
                                                mynwbfile)
        # "<class '__main__.ClassA'>" 1st"_"is 8 & last"'"is -2
        #typestr = str(type(updated_mynwbfile))[8:-2] 
        self.assertEqual( updated_mynwbfile.epoch_tags, ['2_epoch_responses'] )

    @unittest.skip("reason for skipping")
    def test_4_costruct_nwbepoch_nostimulus(self):
        file_metadata = {
                "source": "Where is the data from?, i.e, platform",
                "session_description": "How was the data generated?, i.e, simulation of __",
                "identifier": "a unique modelID, uuid",
                "session_start_time": '01-12-2017 00:00:00', #"when simulation starts"
                "experimenter": "name of the experimenter/username",
                "experiment_description": "described experiment/test description",
                "session_id": "str(hash(str(uuid.uuid1())))",
                "lab": "name of the lab",
                "institution": "name of the institution" }
        # since self.chosenmodel.regions = {'soma': 0.0, 'axon': 0.0}
        epoch_metadata_nostimulus = \
              {"epoch0soma": {"source": "soma_time", "start_time": 0.0, "stop_time": 10.0,
                              "description": "first epoch"},
               "epoch0axon": {"source": "axon", "start_time": 0.0, "stop_time": 10.0,
                              "description": "first epoch"},
               "epoch_tags": ('1_epoch_responses',)}
        mynwbfile = self.fab.build_nwbfile(file_metadata)
        updated_mynwbfile = self.fab.construct_nwbepochs(
                                                epochmd=epoch_metadata_nostimulus,
                                                nwbfile=mynwbfile)
        self.assertEqual( collections.Counter(list(updated_mynwbfile.epochs.keys())),
                          collections.Counter(["epoch0soma", "epoch0axon"]) )

    @unittest.skip("reason for skipping")
    def test_5_construct_nwbepochs_stimulus(self):
        file_metadata = {
                "source": "Where is the data from?, i.e, platform",
                "session_description": "How was the data generated?, i.e, simulation of __",
                "identifier": "a unique modelID, uuid",
                "session_start_time": '01-12-2017 00:00:00', #"when simulation starts"
                "experimenter": "name of the experimenter/username",
                "experiment_description": "described experiment/test description",
                "session_id": "str(hash(str(uuid.uuid1())))",
                "lab": "name of the lab",
                "institution": "name of the institution" }
        # since self.chosenmodel.regions = {'soma': 0.0, 'axon': 0.0}
        epoch_metadata_stimulus = \
              {"epoch0soma": {"source": "soma", "start_time": 0.0, "stop_time": 10.0,
                              "description": "first epoch"},
               "epoch1soma": {"source": "soma", "start_time": 10.0, "stop_time": 20.0,
                              "description": "second epoch"},
               "epoch0axon": {"source": "axon", "start_time": 0.0, "stop_time": 10.0,
                              "description": "first epoch"},
               "epoch1axon": {"source": "axon", "start_time": 10.0, "stop_time": 20.0,
                              "description": "second epoch"},
               "epoch_tags": ('2_epoch_responses',)}
        mynwbfile = self.fab.build_nwbfile(file_metadata)
        updated_mynwbfile = self.fab.construct_nwbepochs(
                                                epochmd=epoch_metadata_stimulus,
                                                nwbfile=mynwbfile)
        compare1 = [ updated_mynwbfile.epochs["epoch0soma"].source,
                     updated_mynwbfile.epochs["epoch1soma"].start_time,
                     updated_mynwbfile.epochs["epoch0axon"].stop_time,
                     updated_mynwbfile.epochs["epoch1axon"].description ]
        compare2 = ["soma", 10.0, 10.0, "second epoch"]
        self.assertEqual( compare1, compare2 )

    @unittest.skip("reason for skipping")
    def test_6_insert_an_intracell_electrode_stimulus(self):
        file_metadata = {
                "source": "Where is the data from?, i.e, platform",
                "session_description": "How was the data generated?, i.e, simulation of __",
                "identifier": "a unique modelID, uuid",
                "session_start_time": '01-12-2017 00:00:00', #"when simulation starts"
                "experimenter": "name of the experimenter/username",
                "experiment_description": "described experiment/test description",
                "session_id": "str(hash(str(uuid.uuid1())))",
                "lab": "name of the lab",
                "institution": "name of the institution" }
        # since self.chosenmodel.regions = {'soma': 0.0, 'axon': 0.0}
        electrode_metadata_of_soma_stimulus = \
              {"name": 'electrode_IClamp_soma', "source": 'from neuron import h >> h.IClamp',
               "location": 'soma', "slice": 'sec=0.5', "seal": 'no seal',
               "filtering": 'no filter function', "resistance": '0 Ohm',
               "initial_access_resistance": '0 Ohm', "device": 'NEURON 7.4 version',
               "description": 'virtual patch-clamp electrode in soma with stimulation'}
        mynwbfile = self.fab.build_nwbfile(file_metadata)
        updated_mynwbfile, anelectrode = Fabricator.insert_an_intracell_electrode(
                                                   electrode_metadata_of_soma_stimulus,
                                                   mynwbfile)
        self.assertEqual( updated_mynwbfile.ic_electrodes[0].description,
                          anelectrode.description )

    @unittest.skip("reason for skipping")
    def test_7_insert_intracell_electrodes_nostimulus(self):
        file_metadata = {
                "source": "Where is the data from?, i.e, platform",
                "session_description": "How was the data generated?, i.e, simulation of __",
                "identifier": "a unique modelID, uuid",
                "session_start_time": '01-12-2017 00:00:00', #"when simulation starts"
                "experimenter": "name of the experimenter/username",
                "experiment_description": "described experiment/test description",
                "session_id": "str(hash(str(uuid.uuid1())))",
                "lab": "name of the lab",
                "institution": "name of the institution" }
        # since self.chosenmodel.regions = {'soma': 0.0, 'axon': 0.0}
        electrode_metadata_nostimulus = \
              {"soma": {"name": 'electrode_soma', "source": 'from neuron import h',
                        "location": 'soma', "slice": 'sec=0.5', "seal": 'no seal',
                        "filtering": 'no filter function', "resistance": '0 Ohm',
                        "initial_access_resistance": '0 Ohm',
                        "description": 'virtual patch-clamp electrode in soma without stimulation',
                        "device": 'NEURON 7.4 version'},
               "axon": {"name": 'electrode_axon', "source": 'from neuron import h',
                        "location": 'axon', "slice": 'sec=0.5', "seal": 'no seal',
                        "filtering": 'no filter function', "resistance": '0 Ohm',
                        "initial_access_resistance": '0 Ohm', 
                        "description": 'virtual patch-clamp electrode in axon without stimulation',
                        "device": 'NEURON 7.4 version'}}
        mynwbfile = self.fab.build_nwbfile(file_metadata)
        updated_mynwbfile, electrodes = self.fab.insert_intracell_electrodes(
                                                   self.chosenmodel,
                                                   electrode_metadata_nostimulus,
                                                   mynwbfile)
        compare1 = [ updated_mynwbfile.ic_electrodes[0].description,
                     updated_mynwbfile.ic_electrodes[1].description ]
        compare2 = [ electrodes['soma'].description, electrodes['axon'].description ]
        self.assertEqual( collections.Counter(compare1),
                          collections.Counter(compare2) )

    @unittest.skip("reason for skipping")
    def test_9_construct_nwbelectrodes_intracell_nostimulus(self):
        file_metadata = {
                "source": "Where is the data from?, i.e, platform",
                "session_description": "How was the data generated?, i.e, simulation of __",
                "identifier": "a unique modelID, uuid",
                "session_start_time": '01-12-2017 00:00:00', #"when simulation starts"
                "experimenter": "name of the experimenter/username",
                "experiment_description": "described experiment/test description",
                "session_id": "str(hash(str(uuid.uuid1())))",
                "lab": "name of the lab",
                "institution": "name of the institution" }
        # since self.chosenmodel.regions = {'soma': 0.0, 'axon': 0.0}
        electrode_metadata_nostimulus = \
              {"soma": {"name": 'electrode_soma', "source": 'from neuron import h',
                        "location": 'soma', "slice": 'sec=0.5', "seal": 'no seal',
                        "filtering": 'no filter function', "resistance": '0 Ohm',
                        "initial_access_resistance": '0 Ohm',
                        "description": 'virtual patch-clamp electrode in soma without stimulation',
                        "device": 'NEURON 7.4 version'},
               "axon": {"name": 'electrode_axon', "source": 'from neuron import h',
                        "location": 'axon', "slice": 'sec=0.5', "seal": 'no seal',
                        "filtering": 'no filter function', "resistance": '0 Ohm',
                        "initial_access_resistance": '0 Ohm', 
                        "description": 'virtual patch-clamp electrode in axon without stimulation',
                        "device": 'NEURON 7.4 version'}}
        mynwbfile = self.fab.build_nwbfile(file_metadata)
        updated_mynwbfile, electrodes = self.fab.construct_nwbelectrodes(
                                                   electype="intracell",
                                                   chosenmodel=self.chosenmodel,
                                                   elecmd=electrode_metadata_nostimulus,
                                                   nwbfile=mynwbfile)
        compare1 = [ updated_mynwbfile.ic_electrodes[0].name,
                     updated_mynwbfile.ic_electrodes[0].location,
                     updated_mynwbfile.ic_electrodes[0].description,
                     updated_mynwbfile.ic_electrodes[1].name,
                     updated_mynwbfile.ic_electrodes[1].location,
                     updated_mynwbfile.ic_electrodes[1].description ]
        compare2 = [ electrodes['soma'].name, electrodes['axon'].name,
                     electrodes['soma'].location, electrodes['axon'].location,
                     electrodes['soma'].description, electrodes['axon'].description ]
        self.assertEqual( collections.Counter(compare1),
                          collections.Counter(compare2) )

if __name__ == '__main__':
    unittest.main()
