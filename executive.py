# ~/executive.py
import importlib
import time
import datetime

from neuron import h

from utilities import UsefulUtils as uu
from managers.filing import FilingManager as fm
from managers.simulation import SimulationManager as sm
from managers.record import RecordManager as rm
from managers.transcribe import TranscribeManager
#from managers.operatorsVisualize.reader import Reader

class ExecutiveControl(object):
    """
    **Available Methods:**

    +------------------------------+---------------------+
    | Method name                  | Method type         |
    +==============================+=====================+
    | :py:meth:`.list_modelscales` | static method       |
    +------------------------------+---------------------+
    | :py:meth:`.list_models`      | static method       |
    +------------------------------+---------------------+
    | :py:meth:`.choose_model`     | static method       |
    +------------------------------+---------------------+      
    | :py:meth:`.launch_model`     | instance method     |
    +------------------------------+---------------------+      
    | :py:meth:`.save_response`    | instance method     |
    +------------------------------+---------------------+
    | :py:meth:`.load_response`    | instance method     |
    +------------------------------+---------------------+

    """

    def __init__(self):
        self.recordings = {"time": None, "response": None, "stimulus": None}
        self.simtime = None
        self.tm = TranscribeManager()
        self.fullname = ""

    @staticmethod
    def list_modelscales():
        """Directs :ref:`FilingManager` to return available model scales.

        **Arguments:** no argument is passed to get the list of model scales.
        """
        x = fm.available_modelscales()
        if "__pycache__" in x:
            x.remove("__pycache__")
        return x

    @staticmethod
    def list_models(modelscale=None):
        """Directs :ref:`FilingManager` to return available model names for a given model scale.

        **Keyword Argument:**

        +----------------+---------------------------------------------------+
        | Key            | Value type                                        |
        +================+===================================================+
        | ``modelscale`` | string; egs. "cells", "microcircuits", "networks" |
        +----------------+---------------------------------------------------+

        *NOTE:* The string value will depend on the availability of model scales which can be checked using :py:meth:`.list_modelscales()`.
        """
        x =  fm.modelscale_inventory(model_scale=modelscale)
        return [model for model in x if model not in ["__pycache__", "DummyTest"]]

    @staticmethod
    def choose_model(modelscale=None, modelname=None):
        """Returns instantiated model for a desired model name available in the specified model scale.

        **Keyword Arguments:**

        +----------------+-------------+
        | Key            | Value type  |
        +================+=============+
        | ``modelscale`` | string      |
        +----------------+-------------+
        | ``modelname``  | string      |
        +----------------+-------------+

        *NOTE*: Currently only ``modelscale="cells"`` are supported. Future releases will include other model scales.
        """
        sm.lock_and_load_model_libraries(modelscale=modelscale, modelname=modelname)
        modelmodule = importlib.import_module("models."+modelscale+".model"+modelname)
        chosenmodel = getattr(modelmodule, uu.classesinmodule(modelmodule)[0].__name__)
        return chosenmodel()
        #return self.chosenmodel # the picked model is available as attribute
        # NOTE: all model __init__ method will have the attributes
        # modelscale and modelname => self.chosenmodel.modelscale/modelname

    def launch_model( self, parameters = None, onmodel = None,
                      stimparameters = None, stimloc = None,
                      capabilities = {'model':None, 'vtest':None},
                      mode="raw" ):
        """Directs the :ref:`SimulationManager` to launch simulation on an instantiated model.

        **Keyword Arguments:**

        +-------------------------------+---------------------------------+
        | Key                           | Value type                      |
        +===============================+=================================+
        | ``parameters``                | dictionary                      |
        +-------------------------------+---------------------------------+
        |  ``onmodel``                  | instantiated model              |
        +-------------------------------+---------------------------------+
        | ``stimparameters`` (optional) | dictionary                      |
        +-------------------------------+---------------------------------+
        | ``stimloc`` (optional)        | attribute of instantiated model |
        +-------------------------------+---------------------------------+
        | ``capabilities`` (optional)   | dictionary                      |
        +-------------------------------+---------------------------------+
        | ``mode`` (optional)           | string;                         |
        |                               |- "raw" (default), "capability"  |
        +-------------------------------+---------------------------------+

        * ``parameters``- *mandatory* whose value is a dictionary. For example, ``parameters = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}``
        * ``onmodel``- *mandatory* whose value is the instantiated model using :py:meth:`.choose_model()`. For example, ``onmodel = <instance>.choose_model(modelscale="a_chosen_scale", modelname="a_chosen_name")``.
        * ``stimparameters``- optional whose value is a dictionary. For example, ``{"type": ["current", "IClamp"], "stimlist": [ {'amp': 0.5, 'dur': 100.0, 'delay': 10.0}, {'amp': 1.0, 'dur': 50.0, 'delay': 10.0+100.0} ] }``.
        * ``stimloc``- optional (mandatory only if ``stimparameters`` argument is provided). Its value is an attribute of the instantiated model. Note that this instantiated model is the value for the mandatory keyword argument ``onmodel``.
        * ``capabilties``- optional whose value is a dictionary. The dictionary **must** have the keys ``model`` and ``vtest``. The value for ``model`` key is a string representing the models method. For example, ``model: "produce_voltage_response"``. The value for ``vtest`` key is a class imported from the installed ``CerebUnit``.

        *NOTE*: Calling this function returns the model as the attribute ``ExecutiveControl.chosenmodel``.
        """
        # NOTE: although it is convenient to use self.chosenmodel
        # to the user having explicitly choose onmodel as an argument is clearer
        uu.check_not_None_in_arg({'parameters': parameters, 'onmodel': onmodel})
        self.simtime = datetime.datetime.now()
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
            if mode == "raw":
                sm.engage_NEURON()
            elif mode == "capability":
                sm.trigger_NEURON( onmodel, modelcapability = capabilities['model'],
                                   # Below are the **kwargs for lock_and_load_capability
                                   parameters=parameters, stimparameters=stimparameters,
                                   stimloc=stimloc, onmodel=onmodel, mode="capability" )
            self.recordings["stimulus"] = \
                    rm.postrun_record_NEURON( injectedcurrents = rec_i_indivs )
        # save the parameters as attributes
        self.chosenmodel = onmodel
        self.parameters = parameters
        self.stimparameters = stimparameters
        return self.chosenmodel
        #return "model was successfully simulated" # for executiveTest.py

    def save_response( self ):
        """Returns filename after saving the model response into a `NWB <https://www.nwb.org/>`_ formated ``.h5`` file located in ``~/response/<modelscale>/<modelname>/`` in root directory of ``cerebmodels``.

        **Arguments:** no argument is passed.
        """
        self.tm.load_metadata( chosenmodel = self.chosenmodel,
                               simtime = self.simtime,
                               recordings = self.recordings,
                               runtimeparameters = self.parameters,
                               stimparameters = self.stimparameters )
        self.tm.compile_nwbfile()
        # saves and returns fullfilename (filepath+filename)
        self.fullfilename = self.tm.save_nwbfile()
        return self.fullfilename

#    def load_response( self ):
#        """Returns file (`NWB <https://www.nwb.org/>`_ formated``.h5`` file) by directing the :ref:`FilingManager` and the ``Reader`` in :ref:`RecordManager` operator to load the response following an earlier simulation run.

#        **Arguments:** no argument is passed.

#        *NOTE:* for now its ability is limited to loading (immediately) preceeding simulation response.
#        """
#        allfiles_paths = fm.show_filenames_with_path( [ "responses",
#                                                        self.chosenmodel.modelscale,
#                                                        self.chosenmodel.modelname ] )
        # extract filepath of current filename and load it using Reader()
#        loadedfile = Reader(allfiles_paths[self.filename])
#        loadedfile.chosenmodel = self.chosenmodel
#        return loadedfile
