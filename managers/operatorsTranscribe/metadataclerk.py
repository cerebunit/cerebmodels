# ~/managers/operatorsTranscribe/metadataclerk.py
import platform
import uuid
import time
import pkg_resources

import neuron

#import numpy.core.defchararray as npd

class MetadataClerk(object):
    """Operators working under TranscribeManager

    Available methods:
    forfile
    """

    @staticmethod
    def get_modelID(model):
        try:
            uuid_value = getattr(model, 'uuid')
            return uuid_value[:8]+"_"+uuid_value[-12:]
        except:
            return "no_model_uuid"

    @staticmethod
    def get_username(username):
        if username is None:
            return "anonymous"
        else:
            return username

    @staticmethod
    def get_testdescription(test):
        if test is None:
            return "raw simulation without running any CerebUnit test"
        else:
            return test.description

    @staticmethod
    def get_labname(labname):
        if labname is None:
            return "no lab name was provided"
        else:
            return labname

    @staticmethod
    def get_institution(instname):
        if instname is None:
            return "no institution was provided"
        else:
            return instname

    def forfile( self, chosenmodel=None, vtest=None, username=None,
                 labname=None, institutename=None ):
        """method that creates the NWB formatted metadata forfile.

        Keyword arguments (mandatory):
        chosenmodel -- instantiated model

        Keyword arguments (optional):
        vtest -- instantiated validation CerebUnit test
        username -- string
        labname -- string
        institutename -- string

        NOTE:
            - vtest is not given for raw stimulation of the chosenmodel

        Use case:
        md = MetadataClerk()
        model = Xyz()
        For simulation without validation test
        filemd = md.forfile(chosenmodel = model)
        Simulation with validation test
        vtest = Pqr()
        filemd = md.forfile(chosenmodel=model, test=vtest, username='john',
                            labname='hbp brain sim lab', institute='CNRS-UNIC')
        """

        if chosenmodel is None:
            raise ValueError("passing an instantiated chosenmodel is mandatory")
        else:
            return {'source': platform.platform(),
                    'session_description': "simulation of " + chosenmodel.modelname,
                    'identifier': self.get_modelID(chosenmodel),
                    'session_start_time': time.asctime(time.gmtime(time.time()))+' '+time.tzname[0],
                    'experimenter': self.get_username(username),
                    'experiment_description': self.get_testdescription(vtest),
                    'session_id': str(hash(str(uuid.uuid1()))),
                    'lab': self.get_labname(labname),
                    'institution': self.get_institution(institutename) }

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
        NOTE:
            - no_of_regions = len(list(chosenmodel.regions.keys()))
            - no_of_stimulus = 2
            - no_of_epochs_per_region = 1 + no_of_stimulus; thus it includes
              period/epoch pre-first stimulus
            - total number of epochs = no_of_regions * no_of_epochs_per_regions
        """
        x = {}
        no_of_epochs_per_region = cls.compute_totalepochs_per_cellregion(parameters)
        for key in chosenmodel.regions.keys():
            [ x.update({"epoch"+str(i)+key: None})
                                   for i in range(no_of_epochs_per_region) ]
        x.update({"epoch_tags": (str(no_of_epochs_per_region)+"_epoch_responses",)})
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
        """
        if "stimlist" not in parameters:
            return {"source": theregion, "start": 0.0, "stop": parameters["tstop"],
                    "description": "there is no stimulation of the model"}
        elif parameters["type"][0]=="current":
            stimlist = parameters["stimlist"]
            if epoch_no_per_region==0: # initial no stimulation region
                return {"source": theregion,
                        "start": 0.0,
                        "stop": 0.0 + stimlist[0]["delay"],
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
                        "start": stimlist[i]["delay"],
                        "stop": stimlist[i]["delay"] + stimlist[i]["dur"],
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
        Use case:
        md = MetadataClerk()
        model = Xyz()
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        For simulation without stimulation
        epochmd = md.forepoch(chosenmodel = model, parameters = runtimeparam)
        Simulation with stimulation
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}
        epochmd = md.forepoch(chosenmodel = model, parameters = stimparameters)
        """

        if (chosenmodel is None) or (parameters is None):
            raise ValueError("passing an instantiated chosenmodel and parameters (for runtime or stimulation) are  mandatory")
        else:
            x = self.epochcontainer( chosenmodel, parameters )
            no_of_epochs_per_region = self.compute_totalepochs_per_cellregion(parameters)
            for cellregion in chosenmodel.regions.keys():
                for i in range(no_of_epochs_per_region):
                    epoch = "epoch"+str(i)+cellregion
                    x[epoch] = self.an_epoch( i, cellregion, parameters )
            return x

    @staticmethod
    def cellelectrode_stimulus(cellregion, stimparameters):
        return {"name": "electrode_"+stimparameters["type"][1]+"_"+cellregion,
                "source": "from neuron import h >> h."+stimparameters["type"][1],
                "location": cellregion,
                "slice": "sec=0.5", # default
                "seal": "no seal",
                "description": "virtual patch-clamp electrode in "+cellregion,
                "resistance": "0 Ohm",
                "filtering": "no filter function",
                "initial_access_resistance": "0 Ohm",
                "device": "NEURON "+pkg_resources.get_distribution("neuron").version +" version" }

    @staticmethod
    def cellelectrode_nostimulus(cellregion):
        return {"name": "electrode_"+cellregion,
                "source": "from neuron import h",
                "location": cellregion,
                "slice": "sec=0.5", # default
                "seal": "no seal",
                "description": "virtual patch-clamp electrode in "+cellregion,
                "resistance": "0 Ohm",
                "filtering": "no filter function",
                "initial_access_resistance": "0 Ohm",
                "device": "NEURON "+pkg_resources.get_distribution("neuron").version +" version" }

    @classmethod
    def forcellelectrode( cls, chosenmodel, parameters ):
        y = {}
        if "stimlist" not in parameters:
            for cellregion in chosenmodel.regions.keys():
                y.update( {cellregion: cls.cellelectrode_nostimulus(cellregion)} )
        else: # for stimulus
            for cellregion in chosenmodel.regions.keys():
                y.update( {cellregion: cls.cellelectrode_stimulus(cellregion, parameters)} )
        return y

    def forelectrode( self, chosenmodel=None, parameters=None ):
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
        Use case:
        md = MetadataClerk()
        model = Xyz()
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        For simulation without stimulation
        elecmd = md.forelectrode(chosenmodel = model, parameters = runtimeparam)
        Simulation with stimulation
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}
        elecmd = md.forelectrode(chosenmodel = model, parameters = stimparameters)

        NOTE:
            - if chosenmodel.regions={"soma": 0.0, "axon": 0.0} then len(elecmd) = 2 since there are two cell regions
            - also, this means elecmd_soma = elecmd["soma"] and elecemd_axon = elecmd["axon"]
        """

        x = {}
        if (chosenmodel is None) or (parameters is None):
            raise ValueError("passing an instantiated chosenmodel and parameters (for runtime or stimulation) are  mandatory")
        elif chosenmodel.modelscale == "cells":
            x.update( self.forcellelectrode( chosenmodel, parameters ) )
        return x

    @staticmethod
    def cellrecordings_response_nostimulus(model, cellregion, rec_t, rec_v, parameters):
        return {"type": "GenericTimeSeries",
                "name": model.modelname+"_nostim_Vm_"+cellregion,
                "source": cellregion,
                "data": rec_v,
                "unit": "mV",
                "resolution": parameters["dt"],
                "conversion": 1000.0, # 1000 => 1ms
                "timestamps": rec_t,
                "starting_time": 0.0,
                "rate": 1/parameters["dt"],
                "comment": "voltage response without stimulation",
                "description": "whole single array of voltage response from "+cellregion+" of "+ model.modelname}

    @staticmethod
    def cellrecordings_response_stimulus(model, cellregion, rec_t, rec_v, parameters):
        return {"type": "CurrentClampSeries",
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
        return {"type": "CurrentClampStimulusSeries",
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
        y = {}
        #if npd.equal(recordings["stimulus"], "Model is not stimulated").item((0)):
        # str because recordings has numpy array as dictionary values resulting in
        # numpy FutureWarning bug as it expects this to be an array as well
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
        if (chosenmodel is None) or (recordings is None) or (runtimeparameters is None):
            raise ValueError("passing an instantiated chosenmodel, the recordings (dictionary) and runtimeparameters are  mandatory")
        elif chosenmodel.modelscale == "cells":
            return self.forcellrecording( chosenmodel=chosenmodel,
                                          recordings=recordings,
                                          runtimeparameters=runtimeparameters,
                                          stimparameters=stimparameters )
