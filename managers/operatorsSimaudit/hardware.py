# ~/managers/operatorsSimaudit/hardware.py
import multiprocessing

#from neuron import h

class HardwareConfigurator(object):
    """Operator working under SimulationManager.

    This manager must be instantiated by passing neuron.h
    Eg: from neuron import h
        hc = HardwareConfigurator(h)

    Available methods:
    activate_cores

    """

    def __init__(self, neuron_dot_h):
        self.h = neuron_dot_h

    def activate_cores(self):
        """

        Arguments:
        Nothing

        Returned values:
        Nothing

        """
        cores = multiprocessing.cpu_count()
        self.h.load_file("parcom.hoc")
        p = self.h.ParallelComputeTool()
        p.change_nthread(cores, 1)
        p.multisplit(1)
        return "cores are activated" # for hardwareTest.py
