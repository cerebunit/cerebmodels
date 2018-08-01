# ~/managers/operatorsTranscribe/metadata_timeseriesgenerator.py
#import numpy.core.defchararray as npd

class TimeseriesGenerator(object):
    """Operators working under TranscribeManager

    Available methods:
    forcellrecording -- classmethod called by forrecording
    forrecording
    """

    @staticmethod
    def cellrecordings_response(model, cellregion, rec_t, rec_i, rec_v, parameters):
        """static method that creates a generic time-series (response) metadata for cells.

        Arguments:
        model -- instantiated model
        cellregion -- string; "soma", "axon", etc ...
        rec_t -- array; recordings["time"]
        rec_v -- array; recordings["response"][cellregion]
        rec_i -- string/array; recordings["stimulus"]
        parameters -- dictionary with keys "dt", "celsius", "tstop", "v_init"
                      Eg: {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        """
        if rec_i=="Model is not stimulated":
            comment = "voltage response without stimulation"
        else:
            comment = "voltage response with stimulation"

        return {"name": model.modelname+"_nostim_Vm_"+cellregion,
                "source": cellregion,
                "data": rec_v,
                "unit": "mV",
                "resolution": parameters["dt"],
                "conversion": 1000.0, # 1000 => 1ms
                "timestamps": rec_t,
                "starting_time": 0.0,
                "rate": 1/parameters["dt"], # NWB suggests using Hz but frequency != rate
                "comment": comment,
                "description": "whole single array of voltage response from "+cellregion+" of "+ model.modelname}

    @staticmethod
    def cellrecordings_currentstimulus(model, cellregion, rec_t, rec_i, parameters):
        """static method that creates a time-series (response) metadata for stimulated cells.

        Arguments:
        model -- instantiated model
        cellregion -- string; "soma", "axon", etc ...
        rec_t -- array; recordings["time"]
        rec_i -- array; recordings["stimulus"]
        parameters -- dictionary with keys "dt", "celsius", "tstop", "v_init"
                      Eg: {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        """
        
        return {"type": "currentclamp_series", #"CurrentClampSeries"
                "name": model.modelname+"_stim_Vm_"+cellregion,
                "source": cellregion,
                "data": rec_v,
                "unit": "mV",
                "gain": 0.0,
                "bias_current": 0.0,
                "bridge_balance": 0.0,
                "capacitance_compensation": 0.0,
                "resolution": parameters["dt"],
                "conversion": 1000.0, # 1000 => 1ms
                "timestamps": rec_t,
                "starting_time": 0.0,
                "rate": 1/parameters["dt"],
                "comment": "voltage response with stimulation",
                "description": "whole single array of voltage response from "+cellregion+" of "+model.modelname}

    @staticmethod
    def cellrecordings_stimulus(model, rec_t, rec_i, parameters, stimparameters):
        """static method that creates a time-series (stimulus) metadata for stimulated cells.

        Arguments:
        model -- instantiated model
        cellregion -- string; "soma", "axon", etc ...
        rec_t -- array; recordings["time"]
        rec_v -- array; recordings["response"][cellregion]
        parameters -- dictionary with keys "dt", "celsius", "tstop", "v_init"
                      Eg: {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        stimparameters -- dictionary with keys "type" and "stimlist" where
                          "type": 2 element list of strings
                                  <stimulus category> <specific type of that category>
                                  NOTE: First element is ALWAYS <stimulus category>
                          Eg: for current inject on cellular model
                              ["current", "IClamp"]
                          "stimlist": is a list with elements as dictionary; like [ {}, {}, ... ]
                          Eg: [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]
                          Eg: [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0, "delay": 5.0},
                                {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0, "delay": 10.0},
                                {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0, "delay": 15.0},
                                {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0, "delay": 20.0} ]
        """
        return {"type": "currentclampstimulus_series", #"CurrentClampStimulusSeries"
                "name": model.modelname+"_stimulus",
                "source": stimparameters["type"],
                "data": rec_i,
                "unit": "nA",
                "gain": 0.0,
                "resolution": parameters["dt"],
                "conversion": 1000.0, # 1000 => 1ms
                "timestamps": rec_t,
                "starting_time": 0.0,
                "rate": 1/parameters["dt"],
                "comment": "current injection, "+stimparameters["type"][1],
                "description": "whole single array of stimulus" }

    @classmethod
    def forcellrecordings_nostimulus(cls, chosenmodel, recordings, runtimeparameters):
        """class method that creates time-series metadata for unstimulated cells.

        Arguments (mandatory):
        chosenmodel -- instantiated model
        recordings -- dictionary with keys "time", "response" and "stimulus" in the form
                      {"time": array, "response": {cellregion_a: array, cellregion_b: array},
                       "stimulus": str("Model is not stimulated") or array}
        runtimeparameters -- dictionary with keys "dt", "celsius", "tstop", "v_init"
                             Eg: {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        """
        y = {}
        for cellregion in chosenmodel.regions.keys():
            y.update( {cellregion:
                       cls.cellrecordings_response_nostimulus(
                                            chosenmodel, cellregion,
                                            recordings["time"],
                                            recordings["response"][cellregion],
                                            runtimeparameters )} )
        return y

    @classmethod
    def forcellrecordings_stimulus(cls, chosenmodel, recordings,
                              runtimeparameters, stimparameters):
        """class method that creates time-series metadata for stimulated cells.

        Arguments (mandatory):
        chosenmodel -- instantiated model
        recordings -- dictionary with keys "time", "response" and "stimulus" in the form
                      {"time": array, "response": {cellregion_a: array, cellregion_b: array},
                       "stimulus": str("Model is not stimulated") or array}
        runtimeparameters -- dictionary with keys "dt", "celsius", "tstop", "v_init"
                             Eg: {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        stimparameters -- dictionary with keys "type" and "stimlist" where
                          "type": 2 element list of strings
                                  <stimulus category> <specific type of that category>
                                  NOTE: First element is ALWAYS <stimulus category>
                          Eg: for current inject on cellular model
                              ["current", "IClamp"]
                          "stimlist": is a list with elements as dictionary; like [ {}, {}, ... ]
                          Eg: [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]
                          Eg: [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0, "delay": 5.0},
                                {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0, "delay": 10.0},
                                {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0, "delay": 15.0},
                                {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0, "delay": 20.0} ]
        """
        y = {}
        y.update( {"stimulus":
                   cls.cellrecordings_stimulus(
                                            chosenmodel,
                                            recordings["time"],
                                            recordings["stimulus"],
                                            runtimeparameters, stimparameters )} )
        for cellregion in chosenmodel.regions.keys():
            y.update( {cellregion:
                       cls.cellrecordings_response_stimulus(
                                            chosenmodel, cellregion,
                                            recordings["time"],
                                            recordings["response"][cellregion],
                                            runtimeparameters )} )
        return y

    def forcellrecording( self, chosenmodel=None, recordings=None,
                          runtimeparameters=None, stimparameters=None ):
        """method that creates the NWB formatted time-series metadata for cells. This is normally not called by the TranscribeManager(), instead it is called by forrecording() below.

        Arguments (mandatory):
        chosenmodel -- instantiated model
        recordings -- dictionary with keys "time", "response" and "stimulus" in the form
                      {"time": array, "response": {cellregion_a: array, cellregion_b: array},
                       "stimulus": str("Model is not stimulated") or array}
        runtimeparameters -- dictionary with keys "dt", "celsius", "tstop", "v_init"
                             Eg: {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        stimparameters -- dictionary with keys "type" and "stimlist" where
                          "type": 2 element list of strings
                                  <stimulus category> <specific type of that category>
                                  NOTE: First element is ALWAYS <stimulus category>
                          Eg: for current inject on cellular model
                              ["current", "IClamp"]
                          "stimlist": is a list with elements as dictionary; like [ {}, {}, ... ]
                          Eg: [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]
                          Eg: [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0, "delay": 5.0},
                                {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0, "delay": 10.0},
                                {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0, "delay": 15.0},
                                {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0, "delay": 20.0} ]
        Use case:
        tg = TimeseriesGenerator()
        # get dummy model
        from models.cells.modelDummyTest import DummyCell
        model = DummyCell()
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        # generate dummy response
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_i = numpy.random.rand(1,len(rec_t))[0] # stimulus
        rec_v = numpy.random.rand(2,len(rec_t))    # response
        # in this dummy model, model.regions = {'soma':0.0, 'axon':0.0}
        For simulation without stimulation
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                      "stimulus": "Model is not stimulated"}
        respmd = tg.forcellrecording(chosenmodel = model, recordings = recordings,
                                     parameters = runtimeparam)
        Simulation with stimulation
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                      "stimulus": rec_i}
        respmd = tg.forcellrecording(chosenmodel = model, recordings = recordings,
                                     parameters = runtimeparam, stimparameters = stimparameters)
        NOTE:
            - if there is NO stimulation and chosenmodel.regions={"soma": 0.0, "axon": 0.0} then len(respmd) = 2 since there are two cell regions
            - also, this means respmd_soma = respmd["soma"] and respmd_axon = respmd["axon"]
            - however, with stimulation there is an additional "stimulus" key stimulmd = respmmd["stimulus"]
        """
        y = {}
        #if npd.equal(recordings["stimulus"], "Model is not stimulated").item((0)):
        # str because recordings has numpy array as dictionary values resulting in
        # numpy FutureWarning bug as it expects this to be an array as well
        # https://stackoverflow.com/questions/40659212/futurewarning-elementwise-comparison-failed-returning-scalar-but-in-the-futur
        if str(recordings["stimulus"])=="Model is not stimulated":
            y.update( self.forcellrecordings_nostimulus( chosenmodel, recordings,
                                                         runtimeparameters ) )
        else: # for stimulus
            if (stimparameters is None):
                raise ValueError("for recording stimuli passing stimparameters is mandatory")
            else:
                y.update( self.forcellrecordings_stimulus( chosenmodel, recordings,
                                              runtimeparameters, stimparameters ) )
        return y

    def forrecording( self, chosenmodel=None, recordings=None,
                      runtimeparameters=None, stimparameters=None ):
        """method that creates the NWB formatted time-series metadata.

        Arguments (mandatory):
        chosenmodel -- instantiated model
        recordings -- dictionary with keys "time", "response" and "stimulus" in the form
                      {"time": array, "response": {cellregion_a: array, cellregion_b: array},
                       "stimulus": str("Model is not stimulated") or array}
        runtimeparameters -- dictionary with keys "dt", "celsius", "tstop", "v_init"
                             Eg: {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        stimparameters -- dictionary with keys "type" and "stimlist" where
                          "type": 2 element list of strings
                                  <stimulus category> <specific type of that category>
                                  NOTE: First element is ALWAYS <stimulus category>
                          Eg: for current inject on cellular model
                              ["current", "IClamp"]
                          "stimlist": is a list with elements as dictionary; like [ {}, {}, ... ]
                          Eg: [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]
                          Eg: [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0, "delay": 5.0},
                                {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0, "delay": 10.0},
                                {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0, "delay": 15.0},
                                {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0, "delay": 20.0} ]
        Use case: [For modelscale="cells"]
        tg = TimeseriesGenerator()
        # get dummy model
        from models.cells.modelDummyTest import DummyCell
        model = DummyCell()
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        # generate dummy response
        rec_t = [ t*runtimeparam["dt"]
                  for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]
        rec_i = numpy.random.rand(1,len(rec_t))[0] # stimulus
        rec_v = numpy.random.rand(2,len(rec_t))    # response
        # in this dummy model, model.regions = {'soma':0.0, 'axon':0.0}
        For simulation without stimulation
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                      "stimulus": "Model is not stimulated"}
        respmd = tg.forcellrecording(chosenmodel = model, recordings = recordings,
                                     parameters = runtimeparam)
        Simulation with stimulation
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}
        recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]},
                      "stimulus": rec_i}
        respmd = tg.forcellrecording(chosenmodel = model, recordings = recordings,
                                     parameters = runtimeparam, stimparameters = stimparameters)
        NOTE:
            - if there is NO stimulation and chosenmodel.regions={"soma": 0.0, "axon": 0.0} then len(respmd) = 2 since there are two cell regions
            - also, this means respmd_soma = respmd["soma"] and respmd_axon = respmd["axon"]
            - however, with stimulation there is an additional "stimulus" key stimulmd = respmmd["stimulus"]
        """
        if (chosenmodel is None) or (recordings is None) or (runtimeparameters is None):
            raise ValueError("passing an instantiated chosenmodel, the recordings (dictionary) and runtimeparameters are  mandatory")
        elif chosenmodel.modelscale == "cells":
            return self.forcellrecording( chosenmodel=chosenmodel,
                                          recordings=recordings,
                                          runtimeparameters=runtimeparameters,
                                          stimparameters=stimparameters )
