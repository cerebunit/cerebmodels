# ~/managers/operatorsTranscribe/metadata_epochgenerator.py

class EpochGenerator(object):
    """Operators working under TranscribeManager

    Available methods:
    epochcontainer -- classmethod called by forepoch
    forepoch
    """

    @staticmethod
    def compute_totalepochs_per_cellregion(parameters):
        """static method that returns the 'total' number of epochs.
        'total' here if for A region, not all regions.

        Argument:
        parameters --
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
                           "tstop": runtimeparameters["tstop"] # only for last epoch
        NOTE:
            - no_of_regions = len(list(chosenmodel.regions.keys()))
            - no_of_stimulus = 2
            - no_of_epochs_per_region = 1 + no_of_stimulus; thus it includes
              period/epoch pre-first stimulus
            - total number of epochs = no_of_regions * no_of_epochs_per_regions
        """
        if "stimlist" in parameters:
            no_of_stimulus = len(parameters["stimlist"])
        else:
            no_of_stimulus = 0
        return 1+no_of_stimulus

    @classmethod
    def epochcontainer(cls, chosenmodel, parameters):
        """static method creates the container for NWP formatted epoch metadata.

        Arguments:
        chosenmodel -- instantiated model
        parameters --
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
                          "tstop": runtimeparameters["tstop"] # only for last epoch
        Returned Value:
        assuming chosenmodel.regions = {'soma': 0.0, 'axon': 0.0} and no of epochs/region=3 (i.e initial state regardless of stimulus is epoch0)
        returned value is a dictionary of the form
        dictionary--
         {"epoch0soma": {'tags': ('3_epoch_responses', 0, soma, modelname, modelscale, "epoch0soma")},
          "epoch1soma": {'tags': ('3_epoch_responses', 1, soma, modelname, modelscale, "epoch1soma")},
          "epoch2soma": {'tags': ('3_epoch_responses', 2, soma, modelname, modelscale, "epoch2soma")},
          "epoch0axon": {'tags': ('3_epoch_responses', 0, axon, modelname, modelscale, "epoch0axon")},
          "epoch1axon": {'tags': ('3_epoch_responses', 1, soma, modelname, modelscale, "epoch1axon")},
          "epoch2axon": {'tags': ('3_epoch_responses', 2, soma, modelname, modelscale, "epoch2axon")}}
        however without stimulation, no of epochs/region = 1 (i.e, only epoch0)
        dictionary--
         {"epoch0soma": {'tags': ('1_epoch_responses', 0, soma, modelname, modelscale, "epoch0soma")},
          "epoch0axon": {'tags': ('1_epoch_responses', 0, soma, modelname, modelscale, "epoch0axon")}}
        NOTE:
            - no_of_regions = len(list(chosenmodel.regions.keys()))
            - no_of_stimulus = 2
            - no_of_epochs_per_region = 1 + no_of_stimulus; thus it includes
              period/epoch pre-first stimulus
            - total number of epochs = no_of_regions * no_of_epochs_per_regions
            - 'tags':
              ( No_epoch_responses, index, cellregion, modelname, modelscale, epoch<index>cellregion )
            - elements of the tuple are "all strings"
        """
        x = {}
        lst = []
        no_of_epochs_per_region = cls.compute_totalepochs_per_cellregion(parameters)
        for cellregion in chosenmodel.regions.keys():
            [ x.update({"epoch"+str(i)+cellregion: {}})
                                   for i in range(no_of_epochs_per_region) ]
            [ x["epoch"+str(i)+cellregion].update({"tags":
                                             (str(no_of_epochs_per_region)+"_epoch_responses",
                                              str(i), cellregion,
                                              chosenmodel.modelname, chosenmodel.modelscale,
                                              "epoch"+str(i)+cellregion)})
                                   for i in range(no_of_epochs_per_region) ]
        return x

    @staticmethod
    def an_epoch( epoch_no_per_region, theregion, parameters ):
        """static method creates the value for one epoch, i.e, value for one of the epoch-key in the container.

        Arguments:
        epoch_no_per_region -- integer
        theregion -- string; key of chosenmodel.regions = {"soma": 0.0, "axon": 0.0}
        parameters --
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
                          "tstop": runtimeparameters["tstop"] # only for last epoch
        Returned Value:
        assuming chosenmodel.regions = {'soma': 0.0, 'axon': 0.0} the epoch metadata for a region, say "soma" is a dictionary
        dictionary -- {"source": "soma", "start_time": float, "stop_time": float,
                       "description": string}
        NOTE:
            - the returned value thas these same four-keys regardless of stimulus (or lack of)
        """
        if "stimlist" not in parameters:
            return {"source": theregion, "start_time": 0.0, "stop_time": float(parameters["tstop"]),
                    "description": "there is no stimulation of the model"}
        elif parameters["type"][0]=="current":
            stimlist = parameters["stimlist"]
            if epoch_no_per_region==0: # initial no stimulation region
                return {"source": theregion,
                        "start_time": 0.0,
                        "stop_time": 0.0 + stimlist[0]["delay"],
                        "description": "first, no stimulus"}
            else:
                i = epoch_no_per_region - 1
                if parameters["type"][1]=="IClamp":
                    descrip = "IClamp stimulation of model with amplitude = " + \
                              str(stimlist[i]["amp"]) + " nA"
                else:
                    descrip = "IRamp stimulation of model with amplitudes from " + \
                              str(stimlist[i]["amp_initial"]) + " to " + \
                              str(stimlist[i]["amp_final"]) + " nA"
                return {"source": theregion,
                        "start_time": float(stimlist[i]["delay"]),
                        "stop_time": float(stimlist[i]["delay"] + stimlist[i]["dur"]),
                        "description": descrip}

    def forepoch( self, chosenmodel=None, parameters=None ):
        """method that creates the NWB formatted metadata forfile.

        Keyword arguments (mandatory):
        chosenmodel -- instantiated model
        parameters --
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
                          "tstop": runtimeparameters["tstop"] # only for last epoch
        Returned Value:
        assuming chosenmodel.regions = {'soma': 0.0, 'axon': 0.0} and no of epochs/region=2 (i.e initial state regardless of stimulus is epoch0)
        returned value is a dictionary of the form
        dictionary -- {"epoch0soma": {"source": "soma", "start_time": float, "stop_time": float,
                                      "description": string},
                       "epoch1soma": {"source": "soma", "start_time": float, "stop_time": float,
                                      "description": string},
                       "epoch0axon": {"source": "soma", "start_time": float, "stop_time": float,
                                      "description": string},
                       "epoch1axon": {"source": "soma", "start_time": float, "stop_time": float,
                                      "description": string},
                       "epoch_tags": ('2_epoch_responses',)}
        however without stimulation, no of epochs/region = 1 (i.e, only epoch0)
        dictionary -- {"epoch0soma": {"source": "soma", "start_time": float, "stop_time": float,
                                      "description": string},
                       "epoch0axon": {"source": "soma", "start_time": float, "stop_time": float,
                                      "description": string},
                       "epoch_tags": ('1_epoch_responses',)}
        Use case:
        eg = EpochGenerator()
        model = Xyz()
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        For simulation without stimulation
        epochmd = eg.forepoch(chosenmodel = model, parameters = runtimeparam)
        Simulation with stimulation
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ],
                          "tstop": runtimeparam["tstop"]}
        epochmd = eg.forepoch(chosenmodel = model, parameters = stimparameters)
        """

        if (chosenmodel is None) or (parameters is None):
            raise ValueError("passing an instantiated chosenmodel and parameters (for runtime or stimulation) are  mandatory")
        else:
            x = self.epochcontainer( chosenmodel, parameters )
            no_of_epochs_per_region = self.compute_totalepochs_per_cellregion(parameters)
            for cellregion in chosenmodel.regions.keys():
                for i in range(no_of_epochs_per_region):
                    epoch = "epoch"+str(i)+cellregion
                    x[epoch].update( self.an_epoch( i, cellregion, parameters ) )
            return x
