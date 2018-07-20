# ~/executive.py
import importlib
import time

from neuron import h

from utilities import UsefulUtils as uu
from managers.managerAccount import AccountManager
from managers.managerSimulation import SimulationManager

class ExecutiveControl(object):

    def __init__(self):
        self.am = AccountManager()
        self.sm = SimulationManager()

    def list_modelscales(self):
        return self.am.available_modelscales()

    def list_models(self, modelscale=None):
        x =  self.am.modelscale_inventory(model_scale=modelscale)
        if "DummyTest" in x: # DummyTest is the Dummy model for running test
            x.remove("DummyTest")
        return x

    def choose_model(self, modelscale=None, modelname=None):
        modelmodule = importlib.import_module("models."+modelscale+"."+"model"+modelname)
        chosenmodel = getattr(modelmodule, uu.classesinmodule(modelmodule)[0].__name__)
        self.chosenmodel = chosenmodel()
        return self.chosenmodel
        # NOTE: all model __init__ method will have the attributes
        # modelscale and modelname => self.chosenmodel.modelscale/modelname

    def launch_model( self, parameters = None, onmodel = None,
                      stimparameters = None, stimloc = None,
                      capabilities = {'model':None, 'test':None} ):
        if onmodel.modelscale is "cells":
            self.sm.prepare_model_NEURON( parameters, onmodel,
                                          modelcapability = capabilities['model'],
                                          cerebunitcapability = capabilities['test'] )
            self.sm.stimulate_model_NEURON( stimparameters, stimloc )
            self.sm.trigger_NEURON( onmodel,
                                    modelcapability = capabilities['model'] )
        return "model was successfully simulated" # for executiveTest.py
