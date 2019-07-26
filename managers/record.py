# ../managers/record.py
import re

from managers.operatorsYield.recorder import Recorder as rc

class RecordManager(object):
    """
    **Available methods:**

    +-----------------------------------------------+-----------------------+
    | Method name                                   | Method type           |
    +===============================================+=======================+
    | :py:meth:`.create_regionkeylist_responselist` | static method         |
    +-----------------------------------------------+-----------------------+
    | :py:meth:`.create_response_dictionary`        | static method         |
    +-----------------------------------------------+-----------------------+
    | :py:meth:`.prepare_recording_NEURON`          | class method          |
    +-----------------------------------------------+-----------------------+
    | :py:meth:`.postrun_record_NEURON`             | static method         |
    +-----------------------------------------------+-----------------------+

    """

    def __init__(self):
        #self.rc = Recorder()
        pass

    @staticmethod
    def create_regionkeylist_responselist(chosenmodel, without=None):
        """Returns a list of strings of region names and a list of response

        **Arguments:**

        +--------------------+------------------------------+
        | Argument           |                              |
        +====================+==============================+
        | first argument     | instantiated NEURON model    |
        +--------------------+------------------------------+
        | without (optional) | None (default) or "channels" |
        +--------------------+------------------------------+

        **Returned values:** list of strings of region names (region_key_list) and a list of response (response_list). The contents of these two lists will depending on at least three cases. But before considering the cases it should be noted that the list of strings of region names may not be exactly the sames as those in chosenmodel.regions.keys().

        For instance for a cellular model, the chosenmodel.regions will be like

        ::

           { "soma": 0.0, "axon": 0.0 }

        or

        ::

           { "soma": 0.0, "axon": 0.0,
             "channels": { "soma": ["pas", "ca", "k"],
                           "axon": ["pas"] } }

        In the first case the ``chosenmodel.regions.keys()`` will  be taken as the region_key_list. That is, ``region_key_list = ["soma", "axon"]``. However, for the second case although initially ``region_key_list = ["soma", "axon", "channels"]`` the element "channels" will be removed resulting in the __transitory value__ ``region_key_list = ["soma", "axon"]``. Now, depending on the cases discussed below the list of region keys may change.

        * case-1: ``without = "channels"``

           - records only the voltage response (i.e section responses)
           - region_key_list will be the list of sections (w/o "channels" if the model regions has it). Thus, ``region_key_list = [ "secA_name", "secB_name", "secC_name" ]``.
           - response_list will be the list of voltage responses from section in corresponding indices of region_key_list. Thus, ``response_list = [ h.Vector of secA, h.Vector of secB, h.Vector of secC ]``.

        * cases when no without is assigned, i.e. ``without = None`` (DEFAULT)

          * case-2: ``chosenmodel.regions`` does not have "channels"

             - records only voltage response
             - region_key_list and response_list outputs will be similar to those of case-1

          * case-3: ``chosenmodel.regions`` has "channels"

             - records voltage response for regions that are section
             - records current response from channels in a section
             - region_key_list will be of the form ``[ "secA", "secB", "channel_secA_chnlx", "channel_secA_chnly", "channel_secB_chnly"]``.
             - response_list will be the list of responses (voltages and currents) from sections and channels in corresponding indices of region_key_list.
             - NOTE: a key in ``chosenmodel.regions.keys()`` is "channels" but each assigned channel in region_key_list the letter "**s**" gets dropped and becomes for eg. "channel_secA_chnlx" and not "channels_secA_chnlx".

        """
        regionkeylist = list(chosenmodel.regions.keys())# Initial keys list of model.regions
        responselist = []                               # placeholder for response
        (lambda keyslist: keyslist.remove("channels")   # removes "channels" in regionkeylist
                          if "channels" in keyslist else keyslist)(regionkeylist)
        # Lambda function for appending section voltage response into responselist
        record_voltage = \
         lambda chosenmodel, regionkey, responselist: \
            responselist.append( rc.response_voltage_NEURON(
                                               getattr(chosenmodel.cell, regionkey) ) )
        # Lambda function for appending channel current response into responselist
        record_current = \
         lambda section, channelkey, responselist: \
            responselist.append( rc.response_current_NEURON(
                                               getattr(section(0.5), channelkey) ) )
        if without is None: # record every thing
            for akey in chosenmodel.regions.keys(): # for all the desired section
                if akey != "channels": # if key refers to a section record voltage response
                    record_voltage(chosenmodel, akey, responselist)
                elif akey == "channels": # if key refers to a channer record current response
                    channels = chosenmodel.regions[akey] # dict value of .regions["channels"]
                    for sec in channels.keys(): # keys in the dictionary are section names
                        section = getattr(chosenmodel.cell, sec) # get h.Section()
                        for achan in channels[sec]: # get each channel name in list
                            regionkeylist.append( "channel_"+sec+"_"+achan )#NOTE: singular
                            record_current(section, achan, responselist)
        elif without == "channels": # record only voltages
            for akey in chosenmodel.regions.keys(): # for all the desired section
                if akey != "channels":
                    record_voltage(chosenmodel, akey, responselist)
        return [regionkeylist, responselist]

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
        #[ x.update({regionslist_str[i]: responselist_num[i]})
        #                            for i in range(len(regionslist_str)) ]
        for i in range(len(regionslist_str)):
            str_list = re.split("_", regionslist_str[i])
            str_no = len(str_list)
            if str_no==1:
                x.update({str_list[0]: responselist_num[i]})
            else:
                node = {str_list[-1]: responselist_num[i]}
                leaf = {}
                for j in reversed(range(str_no-1)):
                    if j != 0: # contruct the dictionary which will be the final value
                        leaf.update( {str_list[j]: node} ) # leaf = {str_list[-2]: node}
                    else: # assign constructed dictionary to the first in string list
                        x.update({str_list[j]: node})
                    node = leaf # set current leaf as node moving up the tree
        return x

    @classmethod
    def prepare_recording_NEURON(cls, chosenmodel, stimuli=None, stimtype=None):
        """Prepares recording for time, voltage and stimulus (optional).

        **Argument:** instantiated NEURON based model.

        **Keyword argument** (optional):

        - with key "stimuli" whose value is a list. For e.g. [h.IClamp(0.5,sec=soma), h.IClamp(0.5,sec=soma)]
        - with key "stimtype" whose value is a list of the form ``["current", "IRamp"]``. Notice that this is the value of the key "type" in stimulation parameter that is passed in ``SimulationManager.stimulate_model_NEURON``. Note that, although optional if the key "stimuli" is passed then "stimtype" **must** also be passed.

        **Returned value:** Three elements in the following order

        +--------+---------------------+-----------------------------------------------+
        | order  | content             | value type                                    |
        +========+=====================+===============================================+
        | first  | recorded time       | list                                          |
        +--------+---------------------+-----------------------------------------------+
        | second | recorded response   |- dictionary                                   |
        |        |                     |- region-name for key whose value is           |
        |        |                     |- key value is list; response from the region  |
        +--------+---------------------+-----------------------------------------------+
        | third  | recorded injections |- list of individual current injections if     |
        |        |                     |stimulated (current clamp)                     |
        |        |                     |- stimuli (argument) for voltage clamp stimulus|
        |        |                     |- else, string "Model is not stimulated"       |
        +--------+---------------------+-----------------------------------------------+

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
        if (stimuli is not None and    # record stimulus
            stimtype is not None and
            stimuli != "Model is not stimulated"): # if model is stimulated
            if stimtype[0]=="current": # record only voltage
                [regionkeylist, volts] = \
                    cls.create_regionkeylist_responselist( chosenmodel, without="channels" )
                volt_record = cls.create_response_dictionary( regionkeylist, volts )
                stim_record = rc.stimulus_individual_currents_NEURON( stimuli )
                return [ time_record, volt_record, stim_record ]
            elif stimtype[0]=="voltage": # record current
                [regionkeylist, volts_currents] = \
                    cls.create_regionkeylist_responselist( chosenmodel )
                volts_currents_record = \
                    cls.create_response_dictionary( regionkeylist, volts_currents )
                stim_voltages = stimuli
                return [ time_record, volts_currents_record, stim_voltages ]
        else: # record voltage & currents if possible when no stimulus is given
            [regionkeylist, volts] = \
                cls.create_regionkeylist_responselist( chosenmodel, without="channels" )
            volt_record = cls.create_response_dictionary( regionkeylist, volts )
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
                return rc.stimulus_overall_voltage_NEURON( injectedstimuli,
                                                           voltclamp=stimtype[1] )
