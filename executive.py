# ~/executive.py
import importlib
import time

from neuron import h

from utilities import UsefulUtils as uu
from managers.managerFiling import FilingManager as fm
from managers.managerSimulation import SimulationManager as sm
from managers.managerRecord import RecordManager as rm
from managers.managerTranscribe import TranscribeManager

class ExecutiveControl(object):
    """
    Main Use Methods:
    list_modelscales
    list_models
    choose_model
    launch_model
    save_response
    load_response

    Instance methods:
    launch_model
    save_response (call must be after launch_model)

    Static methods:
    list_modelscale
    list_models
    choose_model

    """

    def __init__(self):
        self.recordings = {"time": None, "response": None, "stimulus": None}
        self.tm = TranscribeManager()

    @staticmethod
    def list_modelscales():
        return fm.available_modelscales()

    @staticmethod
    def list_models(modelscale=None):
        x =  fm.modelscale_inventory(model_scale=modelscale)
        #if "DummyTest" in x: # DummyTest is the Dummy model for running test
        #    x.remove("DummyTest")
        return x

    @staticmethod
    def choose_model(modelscale=None, modelname=None):
        sm.lock_and_load_model_libraries(modelscale=modelscale, modelname=modelname)
        modelmodule = importlib.import_module("models."+modelscale+".model"+modelname)
        chosenmodel = getattr(modelmodule, uu.classesinmodule(modelmodule)[0].__name__)
        return chosenmodel()
        #return self.chosenmodel # the picked model is available as attribute
        # NOTE: all model __init__ method will have the attributes
        # modelscale and modelname => self.chosenmodel.modelscale/modelname

    def launch_model( self, parameters = None, onmodel = None,
                      stimparameters = None, stimloc = None,
                      capabilities = {'model':None, 'vtest':None} ):
        # NOTE: although it is convenient to use self.chosenmodel
        # to the user having explicitly choose onmodel as an argument is clearer
        uu.check_not_None_in_arg({'parameters': parameters, 'onmodel': onmodel})
        if onmodel.modelscale is "cells":
            sm.prepare_model_NEURON( parameters=parameters, chosenmodel=onmodel,
                                     modelcapability = capabilities['model'],
                                     cerebunitcapability = capabilities['vtest'] )
            stimuli_list = sm.stimulate_model_NEURON(
                                          stimparameters = stimparameters,
                                          modelsite = stimloc )
            self.recordings["time"], self.recordings["response"], rec_i_indivs = \
                    rm.prepare_recording_NEURON( onmodel,
                                                      stimuli = stimuli_list )
            sm.trigger_NEURON( onmodel, modelcapability = capabilities['model'] )
            self.recordings["stimulus"] = \
                    rm.postrun_record_NEURON( injectedcurrents = rec_i_indivs )
        # save the parameters as attributes
        self.chosenmodel = onmodel
        self.parameters = parameters
        self.stimparameters = stimparameters
        return "model was successfully simulated" # for executiveTest.py

    def save_response( self ):
        self.tm.load_metadata( chosenmodel = self.chosenmodel,
                               recordings = self.recordings,
                               runtimeparameters = self.parameters,
                               stimparameters = self.stimparameters )
        self.tm.compile_nwbfile()
        self.tm.save_nwbfile()

    def load_response( self ):
        pass
