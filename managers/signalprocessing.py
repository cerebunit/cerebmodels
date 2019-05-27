# ../managers/signalprocessing.py

from managers.operatorsSignaling.converter import Converter as co

class SignalProcessingManager(object):
    """
    **Available methods:**

    +------------------------------+-----------------+
    | Method name                  |                 |
    +==============================+=================+
    | :py:meth:`.transform_signal` | static method   |
    +------------------------------+-----------------+

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
