# ~/managers/operatorsYield/recorder.py
import numpy as np

from neuron import h

class Recorder(object):
    """Operators working under RecordManager

    Available methods:
    time_NEURON
    response_voltage_NEURON
    stimulus_individual_currents_NEURON
    stimulus_overall_current_NEURON
    """

    @staticmethod
    def time_NEURON():
        """
        Use case:
        rc = Recorder()
        rec_t = rc.time_NEURON()
        """
        recorded_time = h.Vector()
        recorded_time.record(h._ref_t)
        return recorded_time

    @staticmethod
    def response_voltage_NEURON(section):
        """
        Use case:
        rc = Recorder()
        cell = Purkinje()
        vm_soma = rc.response_voltage_NEURON(cell.soma)
        axonNOR3 = rc.response_voltage_NEURON(cell.axonNOR3)
        """
        recorded_voltage = h.Vector()
        recorded_voltage.record(section(0.5)._ref_v)
        return recorded_voltage

    @staticmethod
    def stimulus_individual_currents_NEURON(stimuli):
        """
        Use case:
        rc = Recorder()
        injections = rc.stimulus_individual_currents_NEURON(stimuli)
        """
        no_of_stimuli = len(stimuli)
        recorded_currents = {}
        # record each current
        for i in range(no_of_stimuli):
            key = "stim"+str(i)
            recorded_currents.update( {key: h.Vector()} )
            recorded_currents[key].record( stimuli[i]._ref_i )
        return recorded_currents

    @staticmethod
    def stimulus_overall_current_NEURON(recorded_currents):
        """
        Use case:
        rc = Recorder()
        injections = rc.stimulus_individual_currents_NEURON(stimuli)
        overallinjection = rc.stimulus_overall_current_NEURON(injections)

        NOTE: This method should only be called AFTER h.run()
        """
        no_of_stimuli = len(recorded_currents)
        for i in range(no_of_stimuli - 1):
            j = i+1
            key = "stim"+str(j)
            recorded_currents["stim0"].add( recorded_currents[key] )
        return recorded_currents["stim0"]
        
