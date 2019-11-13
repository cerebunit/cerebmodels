# ~/models/cells/modelPC1997bHausser.py
import os
pwd = os.getcwd() # record root directory path ~/cerebmodels
path_to_files = pwd + os.sep + "models" + os.sep + "cells" + os.sep + \
                "PC1997bHausser" + os.sep # record path to this model/folder

from models.cells.PC1997bHausser.Purkinje import Purkinje
from executive import ExecutiveControl
from managers.simulation import SimulationManager as sm
from managers.read import ReadManager as rm
from managers.signalprocessing import SignalProcessingManager as spm

import sciunit
from cerebunit.capabilities.cells.response import ProducesElectricalResponse
from cerebunit.capabilities.cells.measurements import ProducesEphysMeasurement
#from pdb import set_trace as breakpoint

class PurkinjeCell( sciunit.Model,
                   ProducesElectricalResponse,
                   ProducesEphysMeasurement ):
    """USE CASE:
    """

    # AFTER the model is in the HBP Validation Framework Model catalog, set the generated uuid
    #uuid = "22dc8fd3-c62b-4e07-9e47-f5829e038d6d"

    def __init__(self):
        ### ===================== Descriptive Attributes ======================
        self.modelscale = "cells"
        self.modelname = "PC1997bHausser"
        # ------specify cell-regions from with response are recorded-------
        self.regions = {"soma": ["v"], "dend_root": ["v"]}
        self.recordingunits = {"v": "mV"}
        # -----------attributed inheritance from sciunit.Model--------------
        self.name = "Hausser 20.2.1997 model of PurkinjeCell"
        self.description = "Hausser 20.2.1997 model of PurkinjeCell (PC) and used by Vetter et al. 2001 for Dendritica, published in 10.1152/jn.2001.85.2.926 This model is the SciUnit wrapped version of the NEURON model in modelDB accession # 7907."
        #
        ### =================== Instantiate cell template ====================
        sm.lock_and_load_model_libraries(modelscale=self.modelscale,
                                         modelname=self.modelname)
        os.chdir(path_to_files)
        self.cell = Purkinje()
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
    def produce_restingVm(self, roi, **kwargs):
        """
        roi, region of interest is a string, i.e, 1 key in chosenmodel.regions
        kwargs = { "parameters": dictionary with keys,
                   "stimparameters": dictionary with keys "type" and "stimlist",
                   "onmodel": instantiated model }
        """
        print("Sim produce_"+roi+"_restingVm starting ...")
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
        orderedepochs = rm.order_all_epochs_for_region(nwbfile=nwbfile, region=roi)
        timestamps_over_epochs = [ rm.timestamps_for_epoch( orderedepochs[i] )
                                   for i in range(len(orderedepochs)) ]
        data_over_epochs = [ rm.data_for_epoch( orderedepochs[i] )
                                   for i in range(len(orderedepochs)) ]
        baseVms = spm.distill_baseVm_pre_epoch( timestamps = timestamps_over_epochs,
                                                datavalues = data_over_epochs )
        #print("Signal Processing Done.")
        setattr(model, "prediction", baseVms)
        print("Simulation produce_"+roi+"_restingVm Done.")
        return model

    # ----------------------- produce_soma_restingVm --------------------------
    def produce_soma_restingVm(self, **kwargs):
        return self.produce_restingVm("soma v", **kwargs)

    # ----------------------- produce_soma_spikeheight ------------------------
    def produce_spikeheight(self, roi, **kwargs):
        """
        roi, region of interest is a string, i.e, 1 key in chosenmodel.regions
        kwargs = { "parameters": dictionary with keys,
                   "stimparameters": dictionary with keys "type" and "stimlist",
                   "onmodel": instantiated model }
        """
        print("Sim produce_"+roi+"_spikeheight starting ...")
        ec = ExecutiveControl() # only works when in ~/cerebmodels
        model = ec.launch_model( parameters = kwargs["parameters"],
                                 stimparameters = kwargs["stimparameters"],
                                 stimloc = kwargs["stimloc"], onmodel = kwargs["onmodel"],
                                 capabilities = {"model": "produce_voltage_response",
                                                 "vtest": ProducesElectricalResponse},
                                 mode="capability" )
        nwbfile = rm.load_nwbfile(model.fullfilename)
        orderedepochs = rm.order_all_epochs_for_region(nwbfile=nwbfile, region=roi)
        timestamps_over_epochs = [ rm.timestamps_for_epoch( orderedepochs[i] )
                                   for i in range(len(orderedepochs)) ]
        data_over_epochs = [ rm.data_for_epoch( orderedepochs[i] )
                                   for i in range(len(orderedepochs)) ]
        baseVm = spm.distill_baseVm_pre_epoch( timestamps = timestamps_over_epochs,
                                                datavalues = data_over_epochs )
        try:
            peakVms = spm.distill_peakVm_from_spikes( timestamps = timestamps_over_epochs,
                                                      datavalues = data_over_epochs )
        except:
            peakVms = baseVm
        setattr(model, "prediction", peakVms[0] - baseVm[0])
        print("Simulation produce_"+roi+"_spikeheight Done.")
        return model

    # ----------------------- produce_soma_spikeheight ------------------------
    def produce_soma_spikeheight(self, **kwargs):
        return self.produce_spikeheight("soma v", **kwargs)

    # ------------------ produce_soma_spikeheight_antidromic ------------------
    def produce_soma_spikeheight_antidromic(self, **kwargs):
        return self.produce_spikeheight("dend_root v", **kwargs)

    # ----------------------- produce_spike_train ---------------------------
    def produce_spike_train(self, **kwargs):
        """
        Use case:
        """
        pass
