# ~/managers/operatorsSimaudit/assembler.py
import os
import sys

from neuron import h

# import modules from other directories
# set to ~/cerebmodels
#sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
#
from utilities import UsefulUtils as uu

class SimAssembler(object):
    """Operator working under SimulationManager.

    Available methods:
    activate_cores

    """

    def __init__(self):
        pass

    @staticmethod
    def set_fixed_timesteps():
        """static method that makes time steps fixed

        Return values:
        Nothing. It sets the neuron.h for fixed time-step.

        """
        Fixed_step = h.CVode()
        Fixed_step.active(0)
        return "timestep is fixed" # for assemblerTest.py

    @classmethod
    def set_runtime_NEURON(cls, parameters=None):
        """sets runtime parameters to neuron.h

        Keyword Arguments:
        parameters -- dictionary with keys: dt, celsius, tstop & v_init

        Returned values:
        Nothing is returned

        PS: set_fixed_timesteps() is called here.

        """

        if parameters is None:
            raise ValueError("parameters must be a dictionary with keys: dt, celsius, tstop, and v_init")
        else:
            cls.set_fixed_timesteps()
            for key, value in parameters.iteritems():
                if key in h.__dict__:
                    setattr(h, key, value)
                    return "parameters are set" # for assemblerTest.py
                else:
                    raise AttributeError(key + "is not an attribute in h. Try loading the model mod files.")
