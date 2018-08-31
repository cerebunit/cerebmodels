# ../managers/managerRecord.py

from managers.operatorsYield.recorder import Recorder as rc

class RecordManager(object):
    """Manager working under RecordManager.

    Main Use methods:
    prepare_recording_NEURON
    postrun_record_NEURON

    Class methods:
    prepare_recording_NEURON

    Static methods:
    create_response_dictionary
    postrun_record_NEURON
    """

    def __init__(self):
        #self.rc = Recorder()
        pass

    @staticmethod
    def create_response_dictionary(regionslist_str, responselist_num):
        """static method that creates a dictionary

        Arguments:
        regionslist_str -- list of strings; names of the regions
        responselist_num -- list of numbers; list of lists

        NOTE: len(regionslist_str) == len(responselist_num)

        """
        x = {}
        [ x.update({regionslist_str[i]: responselist_num[i]})
                                    for i in range(len(regionslist_str)) ]
        return x

    @classmethod
    def prepare_recording_NEURON(cls, chosenmodel, stimuli=None):
        """method that prepares recording for time, voltage and stimulus (optional).

        Argument (mandatory):
        chosenmodel -- instantiated NEURON based model, eg., cell = Purkinje()
        NOTE: the function will take the sections which are entries in the list chosenmodel.regions

        Keyword arguments (optional):
        stimuli -- list, eg, [h.IClamp(0.5,sec=soma), h.IClamp(0.5,sec=soma)]

        Returned value:
        three elements in the following order
        recorded time -- list
        recorded response -- dictionary; region-name for key whose value is
                             response from the region as list
        recorded injections -- 
                 list of individual injections; if model was stimulated with currents
                 string "Model is not stimulated"; if model was not stimulated

        The voltage recordings will depend on the number of sections.
        For eg.,
        rm = RecordManager()
        rec_t, rec_v = rm.prepare_recording_NEURON(chosenmodel)
        vm_soma = rec_v[0]
        On the other hand, for chosenmodel.regions = {'soma': 0.0, 'axon': 0.0}
        rec_t, rec_v = rm.prepare_recording_NEURON(chosenmodel)
        vm_soma = rec_v['soma']
        vm_NOR3 = rec_v['axon']

        Another important consideration is the stimuli. If the model is stimulated
        with multiple current injection zones like
        currents = [h.IClamp(0.5, sec=soma), h.IClamp(0.5,sec=soma)] which you can get from
        currents = SimulatorManager().stimulate_model_NEURON(stimparameters = currparameters,
                                                                 modelsite = cell.soma)
        Then
        rec_t, rec_v, rec_injs = rm.prepare_recording_NEURON(chosenmodel,
                                                             stimuli=currents)

        NOTE:
            - rec_injs is a dictionary of individual injections
            - it is not the final desired form
            - the desired single array of current injection trace is achieved only
              after putting the individual currents together
            - the appending of individual currents is not done during the
              preparatory stage; it is done after h.run() is called

        """

        time_record = rc.time_NEURON() # record time
        volts = []         # record voltage
        for key in chosenmodel.regions.keys(): # for all the desired section
            section = getattr(chosenmodel.cell, key)
            volts.append( rc.response_voltage_NEURON(section) )
        volt_record = cls.create_response_dictionary(
                                    list(chosenmodel.regions.keys()), volts )
        if (stimuli is not None and                    # record stimulus
            stimuli != "Model is not stimulated"): # if model is stimulated
            currents_record = rc.stimulus_individual_currents_NEURON( stimuli )
            return [ time_record, volt_record, currents_record ]
        else:
            return [ time_record, volt_record, "Model is not stimulated"]

    @staticmethod
    def postrun_record_NEURON(injectedcurrents=None):
        """method that records variable after the simulator has been engaged.

        Keyword arguments (optional):
        injectedcurrents -- list; this is the list of hoc.objects of individual currents returned from prepare_recording_NEURON() 

        Returned value:
        if no argument is passed -- "Model is not stimulated"
        if list of current is passed -- list whose elements are current magnitudes for the whole simulation.

        NOTE:
            - even if the stimulation does not involve stimulation it is recommended to evoke the postrun_record_NEURON
            - in such case just evoke the function without arguments
            - the returned value will be "Model is not stimulated"

        Use case:
        rm = RecordManager()
        stimuli_list = SimulatorManager().stimulate_model_NEURON(stimparameters = currparameters,
                                                                 modelsite = cell.soma)
        rec_t, rec_v, rec_i_indivs = rm.prepare_recording_NEURON(chosenmodel,
                                                                 stimuli = stimuli_list)
        Then run the simulator, for e.g., SimulatorManager.engage_NEURON()
        Now pass the list of hoc.objects of individual currents
        rec_i = rm.postrun_record_NEURON( injectedcurrents = stimuli_list )

        """

        if ( injectedcurrents is None or
             injectedcurrents == "Model is not stimulated" ):
            return "Model is not stimulated"
        else:
            return rc.stimulus_overall_current_NEURON( injectedcurrents )
