# ../managers/operatorsSignaling/reconstructer.py
import efel
#from quantities import mV

class Reconstructer(object):
    """
    **Available methods:**

    +-------------------------------------------------+--------------------+
    | Method name                                     | Method type        |
    +-------------------------------------------------+--------------------+
    | :py:meth:`.construct_base_efel_trace_individual`| static method      |
    +-------------------------------------------------+--------------------+
    | :py:meth:`.construct_base_efel_trace_overall`   | class method       |
    +-------------------------------------------------+--------------------+

    """
    @staticmethod
    def construct_base_efel_trace_individual(timestamp, datavalue):
        """Returns **a** dictionary with the keys: `"T"`, `"V"`, `"stim_start"` and `"stim_end"`.

        **Arguments:**

        +----------+-----------------+
        | Argument | Value type      |
        +==========+=================+
        | first    | array of times  |
        +----------+-----------------+
        | second   | array of values |
        +----------+-----------------+

        """
        a_trace = {}
        a_trace["V"] = datavalue
        a_trace["T"] = timestamp
        a_trace["stim_start"] = [ timestamp[0] ]
        a_trace["stim_end"]   = [ timestamp[-1] ]
        return a_trace

    @classmethod
    def construct_base_efel_trace_overall(cls, timestamp, datavalue):
        """Returns traces; a list of dictionaries with the keys: `"T"`, `"V"`, `"stim_start"` and `"stim_end"`.

        **Arguments:**

        +----------+-------------------------+
        | Argument | Value type              |
        +==========+=========================+
        | first    | list of array of times  |
        +----------+-------------------------+
        | second   | list of array of values |
        +----------+-------------------------+

        """
        return [ cls.create_base_efel_trace_individual( timestamps[i], datavalues[i] )
                 for i in range(len(timestamps)) ] # [ trace0, trace1, trace2, ... ]

