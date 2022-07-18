# ~/models/cells/modelGrC2020aMasoli.py
import os

pwd = os.getcwd()  # record root directory path ~/cerebmodels
path_to_files = pwd + os.sep + "models" + os.sep + "cells" + os.sep + \
                "GrC2020aMasoli" + os.sep  # record path to this model/folder

from models.cells.GrC2020aMasoli.Granule import GranuleRegular as Granule
from executive import ExecutiveControl
from managers.simulation import SimulationManager as sm
from managers.read import ReadManager as rm
from managers.signalprocessing import SignalProcessingManager as spm

import sciunit
from cerebtests.capabilities.cells.response import ProducesElectricalResponse
from cerebtests.capabilities.cells.measurements import ProducesSpikeFrequency


class GranuleCell(sciunit.Model,
                  ProducesElectricalResponse,
                  ProducesEphysMeasurement):
    """USE CASE:
    """

    # AFTER the model is in the HBP Validation Framework Model catalog, set the generated uuid
    # uuid = "22dc8fd3-c62b-4e07-9e47-f5829e038d6d"

    def __init__(self):
        ### ===================== Descriptive Attributes ======================
        self.modelscale = "cells"
        self.modelname = "GrC2020aMasoli"
        # ------specify cell-regions from with response are recorded-------
        self.regions = {"soma": ["v"]}
        self.recordingunits = {"v": "mV"}
        # -----------attributed inheritance from sciunit.Model--------------
        self.name = "Masoli et al. 2020 model of Regular Firing (non-adapting) GranuleCell"
        self.description = "Masoli et al. 2020 model of Regular Firing (non-adapting) GranuleCell (GrC) and published in 10.1038/s42003-020-0953-x This is the multi-compartment model. It models the rat granule cells because the model was derived from slices taken from 20 +/- 2 days old rats. This model is the SciUnit wrapped version of the NEURON model in modelDB accession # 265584."
        #
        ### =================== Instantiate cell template ====================
        sm.lock_and_load_model_libraries(modelscale=self.modelscale,
                                         modelname=self.modelname)
        os.chdir(path_to_files)
        self.cell = Granule()
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
        # ExecutiveControl.launch_model_raw("cells")
        print("Simulation produce_voltage_response starting ...")
        ec = ExecutiveControl()  # only works when in ~/cerebmodels
        model = ec.launch_model(parameters=kwargs["parameters"],
                                stimparameters=kwargs["stimparameters"],
                                stimloc=kwargs["stimloc"],
                                onmodel=kwargs["onmodel"], mode="raw")
        print("File saving ...")
        fullfilename = ec.save_response()
        setattr(model, "fullfilename", fullfilename)
        print("File saved.")
        print("Simulation produce_voltage_response Done.")
        return model

    # --------------- produce_spike_instantaneous_frequency ------------------
    def produce_spike_instantaneous_frequency(self, **kwargs):
        """
        kwargs = { "parameters": dictionary with keys,
                   "stimparameters": dictionary with keys "type" and "stimlist",
                   "onmodel": instantiated model }
        """
        print("Sim produce_spike_frequency starting ...")
        ec = ExecutiveControl()  # only works when in ~/cerebmodels
        model = ec.launch_model(parameters=kwargs["parameters"],
                                stimparameters=kwargs["stimparameters"],
                                stimloc=kwargs["stimloc"], onmodel=kwargs["onmodel"],
                                capabilities={"model": "produce_voltage_response",
                                              "vtest": ProducesElectricalResponse},
                                mode="capability")
        # self.fullfilename # already saved by invoking produce_voltage_response above
        # print("Signal Processing ...")
        nwbfile = rm.load_nwbfile(model.fullfilename)
        orderedepochs = rm.order_all_epochs_for_region(nwbfile=nwbfile, region="soma")
        timestamps_over_epochs = [rm.timestamps_for_epoch(orderedepochs[i])
                                  for i in range(len(orderedepochs))]
        data_over_epochs = [rm.data_for_epoch(orderedepochs[i])
                            for i in range(len(orderedepochs))]
        # meanfreqs = spm.distill_spike_meanfreq(timestamps=timestamps_over_epochs,
        #                                        datavalues=data_over_epochs)
        # print("Signal Processing Done.")
        setattr(model, "prediction", meanfreqs)
        print("Simulation produce_spike_frequency Done.")
        return model
