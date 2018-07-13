# ~/managers/operatorsSimaudit/assembler.py
import os
import sys

from neuron import h

# import modules from other directories
# set to ~/cerebmodels
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
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
        Fixed_step.activate(0)
