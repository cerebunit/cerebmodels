# ../managers/read.py
from managers.operatorsReadNWB.epoch_unraveller import EpochUnraveller as eu

from pynwb import NWBHDF5IO

#from pdb import set_trace as breakpoint

class ReadManager(object):
    """
    **Available methods:**

    +-----------------------------------------+-----------------+
    | Method name                             | Method type     |
    +=========================================+=================+
    | :py:meth:`.load_nwbfile`                | static method   |
    +-----------------------------------------+-----------------+
    | :py:meth:`.timestamps_for_epoch`        | static method   |
    +-----------------------------------------+-----------------+
    | :py:meth:`.data_for_epoch`              | static method   |
    +-----------------------------------------+-----------------+
    | :py:meth:`.total_epochIDs`              | static method   |
    +-----------------------------------------+-----------------+
    | :py:meth:`.order_all_epochs_for_region` | static method   |
    +-----------------------------------------+-----------------+

    """
    def __init__(self):
        pass

    @staticmethod
    def load_nwbfile(fullname):
        "Returns an `NWBFIle <https://nwb-schema.readthedocs.io/en/latest/format.html#nwbfile>`_ for a given fullname (filepath + filename; string)."
        io = NWBHDF5IO( fullname, mode="r" )
        return io.read() # this is the nwbfile object

    @staticmethod
    def timestamps_for_epoch( an_epoch ):
        """For a given `epoch <https://nwb-schema.readthedocs.io/en/latest/format.html#groups-intervals-epochs>`_ this function returns the snippet of the full ``timestamps`` obtained by calling ``.pluck_timeseries_object`` in :ref:`EpochUnraveller`, cut for indices between the ``start_time`` and ``stop_time`` obtained by calling ``.pull_indices_timeseries_for_epoch`` in :ref:`EpochUnraveller`.

        *NOTE:* For most practical purposes here the given `epoch` will be one of the elements in the list returned by calling :py:meth:`.order_all_epochs_for_region`.

        """
        nwbts = eu.pluck_timeseries_object( an_epoch )
        indices = eu.pull_indices_tseries_for_epoch( an_epoch )
        return [ nwbts.timestamps[i] for i in indices ]

    @staticmethod
    def data_for_epoch( an_epoch ):
        """For a given `epoch <https://nwb-schema.readthedocs.io/en/latest/format.html#groups-intervals-epochs>`_ this function returns the snippet of the full ``data`` obtained by calling ``.pluck_timeseries_object`` in :ref:`EpochUnraveller`, cut for indices between the ``start_time`` and ``stop_time`` obtained by calling ``.pull_indices_timeseries_for_epoch`` in :ref:`EpochUnraveller`.

        *NOTE:*

        * For most practical purposes here the given `epoch` will be one of the elements in the list returned by calling :py:meth:`.order_all_epochs_for_region`.
        * similarity with :py:meth:`.timstamps_for_epoch`, the difference being this one returns ``data``.

        """
        nwbts = eu.pluck_timeseries_object( an_epoch )
        indices = eu.pull_indices_tseries_for_epoch( an_epoch )
        return [ nwbts.data[i] for i in indices ]

    @staticmethod
    def total_epochIDs(nwbfile):
        """Alternative to ``.total_epochs_this_region`` in :ref:`EpochUnraveller`.

        *NOTE:*

        * this one takes the ``nwbfile`` (return of :py:meth:`.load_nwbfile`)
        * while ``.total_epochs_this_region`` takes an ``epoch`` (say, *any* one ``epoch`` in the list returned by calling :py:meth:`.order_all_epochs_for_region`)

        """
        total_N = eu.total_overall_epochs( nwbfile )
        #all_regions = nwbfile.epochs[0][3][] # space separated string
        #list_all_regions = all_regions.split()
        #total_regions = len(list_all_regions)
        #return total_N/total_regions
        an_epoch = nwbfile.epochs[0]
        return eu.total_epochs_this_region( an_epoch )

    @staticmethod
    def order_all_epochs_for_region(nwbfile=None, region=None):
        """For a given region (model region; e.g. cell region like "soma") and the `NWBFIle <https://nwb-schema.readthedocs.io/en/latest/format.html#nwbfile>`_, this function returns an ordered list of ``epochs``.

        **Keyword Arguments:**

        +-----------+----------------------------------------------------------------------------+
        | Key       | Value type                                                                 |
        +===========+============================================================================+
        |``nwbfile``|`NWBFIle <https://nwb-schema.readthedocs.io/en/latest/format.html#nwbfile>`_|
        +-----------+----------------------------------------------------------------------------+
        |``region`` | string; name of the model region, say, cell region like "soma" or "axon"   |
        +-----------+----------------------------------------------------------------------------+
        region => "region_name rec_site_name" or 
                  "group_name region_name component_name rec_site_name"

        """
        all_epochs_for_region = eu.pull_all_epochs_for_region(nwbfile=nwbfile, region=region)
        n = eu.total_epochs_this_region(all_epochs_for_region[0])
        indices = sorted( range(n) ) # ascending order
        orderedepochs = []
        i = 0
        while len(orderedepochs) < n:
            for indx in indices:
                if int(eu.pluck_epoch_id( all_epochs_for_region[indx] ))==i:
                    orderedepochs.append( all_epochs_for_region[indx] )
            i += 1
        return orderedepochs
