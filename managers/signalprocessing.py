# ../managers/signalprocessing.py

import efel
from quantities import mV

from managers.operatorsSignaling.converter import Converter as co
from managers.operatorsSignaling.reconstructer import Reconstructer as recons

class SignalProcessingManager(object):
    """
    **Available methods:**

    +----------------------------------+-----------------+
    | Method name                      | Method type     |
    +==================================+=================+
    | :py:meth:`.transform_signal`     | static method   |
    +----------------------------------+-----------------+
    | :py:meth:`.distill_Vm_pre_epoch` | static method   |
    +----------------------------------+-----------------+

    """

    def __init__(self):
        pass

    @staticmethod
    def transform_signal(tosignal=None, chosenmodel=None, recordings=None):
        """Transforms the recorded 'response' signal.

        **Keyword Arguments:**

        +---------------------+----------------------------------------------------------------+
        | Key                 | Value type                                                     |
        +=====================+================================================================+
        | ``chosenmodel``     | instantiated NEURON based model                                |
        +---------------------+----------------------------------------------------------------+
        | ``recordings``      | - dictionary of the form                                       |
        |                     | - ``{"time": [list], "response": [list], "stimulus": [list]}`` |
        +---------------------+----------------------------------------------------------------+
        | ``tosignal``        | string; "spikes"                                               |
        +---------------------+----------------------------------------------------------------+

        **Returned value:** dictionary; region-name for key whose value is the transformed signal

        **Use case:**

        Let's first set up as follows

        ``>> sm = SimulationManager()``

        ``>> rm = RecordManager()``

        ``>> sp = SignalProcessingManager()``

        ``>> rec = {"time": None, "response": None, "stimulus": None}``

        ``>> sm.prepare_model_NEURON (parameters, modelX)``

        ``>> stimuli_list = sm.stimulate_model_NEURON (stimparameters = currparam, modelsite = modelX.cell.soma)``

        ``>> rec["time"], rec["response"], rec["stimulus"] = rm.prepare_recording_NEURON(modelX)``

        ``>> sm.engage_NEURON()``

        Then to transform the analog signals into spike, do

        ``>> spikes = sp.transform_signal( chosenmodel = modelX, recordings = rec, tosignal = 'spikes' )``

        *NOTE:* Currently only ``tosignal="spikes"`` is supported.

        """
        if (chosenmodel is None) or (recordings is None) or (tosignal is None):
            raise ValueError("A 'chosenmodel' must be simulated resulting in 'recordings' which you want to transform to a particular 'tosignal'")
        else:
            if tosignal is 'spikes':
                return co.voltage_to_spiketrain(chosenmodel, recordings)
            else: # add here for other as needed
                pass

    @staticmethod
    def distill_Vm_pre_epoch(timestamps=None, datavalues=None):
        """Returns an array of voltage for each epoch, such that, each voltage is the voltage right before an epoch.

        **Keyword Arguments:**

        +----------------+-------------------------------+
        | Key            | Value type                    |
        +================+===============================+
        | ``timestamps`` | list of array of timestamps   |
        +----------------+-------------------------------+
        | ``datavalues`` | list of array of data values  |
        +----------------+-------------------------------+

        *NOTE:* Think of each array within a list corresponding to respective values (timestamps or data) of *an* epoch.

        """
        if (timestamps is None) or (datavalues is None):
            raise ValueError("Must pass list of array of times and list of array of data (voltage) values.")
        else:
            traces = recons.construct_base_efel_trace_overall(timestamps, datavalues)
            efelvalues = [ (lambda tr:
                              "nil" if tr["stim_start"][0]==0. # there is not voltage before t=0
                              else efel.getFeatureValues([tr],["voltage_base"])[0])
                           (a_trace)
                           for a_trace in traces ]
            return [ a_value["voltage_base"]*mV                    # mV unit
                     for a_value in efelvalues if a_value!="nil" ] # ~ efelvalues.remove("nil")

