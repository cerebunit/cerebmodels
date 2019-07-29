# ~/managers/operatorsYield/regionParserTest.py
import unittest

from collections import Counter

import os
import sys
# import modules from other directories
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
# this is required for

pwd = os.getcwd()
os.chdir("..") # this moves you up to ~/managers
os.chdir("..") # you are now in parent /cerebmodels
rootwd = os.getcwd()
from models.cells.modelDummyTest import DummyCell
os.chdir(pwd)

#from utilities import UsefulUtils as uu
#from managers.simulation import SimulationManager as sm

from regionparser import RegionParser as rp

#import numpy as np

class RegionParserTest(unittest.TestCase):

    def setUp(self):
        os.chdir(rootwd)
        self.chosenmodel = DummyCell()
        os.chdir(pwd)

    #@unittest.skip("reason for skipping")
    def test_1_get_regionlist(self):
        # self.chosenmodel.regions ->
        # {'axon': ['v'], 'soma': ['v', 'i_cap'], 'channels': {'axon': {'pas': ['i']},
        # 'soma': {'hh': ['il', 'el'], 'pas': ['i']}}}
        regionlist = rp.get_regionlist(self.chosenmodel)
        a = ( Counter(regionlist) == Counter(["soma", "axon"]) )
        self.assertEqual( a, True )

    #@unittest.skip("reason for skipping")
    def test_2_get_componentgrouplist(self):
        # self.chosenmodel.regions ->
        # {'axon': ['v'], 'soma': ['v', 'i_cap'], 'channels': {'axon': {'pas': ['i']},
        # 'soma': {'hh': ['il', 'el'], 'pas': ['i']}}}
        componentgrouplist = rp.get_componentgrouplist(self.chosenmodel)
        a = ( Counter(componentgrouplist) == Counter(["channels"]) )
        self.assertEqual( a, True )

    #@unittest.skip("reason for skipping")
    def test_3_get_regionlist_of_componentgroup(self):
        # self.chosenmodel.regions ->
        # {'axon': ['v'], 'soma': ['v', 'i_cap'], 'channels': {'axon': {'pas': ['i']},
        # 'soma': {'hh': ['il', 'el'], 'pas': ['i']}}}
        regionlist_of_comp = rp.get_regionlist_of_componentgroup(self.chosenmodel, "channels")
        a = ( Counter(regionlist_of_comp) == Counter(["soma", "axon"]) )
        self.assertEqual( a, True )

    #@unittest.skip("reason for skipping")
    def test_4_get_componentlist(self):
        # self.chosenmodel.regions ->
        # {'axon': ['v'], 'soma': ['v', 'i_cap'], 'channels': {'axon': {'pas': ['i']},
        # 'soma': {'hh': ['il', 'el'], 'pas': ['i']}}}
        complist_for_soma = rp.get_componentlist(self.chosenmodel, "channels", "soma")
        complist_for_axon = rp.get_componentlist(self.chosenmodel, "channels", "axon")
        a = ( Counter(complist_for_soma) != Counter(complist_for_axon) )
        self.assertEqual( a, True )

if __name__ == '__main__':
    unittest.main()
