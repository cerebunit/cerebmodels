# ~/managers/operatorsTranscribe/metadata_electrodegenerator.py
import pkg_resources

import neuron

#import numpy.core.defchararray as npd

class ElectrodeGenerator(object):
    """Operators working under TranscribeManager

    Available methods:
    forcellelectrode -- classmethod called by forelectrode
    forelectrode
    """

    @staticmethod
    def cellelectrode_stimulus(cellregion, stimparameters):
        return {"name": "electrode_"+stimparameters["type"][1]+"_"+cellregion,
                "source": "from neuron import h >> h."+stimparameters["type"][1],
                "location": cellregion,
                "slice": "sec=0.5", # default
                "seal": "no seal",
                "description": "virtual patch-clamp electrode in "+cellregion+" with stimulation",
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
                "description": "virtual patch-clamp electrode in "+cellregion+" without stimulation",
                "resistance": "0 Ohm",
                "filtering": "no filter function",
                "initial_access_resistance": "0 Ohm",
                "device": "NEURON "+pkg_resources.get_distribution("neuron").version +" version" }

    @classmethod
    def forcellelectrode( cls, chosenmodel, parameters ):
        """class method that creates the NWB formatted electrode metadata for cells. This is normally not called by the TranscribeManager(), instead it is called by forelectrode() below.

        Arguments (mandatory):
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
        eg = ElectrodeGenerator()
        model = Xyz()
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        For simulation without stimulation
        elecmd = eg.forcellelectrode(chosenmodel = model, parameters = runtimeparam)
        Simulation with stimulation
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}
        elecmd = eg.forcellelectrode(chosenmodel = model, parameters = stimparameters)

        NOTE:
            - if chosenmodel.regions={"soma": 0.0, "axon": 0.0} then len(elecmd) = 2 since there are two cell regions
            - also, this means elecmd_soma = elecmd["soma"] and elecemd_axon = elecmd["axon"]
        """
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
        Use case: [For modelscale="cells"]
        eg = ElectrodeGenerator()
        model = Xyz()
        runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}
        For simulation without stimulation
        elecmd = eg.forelectrode(chosenmodel = model, parameters = runtimeparam)
        Simulation with stimulation
        stimparameters = {"type": ["current", "IClamp"],
                          "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
                                        {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]}
        elecmd = eg.forelectrode(chosenmodel = model, parameters = stimparameters)

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
