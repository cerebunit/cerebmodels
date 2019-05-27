# ~/models/cells/modelPC2015Masoli.py
import os
pwd = os.getcwd()
path_to_files = pwd + os.sep + "models" + os.sep + "cells" + os.sep + \
                "PC2015Masoli" + os.sep

from managers.simulation import SimulationManager as sm
from models.cells.PC2015Masoli.Purkinje import Purkinje


class PurkinjeCell(object):
    """USE CASE:
    """

    # AFTER the model is in the HBP Validation Framework Model catalog, set the generated uuid
    #uuid = "22dc8fd3-c62b-4e07-9e47-f5829e038d6d"

    def __init__(self):
        ### =====================Instantiate the cell======================
        #path_to_files = pwd + os.sep + "models" + os.sep + "cells" + \
        #                os.sep + "PC2015Masoli" + os.sep
        #os.chdir(path_to_files) # change to path_to_files
        #self.cell = Purkinje()
        #os.chdir(pwd)           # reset to start directory
        # ------specify cell-regions from with response are recorded-------
        self.regions = {"soma": 0.0, "axonAIS": 0.0, "axonNOR3": 0.0}
        ### ===============================================================
        #
        ### =====================Essential Attributes======================
        self.modelscale = "cells"
        self.modelname = "PC2015Masoli"
        # -----------attributed inheritance from sciunit.Model--------------
        # pc.name defaults to class name, i.e, PurkinjeCell
        self.name = "Masoli et al. 2015 model of PurkinjeCell"
        self.description = "Masoli et al. 2015 model of PurkinjeCell (PC) and published in 10.3389/fncel.2015.00047 This is general PC model unlike special Z+ or Z- models. The model is based on adult (P90 or 3 months) Guinea pig. PC in younger ones are not mature and they grow until P90. This model is the SciUnit wrapped version of the NEURON model in modelDB accession # 229585."
        #
        sm.lock_and_load_model_libraries(modelscale=self.modelscale,
                                         modelname=self.modelname)
        os.chdir(path_to_files)
        self.cell = Purkinje()
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
