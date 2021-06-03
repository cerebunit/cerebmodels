# ~/models/cells/modelPC2015Masoli.py
import os
pwd = os.getcwd()
path_to_files = pwd + os.sep + "models" + os.sep + "cells" + os.sep + \
                "PC2015Masoli" + os.sep

from models.cells.PC2015Masoli.Purkinje import Purkinje
from executive import ExecutiveControl
from managers.simulation import SimulationManager as sm
from managers.read import ReadManager as rm
from managers.signalprocessing import SignalProcessingManager as spm

import sciunit
from cerebunit.capabilities.cells.response import ProducesElectricalResponse
from cerebunit.capabilities.cells.measurements import ProducesSomaRestingVm, ProducesSomaSpikeHeight
#from pdb import set_trace as breakpoint

import numpy

class PurkinjeCell( sciunit.Model,
                   ProducesElectricalResponse,
                   ProducesSomaRestingVm ):
    """USE CASE:
    """

    # AFTER the model is in the HBP Validation Framework Model catalog, set the generated uuid
    #uuid = "22dc8fd3-c62b-4e07-9e47-f5829e038d6d"

    def __init__(self):
        ### ===================== Descriptive Attributes ======================
        self.modelscale = "cells"
        self.modelname = "PC2015Masoli"
        # ------specify cell-regions from with response are recorded-------
        self.regions = {"soma": ["v"], "dend": ["v"], "axonAIS": ["v"],
                        "axonNOR": ["v"], "axonNOR2": ["v"], "axonNOR3": ["v"]}
        self.recordingunits = {"v": "mV"}
        # -----------attributed inheritance from sciunit.Model--------------
        # pc.name defaults to class name, i.e, PurkinjeCell
        self.name = "Masoli et al. 2015 model of PurkinjeCell"
        self.description = "Masoli et al. 2015 model of PurkinjeCell (PC) and published in 10.3389/fncel.2015.00047 This is general PC model unlike special Z+ or Z- models. The model is based on adult (P90 or 3 months) Guinea pig. PC in younger ones are not mature and they grow until P90. This model is the SciUnit wrapped version of the NEURON model in modelDB accession # 229585."
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
        print("Sim produce_"+roi.replace(" ","_")+"_restingVm starting ...")
        ec = ExecutiveControl() # only works when in ~/cerebmodels
        model = ec.launch_model( parameters = kwargs["parameters"],
                                 stimparameters = kwargs["stimparameters"],
                                 stimloc = kwargs["stimloc"], onmodel = kwargs["onmodel"],
                                 capabilities = {"model": "produce_voltage_response",
                                                 "vtest": ProducesElectricalResponse},
                                 mode="capability")
        nwbfile = rm.load_nwbfile(model.fullfilename)
        orderedepochs = rm.order_all_epochs_for_region(nwbfile=nwbfile, region=roi)
        timestamps_over_epochs = [ rm.timestamps_for_epoch( orderedepochs[i] )
                                   for i in range(len(orderedepochs)) ]
        data_over_epochs = [ rm.data_for_epoch( orderedepochs[i] )
                                   for i in range(len(orderedepochs)) ]
        baseVms = spm.distill_baseVm_pre_epoch( timestamps = timestamps_over_epochs,
                                            datavalues = data_over_epochs )
        setattr(model, "prediction", baseVms)
        print("Simulation produce_"+roi.replace(" ","_")+"_restingVm Done.")
        return model

    # ----------------------- produce_soma_restingVm --------------------------
    def produce_soma_restingVm(self, **kwargs):
        return self.produce_restingVm("soma v", **kwargs)

    # ----------------------- produce_spikeheight -----------------------------
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
        kwargs["stimloc"] = "axonAIS"
        return self.produce_soma_spikeheight(**kwargs)

    # ----------------------- produce_inputR ----------------------------------
    def _compute_inputR(self, baseVms, stimpar):
        "private function called by produce_inputR"
        datapts = len(baseVms)
        list_Rin = []
        currents = stimpar["stimlist"]
        if datapts <= 1:
            raise ValueError("Simulation must be done with >= 3 epochs for computing Rin.")
        else:
            for i in range(datapts-1):
                numer = baseVms[i+1] - baseVms[i]
                denom = [ currents[i]["amp"]-0 if i==0 else
                          currents[i]["amp"]-currents[i-1]["amp"] ][0]
                list_Rin.append( numer/denom ) #Mohm
            return numpy.mean(list_Rin)

    def produce_inputR(self, roi, **kwargs):
        """
        roi, region of interest is a string, i.e, 1 key in chosenmodel.regions
        kwargs = { "parameters": dictionary with keys,
                   "stimparameters": dictionary with keys "type" and "stimlist",
                   "onmodel": instantiated model }
        """
        print("Sim produce_"+roi+"_inputR starting ...")
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
        baseVms = spm.distill_baseVm_pre_epoch( timestamps = timestamps_over_epochs,
                                                datavalues = data_over_epochs )
        setattr(model, "prediction", self._compute_inputR(baseVms, kwargs["stimparameters"]))
        print("Simulation produce_"+roi+"_inputR Done.")
        return model

    # ----------------------- produce_soma_inputR -----------------------------
    def produce_soma_inputR(self, **kwargs):
        return self.produce_inputR("soma v", **kwargs)

    # ----------------------- produce_spike_train ---------------------------
    def produce_spike_train(self, **kwargs):
        """
        Use case:
        """
        pass
