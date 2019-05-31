# ~/models/cells/modelGrC2001DAngelo.py
import os
pwd = os.getcwd() # record root directory path ~/cerebmodels
path_to_files = pwd + os.sep + "models" + os.sep + "cells" + os.sep + \
                "GrC2001DAngelo" + os.sep # record path to this model/folder

from models.cells.GrC2001DAngelo.Granule import Granule
from executive import ExecutiveControl
from managers.managerInterpret import InterpretManager

import sciunit
from cerebunit.capabilities.cells.response import ProducesElectricalResponse
from cerebunit.capabilities.cells.measurements import ProducesEphysMeasurement

class GranuleCell( sciunit.Model,
                   ProducesElectricalResponse,
                   ProducesEphysMeasurement ):
    """USE CASE:
    """

    # AFTER the model is in the HBP Validation Framework Model catalog, set the generated uuid
    #uuid = "22dc8fd3-c62b-4e07-9e47-f5829e038d6d"

    def __init__(self):
        ### ===================== Descriptive Attributes ======================
        self.modelscale = "cells"
        self.modelname = "GrC2001DAngelo"
        # ------specify cell-regions from with response are recorded-------
        self.regions = {"soma": 0.0}
        # -----------attributed inheritance from sciunit.Model--------------
        self.name = "D'Angelo et al. 2001 model of GranuleCell"
        self.description = "D'Angelo et al. 2001 model of GranuleCell (GrC) and published in 10.1523/JNEUROSCI.21-03-00759.2001 This is the single compartment model. It models the rat granule cells because the model was derived from slices taken from 20 +/- 2 days old rats. This model is the SciUnit wrapped version of the NEURON model in modelDB accession # 46839."
        #
        ### =================== Instantiate cell template ====================
        sm.lock_and_load_model_libraries(modelscale=self.modelscale,
                                         modelname=self.modelname)
        os.chdir(path_to_files)
        self.cell = Granule()
        os.chdir(pwd)
        ### ===============================================================
        self.prediction = "Nil"
        #

    # =======================================================================
    # +++++++++++++++++++++++ MODEL CAPABILITIES ++++++++++++++++++++++++++++
    # =======================================================================

    # --------------------- produce_voltage_response ------------------------
    def produce_voltage_response(self, runtimeparam=None, stimparam=None, model=None):
        """generic/essential model response

        **Keyword Arguments:**

        kwargs = { "parameters": dictionary with keys,
                   "stimparameters": None or dictionary with keys "type" and "stimlist",
                   "onmodel": instantiated model }
        """
        #ExecutiveControl.launch_model_raw("cells")
        print("Simulation starting ...")
        ec = ExecutiveControl() # only works when in ~/cerebmodels
        ec.launch_model( parameters = runtimeparam, mode = "raw"
                         stimparameters = stimparam,
                         stimloc = model.cell.soma, onmodel = model )
        print("File saving ...")
        self.fullfilename = ec.save_response()
        print("File saved.")
        print("Simulation Done.")

    # ----------------------- produce_restingVm -----------------------------
    def produce_restingVm(self, **kwargs):
        """
        kwargs = { "parameters": dictionary with keys,
                   "stimparameters": dictionary with keys "type" and "stimlist",
                   "onmodel": instantiated model }
        """
        print("Simulation starting ...")
        ec = ExecutiveControl() # only works when in ~/cerebmodels
        model = kwargs["onmodel"]
        ec.launch_model( parameters = kwargs["parameters"],
                         stimparameters = kwargs["stimparameters"],
                         stimloc = model.cell.soma, onmodel = model,
                         capabilities = {"model": "produce_voltage_response",
                                         "vtest": ProducesElectricalResponse} )
        print("File saving ...")
        ec.save_response()
        print("File saved.")
        print("Interpreting ...")
        im = InterpretManager()
        timestamps, datavalues = \
            im.get_data_and_time_values( loadednwbfile=ec.load_response(),                                                                    modelregion="soma")
        restingVm = \
           im.gather_efel_values( im.get_efel_results(timestamps, datavalues,
                                                      feature_name_list=["voltage_base"]),
                                  "voltage_base" )
        print("Interpreting Done.")
        print("Setting Prediction")
        setattr(model, "prediction", [v for v in restingVm if v is not None])
        print("Prediction Set.")
        print("Simulation Done.")
        #print(self.restingVm)

    # ----------------------- produce_spike_train ---------------------------
    def produce_spike_train(self, **kwargs):
        """
        Use case:
        """
        pass
