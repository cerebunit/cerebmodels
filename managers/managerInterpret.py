# ../managers/managerInterpret.py

import efel


class InterpretManager(object):
    """
    Available methods:
    get_data_and_time_values (staticmethod)
    create_base_efel_trace_individual (staticmethod)
    create_base_efel_trace_overall (classmethod)
    update_traces_with_feature_results (staticmethod)
    apply_feature_after_all_prereqs (classmethod)
    extract_and_pair_featname_values (staticmethod)
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
    def create_base_efel_trace_individual(timestamp, datavalue):
        """This is called by cls.create_efel_trace_overall
        Input: array of times, array of values
        Output: dictionary with keys; 'T', 'V', 'stim_start', 'stim_end'
        """
        a_trace = {}
        a_trace["V"] = datavalue
        a_trace["T"] = timestamp
        a_trace["stim_start"] = [ timestamp[0] ]
        a_trace["stim_end"]   = [ timestamp[-1] ]
        return a_trace

    @classmethod
    def create_base_efel_trace_overall(cls, timestamps, datavalues):
        """This is called by self.get_base_efel_results
        Input: list of array of times (i.e, epochs/intervals)
               list of array of values
        Output: list of base_trace dictionary for each epoch
        """
        return [ cls.create_base_efel_trace_individual( timestamps[i], datavalues[i] )
                 for i in range(len(timestamps)) ] # [ trace0, trace1, trace2, ... ]

    @staticmethod
    def update_traces_with_feature_results(traces, feature_name):
        """Creates key=feature_name for each traceX in [ trace0, trace1, ... ]
        and associate it with its corresponding value, which is generated from the
        old [ trace0, trace1, ... ] via efel.getFeatureValues().
        This returns new [ trace0, trace1, ... ], which has the key=feature_name
        """
        feature_results = efel.getFeatureValues( traces, [ feature_name ] )
        for i in range( len(feature_results) ):
            traces[i][feature_name] = feature_results[i][feature_name]
        return traces

    @classmethod
    def apply_feature_after_all_prereqs(cls, traces, feature_name, its_prereqs):
        """For features that require pre-requisite features, this function considers
        each requirement (in descending order in its_prereqs list) as a feature and
        calls update_traces_with_feature_results(). Each requirement generates an
        updated trace containing the requirement as a key. This is done down the
        order of the its_prereqs list, finally ending with feature_name.
        The method returns a new [ trace0, trace1, ... ], updated with the keys
        that are features in its_prereqs and feature_name

        NOTE:
            - features in its_prereqs list is listed such that preceeding pre-req
              is required by the succeeding pre-req.
            - the last pre-req is the requirement for the feature_name
        """
        for i in range( len(its_prereqs) ):
            prereq_feat = its_prereqs[i]
            traces = cls.update_traces_with_feature_results(traces, prereq_feat)
        return cls.update_traces_with_feature_results(traces, feature_name)

    @staticmethod
    def extract_and_pair_featname_values(traces, feature_name_list):
        """For a given traces, [ trace0, trace1, ... ] and a desired
        feature_name_list, [ 'feat1', 'feat2', 'feat3' ] for each featX its value
        is extracted from the traces. For trace0, this results in {feat1: value,
        feat2: value, feat3: value}. This is done for rest of the trace in traces.
        This method returns a list of dictionaries
        [ {feat1: value, feat2: value, feat3: value}, # from trace0
          {feat1: value, feat2: value, feat3: value}, ... ] # from trace1 and so on
        """
        x = []
        for i in range(len(traces)):
            y = {}
            for feature_name in featurelist:
                y.update({feature_name: traces[i][feature_name]})
            x.append(y)
        return x # efel results

    def get_efel_results( self, timestamps, datavalues,
                          feature_name_list = ["voltage_base"],
                          prereq_list = [ [], ]):
        """This returns a dictionary of { feature_name: feature_value }
        feature_name_list is list of strings, eg, ['feat1', 'feat2', 'feat3']
        prereq_list is list of list of strings; eg,
                    [ ['feat1_prereq1', 'feat1_prereq2], # [] is also valid
                      ['feat2_prereq1'],
                      ['feat3_prereq1', 'feat3_prereq2', 'feat3_prereq3', 'feat4_prereq4'] ]
        NOTE:
            - for the single feature, "voltage_base" in feature_name_list
              the method returns a list of dictionaries for each trace, the key being
              "voltage_base"
            - for the case of single or multiple features with some having pre-requisites
              the method extracts feature values for each of the pre-requisite (down the list)
              finally extracting the values for the main feature
        """
        traces = self.create_base_efel_trace_overall( timestamps, datavalues )
        if feature_name_list == ["voltage_base"]:
            return efel.getFeatureValues( traces, feature_name_list ) # base voltages
        else:
            for i in range( len(feature_name_list) ):
                feature_name = feature_name_list[i]
                its_prereqs = prereq_list[i]
                if len(its_prereqs)==0:
                    traces = self.update_traces_with_feature_results(traces, feature_name)
                else:
                    traces = self.apply_feature_after_all_prereqs(traces, feature_name, its_prereqs)
            return self.extract_and_pair_featname_values(traces, feature_name_list)

    def gather_efel_values(self, trace_results, a_feature_name):
        """This returns a list of feature_value
        NOTE:
           - for use in CerebUnit it is assumed that only one feature_name is in
             the feature_name_list
           - trace_results is a dictionary with only one key (one feature_name)
        """
        return [ feature_value
                 for efel_results in trace_results
                 for feature_name, feature_value in efel_results.items()
                 if feature_name == a_feature_name ]
