# ~/managers/operatorsReadNWB/epoch_unraveller.py
import re

class EpochUnraveller(object):
    """
    **Available methods:**

    +--------------------------------------------+-----------------+
    | Method name                                | Method type     |
    +============================================+=================+
    | :py:meth:`.total_overall_epochs`           | static method   |  
    +--------------------------------------------+-----------------+
    | :py:meth:`.pluck_epoch_row`                | static method   |
    +--------------------------------------------+-----------------+
    | :py:meth:`.pluck_start_time`               | static method   |
    +--------------------------------------------+-----------------+
    | :py:meth:`.pluck_stop_time`                | static method   |
    +--------------------------------------------+-----------------+
    | :py:meth:`.total_epochs_this_region`       | static method   |
    +--------------------------------------------+-----------------+
    | :py:meth:`.pluck_epoch_id`                 | static method   |
    +--------------------------------------------+-----------------+
    | :py:meth:`.pluck_region`                   | static method   |
    +--------------------------------------------+-----------------+
    | :py:meth:`.pluck_modelname`                | static method   |
    +--------------------------------------------+-----------------+
    | :py:meth:`.pluck_modelscale`               | static method   |
    +--------------------------------------------+-----------------+
    | :py:meth:`.pluck_timeseries_object`        | static method   |
    +--------------------------------------------+-----------------+
    | :py:meth:`.pull_all_epochs_for_region`     | class method    |
    +--------------------------------------------+-----------------+
    | :py:meth:`.pull_indices_tseries_for_epoch` | class method    |
    +--------------------------------------------+-----------------+

    """
    def __init__(self):
        pass

    @staticmethod
    def total_overall_epochs ( nwbfile ):
        """Return the total number of available epochs.

        *NOTE:* This is different from :py:meth:`.total_epochs_this_region`.

        """
        return len(nwbfile.epochs)

    @staticmethod
    def pluck_epoch_row( nwbfile, row_i  ):
        "Returns **an** epoch by extracting it from `NWBFile <https://nwb-schema.readthedocs.io/en/latest/format.html#nwbfile>`_ and the given row number (starting from 0). The ``nwbfile.epochs`` is a `VectorData. <https://pynwb.readthedocs.io/en/latest/pynwb.core.html#pynwb.core.VectorData>`_"
        return nwbfile.epochs[row_i]

    @staticmethod
    def pluck_start_time( an_epoch ):
        "Returns the ``start_time`` in seconds for the given epoch."
        return an_epoch[1]

    @staticmethod
    def pluck_stop_time( an_epoch ):
        "Returns the ``stop_time`` in seconds for the given epoch."
        return an_epoch[2]

    @staticmethod
    def total_epochs_this_region( an_epoch ):
        """Returns total epochs available for the region in the given epoch.
        
        *NOTE:*

        * this is not the same as :py:meth:`.total_overall_epochs`
        * generally this value is lesser than the total overall epochs
        * this number is extracted from the ``epoch_tags``
        * see :refer:EpochGenerator for how the epoch_tags were generated.

        """
        x = re.search( "[\d]+(?=_)", an_epoch[3][0] )
        return int(x.group(0))

    @staticmethod
    def pluck_epoch_id( an_epoch ):
        """Returns epoch id for the region in the given epoch.
        
        *NOTE:*

        * for a given region, total number of these id's of all the epochs from this regions is equal to those returned from :py:meth:`.pluck_total_epochs_this_region`.
        * this is extracted from the ``epoch_tags``
        * see :refer:EpochGenerator for how the epoch_tags were generated.

        """
        return an_epoch[3][1] # string

    @staticmethod
    def pluck_region( an_epoch ):
        "Returns region name for which this epoch is associated with."
        return an_epoch[3][2] # 'region rec_site' or 'group region component rec_site'

    @staticmethod
    def pluck_recordingsites( an_epoch ):
        "Returns all the recording sites for which this epoch is associated with just one of the recording site."
        return an_epoch[3][3] # 'rec_siteA rec_siteB'

    @staticmethod
    def pluck_modelname( an_epoch ):
        "Returns model name for which this epoch is associated with."
        return an_epoch[3][4]

    @staticmethod
    def pluck_modelscale( an_epoch ):
        "Returns name of the model scale for which this epoch is associated with."
        return an_epoch[3][5]

    @staticmethod
    def pluck_this_recordingsite( an_epoch ):
        "Returns name of the model scale for which this epoch is associated with."
        s = an_epoch[3][6]
        return s.split()[1] # 'epochXregion rec_site'

    @staticmethod
    def pluck_timeseries_object( an_epoch ):
        "Returns the given epoch's ``TimeSeries`` object."
        return an_epoch[4][0][2]

    @classmethod
    def pull_all_epochs_for_region( cls, nwbfile=None, region=None ):
        """Returns a list of **all** epochs for a particular region from `NWBFile <https://nwb-schema.readthedocs.io/en/latest/format.html#nwbfile>`_

        **Keyword Arguments:**

        +-----------+----------------------------------------------------------------------------+
        | Key       | Value type                                                                 |
        +===========+============================================================================+
        |``nwbfile``|`NWBFile <https://nwb-schema.readthedocs.io/en/latest/format.html#nwbfile>`_|
        +-----------+----------------------------------------------------------------------------+
        |``region`` |string representing name of the regions from which response was recorded    |
        +-----------+----------------------------------------------------------------------------+
        region => "region_name rec_site_name" or
                  "group_name region_name component_name rec_site_name"

        """
        if nwbfile is None:
            raise ValueError("Must pass <class 'pynwb.file.NWBFile'>")
        elif region is None:
            raise ValueError("Must pass a region name in string")
        all_epochs_a_region = []
        for i in range( cls.total_overall_epochs(nwbfile) ):
            an_epoch = cls.pluck_epoch_row(nwbfile, i)
            reg = cls.pluck_region(an_epoch)
            #print( reg )
            if reg==region:
                all_epochs_a_region.append( an_epoch )
        return all_epochs_a_region
        

    @classmethod
    def pull_indices_tseries_for_epoch( cls, an_epoch ):
        """Returns list of indices of the timestamps from the given time-series that is between ``start_time`` and ``stop_time`` in **an** epoch.
        """
        start_time = cls.pluck_start_time(an_epoch)
        stop_time = cls.pluck_stop_time(an_epoch)
        nwbts = cls.pluck_timeseries_object(an_epoch)
        #print(start_time, stop_time, nwbts.num_samples, len(nwbts.timestamps))# num_sample = length
        #
        # Using transformed start_time and stop_time
        #start_up = (start_time/nwbts.resolution) + nwbts.resolution #can miss last few deci.points
        start = start_time / nwbts.resolution
        start_up = (start_time + nwbts.resolution) / nwbts.resolution
        #start_low = (start_time - nwbts.resolution) / nwbts.resolution
        #stop_up = (stop_time + nwbts.resolution) / nwbts.resolution
        stop_low = (stop_time - nwbts.resolution) / nwbts.resolution
        stop = stop_time / nwbts.resolution
        # Transform timestamps
        t_transformed = nwbts.timestamps/nwbts.resolution
        #
        #print(nwbts.timestamps[0], nwbts.timestamps[-1], len(nwbts.timestamps)) # should have
        #print(t_transformed[0], t_transformed[-1], len(t_transformed)) # same lengths
        #print(start_up, start_low, stop_up, stop_low)
        #
        start_i = [ indx for indx in range(nwbts.num_samples)
                              if t_transformed[indx] >= start and
                                 t_transformed[indx] < start_up ][0]
        stop_i = [ indx for indx in range(nwbts.num_samples)
                              if t_transformed[indx] > stop_low and
                                 t_transformed[indx] <= stop ][0]
        # because if start_i = 0 stop_i < stop_up but stop_i = stop_up is desired
        #stop_i = (lambda i0, i1: i1+1 if i0==0 else i1)(start_i, stop_i)
        #print(start_i, stop_i)
        #print("index length", len(range(start_i, stop_i+1)))
        #print( stop_time )
        #print( len(nwbts.timestamps) )
        #print( stop_i )
        #print( start_i )
        #print( nwbts.timestamps[stop_i] )
        return range(start_i, stop_i)#+1) # add 1 to include stop_i

#    @classmethod
#    def pull_indices_epochs_for_region(cls, nwbfile=None, region=None ):
#        chosenregion_epochs = cls.pull_all_epochs_for_region( nwbfile=nwbfile, region=region )
#        n = cls.total_epochs_this_region(chosenregion_epochs[0])
#        return sorted(range(n)) # ascending order
