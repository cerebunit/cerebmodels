# ../managers/managerSimulation.py
import os
import time

from managers.operatorsSimaudit.inspector import SimInspector as si
from managers.operatorsSimaudit.hardware import HardwareConfigurator as hc
from managers.operatorsSimaudit.assembler import SimAssembler as sa
from managers.operatorsSimaudit.stimulator import Stimulator

from neuron import h

st = Stimulator()

class SimulationManager(object):
    """
    **Available Methods:**

    +--------------------------------------+---------------------------+
    | Method name                          | Method type               |
    +======================================+===========================+
    | :py:meth:`.prepare_model_NEURON`     | static method             |
    +--------------------------------------+---------------------------+
    | :py:meth:`.stimulate_model_NEURON`   | static method             |
    +--------------------------------------+---------------------------+
    | :py:meth:`.trigger_NEURON`           | class method              |
    +--------------------------------------+---------------------------+
    | :py:meth:`.lock_and_load_capability` | static method             |
    +--------------------------------------+---------------------------+
    | :py:meth:`.engage_NEURON`            | static method             |
    +--------------------------------------+---------------------------+

    """

    def __init__(self):
        #self.si = SimInspector()
        #self.hc = HardwareConfigurator()
        #self.sa = SimAssembler()
        #self.st = Stimulator()
        pass

    @staticmethod
    def lock_and_load_model_libraries(modelscale=None, modelname=None):
        """Directs :ref:`SimInspector` to load ``nmodl`` libraries if it already exists or else creates them and then loads them.

        **Keyword Arguments:**

        +----------------------+----------------------------------+
        | Key                  | Value type                       |
        +======================+==================================+
        | ``modelscale``       | string; eg: ``"cells"``          |
        +----------------------+----------------------------------+
        | ``modelname``        | string; eg: ``"GrC2001DAngelo"`` |
        +----------------------+----------------------------------+

        **Returned value:** A string message "Model libraries area loaded" letting the user know.

        **Raised Exceptions:** ``ValueError`` is there are no ``model_scale``
 
        """
        if modelscale is None:
            raise ValueError("modelscale must be string: 'cells', 'circuits', 'networks'")
        elif modelscale=="cells":
            si.lock_and_load_nmodl(modelscale = modelscale, modelname = modelname)
            return "Model libraries area loaded" # for managerSimulationTest.py
       
    @staticmethod
    def prepare_model_NEURON( parameters=None, chosenmodel=None,
                              modelcapability = None, cerebunitcapability = None):
        """Directs :ref:`SimInspector` to check for compiled ``nmodl`` files (library) and optionally for capability, followd by directing the :ref:`HardwareConfigurator`. Then, the :ref:`SimAssembler`` is directed to set the run time parameters.

        **Keyword Arguments:**

        +------------------------------------+------------------------------------------------+
        | Key                                | Value type                                     |
        +====================================+================================================+
        | ``chosenmodel``                    | instantiated ``NEURON`` based model            |
        +------------------------------------+------------------------------------------------+
        | ``parameters``                     | dictionary with keys: ``"dt"``, ``"celsius"``, |
        |                                    |                      ``"tstop"``, ``"v_init"`` |
        +------------------------------------+------------------------------------------------+
        | ``modelcapability`` (optional)     | string; eg ``"produces_spike_train"``          |
        +------------------------------------+------------------------------------------------+
        | ``cerebunitcapability`` (optional) | imported class, for eg., ProducesSpikeTrain    |
        +------------------------------------+------------------------------------------------+

        **Returned value:** Nothing is returned

        *NOTE:*
        * although not manadatory it is recommended to use the keyword arguments
        * also ``modelcapability`` and ``cerebunitcapability`` is recommended especially if you want to use ``CerebUnit``

        **Use case:**

        ``>> modelmodule = importlib.import_module("models.cells.modelPC2015Masoli")``

        ``>> pickedmodel = getattr(modelmodule, uu.classesinmodule(modelmodule)[0].__name__)``

        ``>> chosenmodel = pickedmodel()``

        ``>> parameters = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}``

        ``>> sm = SimulationManager()``

        ``>> sm.prepare_model_NEURON(parameters=parameters, chosenmodel=chosenmodel)``

        """

        if (parameters is None) or (chosenmodel is None):
            raise ValueError("an instantiated model must be given for 'chosenmodel' with its runtime 'parameters'")
        else:
            #cls.lock_and_load_model_libraries(modelscale=chosenmodel.modelscale,
            #                                  modelname=chosenmodel.modelname)
            si.check_compatibility(capability_name = modelcapability,
                                        CerebUnit_capability = cerebunitcapability)
            hc.activate_cores()
            sa.set_runtime_NEURON(parameters = parameters)
            return "NEURON model is ready" # for managerSimulationTest.py

    @staticmethod
    def stimulate_model_NEURON(stimparameters=None, modelsite=None):
        """Stimulates the prepared model but before locking & loading the capability :py:meth:`.lock_and_load_capability` or before engaging the simulator :py:meth:`.engage_NEURON`. If arguments are passed, i.e, the model is to be stimulated then the :ref:`Stimulator` is directed to stimulate the model with the given parameters.

        **Keyword Arguments (optional):** If not stimulation is required then do not pass any arguments.

        +---------------------+--------------------------------------------------------------+
        | Key                 | Value type                                                   |
        +=====================+==============================================================+
        | ``stimparameters``  | - dictionary with keys ``"type"`` and ``"stimlist"``         |
        |                     | - value for ``"type"``is a two element list of strings       |
        |                     | - ``<stimulus category> <specific type of that category>``   |
        |                     | - the first element is ALWAYS ``<stimulus category>``        |
        |                     | - Eg: for current inject on a cell`` ["current", "IClamp"]`` |
        |                     | - value for `` "stimlist"`` is a list with elements as       |
        |                     | dictionary; like [ {}, {}, ... ]                             |
        |                     | - Eg1: [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},          |
        |                     | {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]             |
        |                     | - Eg2: [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0,  |
        |                     | "delay": 5.0},                                               |
        |                     | {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0,           |
        |                     | "delay": 10.0},                                              |
        |                     | {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0,           |
        |                     | "delay": 15.0},                                              |
        |                     | {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0,           |
        |                     | "delay": 20.0} ]                                             |
        +---------------------+--------------------------------------------------------------+
        | ``modelsite``       | section of the instantiated ``NEURON`` based model where you |
        |                     | would want to stimulate. For eg. ``chosenmodel.cell.soma``   |
        +---------------------+--------------------------------------------------------------+

        **Returned value:**

        * if ``stimparameters`` are given the returned value is a list of stimuli where each element is a ``hoc`` object. For current inject it is ``h.IClamp``, ``h.IRamp``, etc ...  depending on ``currenttype``, i.e, ``<specific type of that category>``.
        * if no argument is given it returns a string  ``"Model is not stimulated"``.

        *NOTE:*

        * even if the stimulation does not involve stimulation it is recommended to evoke this function (without the arguments off course).

        **Use case:**

        ``>> modelmodule = importlib.import_module("models.cells.modelPC2015Masoli")``

        ``>> pickedmodel = getattr(modelmodule, uu.classesinmodule(modelmodule)[0].__name__)``

        ``>> chosenmodel = pickedmodel()``

        ``>> runparameters = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}``

        ``>> currparameters = {"type": ["current", "IClamp"], "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0}, {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}``

        ``>> sm = SimulationManager()``

        ``>> sm.prepare_model_NEURON(runparameters, chosenmodel)``

        ``>> sm.stimulate_model_NEURON(stimparameters = currparamters, modelsite=chosenmodel.cell.soma)``

        """
        if stimparameters is None or modelsite is None:
            return "Model is not stimulated"
        elif ( "type" not in stimparameters or
             "stimlist" not in stimparameters or
             len(stimparameters["type"]) != 2 ):
            raise ValueError("stimparameters should be a dictionary with " 
                             "keys 'type' and 'stimlist' where" 
                             "'type': 2 element list of strings"
                                     "<stimulus category> <specific type of that category>" 
                                     "Eg: for current inject on cellular model" 
                                         "['current', 'IClamp']" 
                             "'stimlist': is a list with elements as dictionary"
                             "Eg: [ {'amp': 0.5, 'dur': 100.0, 'delay': 10.0}," 
                                   "{'amp': 1.0, 'dur': 50.0, 'delay': 10.0+100.0} ]")
        else:
            if stimparameters["type"][0] is "current":
                stimuli_list = st.inject_current_NEURON(
                                           currenttype = stimparameters["type"][1],
                                           injparameters = stimparameters["stimlist"],
                                           neuronsection = modelsite) 
                return stimuli_list

    @staticmethod
    def lock_and_load_capability(chosenmodel, modelcapability, **kwargs):
        """Loads model capability hence running the simulation. This is because a ``modelcapability`` is a method attribute of the model.

        **Arguments:**

        +-------------------------+-----------------------------------------------------------+
        | Argument                | Value type                                                |
        +=========================+===========================================================+
        | first argument          | instantiated model                                        |
        +-------------------------+-----------------------------------------------------------+
        | second argument         | string for modelcapability; eg ``"produces_spike_train"`` |
        +-------------------------+-----------------------------------------------------------+
        | ``**kwargs``            |  Optional Variable Keyword arguments.                     |
        +-------------------------+-----------------------------------------------------------+

        **Returned value:** Nothing is returned

        **Use case:**

        ``>> modelmodule = importlib.import_module("models.cells.modelPC2015Masoli")``

        ``>> pickedmodel = getattr(modelmodule, uu.classesinmodule(modelmodule)[0].__name__)``

        ``>> chosenmodel = pickedmodel()``

        ``>> sm = SimulationManager()``

        ``>> sm.lock_and_load_capability(chosenmodel, modelcapability="produce_spike_train")``

        """
        run_model = getattr(chosenmodel, modelcapability)
        return run_model(**kwargs)

    @staticmethod
    def engage_NEURON():
        """Starts the `NEURON <https://neuron.yale.edu/neuron/>`_ based model WITHOUT implementing capability.

        **Argument:** No argument is passed.

        **Returned values:** Nothing is returned.

        """
        h.finitialize()
        h.run()
        #print(str(h.dt) + " " + str(h.tstop))

    @classmethod
    def trigger_NEURON(cls, chosenmodel, modelcapability=None, **kwargs):
        """Starts the simulation by calling either :py:meth:`.lock_and_load_capability` or :py:meth:`.engage_NEURON`.

        **Arguments:**

        +-------------------------+----------------------------------------------+
        | Arguments               | Value type                                   |
        +=========================+==============================================+
        | first argument          | instantiated model                           |
        +-------------------------+----------------------------------------------+
        | ``modelcapability`` key | string for eg ``"produces_spike_train"``     |
        +-------------------------+----------------------------------------------+
        | ``**kwargs``            |  Optional Variable Keyword arguments.        |
        +-------------------------+----------------------------------------------+

        **Returned values:** Prints the duration of the simulation run and returns a string saying "model was successfully triggered via NEURON".

        """
        if (modelcapability is not None): #and (len(kwargs) != 0):
            start_time = time.clock()
            cls.lock_and_load_capability( chosenmodel,
                                          modelcapability = modelcapability, **kwargs )
        else:
            start_time = time.clock()
            cls.engage_NEURON()
        print("--- %s seconds ---" % (time.clock() - start_time))
        return "model was successfully triggered via NEURON" # for managerSimulationTest.py
