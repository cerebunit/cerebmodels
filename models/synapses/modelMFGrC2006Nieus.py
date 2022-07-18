# ~/models/cells/modelMFGrC2006Nieus.py
import os
pwd = os.getcwd() # record root directory path ~/cerebmodels
path_to_files = pwd + os.sep + "models" + os.sep + "cells" + os.sep + \
                "MFGrC2006Nieus" + os.sep # record path to this model/folder

from models.cells.MFGrC2006Nieus.MossyGranule import MossyGranule
from executive import ExecutiveControl
from managers.simulation import SimulationManager as sm
from managers.read import ReadManager as rm
from managers.signalprocessing import SignalProcessingManager as spm

import sciunit
from cerebtests.capabilities.cells.response import ProducesElectricalResponse
from cerebtests.capabilities.cells.measurements import ProducesEphysMeasurement

class MossyFiberGranuleCell( sciunit.Model,
                             ProducesElectricalResponse,
                             ProducesEphysMeasurement ):
    """USE CASE:
    """

    # AFTER the model is in the HBP Validation Framework Model catalog, set the generated uuid
    #uuid = "22dc8fd3-c62b-4e07-9e47-f5829e038d6d"

    def __init__(self):
        ### ===================== Descriptive Attributes ======================
        self.modelscale = "synapses"
        self.modelname = "MGGrC2006Nieus"
        # ------specify cell-regions from with response are recorded-------
        self.regions = {"soma": 0.0}
        # -----------attributed inheritance from sciunit.Model--------------
        self.name = "Nieus et al. 2006 model of Mossy fiber to Granule cell soma"
        self.description = "Nieus 2006 model of MossyFiber (MF) to GranuleCell (GrC) and published in 10.1152/jn.00696.2005 This is the single compartment (soma) model. This model is the SciUnit wrapped version of the NEURON model in modelDB accession # 128446."
        #
        ### =================== Instantiate cell template ====================
        sm.lock_and_load_model_libraries(modelscale=self.modelscale,
                                         modelname=self.modelname)
        os.chdir(path_to_files)
        self.cell = MossyGranule()
        os.chdir(pwd)
        ### ===============================================================
        self.fullfilename = "nil"
        self.prediction = "nil"
        #

    # =======================================================================
    # +++++++++++++++++++++++ MODEL CAPABILITIES ++++++++++++++++++++++++++++
    # =======================================================================

    # --------------------- produce_voltage_response ------------------------
    def produce_voltage_response(self, **kwargs):
        """generic/essential model response

        **Keyword Arguments:**

        kwargs = { "parameters": dictionary with keys,
                   "stimparameters": None or dictionary with keys "type" and "stimlist",
                   "onmodel": instantiated model }
        """
        #ExecutiveControl.launch_model_raw("cells")
        print("Simulation produce_voltage_response starting ...")
        ec = ExecutiveControl() # only works when in ~/cerebmodels
        model = ec.launch_model( parameters = kwargs["parameters"],
                                 stimparameters = kwargs["stimparameters"],
                                 stimloc = kwargs["stimloc"],
                                 onmodel = kwargs["onmodel"], mode = "raw" )
        print("File saving ...")
        fullfilename = ec.save_response()
        setattr(model, "fullfilename", fullfilename)
        print("File saved.")
        print("Simulation produce_voltage_response Done.")
        return model

    # ----------------------- produce_restingVm -----------------------------
    def produce_restingVm(self, **kwargs):
        """
        kwargs = { "parameters": dictionary with keys,
                   "stimparameters": dictionary with keys "type" and "stimlist",
                   "onmodel": instantiated model }
        """
        print("Sim produce_restingVm starting ...")
        ec = ExecutiveControl() # only works when in ~/cerebmodels
        model = ec.launch_model( parameters = kwargs["parameters"],
                                 stimparameters = kwargs["stimparameters"],
                                 stimloc = kwargs["stimloc"], onmodel = kwargs["onmodel"],
                                 capabilities = {"model": "produce_voltage_response",
                                                 "vtest": ProducesElectricalResponse},
                                 mode="capability")
        #self.fullfilename # already saved by invoking produce_voltage_response above
        #print("Signal Processing ...")
        nwbfile = rm.load_nwbfile(model.fullfilename)
        orderedepochs = rm.order_all_epochs_for_region(nwbfile=nwbfile, region="soma")
        timestamps_over_epochs = [ rm.timestamps_for_epoch( orderedepochs[i] )
                                   for i in range(len(orderedepochs)) ]
        data_over_epochs = [ rm.data_for_epoch( orderedepochs[i] )
                                   for i in range(len(orderedepochs)) ]
        baseVms = spm.distill_Vm_pre_epoch( timestamps = timestamps_over_epochs,
                                            datavalues = data_over_epochs )
        #print("Signal Processing Done.")
        setattr(model, "prediction", baseVms)
        print("Simulation produce_restingVm Done.")
        return model

    # ----------------------- produce_spike_train ---------------------------
    def produce_spike_train(self, **kwargs):
        """
        Use case:
        """
        pass
