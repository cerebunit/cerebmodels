# ~/models/cells/modelGrC2001DAngelo.py
import os
pwd = os.getcwd()
path_to_files = pwd + os.sep + "models" + os.sep + "cells" + os.sep + \
                "GrC2001DAngelo" + os.sep

from managers.managerSimulation import SimulationManager as sm
from models.cells.GrC2001DAngelo.Granule import Granule


class GranuleCell(object):
    """USE CASE:
    """

    # AFTER the model is in the HBP Validation Framework Model catalog, set the generated uuid
    #uuid = "22dc8fd3-c62b-4e07-9e47-f5829e038d6d"

    def __init__(self):
        ### =====================Instantiate the cell======================
        #path_to_files = pwd + os.sep + "models" + os.sep + "cells" + \
        #                os.sep + "GrC2001DAngelo" + os.sep
        #os.chdir(path_to_files) # change to path_to_files
        #self.cell = Granule()
        #os.chdir(pwd)           # reset to start directory
        # ------specify cell-regions from with response are recorded-------
        self.regions = {"soma": 0.0}
        ### ===============================================================
        #
        ### =====================Essential Attributes======================
        self.modelscale = "cells"
        self.modelname = "GrC2001DAngelo"
        # -----------attributed inheritance from sciunit.Model--------------
        # grc.name defaults to class name, i.e, GranuleCell
        self.name = "D'Angelo et al. 2001 model of GranuleCell"
        self.description = "D'Angelo et al. 2001 model of GranuleCell (GrC) and published in 10.1523/JNEUROSCI.21-03-00759.2001 This is the single compartment model. It models the rat granule cells because the model was derived from slices taken from 20 +/- 2 days old rats. This model is the SciUnit wrapped version of the NEURON model in modelDB accession # 46839."
        #
        sm.lock_and_load_model_libraries(modelscale=self.modelscale,
                                         modelname=self.modelname)
        os.chdir(path_to_files)
        self.cell = Granule()
        os.chdir(pwd)
        ### ===============================================================

    # =======================================================================
    # +++++++++++++++++++++++ MODEL CAPABILITIES ++++++++++++++++++++++++++++
    # =======================================================================

    # --------------------- produce_voltage_response ------------------------
    def produce_voltage_response():
        """generic/essential model response

        Argument:
        sm -- instantiated SimulationManager()
        """
        sm.engage_NEURON()
        
    # ----------------------- produce_spike_train ---------------------------
    def produce_spike_train(self, **kwargs):
        """
        Use case:
        """
        pass
