# ../managers/managerTranscribe.py

from managers.operatorsTranscribe.metadata_filegenerator import FileGenerator
from managers.operatorsTranscribe.metadata_timeseriesgenerator import TimeseriesGenerator
from managers.operatorsTranscribe.metadata_epochgenerator import EpochGenerator
from managers.operatorsTranscribe.fabricator import Fabricator

from managerFiling import FilingManager

class TranscribeManager(object):

    def __init__(self):
        self.fg = FileGenerator()
        self.tg = TimeseriesGenerator()
        self.eg = EpochGenerator()
        self.fab = Fabricator()
        self.fm = FilingManager()

    def load_metadata(self, chosenmodel=None, recordings=None,
                      runtimeparameters=None, stimparameters=None, vtest=None,
                      username=None, labname=None, institutename=None):
        self.chosenmodel = chosenmodel
        self.filemd = self.fg.forfile( chosenmodel = self.chosenmodel,
                                       vtest = vtest,
                                       username = username,
                                       labname = labname,
                                       institutename = institutename )
        self.respmd = self.tg.forrecording( chosenmodel = self.chosenmodel,
                                            recordings = recordings,
                                            runtimeparameters = runtimeparameters,
                                            stimparameters = stimparameters )
        if stimparameters is None:
            self.epochmd = self.eg.forepoch( chosenmodel = self.chosenmodel,
                                             parameters = runtimeparameters )
        else:
            self.epochmd = self.eg.forepoch( chosenmodel = self.chosenmodel,
                                             parameters = stimparameters )

    def compile_nwbfile(self):
        nwbfile = self.fab.build_nwbfile(self.filemd)
        nwbts = self.fab.build_nwbseries(chosenmodel = self.chosenmodel,
                                         tsmd = self.respmd)
        update_nwbfile = self.fab.affix_nwbseries_to_nwbfile(nwbts=nwbts,
                                                             nwbfile=nwbfile)
        self.nwbfile = self.fab.build_nwbepochs( nwbfile = update_nwbfile,
                                                 epochmd = self.epochmd,
                                                 nwbts = nwbts )

    def save_nwbfile(self):
        #path = self.fm.responsepath_check_create(list_dir_names=
        #            ['responses', self.chosenmodel.modelscale, self.chosenmodel.modelname])
        path = self.fm.responsepath_check_create(chosenmodel = self.chosenmodel)
        self.fab.write_nwbfile(nwbfile = self.nwbfile, filepath = path)
