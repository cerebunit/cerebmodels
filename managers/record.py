# ../managers/record.py
#import re

from managers.operatorsYield.recorder import Recorder as rc
from managers.operatorsYield.regionparser import RegionParser as rp

class RecordManager(object):
    """
    **Available methods:**

    +--------------------------------------------------------+-----------------------+
    | Method name                                            | Method type           |
    +========================================================+=======================+
    | :py:meth:`.recordings_of_cellular_regionbodies_NEURON` | static method         |
    +--------------------------------------------------------+-----------------------+
    | :py:meth:`.recordings_of_cellular_components_NEURON`   | static method         |
    +--------------------------------------------------------+-----------------------+
    | :py:meth:`.prepare_recording_NEURON`                   | class method          |
    +--------------------------------------------------------+-----------------------+
    | :py:meth:`.postrun_record_NEURON`                      | static method         |
    +--------------------------------------------------------+-----------------------+

    """

    def __init__(self):
        #self.rc = Recorder()
        pass

    @staticmethod
    def recordings_of_cellular_regionbodies_NEURON(chosenmodel):
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
        regionbodylist = rp.get_regionlist(chosenmodel)
        recordings = {}
        for region_name in regionbodylist:
            region = getattr(chosenmodel.cell, region_name)
            rectypes = chosenmodel.regions[region_name]
            recordings.update(
               {region_name: rc.response_body_allrectypes_NEURON(region, rectypes)} )
        return recordings # dictionary

    @staticmethod
    def recordings_of_cellular_components_NEURON(chosenmodel):
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
        componentgrouplist = rp.get_componentgrouplist(chosenmodel)
        recordings = {} # {compgroup: {region_name: {a_comp_name: [ [], [] ]} } }
        for compgroup_name in componentgrouplist:
            its_regionlist = rp.get_regionlist_of_componentgroup(chosenmodel, compgroup_name)
            ans2 = {} # {region_name: {a_comp_name: [ Vector[], Vector[], ... ]} }
            for region_name in its_regionlist: # for ans2
                complist = rp.get_componentlist(chosenmodel, compgroup_name, region_name)
                ans1 = {} # {a_comp_name: [ Vector[], Vector[], ... ]
                for a_comp_name in complist: # for ans1
                    region = getattr(chosenmodel.cell, region_name)
                    rectypes = chosenmodel.regions[compgroup_name][region_name][a_comp_name]
                    ans1.update({a_comp_name: # update ans1
                    rc.response_component_allrectypes_NEURON(region, a_comp_name, rectypes)})
                ans2.update( {region_name: ans1} ) # update ans2
            recordings.update( {compgroup_name: ans2} )
        return recordings

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
                stim_record = rc.stimulus_individual_currents_NEURON( stimuli )
            elif stimtype[0]=="voltage": # record current
                stim_record = stimuli
        else:
            stim_record = "Model is not stimulated"
        responses = cls.recordings_of_cellular_regionbodies_NEURON( chosenmodel )
        responses.update(cls.recordings_of_cellular_components_NEURON(chosenmodel))
        return [ time_record, responses, stim_record]

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
