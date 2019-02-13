# ~/managers/operatorsSimaudit/stimulator.py
import os
import sys

from neuron import h

# import modules from other directories
# set to ~/cerebmodels
#sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
#
from utilities import UsefulUtils as uu

class Stimulator(object):
    """Operator working under SimulationManager.

    Available methods:
    inject_IClamp -- returns list_of_currents where each element is hoc object h.IClamp
    inject_IRamp -- returns list_of_currents where each element is hoc object h.IRamp
    inject_current_NEURON -- returns stimuli_list where each element is hoc object h.IClamp or h.IRamp depending on currenttype

    """

    def __init__(self):
        #self.h = neuron_dot_h
        pass

    @staticmethod
    def inject_IClamp(parameters, injectsite):
        """static method that injects IClamp for NEURON

        Argument:
        parameters -- list such that each element is a dictionary [ {}, {}, {} ]
        Eg: [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
              {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]
        injecsite -- neuron section, for e.g., cell.soma

        Return values:
        list_of_currents -- each element is hoc object h.IClamp

        """
        no_of_currents = len(parameters) # number of currents
        list_of_currents = []
        for i in range(no_of_currents):
            list_of_currents.append( h.IClamp(0.5, sec=injectsite) )
            for key, value in parameters[i].iteritems():
                if key in list_of_currents[i].__dict__:
                    setattr(list_of_currents[i], key, value)
                else:
                    raise AttributeError( key + " is not an attribute in h.IClamp." )
        return list_of_currents

    @staticmethod
    def inject_IRamp(parameters, injectsite):
        """static method that injects IRamp for NEURON

        Argument:
        parameters -- list such that each element is a dictionary [ {}, {}, {} ]
        Eg: [ {"amp_initial": 0.0, "amp_final": 1.0, "dur": 100.0, "delay": 10.0},
              {"amp_initial"": 1.0, "amp_final": 0.0, "dur": 100.0, "delay": 10.0+100.0} ]
        injecsite -- neuron section, for e.g., cell.soma

        Return values:
        list_of_currents -- each element is hoc object h.IRamp

        """
        no_of_currents = len(parameters) # number of currents
        list_of_currents = []
        for i in range(no_of_currents):
            list_of_currents.append( h.IRamp(0.5, sec=injectsite) )
            for key, value in parameters[i].iteritems():
                if key not in list_of_currents[i].__dict__:
                    raise AttributeError( key + " is not an attribute in h.IRamp." )
                else:
                    if i == 0 or ( i > 0 and key is not "amp_final"):
                        setattr(list_of_currents[i], key, value)
                    else: # for amp_final
                        adjusted_value = value - list_of_currents[i].amp_initial
                        setattr(list_of_currents[i], key, adjusted_value)
        return list_of_currents

    @staticmethod
    def inject_GrC_Sine(parameters, injecsite):
        """static method that injects GrC_Sine for NEURON

        Argument:
        parameters -- list such that each element is a dictionary [ {}, {}, {} ]
        Eg: [ {"amp": 0.006, "dur": 800.0, "delay": 100.0, "freq": 4.0, "phase": 0.0},
              {"amp": 0.006, "dur": 400.0, "delay": 100.0+800.0, "freq": 8.0, "phase": 0.0} ]
        injectsite -- neuron section, for e.g., cell.soma

        Return values:
        list_of_currents -- each element is hoc object h.GrC_Sine

        """
        no_of_sinucurrents = len(parameters)
        list_of_sinucurrents = []
        for i in range(no_of_sinucurrents):
            list_of_sinucurrents.append( h.GrC_Sine(0.5, sec=injecsite) )
            for key, value in parameters[i].iteritems():
                if key in list_of_sinucurrents[i].__dict__:
                    setattr(list_of_sinucurrents[i], key, value)
                else:
                    raise AttributeError( key + " is not an attribute in h.GrC_Sine" )
        return list_of_sinucurrents

    def inject_current_NEURON(self, currenttype=None, injparameters=None, neuronsection=None):
        """sets current injection parameters to either h.IClamp, h.IRamp, GrC_Sine

        Keyword Arguments:
        currenttype -- 'IClamp', 'IRamp' or "GrC_Sine"; only these choice
        injparameters -- list with elements as dictionary; like [ {}, {}, ... ]
        Eg: [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},
              {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]
        Eg: [ {"amp_initial": 0.0, "amp_final": 1.0, "dur": 100.0, "delay": 10.0},
              {"amp_inital"": 1.0, "amp_final": 0.0, "dur": 100.0, "delay": 10.0+100.0} ]
        Eg: [ {"amp": 0.006, "dur": 800.0, "delay": 100.0, "freq": 4.0, "phase": 0.0},
              {"amp": 0.006, "dur": 400.0, "delay": 100.0+800.0, "freq": 8.0, "phase": 0.0} ]
        neuronsection -- neuron section, for e.g., cell.soma where cell=CellTemplate()

        Return values:
        stimuli_list -- each element is hoc object h.IClamp or h.IRamp depending on currenttype

        NOTE:
           - depending on the currenttype choice inject_IClamp(), inject_IRamp() or
             inject_GrC_Sine is called
           - h.IClamp is available in NEURON by default
           - h.IRamp is custom which creates a current ramp
           - h.GrC_Sine is custom available in ~/GrC2001DAngela/mod_files
           
        """

        if currenttype is None or injparameters is None or neuronsection is None:
            raise ValueError("currenttype must be either 'IClamp' or 'IRamp'. injparameters must be a list such that its elements are dictionaries [ {}, {}, ... ]. neuronsection must be for eg cell.soma where cell = CellTemplate().")
        else:
            if currenttype is "IClamp" or \
               currenttype is "IRamp" or \
               currenttype is "GrC_Sine":
                desiredfunc = self.__getattribute__( "inject_"+currenttype )
                stimuli_list = desiredfunc( injparameters, neuronsection )
            else:
                raise ValueError("currenttype must be 'IClamp', 'IRamp','GrC_Sine'")
        return stimuli_list
