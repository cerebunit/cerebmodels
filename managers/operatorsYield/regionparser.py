# ~/managers/operatorsYield/regionparser.py
import numpy as np
from random import randint

from neuron import h

class RegionParser(object):
    """
    ** Available methods:**

    +-------------------------------------------------+------------------------+
    | Method name                                     | Method type            |
    +=================================================+========================+
    | :py:meth:`.get_regionkeylist`                   | static method          |
    +-------------------------------------------------+------------------------+
    | :py:meth:`.response_body_NEURON`                | static method          |
    +-------------------------------------------------+------------------------+
    | :py:meth:`.response_component_NEURON`           | static method          |
    +-------------------------------------------------+------------------------+
    | :py:meth:`.stimulus_individual_currents_NEURON` | static method          |
    +-------------------------------------------------+------------------------+
    | :py:meth:`.stimulus_overall_current_NEURON`     | static method          |
    +-------------------------------------------------+------------------------+
    | :py:meth:`.stimulus_overall_voltage_NEURON`     | static method          |
    +-------------------------------------------------+------------------------+

    """

    @staticmethod
    def get_regionlist(chosenmodel):
        """Returns an array (NEURON's ``h.Vector``) of recorded time.

        **Arguments:** No arguments

        **Returned value:** ``h.Vector`` of recorded times (time-axis). `More about this data type. <https://www.neuron.yale.edu/neuron/static/new_doc/programming/math/vector.html>`_

        **Use case:**

        ``>> rc = Recorder()``

        ``>> rec_t = rc.time_NEURON()``

        """
        regionlist = list(chosenmodel.regions.keys())
        [ regionlist.remove(key) for key in regionlist
                                    if type(chosenmodel.regions[key]) is dict ]
        return regionlist

    @staticmethod
    def get_componentgrouplist(chosenmodel):
        """Returns an array (NEURON's ``h.Vector``) of recorded time.

        **Arguments:** No arguments

        **Returned value:** ``h.Vector`` of recorded times (time-axis). `More about this data type. <https://www.neuron.yale.edu/neuron/static/new_doc/programming/math/vector.html>`_

        **Use case:**

        ``>> rc = Recorder()``

        ``>> rec_t = rc.time_NEURON()``

        """
        componentgrouplist = list(chosenmodel.regions.keys())
        [ componentgrouplist.remove(key) for key in componentgrouplist
                                    if type(chosenmodel.regions[key]) is not dict ]
        return componentgrouplist

    @staticmethod
    def get_regionlist_of_componentgroup(chosenmodel, componentgroup):
        """Returns an array (NEURON's ``h.Vector``) of recorded time.

        **Arguments:** No arguments

        **Returned value:** ``h.Vector`` of recorded times (time-axis). `More about this data type. <https://www.neuron.yale.edu/neuron/static/new_doc/programming/math/vector.html>`_

        **Use case:**

        ``>> rc = Recorder()``

        ``>> rec_t = rc.time_NEURON()``

        """
        return list(chosenmodel.regions[componentgroup].keys())

    @staticmethod
    def get_componentlist(chosenmodel, componentgroup, region):
        return list( chosenmodel.regions[componentgroup][region].keys() )

    @staticmethod
    def response_body_NEURON(region, rectype):
        """Returns an array (NEURON's ``h.Vector``) of recorded voltage response from a given cell section.

        **Arguments:** Pass a NEURON `section <https://www.neuron.yale.edu/neuron/static/new_doc/modelspec/programmatic/topology/secspec.html>`_ or a list whose elements are NEURON sections (e.g. dendrites) of the cell, assuming that the model is instantiated. An a rectype is a string such as "v", "i_membrane", "i_cap".

        NOTE: If the argument is a list of sections (of a particular anatomical region) then rather than record for each and every section within the list only one section is recorded. This one section is picked randomly hence each section has equal probability to be picked. Also, note that this picking of a section may be determined and done within the __cell template__ (**not** the model template). Then, the regions (passed here as the argument) will most likely be a NEURON section.

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
        recording = h.Vector()
        recording.record( getattr(section(0.5), "_ref_"+rectype) )
        return recording

    @staticmethod
    def response_component_NEURON(region, component, rectype):
        """Returns an array (NEURON's ``h.Vector``) of recorded voltage response from a given cell section.

        **Arguments:** Pass a NEURON `section <https://www.neuron.yale.edu/neuron/static/new_doc/modelspec/programmatic/topology/secspec.html>`_ or a list whose elements are NEURON sections (e.g. dendrites) of the cell, assuming that the model is instantiated.

        NOTE: If the argument is a list of sections (of a particular anatomical region) then rather than record for each and every section within the list only one section is recorded. This one section is picked randomly hence each section has equal probability to be picked. Also, note that this picking of a section may be determined and done within the __cell template__ (**not** the model template). Then, the regions (passed here as the argument) will most likely be a NEURON section.

        **Returned value:** ``h.Vector`` of recorded voltages. `More about this data type. <https://www.neuron.yale.edu/neuron/static/new_doc/programming/math/vector.html>`_

        **Use case:**

        ``>> rc = Recorder()``

        ``>> cell = Purkinje() # instantiate``

        ``>> vm_soma = rc.response_voltage_NEURON(cell.soma)``

        ``>> axonNOR3 = rc.response_voltage_NEURON(cell.axonNOR3)``

        """
        #if type(region).__name__=="Mechanism":
        compo = getattr(region(0.5), component)
        recording = h.Vector()
        recording.record( getattr(compo, "_ref_"+rectype) )
        return recording

    @staticmethod
    def stimulus_individual_currents_NEURON(stimuli):
        """Returns a dictionary with keys in the form: "stim0", "stim1", "stim2", and so on ..., each representing an interval of current injection. The value for each key is an array (NEURON's ``h.Vector``) of recorded current injections given to a cell section.

        **Arguments:** Pass a list made up of `h.Vector <https://www.neuron.yale.edu/neuron/static/new_doc/programming/math/vector.html>`_. The ``h.Vector``'s representing any of the available current types, like, ``h.IClamp``, ``h.IRamp``, etc ...

        **Returned value:** {"stim0": ``h.Vector``, "stim1": ``h.Vector``, ..., "stimN": ``h.Vector``} and each respective ``h.Vector`` contains the array of amplitude of the injected current for the respective interval.

        **Use case:**
        For current-clamping scenarios,

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
        For current-clamping scenarios,

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
        
    @staticmethod
    def stimulus_overall_voltage_NEURON(stimuli, voltclamp="SEClamp"):
        """Returns an array (NumPy) such that all the amplitude values (in ``h.SEClamp`` or ``h.VClamp`` is combined/flattened into just one. That is, one trace of all the voltage injections (amplitudes).

        **Arguments:** Pass a voltage clamping stimulus, either ``h.SEClamp`` or ``h.VClamp``. The argument is optional. It is the keyword argument __voltclamp__. By default it is "SEClamp" because for NEURON this is the `recommended voltage clamping method <https://www.neuron.yale.edu/phpBB/viewtopic.php?t=505>`_. However, in those special cases where ``h.VClamp`` is used the user **must** pass the keyword argument ``voltclamp = "VClamp"``.

        **Returned value:** An array of stimulus, voltage amplitudes.

        **Use case:**
        For current-clamping scenarios,

        ``>> rc = Recorder()``

        ``>> overallinjection = rc.stimulus_overall_voltage_NEURON(injections)``

        *NOTE:*

        * This method should only be called AFTER ``h.run()``
        * When the amplitude is 0 the corresponding array value is equal to ``h.v_init``

        """
        clamped_voltages = np.linspace(h.v_init, h.v_init, int(h.tstop/h.dt) + 1)
        time_axis = np.arange(0, h.tstop+h.dt, h.dt)
        i = 0
        if voltclamp=="VClamp":
            for t in time_axis:
                if t < stimuli.dur[0]-h.dt:
                    clamped_voltages[i] = clamped_voltages[i] + stimuli.amp[0]
                elif (t >= stimuli.dur[0]-h.dt) and (t < stimuli.dur[1]-h.dt):
                    clamped_voltages[i] = clamped_voltages[i] + stimuli.amp[1]
                elif (t >= stimuli.dur[1]-h.dt) and (t < stimuli.dur[2]-h.dt):
                    clamped_voltages[i] = clamped_voltages[i] + stimuli.amp[2]
                elif t >= stimuli.dur[2]-h.dt:
                    clamped_voltages[i] = clamped_voltages[i]
                i += 1
        else: #voltclamp=="SEClamp" #DEFAULT
            for t in time_axis:
                if t < stimuli.dur1-h.dt:
                    clamped_voltages[i] = clamped_voltages[i] + stimuli.amp1
                elif (t >= stimuli.dur1-h.dt) and (t < stimuli.dur2-h.dt):
                    clamped_voltages[i] = clamped_voltages[i] + stimuli.amp2
                elif (t >= stimuli.dur2-h.dt) and (t < stimuli.dur3-h.dt):
                    clamped_voltages[i] = clamped_voltages[i] + stimuli.amp3
                elif t >= stimuli.dur3-h.dt:
                    clamped_voltages[i] = clamped_voltages[i]
                i += 1
        return clamped_voltages
