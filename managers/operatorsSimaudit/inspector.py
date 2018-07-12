# ~/managers/operatorsSimaudit/inspector.py
import os
import sys
import subprocess

import neuron
#from neuron import h

# import modules from other directories
# set to ~/cerebmodels
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
#
from managers.operatorsFiling.pathspawner import PathSpawner

# import as usual for local modules
# from local import Local

class SimInspector(object):
    """Operator working under SimulationManager.

    Available methods:
    inspect_compiled_nmodl

    """

    def __init__(self):
        self.ps = PathSpawner()

    def lock_and_load_nmodl(self, modelscale=None, modelname=None):
        """method that checks for the compiled libnrnmech.so.0 file or else generates it.

        Keyword arguments:
        modelscale -- string; egs. "cells", "microcircuits", "networks"
        modelname -- string; "XY2000Author"

        Returned value:
        prints "compiled files already exists" or else
        Nil, it just generates the libnrnmech.so.0

        """
        # generate the 'standard' path to mod and lib files
        mod_path, lib_path = self.ps.hatch_path_to_nmodl(modelscale=modelscale,
                                                    modelname=modelname)
        # check if the librnmech.so.0 already exists
        if os.path.isfile(lib_path) is False:
            # if it does not exist, create it
            paths = os.path.split(mod_path)
            subprocess.call("cd " + paths[0] + ";nrnivmodl " + paths[1], shell=True)
            return "nmodl has just been compiled"
        else:
            return "nmodl was already compiled"
        # load the mod files, i.e, directory containing x86_64
        neuron.load_mechanisms(os.path.dirname(mod_path))
