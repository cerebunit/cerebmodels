# ~/managers/operatorsTranscribe/fabricator.py
import os # only for filepath/filename in writing nwbfile
from datetime import datetime

from managers.operatorsYield.regionparser import RegionParser as rp

import numpy

import pynwb
from pynwb import NWBFile
from pynwb import TimeSeries
#from pynwb.icephys import IntracellularElectrode
#from pynwb.icephys import CurrentClampSeries, CurrentClampStimulusSeries
#from pynwb.icephys import VoltageClampSeries, VoltageClampStimulusSeries
#from pynwb import get_manager
from pynwb import NWBHDF5IO

#from pdb import set_trace as breakpoint

class Fabricator(object):
    """
    **Available Methods:**

    +------------------------------------------------+---------------------+
    | Method name                                    | Method type         |
    +================================================+=====================+
    | :py:meth:`.build_nwbfile`                      | class method        |
    +------------------------------------------------+---------------------+
    | :py:meth:`.build_nwbseries`                    | class method        |
    +------------------------------------------------+---------------------+
    | :py:meth:`.affix_nwbseries_to_nwbfile`         | class method        |
    +------------------------------------------------+---------------------+
    | :py:meth:`.build_nwbepochs`                    | class method        |
    +------------------------------------------------+---------------------+
    | :py:meth:`.write_nwbfile`                      | class method        |
    +------------------------------------------------+---------------------+
    | :py:meth:`.construct_nwbseries_nostimulus`     | class method        |
    +------------------------------------------------+---------------------+
    | :py:meth:`.generic_timeseries`                 | static method       |
    +------------------------------------------------+---------------------+
    | :py:meth:`.link_nwbseriesresponses_to_nwbfile` | static method       |
    +------------------------------------------------+---------------------+
    | :py:meth:`.strip_out_stimulus_from_nwbseries`  | static method       |
    +------------------------------------------------+---------------------+
    | :py:meth:`.indices_tseries_for_epoch`          | static method       |
    +------------------------------------------------+---------------------+
    | :py:meth:`.tseries_for_epoch`                  | class method        |
    +------------------------------------------------+---------------------+
    | :py:meth:`.insert_a_nwbepoch`                  | class method        |
    +------------------------------------------------+---------------------+

    """

    @classmethod
    def build_nwbfile( cls, filemd ):
        """Builds the nwbfile

        **Argument:**

        +----------+----------------------------------------------------------------+
        | Argument | Value type                                                     |
        +==========+================================================================+
        | only one | dictionary of the file metadata such that                      |
        |          |                                                                |
        |          |::                                                              |
        |          |                                                                |
        |          |    {                                                           |
        |          |     "session_description": "How was the data generated?",      |
        |          |     "identifier": "a unique ID",                               |
        |          |     "session_start_time": datetime(time when recording began), |
        |          |     "experimenter": "name of the experimenter",                |
        |          |     "experiment_description": "described experiment",          |
        |          |     "session_id": "collab ID",                                 |
        |          |     "institution": "name of the institution",                  |
        |          |     "lab": "name of the lab"                                   |
        |          |     }                                                          |
        +----------+----------------------------------------------------------------+

        **Returned Value:** The returned nwbfile has the following attributes of interests: ``nwbfile.session_description``, ``nwbfile.identifier``, ``nwbfile.session_start_time``, ``nwbfile.experimenter``, ``nwbfile.experiment_description``, ``nwbfile.session_id``, ``nwbfile.lab`` and ``nwbfile.institution``.

        **Use case:**

        ``>> file_to_write = build_nwbfile( file_metadata )``

        *NOTE:* The overall available attributes are however

        :: 

           pynwb.file.NWBFile(
                session_description, identifier, session_start_time,
                file_create_date=None, experimenter=None, experiment_description=None,
                session_id=None, institution=None, notes=None, pharmacology=None,
                protocol=None, related_publications=None, slices=None,
                source_script=None, source_script_file_name=None, data_collection=None,
                surgery=None, virus=None, stimulus_notes=None, lab=None,
                acquisition=None, stimulus=None, stimulus_template=None, epochs=None,
                epoch_tags=set(), trials=None, modules=None, ec_electrodes=None,
                ec_electrode_groups=None, ic_electrodes=None, imaging_planes=None,
                ogen_sites=None, devices=None, subject=None )

        `Refer to pynwb documentation. <http://pynwb.readthedocs.io/en/latest/pynwb.file.html#pynwb.file.NWBFile>`_

        """
        return NWBFile( #source = filemd["source"],
                        session_description = filemd["session_description"], # Required NWB2.0
                        identifier = filemd["identifier"],                   # Required NWB2.0
                        session_start_time = filemd["session_start_time"],   # Required NWB2.0
                        file_create_date = datetime.now(),                   # optional datetime
                        experimenter = filemd["experimenter"],               # optional
                        experiment_description = filemd["experiment_description"], # optional
                        session_id = filemd["session_id"],                   # optional
                        lab = filemd["lab"],                                 # optional
                        institution = filemd["institution"] )                # optional

    @staticmethod
    def generic_timeseries(metadata):
        """Creates a generic NWB time-series object.

        **Argument:**

        +----------+--------------------------------------------------------------+
        | Argument | Value type                                                   |
        +==========+==============================================================+
        | only one |- dictionary of time-series metadata                          |
        |          |- it must have the following keys and their value type        |
        |          +-----------------+--------------------------------------------+
        |          | key             | value type                                 |
        |          +-----------------+--------------------------------------------+
        |          | ``"name"``      | string                                     |
        |          +-----------------+--------------------------------------------+
        |          | ``"data"``      | list/tuple/array                           |
        |          +-----------------+--------------------------------------------+
        |          | ``"unit"``      | string                                     |
        |          +-----------------+--------------------------------------------+
        |          | ``"resolution"``| string/float                               |
        |          +-----------------+--------------------------------------------+
        |          | ``"conversion"``| string/float                               |
        |          +-----------------+--------------------------------------------+
        |          |``"timestamps"`` | list/tuple/array                           |
        |          +-----------------+--------------------------------------------+
        |          |``"comments"``   | string                                     |
        |          +-----------------+--------------------------------------------+
        |          |``"description"``| string                                     |
        +----------+-----------------+--------------------------------------------+

        **Returned Value:** The NWB time-series object, say ``nwbts`` will have the following useful attributes ``nwbts.name``, ``nwbts.data``, ``nwbts.timestamps``, ``nwbts.unit``, ``nwbts.resolution``, ``nwbts.converstion``, ``#nwbts.starting_time``, ``#nwbts.rate``, ``nwbts.comment``, ``nwbts.description``.

        *NOTE:* The overall available attributes are however

        ::

           pynwb.base.TimeSeries(
                              name, data=None, unit=None, resolution=0.0,
                              conversion=1.0, timestamps=None, starting_time=None,
                              rate=None, comments='no comments',
                              description='no description', control=None,
                              control_description=None, parent=None )

        `Refer to pynwb documentation. <https://pynwb.readthedocs.io/en/latest/pynwb.base.html#pynwb.base.TimeSeries>`_

        *Potential Bug:*

        * due to the `bug I reported <https://github.com/NeurodataWithoutBorders/pynwb/issues/579>`_ ``starting_time`` and ``rate`` attributes are not included thus defaults to ``None``
        * pynwb developer says ".. is because you either enter timestamps or rate+starting_time, not all three. We should catch this and raise an error."
        * so to avoid error in future pynwb version the two attributes are taken out.

        """
        return TimeSeries( metadata["name"],
                           #metadata["source"],                 # no longer in NWB2.0
                           data = numpy.array(metadata["data"]),
                           unit = metadata["unit"],
                           resolution = metadata["resolution"],
                           conversion = metadata["conversion"],
                           timestamps = numpy.array(metadata["timestamps"]),
                           #starting_time = metadata["starting_time"],
                           #rate = metadata["rate"],
                           comments = metadata["comments"],
                           description = metadata["description"] )

    @classmethod
    def construct_nwbseries_regionbodies( model, tsmd ):
        regionlist = rp.get_regionlist(model)
        nwbseries = {}
        for a_region_name in regionlist:
            no_of_rec = len(model.regions[a_region_name])
            for ith_rec_type in range(no_of_rec):
                rec_of = model.regions[a_region_name][ith_rec_type]

    @classmethod
    def construct_nwbseries_nostimulus(cls, chosenmodel, tsmd):
        """Creates `NWB time-series object <https://pynwb.readthedocs.io/en/latest/pynwb.base.html#pynwb.base.TimeSeries>`_ without stimulus.

        **Arguments:**

        +-----------+--------------------------------------------------------------+
        | Arguments | Value type                                                   |
        +===========+==============================================================+
        | first     | instantiated model                                           |
        +-----------+-----------------+--------------------------------------------+
        | second    |- dictionary of time-series metadata                          |
        |           |- it must have the following keys and their values            |
        |           +-----------------+--------------------------------------------+
        |           | key             | value type                                 |
        |           +-----------------+--------------------------------------------+
        |           | ``"name"``      | string                                     |
        |           +-----------------+--------------------------------------------+
        |           | ``"data"``      | list/tuple/array                           |
        |           +-----------------+--------------------------------------------+
        |           | ``"unit"``      | string                                     |
        |           +-----------------+--------------------------------------------+
        |           | ``"resolution"``| string/float                               |
        |           +-----------------+--------------------------------------------+
        |           | ``"conversion"``| string/float                               |
        |           +-----------------+--------------------------------------------+
        |           |``"timestamps"`` | list/tuple/array                           |
        |           +-----------------+--------------------------------------------+
        |           |``"comments"``   | string                                     |
        |           +-----------------+--------------------------------------------+
        |           |``"description"``| string                                     |
        +-----------+-----------------+--------------------------------------------+

        **Returned Value:** The NWB time-series object, say ``nwbts`` will have the following useful attributes

        ::

           nwbts[key].name, nwbts[key].data,
           nwbts[key].timestamps, nwbts[key].unit,
           nwbts[key].resolution, nwbts[key].converstion,
           nwbts[key].starting_time, nwbts[key].rate,
           nwbts[key].comment, nwbts[key].description

        such that a ``key`` are the keys in ``chosemodel.regions = {'soma':0.0, 'axon':0.0}``.

        *NOTE:* The overall available attributes are however

        ::

           pynwb.base.TimeSeries(
                               name, data=None, unit=None, resolution=0.0,
                               conversion=1.0, timestamps=None, starting_time=None,
                               rate=None, comments='no comments',
                               description='no description', control=None,
                               control_description=None, parent=None )

        `Refer to pynwb documentation. <https://pynwb.readthedocs.io/en/latest/pynwb.base.html#pynwb.base.TimeSeries>`_

        """
        nwbseries = {}
        for cellregion in chosenmodel.regions.keys():
            nwbseries.update( {cellregion:
                              cls.generic_timeseries(tsmd[cellregion])} )
        return nwbseries

    @classmethod
    def build_nwbseries(cls, chosenmodel=None, tsmd=None):
        """Builds an `NWB time-series object. <https://pynwb.readthedocs.io/en/latest/pynwb.base.html#pynwb.base.TimeSeries>`_

        **Keyword Arguments:**

        +-----------------+--------------------------------------------------------------+
        | Key             | Value type                                                   |
        +=================+==============================================================+
        | ``chosenmodel`` |instantiated model                                            |
        | ``tsmd``        |- dictionary of time-series metadata                          |
        |                 +---------------------------+----------------------------------+
        |                 | key                       | value type                       |
        |                 +---------------------------+----------------------------------+
        |                 | ``"name"``                | string                           |
        |                 +---------------------------+----------------------------------+
        |                 | ``"data"``                | list/tuple/array                 |
        |                 +---------------------------+----------------------------------+
        |                 | ``"unit"``                | string                           |
        |                 +---------------------------+----------------------------------+
        |                 | ``"resolution"``          | string/float                     |
        |                 +---------------------------+----------------------------------+
        |                 | ``"conversion"``          | string/float                     |
        |                 +---------------------------+----------------------------------+
        |                 |``"timestamps"``           | list/tuple/array                 |
        |                 +---------------------------+----------------------------------+
        |                 |``"comments"``             | string                           |
        |                 +---------------------------+----------------------------------+
        |                 |``"description"``          | string                           |
        |                 +---------------------------+----------------------------------+
        |                 | ``"stimulus"`` (optional) |                                  |
        +-----------------+---------------------------+----------------------------------+

        **Returned Value:** The NWB time-series object, say ``nwbts`` will have the following useful attributes

        ::

           nwbts[key].name, nwbts[key].data,
           nwbts[key].timestamps, nwbts[key].unit,
           nwbts[key].resolution, nwbts[key].converstion,
           nwbts[key].starting_time, nwbts[key].rate,
           nwbts[key].comment, nwbts[key].description

        such that a ``key`` are the keys in ``chosemodel.regions = {'soma':0.0, 'axon':0.0}`` and with or without ``"stimulus"`` key.

        *NOTE:* The overall available attributes are however

        ::

           pynwb.base.TimeSeries(
                               name, data=None, unit=None, resolution=0.0,
                               conversion=1.0, timestamps=None, starting_time=None,
                               rate=None, comments='no comments',
                               description='no description', control=None,
                               control_description=None, parent=None )

        `Refer to pynwb documentation. <https://pynwb.readthedocs.io/en/latest/pynwb.base.html#pynwb.base.TimeSeries>`_

        """
        nwbseries = {}
        if "stimulus" in tsmd:
            nwbseries.update( {"stimulus": cls.generic_timeseries(tsmd["stimulus"])} )
            nwbseries.update( cls.construct_nwbseries_nostimulus(chosenmodel, tsmd) )
        else:
            nwbseries.update( cls.construct_nwbseries_nostimulus(chosenmodel, tsmd) )
        return nwbseries

    @staticmethod
    def link_nwbseriesresponses_to_nwbfile(nwbseries, nwbfile):
        """Adds response related time-series NOT the stimulus signal (time-series). This is called by :py:meth:`.affix_nwbseries_to_nwbfile`.

        **Arguments:**

        +-----------+------------------------------------------------------------+
        | Arguments | Value type                                                 |
        +===========+============================================================+ 
        | first     |- dictionary of NWB time-series object                      |
        |           |- its keys are the keys in                                  |
        |           |``chosenmodel.regions = {"soma": 0.0, "axon", 0.0}``        |
        |           |- value for each key is a ``pynwb.base.TimeSeries`` object, |
        |           | obtained using :py:meth:`.build_nwbseries method`          |
        +-----------+------------------------------------------------------------+
        | second    |- the built NWB file of type ``pynwb.file.NWBFile``         |
        |           |- obtained using :py:meth:`.build_nwbfile method`           |
        +-----------+------------------------------------------------------------+

        **Returned value:** This is the NWB file fed as an argument but updated by adding the time-series, say, ``updated_nwbfile``. The ``TimeSeries`` object can be extracted as

        ``>> ts_of_key = updated_nwbfile.get_acquisition(nwbseries[key].name)``

        where key is the region. For example,

        ``>> ts_soma = updated_nwbfile.get_acquisition(nwbseries["soma"].name)``

        Then you can get all the available attributes as usual

        ::

           ts_soma.name, ts_soma.data,
           ts_soma.timestamps, ts_soma.unit,
           ts_soma.resolution, ts_soma.converstion,
           ts_soma.starting_time, ts_soma.rate,
           ts_soma.comment, ts_soma.description

        *NOTE:*

        * unlike the returned value for :py:meth:`.build_nwbseries` the time-series here are for a particular key therefore it is no longer a dictionary.

        """
        for key in nwbseries.keys():
            nwbfile.add_acquisition(nwbseries[key])
        return nwbfile

    @staticmethod
    def strip_out_stimulus_from_nwbseries(nwbseries):
        """Extracts from the root time-series object all the time-series objects with the exception of the stimulus time-series. This method is called by :py:meth:`.affix_nwbseries_to_nwbfile`.
        """
        return { x: nwbseries[x] for x in nwbseries
                                  if x not in {"stimulus"} }

    @classmethod
    def affix_nwbseries_to_nwbfile(cls, nwbts=None, nwbfile=None):
        """Adds time-series (response time-series with or without the stimulus time-series).

        **Keyword Arguments:**

        +-------------+------------------------------------------------------------+
        | Key         | Value type                                                 |
        +=============+============================================================+ 
        | ``nwbts``   |- dictionary of NWB time-series object                      |
        |             |- its keys are the keys in                                  |
        |             |``chosenmodel.regions = {"soma": 0.0, "axon", 0.0}``        |
        |             |- the key ``"stimulus"`` is optional                        |
        |             |- value for each key is a ``pynwb.base.TimeSeries`` object, |
        |             |obtained using :py:meth:`.build_nwbseries method`           |
        +-------------+------------------------------------------------------------+
        | ``nwbfile`` |- the built NWB file of type ``pynwb.file.NWBFile``         |
        |             |- obtained using :py:meth:`.build_nwbfile method`           |
        +-------------+------------------------------------------------------------+

        **Returned value:** This is the NWB file fed as an argument but updated by adding the time-series, say, ``updated_nwbfile``. The ``TimeSeries`` object can be extracted as

        ``>> ts_of_key = updated_nwbfile.get_acquisition(nwbseries[key].name)``

        where key is the region. For example,

        ``>> ts_soma = updated_nwbfile.get_acquisition(nwbseries["soma"].name)``

        Then you can get all the available attributes as usual

        ::

           ts_soma.name, ts_soma.data,
           ts_soma.timestamps, ts_soma.unit,
           ts_soma.resolution, ts_soma.converstion,
           ts_soma.starting_time, ts_soma.rate,
           ts_soma.comment, ts_soma.description

        But if ``"stimulus"`` is one of the availabe keys then do

        ``>> ts_stim = updated_nwbfile.get_stimulus(nwbseries["stimulus"].name)``

        Now all the aforementioned attributes are available as usual.

        *NOTE:* Unlike the returned value for :py:meth:`.build_nwbseries` the time-series here are for a particular key therefore it is no longer a dictionary.

        """
        if "stimulus" in nwbts.keys():
            nwbfile.add_stimulus(nwbts["stimulus"])
            stripped_nwbseries = cls.strip_out_stimulus_from_nwbseries(nwbts)
            nwbfile = cls.link_nwbseriesresponses_to_nwbfile(stripped_nwbseries,
                                                             nwbfile)
        else:
            nwbfile = cls.link_nwbseriesresponses_to_nwbfile(nwbts,
                                                             nwbfile)
        return nwbfile

    @staticmethod
    def indices_tseries_for_epoch( epochmd_i_cellregion, nwbts ):
        """Returns list of indices of the timestamps from the given time-series that is between ``start_time`` and ``stop_time`` in **an** epoch of a given *region*.

        **Arguments:**

        +----------+------------------------------------------------------------------+
        | Argument | Value type                                                       |
        +==========+==================================================================+
        | first    |- dictionary of time-series metadata for a particular region of   |
        |          | **an** epoch                                                     |
        |          |- considering the case                                            |
        |          |``chosenmodel.regions = {'soma': 0.0, 'axon': 0.0}`` and the      |
        |          |number of epochs per region = 2                                   |
        |          |- when there is a stimulation the dictionary will be of the form  |
        |          |                                                                  |
        |          |::                                                                |
        |          |                                                                  |
        |          |   {"epoch0soma":                                                 |
        |          |       {"source": "soma", "start_time": float, "stop_time": float,|
        |          |                  "description": string, "tags": tuple}           |
        |          |    "epoch1soma":                                                 |
        |          |       {"source": "soma", "start_time": float, "stop_time": float,|
        |          |                  "description": string, "tags": tuple}           |
        |          |    "epoch0axon":                                                 |
        |          |       {"source": "axon", "start_time": float, "stop_time": float,|
        |          |                  "description": string, "tags": tuple}           |
        |          |    "epoch1axon":                                                 |
        |          |       {"source": "axon", "start_time": float, "stop_time": float,|
        |          |                  "description": string, "tags": tuple}}          |
        |          |                                                                  |
        |          |- but when there is no stimulation the dictionary will look as    |
        |          |                                                                  |
        |          |::                                                                |
        |          |                                                                  |
        |          |   {"epoch0soma":                                                 |
        |          |       {"source": "soma", "start_time": float, "stop_time": float,|
        |          |                  "description": string, "tags": tuple}           |
        |          |    "epoch0axon":                                                 |
        |          |       {"source": "axon", "start_time": float, "stop_time": float,|
        |          |                  "description": string, "tags": tuple}}          |
        +----------+------------------------------------------------------------------+
        | second   |- dictionary of NWB time-series object                            |
        |          |- its keys are the keys in                                        |
        |          |``chosenmodel.regions = {"soma": 0.0, "axon", 0.0}``              |
        |          |- the key ``"stimulus"`` is optional                              |
        |          |- value for each key is a ``pynwb.base.TimeSeries`` object,       |
        |          |obtained using :py:meth:`.build_nwbseries method`                 |
        +----------+------------------------------------------------------------------+

        *NOTE:*

        * the whole NWB TimeSeries is not passed here
        * only time series that corresponds to the respective region is passed into this function
        * the epoch metadata has the key ``"source"``. This represents the region from which epoch is considered this should not be confused with any attribute of the NWB file. Besides, since NWB2.0 ``source`` is no longer an attribute of NWB file.

        """ 
        start_up = epochmd_i_cellregion["start_time"] + nwbts.resolution
        start_low = epochmd_i_cellregion["start_time"] - nwbts.resolution
        stop_up = epochmd_i_cellregion["stop_time"] + nwbts.resolution
        stop_low = epochmd_i_cellregion["stop_time"] - nwbts.resolution
        start_i = [indx for indx in range(nwbts.num_samples)
                   if nwbts.timestamps[indx] > start_low and nwbts.timestamps[indx] < start_up][0]
        stop_i = [indx for indx in range(nwbts.num_samples)
                   if nwbts.timestamps[indx] > stop_low and nwbts.timestamps[indx] < stop_up][0]
        return range(start_i, stop_i+1) # add 1 to include stop_i

    @classmethod
    def tseries_for_epoch( cls, epochmd_i_cellregion, nwbts ):
        """Returns the NWB ``TimeSeries`` object with ``data`` and ``timestamps`` occuring between ``start_time`` and ``stop_time`` in **an** epoch of a given *region*. This method is called by :py:meth::`.insert_a_nwbepoch`.

        **Arguments:**

        +----------+------------------------------------------------------------------+
        | Argument | Value type                                                       |
        +==========+==================================================================+
        | first    |- dictionary of time-series metadata for a particular region of   |
        |          | **an** epoch                                                     |
        |          |- considering the case                                            |
        |          |``chosenmodel.regions = {'soma': 0.0, 'axon': 0.0}`` and the      |
        |          |number of epochs per region = 2                                   |
        |          |- when there is a stimulation the dictionary will be of the form  |
        |          |                                                                  |
        |          |::                                                                |
        |          |                                                                  |
        |          |   {"epoch0soma":                                                 |
        |          |       {"source": "soma", "start_time": float, "stop_time": float,|
        |          |                  "description": string, "tags": tuple}           |
        |          |    "epoch1soma":                                                 |
        |          |       {"source": "soma", "start_time": float, "stop_time": float,|
        |          |                  "description": string, "tags": tuple}           |
        |          |    "epoch0axon":                                                 |
        |          |       {"source": "axon", "start_time": float, "stop_time": float,|
        |          |                  "description": string, "tags": tuple}           |
        |          |    "epoch1axon":                                                 |
        |          |       {"source": "axon", "start_time": float, "stop_time": float,|
        |          |                  "description": string, "tags": tuple}}          |
        |          |                                                                  |
        |          |- but when there is no stimulation the dictionary will look as    |
        |          |                                                                  |
        |          |::                                                                |
        |          |                                                                  |
        |          |   {"epoch0soma":                                                 |
        |          |       {"source": "soma", "start_time": float, "stop_time": float,|
        |          |                  "description": string, "tags": tuple}           |
        |          |    "epoch0axon":                                                 |
        |          |       {"source": "axon", "start_time": float, "stop_time": float,|
        |          |                  "description": string, "tags": tuple}}          |
        +----------+------------------------------------------------------------------+
        | second   |- dictionary of NWB time-series object                            |
        |          |- its keys are the keys in                                        |
        |          |``chosenmodel.regions = {"soma": 0.0, "axon", 0.0}``              |
        |          |- the key ``"stimulus"`` is optional                              |
        |          |- value for each key is a ``pynwb.base.TimeSeries`` object,       |
        |          |obtained using :py:meth:`.build_nwbseries method`                 |
        +----------+------------------------------------------------------------------+

        *NOTE:*

        * the whole NWB TimeSeries is not passed here
        * only time series that corresponds to the respective region is passed into this function
        * the epoch metadata has the key ``"source"``. This represents the region from which epoch is considered this should not be confused with any attribute of the NWB file. Besides, since NWB2.0 ``source`` is no longer an attribute of NWB file.

        """ 
        indices = cls.indices_tseries_for_epoch( epochmd_i_cellregion, nwbts )
        ts_md = { 
          "name": nwbts.name, "comments": nwbts.name, "description": nwbts.description,
          "unit": nwbts.unit, "resolution": nwbts.resolution, "conversion": nwbts.conversion,
          "timestamps": [nwbts.timestamps[i] for i in indices],
          "data": [nwbts.data[i] for i in indices] }
        return cls.generic_timeseries(ts_md)

    @classmethod
    def insert_a_nwbepoch( cls, epoch_i_cellregion, epochmd, nwbfile, nwbts ):
        """Creates an epoch for a given region and updates the already created parent NWB file. This method called by :py:meth:`.construct_nwbepochs`.

        **Arguments:**

        +----------+------------------------------------------------------------------+
        | Argument | Value type                                                       |
        +==========+==================================================================+
        | first    |string for key of an epoch from a particular region, say,         |
        |          |``"epoch1soma"``                                                  |
        +----------+------------------------------------------------------------------+
        | second   |- dictionary of time-series metadata                              |
        |          |- considering the case                                            |
        |          |``chosenmodel.regions = {'soma': 0.0, 'axon': 0.0}`` and the      |
        |          |number of epochs per region = 2                                   |
        |          |- when there is a stimulation the dictionary will be of the form  |
        |          |                                                                  |
        |          |::                                                                |
        |          |                                                                  |
        |          |   {"epoch0soma":                                                 |
        |          |       {"source": "soma", "start_time": float, "stop_time": float,|
        |          |                  "description": string, "tags": tuple}           |
        |          |    "epoch1soma":                                                 |
        |          |       {"source": "soma", "start_time": float, "stop_time": float,|
        |          |                  "description": string, "tags": tuple}           |
        |          |    "epoch0axon":                                                 |
        |          |       {"source": "axon", "start_time": float, "stop_time": float,|
        |          |                  "description": string, "tags": tuple}           |
        |          |    "epoch1axon":                                                 |
        |          |       {"source": "axon", "start_time": float, "stop_time": float,|
        |          |                  "description": string, "tags": tuple}}          |
        |          |                                                                  |
        |          |- but when there is no stimulation the dictionary will look as    |
        |          |                                                                  |
        |          |::                                                                |
        |          |                                                                  |
        |          |   {"epoch0soma":                                                 |
        |          |       {"source": "soma", "start_time": float, "stop_time": float,|
        |          |                  "description": string, "tags": tuple}           |
        |          |    "epoch0axon":                                                 |
        |          |       {"source": "axon", "start_time": float, "stop_time": float,|
        |          |                  "description": string, "tags": tuple}}          |
        +----------+------------------------------------------------------------------+
        | third    |- the built NWB file of type ``pynwb.file.NWBFile``               |
        |          |- obtained using :py:meth:`.build_nwbfile method`                 |
        +----------+------------------------------------------------------------------+
        | fourth   |- dictionary of NWB time-series object                            |
        |          |- its keys are the keys in                                        |
        |          |``chosenmodel.regions = {"soma": 0.0, "axon", 0.0}``              |
        |          |- the key ``"stimulus"`` is optional                              |
        |          |- value for each key is a ``pynwb.base.TimeSeries`` object,       |
        |          |obtained using :py:meth:`.build_nwbseries method`                 |
        +----------+------------------------------------------------------------------+

        *NOTE:*

        * the whole NWB TimeSeries is not passed here
        * only time series that corresponds to the respective region is passed into this function
        * the epoch metadata has the key ``"source"``. This represents the region from which epoch is considered this should not be confused with any attribute of the NWB file. Besides, since NWB2.0 ``source`` is no longer an attribute of NWB file.

        **Use case:**

        ::

           epochmd = {"epoch0soma": {"source": "soma", "start_time": float, "stop_time": float,
                                     "description": string, "tags": tuple},
                      "epoch1axon": {"source": "soma", "start_time": float, "stop_time": float,
                                     "description": string, "tags": tuple},
                      "epoch0axon": {"source": "axon", "start_time": float, "stop_time": float,
                                     "description": string, "tags": tuple},
                      "epoch1axon": {"source": "axon", "start_time": float, "stop_time": float,
                                     "description": string, "tags": tuple}}
           updated_nwbfile = insert_a_nwbepoch( "epoch0soma", epochmd, nwbfile )

        **Returned Value:** The updated file, say, ``nwbfile`` is returned such that it now has ``.epochs`` attributes. For example,

        ``>> len(nwbfile.epochs)``

        returns ``1`` because we inserted only one epoch. The number will reflect the number of epochs. See `VectorData. <https://pynwb.readthedocs.io/en/latest/pynwb.core.html#pynwb.core.VectorData>`_ Thus ``print(nwbfile.epochs[0])`` returns a tuple such that

        ::

           ( 0,  # => row number, i.e, epoch number in the order of insertion
             0.0,   # => epochmd["epoch0soma"]["start_time"] 
             0.05,  # => epochmd["epoch0soma"]["stop_time"]
             ['1_epoch_responses', '0', 'axon', 'DummyTest', 'cellsepoch0axon'], # => epochmd["epoch0soma"]["tags"]
             [(0, 5,
              DummyTest_axon <class 'pynwb.base.TimeSeries'>
              Fields:
                comments: DummyTest_axon
                conversion: 1000.0
                data: [0.73745691 0.16092811 0.83702311 0.73879371 0.55916576 0.78635451]
                description: whole single array of voltage response from axon of DummyTest
                interval: 1
                num_samples: 6
                resolution: 0.01
                timestamps: [0.   0.01 0.02 0.03 0.04 0.05]
                timestamps_unit: Seconds
                unit: mV
           )])

         *NOTE:*

         * for a particular epoch such tuple has 5-elements
         * pynwb puts all the epochs in a `DynamicTable <https://pynwb.readthedocs.io/en/latest/pynwb.core.html#pynwb.core.DynamicTable>`_ such that

           - a row corresponds to a particular epoch
           - there are 5-columns which corresponds to the 5-elements of an epoch's tuple (as seen above)
           - the first column (seen above as ``0`` NOT ``0.0``) is like the row number or epoch number.
           - the rest have names which by doing ``nwbfile.epochs.colnames`` returns ``('start_time', 'stop_time', 'tags', 'timeseries')``

         * if this function was called again, say, ``updated_nwbfile = insert_a_nwbepoch( "epoch0axon", epochmd, nwbfile )`` then the same ``print(nwbfile.epochs[0])`` (as above) returns the same tuple

        Accessing Data
        --------------

        For all practical purposes we are interested in the created epoch data, in particular the time-series data associated with a particular epoch.

        Root data for any given epoch
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Since the last column of the table (i.e, 5th column) is labelled ``"timeseries"`` doing ``nwbfile.epochs[0][4]`` returns

        ::

           [(0, 5,
             DummyTest_axon <class 'pynwb.base.TimeSeries'>
             Fields:
               comments: DummyTest_axon
               conversion: 1000.0
               data: [0.73745691 0.16092811 0.83702311 0.73879371 0.55916576 0.78635451]
               description: whole single array of voltage response from axon of DummyTest
               interval: 1
               num_samples: 6
               resolution: 0.01
               timestamps: [0.   0.01 0.02 0.03 0.04 0.05]
               timestamps_unit: Seconds
               unit: mV
           )]

        Since this is a list with tuple elements and we are interested in the tuple this can be extracted as ``nwbfile.epochs[0][4][0]``.

        * the first index (i.e, ``[0]``) is the row index thus representing a particular epoch

          - here the index = 0 because there is only one epoch

        * the data (i.e, timeseries) is always index = 4, i.e, 5th column
        * therefore, **data for i'th epoch will be** ``nwbfile.epochs[i][4]``

        ``TimeSeries`` object within the root data
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Since ``nwbfile.epochs.[0][4]`` returns returned a list of tuple elements (above we see a list of only one because only one epoch was inserted), doing ``nwbfile.epochs.[0][4][0]`` returns the tuple containing the NWB ``TimeSeries`` class.

        Doing ``nwbfile.epochs.[0][4][0][2]`` returns the ``TimeSeries`` class

        * the third index corresponds to the row index
        * for i'th epoch, ``nwbfile.epochs[i][4]`` its corresponding tuple containing the ``TimeSeries`` is ``nwbfile.epochs[i][4][0]``
        * the ``TimeSeries`` object is the **3rd column** (index = 2), that is, ``nwbfile.epochs[i][4][0][2]``

        Time-series ``data`` and ``timestamps`` within ``TimeSeries`` object
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Finally to retrieve the time-series ``data`` and ``timestamps`` associated with i'th epoch is achieved by

        ``nwbfile.epochs.[i][4][i][2].timestamps``

        ``nwbfile.epochs.[i][4].[i][2].data``

        Comments on *tables* in NWB
        ---------------------------

        * ``len(nwbfile.epochs) = len(epoch_metadata)``, i.e, the total number of rows and hence the total number of epochs in the created NWB file.

          - ``nwbfile.epochs`` is a `VectorTable <https://pynwb.readthedocs.io/en/latest/pynwb.core.html#pynwb.core.VectorData>`_ whose length is equal to the number of epochs.
          - hence ``len(nwbfile.epochs[0]) = len(nwbfile.epochs[i]) = 1``
          - and each ``print(nwbfile.epochs[i])`` is a tuple as seen in the beginning of the above example

        * the root tuple of any i'th epoch ``nwbfile.epochs[i]`` is always a tuple of **five** elements.

          - ``nwbfile.epochs[i]`` is a `DynamicTable <https://pynwb.readthedocs.io/en/latest/pynwb.core.html#pynwb.core.DynamicTable>`_ with five columns.
          - its fifth element ``nwbfile.epochs[i][4]`` is a list with one tuple

        * the only child tuple of any i'th epoch ``nwbfile.epochs.[i][4][0]`` is always a tuple of **three** elements

          - ``nwbfile.epochs[i][4][0]`` is a `DynamicTable <https://pynwb.readthedocs.io/en/latest/pynwb.core.html#pynwb.core.DynamicTable>`_ with three columns.
          - the third element ``nwbfile.epochs[i][4][0][2]`` within the tuple is the ``TimeSeries`` class

        * (in other words) for any i (over all epochs) ``nwbfile.epochs.[i][4]`` is the same for all the epochs.

          - this is because ``nwbfile.epochs[i][4]`` is a `DynamicTable <https://pynwb.readthedocs.io/en/latest/pynwb.core.html#pynwb.core.DynamicTable>`_

        * recall that ``nwbfile.epochs`` is also a *table* however, they are not the same table types

          - ``nwbfile.epochs`` is a `VectorTable <https://pynwb.readthedocs.io/en/latest/pynwb.core.html#pynwb.core.VectorData>`_ whose length is equal to the number of epochs.
          - ``nwbfile.epochs[i][4]`` is a `DynamicTable <https://pynwb.readthedocs.io/en/latest/pynwb.core.html#pynwb.core.DynamicTable>`_ with five columns.
          - but in both tables its rows correspond to respective epoch
          - therefore, ``nwbfile.epochs[i][4][i]`` **for i'th epoch**

        *Refer:*

         * http://pynwb.readthedocs.io/en/latest/pynwb.epoch.html#pynwb.epoch.Epochs
         * https://github.com/AllenInstitute/nwb-api/blob/master/ainwb/nwb/nwbep.py
         * https://pynwb.readthedocs.io/en/latest/pynwb.core.html#pynwb.core.VectorData
         * https://pynwb.readthedocs.io/en/latest/pynwb.core.html#pynwb.core.DynamicTable

        """
        nwbfile.add_epoch(start_time = epochmd[epoch_i_cellregion]["start_time"],
                          stop_time = epochmd[epoch_i_cellregion]["stop_time"],
                          #timeseries = cls.tseries_for_epoch(epochmd[epoch_i_cellregion],nwbts),
                          timeseries = nwbts,
                          tags = epochmd[epoch_i_cellregion]["tags"] )
        return nwbfile

    @classmethod
    def build_nwbepochs( cls, epochmd=None, nwbfile=None, nwbts=None ):
        """method for contructing epochs into the built nwbfile

        **Keyword Arguments:**

        +-------------+------------------------------------------------------------------+
        | Key         | Value type                                                       |
        +=============+==================================================================+
        | ``epochmd`` |- dictionary of time-series metadata                              |
        |             |- considering the case                                            |
        |             |``chosenmodel.regions = {'soma': 0.0, 'axon': 0.0}`` and the      |
        |             |number of epochs per region = 2                                   |
        |             |- when there is a stimulation the dictionary will be of the form  |
        |             |                                                                  |
        |             |::                                                                |
        |             |                                                                  |
        |             |   {"epoch0soma":                                                 |
        |             |       {"source": "soma", "start_time": float, "stop_time": float,|
        |             |                  "description": string, "tags": tuple}           |
        |             |    "epoch1soma":                                                 |
        |             |       {"source": "soma", "start_time": float, "stop_time": float,|
        |             |                  "description": string, "tags": tuple}           |
        |             |    "epoch0axon":                                                 |
        |             |       {"source": "axon", "start_time": float, "stop_time": float,|
        |             |                  "description": string, "tags": tuple}           |
        |             |    "epoch1axon":                                                 |
        |             |       {"source": "axon", "start_time": float, "stop_time": float,|
        |             |                  "description": string, "tags": tuple}}          |
        |             |                                                                  |
        |             |- but when there is no stimulation the dictionary will look as    |
        |             |                                                                  |
        |             |::                                                                |
        |             |                                                                  |
        |             |   {"epoch0soma":                                                 |
        |             |       {"source": "soma", "start_time": float, "stop_time": float,|
        |             |                  "description": string, "tags": tuple}           |
        |             |    "epoch0axon":                                                 |
        |             |       {"source": "axon", "start_time": float, "stop_time": float,|
        |             |                  "description": string, "tags": tuple}}          |
        +-------------+------------------------------------------------------------------+
        | ``nwbfile`` |- the built NWB file of type ``pynwb.file.NWBFile``               |
        |             |- obtained using :py:meth:`.build_nwbfile method`                 |
        +-------------+------------------------------------------------------------------+
        | ``nwbts``   |- dictionary of NWB time-series object                            |
        |             |- its keys are the keys in                                        |
        |             |``chosenmodel.regions = {"soma": 0.0, "axon", 0.0}``              |
        |             |- the key ``"stimulus"`` is optional                              |
        |             |- value for each key is a ``pynwb.base.TimeSeries`` object,       |
        |             |obtained using :py:meth:`.build_nwbseries method`                 |
        +-------------+------------------------------------------------------------------+

        *NOTE:*

        * the epoch metadata has the key ``"source"``. This represents the region from which epoch is considered this should not be confused with any attribute of the NWB file. Besides, since NWB2.0 ``source`` is no longer an attribute of NWB file.

        **Use case:**

        ::

           epoch_meta_data = {
             "epoch0soma": {
                  "source": "soma",
                  "start_time": 0.0, "stop_time": 5.0,
                  "description": "first epoch",
                  "tags": ('1_epoch_responses', '0', 'soma', 'DummyTest', 'cells', "epoch0soma")},
             "epoch0axon": {
                  "source": "axon",
                  "start_time": 5.0, "stop_time": 10.0,
                  "description": "first epoch",
                  "tags": ('1_epoch_responses', '0', 'axon', 'DummyTest', 'cells', "epoch0axon")}
                  }
           updated_nwbfile = build_nwbepochs(nwbfile=nwbfile, epochmd=epoch_meta_data, nwbts=nwbts)

        **Returned Value:** The updated file, say, ``nwbfile`` is returned such that it now has ``.epochs`` attributes. For example,

        ``>> len(nwbfile.epochs)``

        returns ``2``, reflecting the number of epochs. Thus epoch in first row ``print(nwbfile.epochs[0])`` will appear as

        ::

           [(0, # => epochmd["epoch0soma"]["start_time"] 
             5, # => epochmd["epoch0soma"]["stop_time"]
             DummyTest_soma <class 'pynwb.base.TimeSeries'>
             Fields:
               comments: DummyTest_soma
               conversion: 1000.0
               data: [0.73745691 0.16092811 0.83702311 ... 0.78635451]
               description: whole single array of voltage response from soma of DummyTest
               interval: 1
               num_samples: 501
               resolution: 0.01
               timestamps: [0.   0.01 0.02 ... 5.0]
               timestamps_unit: Seconds
               unit: mV
           )]

        The epoch in second row ``print(nwbfile.epochs[1])`` will return

        ::

           [(5, # => epochmd["epoch0axon"]["start_time"] 
             10, # => epochmd["epoch0axon"]["stop_time"]
             DummyTest_axon <class 'pynwb.base.TimeSeries'>
             Fields:
               comments: DummyTest_axon
               conversion: 1000.0
               data: [0.73745691 0.16092811 0.83702311 ... 0.78635451]
               description: whole single array of voltage response from axon of DummyTest
               interval: 1
               num_samples: 501
               resolution: 0.01
               timestamps: [5.   5.01 5.02 ... 10.0]
               timestamps_unit: Seconds
               unit: mV
           )]

        Accessing Data
        --------------

        For all practical purposes we are interested in the created epoch data, in particular the time-series data associated with a particular epoch. Let us assume our epoch of interest is in the first row of ``nwbfile.epochs``, i.e, ``nwbfile.epochs[0]``.

        Root data for any given epoch
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Since the last column of the table (i.e, 5th column) is labelled ``"timeseries"`` doing ``nwbfile.epochs[0][4]`` returns

        ::

           [(0, # => epochmd["epoch0soma"]["start_time"] 
             5, # => epochmd["epoch0soma"]["stop_time"]
             DummyTest_soma <class 'pynwb.base.TimeSeries'>
             Fields:
               comments: DummyTest_soma
               conversion: 1000.0
               data: [0.73745691 0.16092811 0.83702311 ... 0.78635451]
               description: whole single array of voltage response from soma of DummyTest
               interval: 1
               num_samples: 501
               resolution: 0.01
               timestamps: [0.   0.01 0.02 ... 5.0]
               timestamps_unit: Seconds
               unit: mV
           )]

        * therefore, **root data for i'th epoch will be** ``nwbfile.epochs[i][4]``

        ``TimeSeries`` object within the root data
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Doing ``nwbfile.epochs.[0][4][0][2]`` returns the ``TimeSeries`` class

        ::

           DummyTest_soma <class 'pynwb.base.TimeSeries'>
            Fields:
              comments: DummyTest_soma
              conversion: 1000.0
              data: [0.73745691 0.16092811 0.83702311 ... 0.78635451]
              description: whole single array of voltage response from soma of DummyTest
              interval: 1
              num_samples: 501
              resolution: 0.01
              timestamps: [0.   0.01 0.02 ... 5.0]
              timestamps_unit: Seconds
              unit: mV

        * the ``TimeSeries`` object is the **3rd column** (index = 2), that is, ``nwbfile.epochs[i][4][0][2]``

        Time-series ``data`` and ``timestamps`` within ``TimeSeries`` object
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Finally to retrieve the time-series ``data`` and ``timestamps`` associated with i'th epoch is achieved by

        ``nwbfile.epochs.[i][4][i][2].timestamps``

        ``nwbfile.epochs.[i][4].[i][2].data``

        *Refer:*

         * :py:meth:`.insert_a_nwbepoch` documentation.

        *NOTE:* If we are interested in extracting an epoch in a more organized manner for instance epoch of interest may be a particular epoch for recording done from a particular region, then using the above method of extraction based on picking a row of the `VectorTable <https://pynwb.readthedocs.io/en/latest/pynwb.core.html#pynwb.core.VectorData>`_ is not sufficient. The more improved approach of extraction will be done by the manager.

        """
        for epoch_i_region in epochmd.keys():
            region = epochmd[epoch_i_region]["source"]
            updated_nwbfile = cls.insert_a_nwbepoch( epoch_i_region, epochmd, nwbfile,
                                                      nwbts[region]  )
        return updated_nwbfile

    @classmethod
    def write_nwbfile(cls, nwbfile=None, filepath=None):
        """Writes the created NWB file into a HDF5 file in the given filepath.

        **Keyword Arguments:**

        +--------------+------------------------------------------------------+
        | Key          | Value type                                           |
        +==============+======================================================+
        | ``nwbfile``  |- the built NWB file of type ``pynwb.file.NWBFile``   |
        |              |- obtained using :py:meth:`.build_nwbfile method`     |
        +--------------+------------------------------------------------------+
        | ``filepath`` |string; eg, "/path/to/desired/directory/"             |
        +--------------+------------------------------------------------------+

        **Return value:** The filename of the saved file.

        """
        sesstime = str(nwbfile.session_start_time).replace(" ", "_")[0:-6]
        filename = nwbfile.session_id + "_" + sesstime.replace(":", "-") + ".h5"
        if filepath is None:
            fullname = filename
            io = NWBHDF5IO( fullname, mode='w' )
        else:
            fullname = filepath+os.sep+filename
            io = NWBHDF5IO( fullname, mode='w')
        #print(nwbfile)
        #cls.less(nwbfile, 5)
        #breakpoint()
        io.write(nwbfile)
        #print("debug")
        #breakpoint()
        io.close()
        return fullname
