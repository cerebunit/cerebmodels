# ~/managers/operatorsSimaudit/hardware.py
import multiprocessing

from neuron import h

class HardwareConfigurator(object):
    """Operator working under SimulationManager.

    This manager must be instantiated by passing neuron.h
    Eg: from neuron import h
        hc = HardwareConfigurator(h)

    Available methods:
    activate_cores -- Nothing is returned

    """

    def __init__(self):
        #self.h = neuron_dot_h
        pass

    @staticmethod
    def activate_cores():
        """

        Arguments:
        Nothing

        Returned values:
        Nothing

        """
        cores = multiprocessing.cpu_count()
        h.load_file("parcom.hoc")
        p = h.ParallelComputeTool()
        #p.change_nthread(cores, 1)
        p.multisplit(1)
        return "cores are activated" # for hardwareTest.py
