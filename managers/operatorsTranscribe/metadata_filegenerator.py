# ~/managers/operatorsTranscribe/metadata_filegenerator.py
import platform
import uuid
import time
from datetime import datetime
from dateutil.tz import tzlocal

class FileGenerator(object):
    """
    **Available Methods:**

    +---------------------------------+----------------------------------+
    | Method name                     | Method type                      |
    +=================================+==================================+
    | :py:meth:`.forfile`             | class method                     |
    +---------------------------------+----------------------------------+
    | :py:meth:`.get_modelID`         | static method                    |
    +---------------------------------+----------------------------------+
    | :py:meth:`.get_username`        | static method                    |
    +---------------------------------+----------------------------------+
    | :py:meth:`.get_testdescription` | static method                    |
    +---------------------------------+----------------------------------+
    | :py:meth:`.get_labelname`       | static method                    |
    +---------------------------------+----------------------------------+
    | :py:meth:`.get_institution`     | static method                    |
    +---------------------------------+----------------------------------+

    """

    @staticmethod
    def get_modelID(model):
        """Try extracting the ``uuid`` attribute value of the model and return it or return ``"no_model_uuid"``.

        **Argument:** The instantiated model is passed into this function.

        """
        try:
            uuid_value = getattr(model, 'uuid')
            return uuid_value[:8]+"_"+uuid_value[-12:]
        except:
            return "no_model_uuid"

    @staticmethod
    def get_username(username):
        """Returns the username (also argument passed as a string) or returns "anonymous" if argument is ``None``.

        """
        if username is None:
            return "anonymous"
        else:
            return username

    @staticmethod
    def get_testdescription(test):
        """Returns the string "raw simulation without running any CerebUnit test" if the argument is ``None`` otherwise it returns the attribute ``.description`` of the argument.

        *Note:* The argument should be the test metadata.

        """
        if test is None:
            return "raw simulation without running any CerebUnit test"
        else:
            return test.description

    @staticmethod
    def get_labname(labname):
        """Returns the string "no lab name was provided" if the argument is ``None`` otherwise it returns the attribute the argument (a string) itself.

        *Note:* The argument should be the name of the laboratory.

        """
        if labname is None:
            return platform.platform()
        else:
            return labname

    @staticmethod
    def get_institution(instname):
        """Returns the string "no institution was provided" if the argument is ``None`` otherwise it returns the attribute the argument (a string) itself.

        *Note:* The argument should be the name of the institute.

        """
        if instname is None:
            return "no institution was provided"
        else:
            return instname

    @classmethod
    def forfile( cls, chosenmodel=None, simtime=None, vtest=None,
                 username=None, labname=None, institutename=None ):
        """Creates the `NWB <https://www.nwb.org/>`_ formatted metadata for an intended file to be saved.

        **Keyword Arguments:**

        +------------------------------+--------------------------------------------+
        | Key                          | Value type                                 |
        +==============================+============================================+
        | ``chosenmodel``              | instantiated model                         |
        +------------------------------+--------------------------------------------+
        | ``simtime``                  | datetime.datetime when simulation started  |
        +------------------------------+--------------------------------------------+
        | ``vtest`` (optional)         | instantiated validation ``CerebUnit`` test |
        +------------------------------+--------------------------------------------+
        | ``username`` (optional)      | string                                     |
        +------------------------------+--------------------------------------------+
        | ``labname`` (optional)       | string                                     |
        +------------------------------+--------------------------------------------+
        | ``institutename`` (optional) | string                                     |
        +------------------------------+--------------------------------------------+

        **Returned value:** It is a dictionary of the form

        .. code-block:: python

           { "session_description":    string;
             "identifier":             string,
             "session_start_time":     datetime,
             "experimenter":           string,
             "experiment_description": string,
             "session_id":             string,
             "lab":                    string,
             "institution":            string }

        *NOTE:*

        * ``vtest`` is not given for raw stimulation of the chosenmodel
        * http://pynwb.readthedocs.io/en/latest/pynwb.file.html#pynwb.file.NWBFile

        **Use case:**

        ``>> fg = FileGenerator()``

        ``>> model = Xyz()``

        For simulation without validation test

        ``>> filemd = fg.forfile(chosenmodel = model)``

        For simulation with validation test

        ``>> vtest = SomeTest()``

        ``>> filemd = fg.forfile(chosenmodel=model, simtime=datetime.datetime.now(), test=vtest, username='john', labname='hbp brain sim lab', institute='CNRS-UNIC')``

        """

        if chosenmodel is None and simtime is None:
            raise ValueError("passing an instantiated chosenmodel and datetime is mandatory")
        else:
            return {
              #'source': platform.platform(), #string. No longer part of NWB2.0
              # Required
              'session_description': "simulation of " + chosenmodel.modelname,
              'identifier': cls.get_modelID(chosenmodel), #string
              'session_start_time': datetime(simtime.year, simtime.month, simtime.day,
                                             simtime.hour, simtime.minute, simtime.second,
                                             simtime.microsecond, tzinfo=tzlocal()),
              #'session_start_time': time.asctime(time.gmtime(time.time()))+' '+time.tzname[0],
              # Optional
              'experimenter': cls.get_username(username), #string
              'experiment_description': cls.get_testdescription(vtest), #string
              'session_id': str(hash(str(uuid.uuid1()))).replace('-',''), # remove any minus
              'lab': cls.get_labname(labname), #string
              'institution': cls.get_institution(institutename) }
