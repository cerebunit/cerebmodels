# ../managers/managerSignalProcessing.py

from managers.operatorsSignaling.converter import Converter

class SignalProcessingManager(object):

    def __init__(self):
        self.co = Converter()

    def transform_signal(self, tosignal=None, chosenmodel=None, recordings=None):
        """method that transforms the recorded 'response' signal.

        Keyword Arguments:
        chosenmodel -- instantiated NEURON based model
        recordings -- dictionary of the form
                      {"time": [list], "response": [list], "stimulus": [list]}
        tosignal -- string; 'spikes'

        Returned value:
        dictionary; region-name for key whose value is the transformed signal

        Use case:
        sm = SimulationManager()
        rm = RecordManager()
        sp = SignalProcessingManager()
        rec = {"time": None, "response": None, "stimulus": None}
        sm.prepare_model_NEURON (parameters, modelX)
        stimuli_list = sm.stimulate_model_NEURON (stimparameters = currparam,
                                                  modelsite = modelX.cell.soma)
        rec["time"], rec["response"], rec["stimulus"] = \
                       rm.prepare_recording_NEURON(modelX)
        sm.engage_NEURON()
        spikes = sp.transform_signal( chosenmodel = modelX,
                                      recordings = rec,
                                      tosignal = 'spikes' )

        """
        if (chosenmodel is None) or (recordings is None) or (tosignal is None):
            raise ValueError("A 'chosenmodel' must be simulated resulting in 'recordings' which you want to transform to a particular 'tosignal'")
        else:
            if tosignal is 'spikes':
                return self.co.voltage_to_spiketrain(chosenmodel, recordings)
            else: # add here for other as needed
                pass
