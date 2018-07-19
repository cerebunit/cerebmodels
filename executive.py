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
                      capabilities = {'model':None, 'test':None} ):
        self.sm.prepare_model_NEURON( parameters, onmodel,
                                      modelcapability = capabilities['model'],
                                      cerebunitcapability = capabilities['test'] )
        if capabilities['model'] is not None:
            start_time = time.clock()
            self.sm.lock_and_load_capability( onmodel,
                                              modelcapability = capabilities['model'] )
            #run_model = getattr(onmodel, capabilities['model'])
            #run_model()
        else:
            #h.finitialize()
            start_time = time.clock()
            #h.run()
            self.sm.engage_NEURON()
        print("--- %s seconds ---" % (time.clock() - start_time))
        return "model was successfully simulated" # for executiveTest.py
