# ~/models/cells/modelGrC2001DAngelo.py
import os
pwd = os.getcwd() # record root directory path ~/cerebmodels
path_to_files = pwd + os.sep + "models" + os.sep + "cells" + os.sep + \
                "GrC2001DAngelo" + os.sep # record path to this model/folder

from managers.managerSimulation import SimulationManager as sm
from models.cells.GrC2001DAngelo.Granule import Granule
from executive import ExecutiveControl
from managers.managerInterpret import InterpretManager as im

import sciunit
from cerebunit.capabilities.cells.response import ProducesElectricalResponse
from cerebunit.capabilities.measurements_ephys import ProducesEphysMeasurement

class GranuleCell( sciunit.Model,
                   ProducesElectricalResponse,
                   ProducesEphysMeasurement ):
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
        #
        ec = ExecutiveControl() # only works when in ~/cerebmodels

    # =======================================================================
    # +++++++++++++++++++++++ MODEL CAPABILITIES ++++++++++++++++++++++++++++
    # =======================================================================

    # --------------------- produce_voltage_response ------------------------
    def produce_voltage_response(self, **kwargs):
        """generic/essential model response

        Argument:
        sm -- instantiated SimulationManager()
        """
        sm.engage_NEURON()

    # ----------------------- produce_restingVm -----------------------------
    def produce_restingVm(self, **kwargs):
        """
        kwargs = { "parameters": dictionary with keys,
                   "stimparameters": dictionary with keys "type" and "stimlist",
                   "onmodel": instantiated model }
        """
        model = kwargs["onmodel"]
        ec.launch_model( parameters = kwargs["parameters"],
                         stimparameters = kwargs["stimparameters"],
                         stimloc = model.cell.soma, onmodel = model,
                         capabilities = {"model": "produce_voltage_response",
                                         "vtest": ProducesEletricalResponse} )
        ec.save_response()
        timestamps, datavalues = \
            im.get_data_and_time_values( loadednwbfile=ec.load_response(),                                                                    modelregion="soma")
        self.restingVm = \
            im.gather_efel_values( im.get_efel_results(timestamps, datavalues,
                                                      feature_name_list=["voltage_base"]),
                                   "voltage_base" )

    # ----------------------- produce_spike_train ---------------------------
    def produce_spike_train(self, **kwargs):
        """
        Use case:
        """
        pass
