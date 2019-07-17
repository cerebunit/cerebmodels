# ~/managers/operatorsYield/recorder.py
import numpy as np
from random import randint

from neuron import h

class Recorder(object):
    """
    ** Available methods:**

    +-------------------------------------------------+------------------------+
    | Method name                                     | Method type            |
    +=================================================+========================+
    | :py:meth:`.time_NEURON`                         | static method          |
    +-------------------------------------------------+------------------------+
    | :py:meth:`.response_voltage_NEURON`             | static method          |
    +-------------------------------------------------+------------------------+
    | :py:meth:`.stimulus_individual_currents_NEURON` | static method          |
    +-------------------------------------------------+------------------------+
    | :py:meth:`.stimulus_overall_current_NEURON`     | static method          |
    +-------------------------------------------------+------------------------+

    """

    @staticmethod
    def time_NEURON():
        """Returns an array (NEURON's ``h.Vector``) of recorded time.

        **Arguments:** No arguments

        **Returned value:** ``h.Vector`` of recorded times (time-axis). `More about this data type. <https://www.neuron.yale.edu/neuron/static/new_doc/programming/math/vector.html>`_

        **Use case:**

        ``>> rc = Recorder()``

        ``>> rec_t = rc.time_NEURON()``

        """
        recorded_time = h.Vector()
        recorded_time.record(h._ref_t)
        return recorded_time

    @staticmethod
    def response_voltage_NEURON(region):
        """Returns an array (NEURON's ``h.Vector``) of recorded voltage response from a given cell section.

        **Arguments:** Pass a NEURON `section <https://www.neuron.yale.edu/neuron/static/new_doc/modelspec/programmatic/topology/secspec.html>`_ or a list whose elements are NEURON sections (e.g. dendrites) of the cell, assuming that the model is instantiated.

        **Returned value:** ``h.Vector`` of recorded voltages. `More about this data type. <https://www.neuron.yale.edu/neuron/static/new_doc/programming/math/vector.html>`_

        **Use case:**

        ``>> rc = Recorder()``

        ``>> cell = Purkinje() # instantiate``

        ``>> vm_soma = rc.response_voltage_NEURON(cell.soma)``

        ``>> axonNOR3 = rc.response_voltage_NEURON(cell.axonNOR3)``

        """
        if isinstance(region, type(h.Section())):
            section = region
        else:
            section = region[ randint(0, len(region)-1) ]
        #
        recorded_voltage = h.Vector()
        recorded_voltage.record(section(0.5)._ref_v)
        return recorded_voltage

    @staticmethod
    def stimulus_individual_currents_NEURON(stimuli):
        """Returns a dictionary with keys in the form: "stim0", "stim1", "stim2", and so on ..., each representing an interval of current injection. The value for each key is an array (NEURON's ``h.Vector``) of recorded current injections given to a cell section.

        **Arguments:** Pass a list made up of `h.Vector <https://www.neuron.yale.edu/neuron/static/new_doc/programming/math/vector.html>`_. The ``h.Vector``'s representing any of the available current types, like, ``h.IClamp``, ``h.IRamp``, etc ...

        **Returned value:** {"stim0": ``h.Vector``, "stim1": ``h.Vector``, ..., "stimN": ``h.Vector``} and each respective ``h.Vector`` contains the array of amplitude of the injected current for the respective interval.

        **Use case:**

        ``>> rc = Recorder()``

        ``>> injections = rc.stimulus_individual_currents_NEURON(stimuli)``

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
        """Returns an array, NEURON's `h.Vector <https://www.neuron.yale.edu/neuron/static/new_doc/programming/math/vector.html>`_, such that all the ``h.Vector``'s from :py:meth:`.stimulus_individual_currents_NEURON` is combined/flattened into just one. That is, one trace of all the current injections (amplitudes).

        **Arguments:** Pass the dictionary {"stim0": ``h.Vector``, "stim1": ``h.Vector``, ..., "stimN": ``h.Vector``} with each respective ``h.Vector`` containing the array of amplitude of the injected current for the respective interval.

        *NOTE:* The dictionary for the argument is the returned value of :py:meth:`.stimulus_individual_currents_NEURON`.

        **Returned value:** ``h.Vector`` of recorded currents. `More about this data type. <https://www.neuron.yale.edu/neuron/static/new_doc/programming/math/vector.html>`_

        **Use case:**

        ``>> rc = Recorder()``

        ``>> injections = rc.stimulus_individual_currents_NEURON(stimuli)``

        ``>> overallinjection = rc.stimulus_overall_current_NEURON(injections)``

        *NOTE:*

        * This method should only be called AFTER ``h.run()``
        * Flattening of the currents is done by appending into the value of "stim0", i.e., appending into its ``h.Vector``.

        """
        no_of_stimuli = len(recorded_currents)
        for i in range(no_of_stimuli - 1):
            j = i+1
            key = "stim"+str(j)
            recorded_currents["stim0"].add( recorded_currents[key] )
        return recorded_currents["stim0"]
        
