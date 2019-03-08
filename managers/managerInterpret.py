# ../managers/managerInterpret.py

import efel


class InterpretManager(object):
    """
    Available methods:
    get_data_and_time_values (staticmethod)
    create_efel_trace_individual (staticmethod)
    create_efel_trace_overall (classmethod)
    get_efel_results (instantiated method)
    gather_efel_values (instantiated method)

    """

    def __init__(self):
        pass

    @staticmethod
    def get_data_and_time_values(loadednwbfile=None, modelregion=None):
        """loadednwbfile is the file loaded from /responses directory
           modelregion is a string, eg, "soma"
        """
        orderedepoch = loadednwbfile.drawout_orderedepochs(modelregion)
        datavalues = [ loadednwbfile.get_datavalues_for_epoch(i, orderedepochs)
                       for i in range(len(orderedepochs)) ]
        timestamps = [ loadednwbfile.get_timestamps_for_epoch(i, orderedepochs)
                       for i in range(len(orderedepochs)) ]
        return timestamps, datavalues

    @staticmethod
    def create_efel_trace_individual(timestamp, datavalue):
        """This is called by cls.create_efel_trace_overall
        """
        a_trace = {}
        a_trace["V"] = datavalue
        a_trace["T"] = timestamp
        a_trace["stim_start"] = [ timestamp[0] ]
        a_trace["stim_end"]   = [ timestamp[-1] ]
        return a_trace

    @classmethod
    def create_efel_trace_overall(cls, timestamps, datavalues):
        """This is called by self.get_efel_results
        """
        return [ cls.create_efel_trace_individual( timestamps[i], datavalues[i] )
                 for i in range(len(timestamps)) ]

    def get_efel_results(self, timestamps, datavalues, feature_name_list):
        """This returns a dictionary of { feature_name: feature_value }
        feature_name_list is list of strings, eg, ['voltage_base']
        """
        traces = self.create_efel_trace_overall( timestamps, datavalues )
        return efel.getFeatureValues( traces, feature_name_list )

    def gather_efel_values(self, trace_results):
        """This returns a list of feature_value
        NOTE:
           - for use in CerebUnit it is assumed that only one feature_name is in
             the feature_name_list
           - trace_results is a dictionary with only one key (one feature_name)
        """
        return [ feature_value
                 for feature_name, feature_value in trace_results.items() ]
