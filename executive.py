# ~/executive.py
import importlib
import time

from neuron import h

from utilities import UsefulUtils as uu
from managers.managerFiling import FilingManager
from managers.managerSimulation import SimulationManager
from managers.managerRecord import RecordManager
from managers.managerTranscribe import TranscribeManager

class ExecutiveControl(object):

    def __init__(self):
        self.fm = FilingManager()
        self.sm = SimulationManager()
        self.rm = RecordManager()
        self.recordings = {"time": None, "response": None, "stimulus": None}
        self.tm = TranscribeManager()

    def list_modelscales(self):
        return self.fm.available_modelscales()

    def list_models(self, modelscale=None):
        x =  self.fm.modelscale_inventory(model_scale=modelscale)
        #if "DummyTest" in x: # DummyTest is the Dummy model for running test
        #    x.remove("DummyTest")
        return x

    def choose_model(self, modelscale=None, modelname=None):
        modelmodule = importlib.import_module("models."+modelscale+"."+"model"+modelname)
        chosenmodel = getattr(modelmodule, uu.classesinmodule(modelmodule)[0].__name__)
        self.chosenmodel = chosenmodel()
        return self.chosenmodel # the picked model is available as attribute
        # NOTE: all model __init__ method will have the attributes
        # modelscale and modelname => self.chosenmodel.modelscale/modelname

    def launch_model( self, parameters = None, onmodel = None,
                      stimparameters = None, stimloc = None,
                      capabilities = {'model':None, 'test':None} ):
        # NOTE: although it is convenient to use self.chosenmodel
        # to the user having explicitly choose onmodel as an argument is clearer
        uu.check_not_None_in_arg({'parameters': parameters, 'onmodel': onmodel})
        if onmodel.modelscale is "cells":
            self.sm.prepare_model_NEURON( parameters=parameters, chosenmodel=onmodel,
                                          modelcapability = capabilities['model'],
                                          cerebunitcapability = capabilities['test'] )
            stimuli_list = self.sm.stimulate_model_NEURON(
                                          stimparameters = stimparameters,
                                          modelsite = stimloc )
            self.recordings["time"], self.recordings["response"], rec_i_indivs = \
                    self.rm.prepare_recording_NEURON( onmodel,
                                                      stimuli = stimuli_list )
            self.sm.trigger_NEURON( onmodel,
                                    modelcapability = capabilities['model'] )
            self.recordings["stimulus"] = \
                    self.rm.postrun_record_NEURON( injectedcurrents = rec_i_indivs )
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
