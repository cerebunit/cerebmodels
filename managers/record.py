# ../managers/record.py

from managers.operatorsYield.recorder import Recorder as rc

class RecordManager(object):
    """
    **Available methods:**

    +----------------------------------------+-----------------------+
    | Method name                            | Method type           |
    +========================================+=======================+
    | :py:meth:`.prepare_recording_NEURON`   | class method          |
    +----------------------------------------+-----------------------+
    | :py:meth:`.create_response_dictionary` | static method         |
    +----------------------------------------+-----------------------+
    | :py:meth:`.postrun_record_NEURON`      | static method         |
    +----------------------------------------+-----------------------+

    """

    def __init__(self):
        #self.rc = Recorder()
        pass

    @staticmethod
    def create_regionslist_str(chosenmodel, without=None):
        """Returns a list of strings of region names

        **Arguments:**

        +--------------------+------------------------------+
        | Argument           |                              |
        +====================+==============================+
        | first argument     | instantiated NEURON model    |
        +--------------------+------------------------------+
        | without (optional) | None (default) or "channels" |
        +--------------------+------------------------------+

        """
        strip_channels_key = \
         lambda keyslist: keyslist.remove("channels") if "channels" in keyslist else keyslist
        x = list(chosenmodel.regions.keys())
        if without=="channels":
            strip_channels_key(x)
        return x

    @staticmethod
    def create_response_dictionary(regionslist_str, responselist_num):
        """Returns a dictionary whose value represent model response

        **Arguments:**

        +-----------------+-------------------------------------------------+
        | Argument        | Value type                                      |
        +=================+=================================================+
        | first argument  | list of strings; names of the regions           |
        +-----------------+-------------------------------------------------+
        | second argument | list of numbers/array; list of lists            |
        +-----------------+-------------------------------------------------+

        *NOTE:* ``len(regionslist_str) == len(responselist_num)``

        """
        x = {}
        [ x.update({regionslist_str[i]: responselist_num[i]})
                                    for i in range(len(regionslist_str)) ]
        return x

    @classmethod
    def prepare_recording_NEURON(cls, chosenmodel, stimuli=None, stimtype=None):
        """Prepares recording for time, voltage and stimulus (optional).

        **Argument:** instantiated NEURON based model.

        **Keyword argument** (optional):

        - with key "stimuli" whose value is a list. For e.g. [h.IClamp(0.5,sec=soma), h.IClamp(0.5,sec=soma)]
        - with key "stimtype" whose value is a list of the form ``["current", "IRamp"]``. Notice that this is the value of the key "type" in stimulation parameter that is passed in ``SimulationManager.stimulate_model_NEURON``. Note that, although optional if the key "stimuli" is passed then "stimtype" **must** also be passed.

        **Returned value:** Three elements in the following order

        +--------+---------------------+----------------------------------------------+
        | order  | content             | value type                                   |
        +========+=====================+==============================================+
        | first  | recorded time       | list                                         |
        +--------+---------------------+----------------------------------------------+
        | second | recorded response   |- dictionary                                  |
        |        |                     |- region-name for key whose value is          |
        |        |                     |- key value is list; response from the region |
        +--------+---------------------+----------------------------------------------+
        | third  | recorded injections |- list of individual current injections if    |
        |        |                     |stimulated (current clamp)                    |
        |        |                     |- empty list ``[]`` for voltage clamp stimulus|
        |        |                     |- else, string "Model is not stimulated"      |
        +--------+---------------------+----------------------------------------------+

        **Use case:**

        The voltage recordings will depend on the number of sections.
        For eg.,

        ::

            rm = RecordManager()
            rec_t, rec_v = rm.prepare_recording_NEURON(chosenmodel)
            vm_soma = rec_v[0]

        On the other hand, for ``chosenmodel.regions = {'soma': 0.0, 'axon': 0.0}``

        ::

            rec_t, rec_v = rm.prepare_recording_NEURON(chosenmodel)
            vm_soma = rec_v['soma']
            vm_NOR3 = rec_v['axon']

        Another important consideration is the stimuli. If the model is stimulated with multiple current injection zones like

        ::

            currents = [h.IClamp(0.5, sec=soma), h.IClamp(0.5,sec=soma)]

        which you can get from

        ::

            currents = SimulatorManager().stimulate_model_NEURON(stimparameters = currparameters,
                                                                 modelsite = cell.soma)
        Then

        ::

            rec_t, rec_v, rec_injs = rm.prepare_recording_NEURON(chosenmodel, stimuli=currents,
                                                                 stimtype="current-clamp")

        *NOTE:*

        * ``rec_injs`` is a dictionary of individual current injections
        * it is not the final desired form
        * the desired single array of current injection trace is achieved only after putting the individual currents together
        * the appending of individual currents is not done during the preparatory stage; it is done after ``h.run()`` is called
        * however, for voltage injections (i.e, voltage clamp), ``rec_injs`` is just an empty list ``[]``

        """
        time_record = rc.time_NEURON() # record time
        strip_channels_key = \
         lambda keyslist: keyslist.remove("channels") if "channels" in keyslist else keyslist
        if (stimuli is not None and    # record stimulus
            stimtype is not None and
            stimuli != "Model is not stimulated"): # if model is stimulated
            if stimtype[0]=="current":
                volts = []         # record voltage
                for key in chosenmodel.regions.keys(): # for all the desired section
                    if key != "channels":
                        section = getattr(chosenmodel.cell, key)
                        volts.append( rc.response_voltage_NEURON(section) )
                x = list(chosenmodel.regions.keys())
                strip_channels_key(x)
                print( x )
                volt_record = cls.create_response_dictionary(
                                    strip_channels_key(list(chosenmodel.regions.keys())),
                                    volts )
                currents_record = rc.stimulus_individual_currents_NEURON( stimuli )
                return [ time_record, volt_record, currents_record ]
            elif stimtype[0]=="voltage":
                volts = []         # record voltage
                for key in chosenmodel.regions.keys(): # for all the desired section
                    section = getattr(chosenmodel.cell, key)
                    volts.append( rc.response_voltage_NEURON(section) )
                #print(len(volts))
                volt_record = cls.create_response_dictionary(
                                    strip_channels_key(list(chosenmodel.regions.keys())),
                                    volts )
                return [ time_record, volt_record, stimuli ] 
        else:
            volts = []         # record voltage
            for key in chosenmodel.regions.keys(): # for all the desired section
                if key != "channels":
                    section = getattr(chosenmodel.cell, key)
                    volts.append( rc.response_voltage_NEURON(section) )
                    regionkeylist = cls.create_regionslist_str(chosenmodel,
                                                               without="channels")
            volt_record = cls.create_response_dictionary(
                                    regionkeylist,
                                    volts )
            return [ time_record, volt_record, "Model is not stimulated"]

    @staticmethod
    def postrun_record_NEURON(injectedstimuli=None, stimtype=None):
        """Records variable values after the simulator has been engaged.

        **Keyword arguments (optional):** This method can run without any arguments but optionally one can pass an argument with key "injectedcurrents" whose value type is a list; this is the list of ``hoc.objects`` of individual currents returned from :py:meth`.prepare_recording_NEURON`.

        **Returned value:**

        * ``"Model is not stimulated"``; if no argument is passed
        * list whose elements are current magnitudes for the whole simulation; if list of current is passed

        *NOTE:*

        * even if the stimulation does not involve stimulation it is recommended to evoke the :py:meth:`.postrun_record_NEURON`

          - in such case just evoke the function without arguments
          - the returned value will be ``"Model is not stimulated"``

        **Use case:**

        ::

            rm = RecordManager()
            stimuli_list = SimulatorManager().stimulate_model_NEURON(stimparameters=currparameters,
                                                                     modelsite = cell.soma)
            rec_t, rec_v, rec_i_indivs = rm.prepare_recording_NEURON(chosenmodel,
                                                                     stimuli = stimuli_list)

        Then run the simulator, for e.g., ``SimulatorManager.engage_NEURON()``

        Now pass the list of ``hoc.objects`` of individual currents

        ::
            rec_i = rm.postrun_record_NEURON( injectedstimuli = stimuli_list )

        """

        if ( injectedstimuli is None or
             injectedstimuli == "Model is not stimulated" ):
            return "Model is not stimulated"
        else:
            if stimtype[0]=="current":
                return rc.stimulus_overall_current_NEURON( injectedstimuli )
            elif stimtype[0]=="voltage":
                return rc.stimulus_overall_voltage_NEURON( injectedstimuli, voltclamp=stimtype[1] )
