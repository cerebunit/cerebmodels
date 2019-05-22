# ../managers/managerTranscribe.py

from managers.operatorsTranscribe.metadata_filegenerator import FileGenerator as fg
from managers.operatorsTranscribe.metadata_timeseriesgenerator import TimeseriesGenerator as tg
from managers.operatorsTranscribe.metadata_epochgenerator import EpochGenerator as eg
from managers.operatorsTranscribe.fabricator import Fabricator as fab

from managerFiling import FilingManager as fm

#from pdb import set_trace as breakpoint

class TranscribeManager(object):
    """
    **Available methods:**

    +-------------------------------+-----------------------+
    | Method name                   | Method type           |
    +===============================+=======================+
    | :py:meth:`.load_metadata`     | instance method       | 
    +-------------------------------+-----------------------+
    | :py:meth:`.compile_nwbfile`   | instance method       |
    +-------------------------------+-----------------------+
    | :py:meth:`.save_nwbfile`      | instance method       |
    +-------------------------------+-----------------------+

    *NOTE:* Unlike most managers ``TranscribeManager`` methods are instance method.

    """

    def __init__(self):
        #self.fg = FileGenerator()
        #self.tg = TimeseriesGenerator()
        #self.eg = EpochGenerator()
        #self.fab = Fabricator()
        #self.fm = FilingManager()
        pass

    def load_metadata(self, chosenmodel=None, simtime=None, recordings=None,
                      runtimeparameters=None, stimparameters=None, vtest=None,
                      username=None, labname=None, institutename=None):
        """Directs :ref:`FileGenerator` (``.forfile``) to create a meta-data for the file followed by :ref:`TimeseriesGenerator` (``.forrecording``) for generating the meta-data for the recordings. Finally, the :ref:`EpochGenerator` (``.forepoch``) generates the meta-data for the epoch/s.

        **Keyword Arguments:*

        +-----------------------------+---------------------------------------------------------------+
        | Key                         | Value type                                                    |
        +=============================+===============================================================+
        |``chosenmodel``              | instantiated model                                            |
        +-----------------------------+---------------------------------------------------------------+
        |``simtime``                  | datetime.datetime when simulation started                     |
        +-----------------------------+---------------------------------------------------------------+
        |``recordings``               | - dictionary with keys: ``"time"``, ``"response"`` and        |
        |                             |                                            ``"stimulus"``     |
        |                             | - Eg: {"time": array, "response": {cellregion_a: array,       |
        |                             |                                     cellregion_b: array},     |
        |                             |        "stimulus": str("Model is not stimulated") or array}   |
        +-----------------------------+---------------------------------------------------------------+
        |``runtimeparameters``        | - dictionary with keys ``"dt"``, ``"celsius"``, ``"tstop"``   |
        |                             |                                            and ``"v_init"``   |
        |                             | - Eg: {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65} |
        +-----------------------------+---------------------------------------------------------------+
        |``stimparameters`` (optional)| - dictionary with keys ``"type"``, ``"stimlist"`` and         |
        |                             |                                                 ``"tstop"``   |
        |                             | - value for ``"type"`` is a two element list of strings of    |
        |                             |the form <stimulus category> <specific type of that category>  |
        |                             | - the first element is ALWAYS ``<stimulus category>``         |
        |                             | -  Eg: current inject on a cell ``["current", "IClamp"]``     |
        |                             | - value for ``"stimlist"`` is list with elements as dictionary|
        |                             |of the form [ {}, {}, ... ]                                    |
        |                             | - Eg1: [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},           |
        |                             |          {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]     |
        |                             | - Eg2: [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0,   |
        |                             |                                                 "delay": 5.0},|
        |                             |          {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0,   |
        |                             |                                                "delay": 10.0},|
        |                             |          {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0,   |
        |                             |                                                "delay": 15.0},|
        |                             |          {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0,   |
        |                             |                                                "delay": 20.0}]|
        |                             | - value for ``"tstop"`` is a number, time for generating the  |
        |                             |last epoch. Therefore, ``"tstop": parameters["tstop"]``.       |
        +-----------------------------+---------------------------------------------------------------+
        |``vtest`` (optional)         | instantiated validation ``CerebUnit`` test                    |
        +-----------------------------+---------------------------------------------------------------+
        |``username`` (optional)      | string                                                        |
        +-----------------------------+---------------------------------------------------------------+
        |``labname`` (optional)       | string                                                        |
        +-----------------------------+---------------------------------------------------------------+
        |``institutename`` (optional) | string                                                        |
        +-----------------------------+---------------------------------------------------------------+

        **Returned Values:** There are no values returned per se but four attributes are assigned

        * ``self.chosenmodel``, whose value is the instantiated model
        * ``self.filemd``, whose value is the meta-data created by :ref:`FileGenerator` (``.forfile``)
        * ``self.respmd``, whose value is the meta-data created by :ref:`TimeseriesGenerator` (``.forrecording``)
        * ``self.epochmd``, whose value is the meta-data created by :ref:`EpochGenerator` (``.forepoch``)

        *NOTE:*

        * the above assignment of attributes is the major reason why ``TranscribeManager`` methods are instance methods
        * for more on arguments: ``vtest``, ``username``, ``labname`` and ``insitutename`` see `.forfile` in :ref:`FileGenerator`
        * for more on argument ``stimparameters`` see `.forrecording` in :ref:`TimeseriesGenerator`

        """
        self.chosenmodel = chosenmodel
        self.filemd = fg.forfile( chosenmodel = self.chosenmodel,
                                  simtime = simtime,
                                  vtest = vtest,
                                  username = username,
                                  labname = labname,
                                  institutename = institutename )
        self.respmd = tg.forrecording( chosenmodel = self.chosenmodel,
                                       recordings = recordings,
                                       runtimeparameters = runtimeparameters,
                                       stimparameters = stimparameters )
        if stimparameters is None:
            self.epochmd = eg.forepoch( chosenmodel = self.chosenmodel,
                                        parameters = runtimeparameters )
        else:
            self.epochmd = eg.forepoch( chosenmodel = self.chosenmodel,
                                        parameters = stimparameters )

    def compile_nwbfile(self):
        """**After** evoking :py:meth:`.load_metadata`, calling this function results in the creation of the `NWBFile <https://nwb-schema.readthedocs.io/en/latest/format.html#nwbfile>`_. This is done by directing the :ref:`Fabricator`.

        **Arguments:** No argument is passed but it is imperative that :py:meth:`.load_metadata` is called first. The four attributes ``self.chosenmodel``, ``self.filemd``, ``self.respmd`` and ``self.epochmd`` are essential for this function.

        **Returned Values:** There are no values returned but one attribute ``self.nwbfile`` is assigned. Its value is the created `NWBFile <https://nwb-schema.readthedocs.io/en/latest/format.html#nwbfile>`_.


        """
        nwbfile = fab.build_nwbfile(self.filemd)
        nwbts = fab.build_nwbseries(chosenmodel = self.chosenmodel,
                                    tsmd = self.respmd)
        update_nwbfile = fab.affix_nwbseries_to_nwbfile(nwbts=nwbts,
                                                        nwbfile=nwbfile)
        self.nwbfile = fab.build_nwbepochs( nwbfile = update_nwbfile,
                                            epochmd = self.epochmd,
                                            nwbts = nwbts )

    def save_nwbfile(self):
        """**After** evoking :py:meth:`.compile_nwbfile`, calling this function writes the created ``self.nwbfile`` into an HDF5 file.

        **Arguments:** No argument is passed but it is imperative that :py:meth:`.load_metadata` is called first followd by :py:meth:`.compile_nwbfile`. The attributes ``self.chosenmodel`` and ``self.nwbfile`` are essential for this function.

        **Returned Values:** The fullname (string; filepath with filename) is returned.

        *NOTE:* The returned fullname is useful for loading this particular file.

        """
        #path = self.fm.responsepath_check_create(list_dir_names=
        #            ['responses', self.chosenmodel.modelscale, self.chosenmodel.modelname])
        path = fm.responsepath_check_create(chosenmodel = self.chosenmodel)
        return fab.write_nwbfile(nwbfile = self.nwbfile, filepath = path) #fullname (w/ filepath)
