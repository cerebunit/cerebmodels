 #/managers/operatorsTranscribe/fabricatorTest.py
import unittest

import collections # for comparing unordered lists
import os
import sys
# import modules for other directories
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
# this is required for
from models.cells.modelDummyTest import DummyCell

from fabricator import Fabricator

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
                "session_id": "str(hash(str(uuid.uuid1())))",
                "lab": "name of the lab",
                "institution": "name of the institution" }
        nwbfile = self.fab.build_nwbfile(file_metadata)
        # "<class '__main__.ClassA'>" 1st"_"is 8 & last"'"is -2
        typestr = str(type(nwbfile))[8:-2] 
        self.assertEqual( typestr, "pynwb.file.NWBFile" )

    #@unittest.skip("reason for skipping")
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
        epoch_metadata_nostimulus = \
              {"epoch0soma": {"source": "soma", "start": 0.0, "stop": 10.0,
                              "description": "first epoch"},
               "epoch0axon": {"source": "axon", "start": 0.0, "stop": 10.0,
                              "description": "first epoch"},
               "epoch_tags": ('1_epoch_responses',)}
        mynwbfile = self.fab.build_nwbfile(file_metadata)
        updated_mynwbfile = Fabricator.insert_a_nwbepoch("epoch0axon",
                                                epoch_metadata_nostimulus,
                                                mynwbfile)
        # "<class '__main__.ClassA'>" 1st"_"is 8 & last"'"is -2
        typestr = str(type(updated_mynwbfile))[8:-2] 
        self.assertEqual( typestr, "pynwb.file.NWBFile" )

    #@unittest.skip("reason for skipping")
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
              {"epoch0soma": {"source": "soma", "start": 0.0, "stop": 10.0,
                              "description": "first epoch"},
               "epoch1soma": {"source": "soma", "start": 10.0, "stop": 20.0,
                              "description": "second epoch"},
               "epoch0axon": {"source": "axon", "start": 0.0, "stop": 10.0,
                              "description": "first epoch"},
               "epoch1axon": {"source": "axon", "start": 10.0, "stop": 20.0,
                              "description": "second epoch"},
               "epoch_tags": ('2_epoch_responses',)}
        mynwbfile = self.fab.build_nwbfile(file_metadata)
        updated_mynwbfile = Fabricator.insert_a_nwbepoch("epoch0axon",
                                                epoch_metadata_stimulus,
                                                mynwbfile)
        # "<class '__main__.ClassA'>" 1st"_"is 8 & last"'"is -2
        #typestr = str(type(updated_mynwbfile))[8:-2] 
        self.assertEqual( updated_mynwbfile.epoch_tags, ['2_epoch_responses'] )

    #@unittest.skip("reason for skipping")
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
              {"epoch0soma": {"source": "soma", "start": 0.0, "stop": 10.0,
                              "description": "first epoch"},
               "epoch0axon": {"source": "axon", "start": 0.0, "stop": 10.0,
                              "description": "first epoch"},
               "epoch_tags": ('1_epoch_responses',)}
        mynwbfile = self.fab.build_nwbfile(file_metadata)
        updated_mynwbfile = self.fab.construct_nwbepochs(
                                                epochmd=epoch_metadata_nostimulus,
                                                nwbfile=mynwbfile)
        self.assertEqual( collections.Counter(list(updated_mynwbfile.epochs.keys())),
                          collections.Counter(["epoch0soma", "epoch0axon"]) )

    #@unittest.skip("reason for skipping")
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
              {"epoch0soma": {"source": "soma", "start": 0.0, "stop": 10.0,
                              "description": "first epoch"},
               "epoch1soma": {"source": "soma", "start": 10.0, "stop": 20.0,
                              "description": "second epoch"},
               "epoch0axon": {"source": "axon", "start": 0.0, "stop": 10.0,
                              "description": "first epoch"},
               "epoch1axon": {"source": "axon", "start": 10.0, "stop": 20.0,
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

if __name__ == '__main__':
    unittest.main()
