# ../managers/managerTranscribe.py

from managers.operatorsTranscribe.metadata_filegenerator import FileGenerator as fg
from managers.operatorsTranscribe.metadata_timeseriesgenerator import TimeseriesGenerator as tg
from managers.operatorsTranscribe.metadata_epochgenerator import EpochGenerator as eg
from managers.operatorsTranscribe.fabricator import Fabricator as fab

from managerFiling import FilingManager as fm

class TranscribeManager(object):

    def __init__(self):
        #self.fg = FileGenerator()
        #self.tg = TimeseriesGenerator()
        #self.eg = EpochGenerator()
        #self.fab = Fabricator()
        #self.fm = FilingManager()
        pass

    def load_metadata(self, chosenmodel=None, recordings=None,
                      runtimeparameters=None, stimparameters=None, vtest=None,
                      username=None, labname=None, institutename=None):
        self.chosenmodel = chosenmodel
        self.filemd = fg.forfile( chosenmodel = self.chosenmodel,
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
        nwbfile = fab.build_nwbfile(self.filemd)
        nwbts = fab.build_nwbseries(chosenmodel = self.chosenmodel,
                                    tsmd = self.respmd)
        update_nwbfile = fab.affix_nwbseries_to_nwbfile(nwbts=nwbts,
                                                        nwbfile=nwbfile)
        self.nwbfile = fab.build_nwbepochs( nwbfile = update_nwbfile,
                                            epochmd = self.epochmd,
                                            nwbts = nwbts )

    def save_nwbfile(self):
        #path = self.fm.responsepath_check_create(list_dir_names=
        #            ['responses', self.chosenmodel.modelscale, self.chosenmodel.modelname])
        path = fm.responsepath_check_create(chosenmodel = self.chosenmodel)
        fab.write_nwbfile(nwbfile = self.nwbfile, filepath = path)
