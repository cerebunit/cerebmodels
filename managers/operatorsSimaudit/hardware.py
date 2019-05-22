# ~/managers/operatorsSimaudit/hardware.py
import multiprocessing

from neuron import h

class HardwareConfigurator(object):
    """
    **Available methods:**

    +------------------------------+----------------------+
    | Method name                  | Method type          |
    +==============================+======================+
    | :py:meth:`.activate_cores`   | static method        |
    +------------------------------+----------------------+

    *NOTE:*

    * ``activate_cores``-  Nothing is returned

    """

    def __init__(self):
        #self.h = neuron_dot_h
        pass

    @staticmethod
    def activate_cores():
        """Activates cores

        **Arguments:** Nothing is passed.

        **Returned values:** Nothing is returned.

        """
        cores = multiprocessing.cpu_count()
        h.load_file("parcom.hoc")
        p = h.ParallelComputeTool()
        #p.change_nthread(cores, 1)
        #p.multisplit(1)
        return "cores are activated" # for hardwareTest.py
