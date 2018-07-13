# ~/managers/operatorsSimaudit/hardware.py
import multiprocessing

from neuron import h

class HardwareConfigurator(object):
    """Operator working under SimulationManager.

    Available methods:
    activate_cores

    """

    def __init__(self):
        pass

    def activate_cores(self):
        """

        Arguments:
        Nothing

        Returned values:
        Nothing

        """
        cores = multiprocessing.cpu_count()
        h.load_file("parcom.hoc")
        p = h.ParallelComputeTool()
        p.change_nthread(cores, 1)
        p.multisplit(1)
