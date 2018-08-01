# ~/managers/operatorsTranscribe/metadata_filegenerator.py
import platform
import uuid
import time

class FileGenerator(object):
    """Operators working under TranscribeManager

    Available methods:
    forfile
    """

    @staticmethod
    def get_modelID(model):
        try:
            uuid_value = getattr(model, 'uuid')
            return uuid_value[:8]+"_"+uuid_value[-12:]
        except:
            return "no_model_uuid"

    @staticmethod
    def get_username(username):
        if username is None:
            return "anonymous"
        else:
            return username

    @staticmethod
    def get_testdescription(test):
        if test is None:
            return "raw simulation without running any CerebUnit test"
        else:
            return test.description

    @staticmethod
    def get_labname(labname):
        if labname is None:
            return "no lab name was provided"
        else:
            return labname

    @staticmethod
    def get_institution(instname):
        if instname is None:
            return "no institution was provided"
        else:
            return instname

    def forfile( self, chosenmodel=None, vtest=None, username=None,
                 labname=None, institutename=None ):
        """method that creates the NWB formatted metadata forfile.

        Keyword arguments (mandatory):
        chosenmodel -- instantiated model

        Keyword arguments (optional):
        vtest -- instantiated validation CerebUnit test
        username -- string
        labname -- string
        institutename -- string

        Returned value:
        dictionary -- {'source':  string,
                       'session_description': string;
                       'identifier': string,
                       'session_start_time': string,
                       'experimenter': string,
                       'experiment_description': string,
                       'session_id': string,
                       'lab': string,
                       'institution': string}
        NOTE:
            - vtest is not given for raw stimulation of the chosenmodel
            - http://pynwb.readthedocs.io/en/latest/pynwb.file.html#pynwb.file.NWBFile

        Use case:
        fg = FileGenerator()
        model = Xyz()
        For simulation without validation test
        filemd = fg.forfile(chosenmodel = model)
        Simulation with validation test
        vtest = Pqr()
        filemd = fg.forfile(chosenmodel=model, test=vtest, username='john',
                            labname='hbp brain sim lab', institute='CNRS-UNIC')
        """

        if chosenmodel is None:
            raise ValueError("passing an instantiated chosenmodel is mandatory")
        else:
            return {
              'source': platform.platform(), #string
              'session_description': "simulation of " + chosenmodel.modelname,
              'identifier': self.get_modelID(chosenmodel), #string
              'session_start_time': time.asctime(time.gmtime(time.time()))+' '+time.tzname[0],
              'experimenter': self.get_username(username), #string
              'experiment_description': self.get_testdescription(vtest), #string
              'session_id': str(hash(str(uuid.uuid1()))).replace('-',''), # remove any minus
              'lab': self.get_labname(labname), #string
              'institution': self.get_institution(institutename) }
