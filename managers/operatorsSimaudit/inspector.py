# ~/managers/operatorsSimaudit/inspector.py
import os
import sys
import subprocess

import neuron
#from neuron import h

# import modules from other directories
# set to ~/cerebmodels
#sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
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

    def check_compatibility(self, capability_name=None, CerebUnit_capability=None):
        """if model capability is known to be consistent with cerebunit module this module is not necessary to run.

        Keyword arguments:
        capability_name -- string; eg., "produce_spike_train"
        CerebUnit_capability -- imported class; eg., ProducesSpikeTrain

        Returned values:
        Nothing is returned

        """

        if capability_name is not None and CerebUnit_capability is not None:
            if not capability_name in dir(CerebUnit_capability):
                raise AttributeError(CerebUnit_capability.__name__ +
                                     " has no method " +
                                     capability_name)
            else:
                return CerebUnit_capability.__name__ + " has the method " + capability_name
        #pass
