# ../managers/managerSimulation.py
import os

from managers.operatorsSimaudit.inspector import SimInspector
from managers.operatorsSimaudit.hardware import HardwareConfigurator
from managers.operatorsSimaudit.assembler import SimAssembler

class SimulationManager(object):

    def __init__(self):
        self.si = SimInspector()
        self.hc = HardwareConfigurator()
        self.sa = SimAssembler()

    def prepare_model_NEURON(self, parameters, chosenmodel, modelcapability = None,
                      cerebunitcapability = None):
        """method that checks for compiled nmodl and optionally for capability.

        Argument (mandatory):
        instantiated NEURON based model
        parameters -- dictionary wit keys: dt, celsius, tstop, v_init

        Keyword arguments (optional):
        modelcapability -- string; eg "produces_spike_train"
        cerebunitcapability -- imported class, for eg., ProducesSpikeTrain

        Returned value:
        nothing is returned

        Use case:
        modelmodule = importlib.import_module("models.cells.modelPC2015Masoli")
        pickedmodel = getattr(modelmodule, uu.classesinmodule(modelmodule)[0].__name__)
        chosenmodel = pickedmodel()
        sm = SimulationManager()
        sm.prepare_model_NEURON(chosenmodel)

        """

        self.si.lock_and_load_nmodl(modelscale = chosenmodel.modelscale,
                                    modelname = chosenmodel.modelname)
        self.si.check_compatibility(capability_name = modelcapability,
                                    CerebUnit_capability = cerebunitcapability)
        self.hc.activate_cores()
        self.sa.set_runtime_NEURON(parameters = parameters)
        return "NEURON model is ready" # for managerSimulationTest.py

    def lock_and_load_capability(self, chosenmodel, modelcapability=None):
        """method loads model capability hence running the simulation

        Argument (mandatory):
        instantiated model

        Keyword arguments (mandatory):
        modelcapability -- string; eg "produces_spike_train"

        Returned value:
        nothing is returned

        Use case:
        modelmodule = importlib.import_module("models.cells.modelPC2015Masoli")
        pickedmodel = getattr(modelmodule, uu.classesinmodule(modelmodule)[0].__name__)
        chosenmodel = pickedmodel()
        sm = SimulationManager()
        sm.lock_and_load_capability(chosenmodel, modelcapability="produce_spike_train")

        """
        run_model = getattr(chosenmodel, modelcapability)
        return run_model()

