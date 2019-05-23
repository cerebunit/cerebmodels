# ~/managers/operatorsTranscribe/metadata_timeseriesgenerator.py
#import numpy.core.defchararray as npd

class TimeseriesGenerator(object):
    """
    **Available Methods:**

    +---------------------------------------------+-------------------------+
    | Method name                                 | Method type             |
    +=============================================+=========================+
    | :py:meth:`.forrecording`                    | class method            |
    +---------------------------------------------+-------------------------+
    | :py:meth:`.recordings_cellstimulus`         | class method            |
    +---------------------------------------------+-------------------------+
    | :py:meth:`.forcellrecordings_nostimulus`    | class method            |
    +---------------------------------------------+-------------------------+
    | :py:meth:`.forcellrecordings_stimulus`      | class method            |
    +---------------------------------------------+-------------------------+
    | :py:meth:`.forcellrecording`                | class method            |
    +---------------------------------------------+-------------------------+
    | :py:meth:`.forrecording`                    | class method            |
    +---------------------------------------------+-------------------------+
    | :py:meth:`.cellrecordings_response`         | static method           |
    +---------------------------------------------+-------------------------+
    | :py:meth:`.recordings_cell_currentstimulus` | static method           |
    +---------------------------------------------+-------------------------+

    """
    @staticmethod
    def cellrecordings_response(model, cellregion, rec_t, specific_rec_i, rec_v, parameters):
        """Creates a generic time-series (response) metadata for cells. This method is called by :py:meth:`.forcellrecordings_nostimulus` and :py:meth:`.forcellrecordings_stimulus`.

        **Arguments:**

        +---------------+------------------------------------------------------------+
        | Arguments     | Value type                                                 |
        +===============+============================================================+
        | first         | instantiated model                                         |
        +---------------+------------------------------------------------------------+
        | second        | string for cellregion; "soma", "axon", etc ...             |
        +---------------+------------------------------------------------------------+
        | third         | array; eg: recordings["time"] = rec_t                      |
        +---------------+------------------------------------------------------------+
        | fourth        | array; eg: recordings["response"][cellregion] = rec_v      |
        +---------------+------------------------------------------------------------+
        | fifth         | - string "not stimulated" or                               |
        |               | - array; eg: recordings["stimulus"] = rec_i                |
        +---------------+------------------------------------------------------------+
        | sixth         | - dictionary for runtime parameters                        |
        |               | - keys: ``"dt"``, ``"celsius"``, ``"tstop"``, ``"v_init"`` |
        +---------------+------------------------------------------------------------+

        **Returned value:** Is is a dictionary of the form

        ::

           { "name":         string,
             "data":         array,
             "unit":         string,
             "resolution":   float,
             "conversion":   float,
             "timestamps":   array,
             "comments":      string,
             "description":  string }

        *NOTE:*

        * ``recordings["stimulus"] = ``"Model is not stimulated"`` ``!= specific_rec_i``
        * but ``recordings["stimulus"]`` = ``array`` = ``specific_rec_i``

        """
        if (type(specific_rec_i) is str) and (specific_rec_i=="not stimulated"):
            comments = "voltage response without stimulation"
        else:
            comments = "voltage response with stimulation"

        return {"name": model.modelname+"_"+cellregion, # "source": cellregion, # No longer NWB2.0
                "data": rec_v, "unit": "mV", "resolution": float(parameters["dt"]),
                "conversion": 1000.0, #1000=>1ms
                "timestamps": rec_t, #"starting_time": 0.0,
                #"rate": 1/parameters["dt"], # NWB suggests using Hz but frequency != rate
                "comments": comments,
                "description": "whole single array of voltage response from "+cellregion+" of "+ model.modelname}

    @staticmethod
    def recordings_cell_currentstimulus(model, rec_t, rec_i, parameters, stimparameters):
        """Creates a time-series (response) metadata for stimulated cells. This method is called by :py:meth`.recordings_cellstimulus`.

        **Arguments:**

        +-------------+------------------------------------------------------------------+
        | Argument    | Value type                                                       |
        +=============+==================================================================+
        | first       | instantiated model                                               |
        +-------------+------------------------------------------------------------------+
        | second      | array; eg: recordings["time"] = rec_t                            |
        +-------------+------------------------------------------------------------------+
        | third       | array; eg: recordings["stimulus"] = rec_i                        |
        +-------------+------------------------------------------------------------------+
        | fourth      | - dictionary for runtime parameters                              |
        |             | - keys ``"dt"``, ``"celsius"``, ``"tstop"``, ``"v_init"``        |
        +-------------+------------------------------------------------------------------+
        | fifth       | - dictionary for stimulation parameters                          |
        |             | - keys ``"type"``, ``"stimlist"`` and ``"tstop"``                |
        |             | - value for ``"type"`` is a two element list of strings of       |
        |             |the form <stimulus category> <specific type of that category>     |
        |             | - the first element is ALWAYS ``<stimulus category>``            |
        |             | -  Eg: current inject on a cell ``["current", "IClamp"]``        |
        |             | - value for ``"stimlist"`` is a list with elements as dictionary |
        |             |of the form [ {}, {}, ... ]                                       |
        |             | - Eg1: [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},              |
        |             |          {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]        |
        |             | - Eg2: [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0,      |
        |             |                                                 "delay": 5.0},   |
        |             |          {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0,      |
        |             |                                                 "delay": 10.0},  |
        |             |          {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0,      |
        |             |                                                 "delay": 15.0},  |
        |             |          {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0,      |
        |             |                                                 "delay": 20.0} ] |
        |             | - value for ``"tstop"`` is a number, time for generating the last|
        |             |epoch. Therefore, ``"tstop": parameters["tstop"]``.               |
        +-------------+------------------------------------------------------------------+

        **Returned value:** Is is a dictionary of the form

        ::

           { "name":         string,
             "data":         array,
             "unit":         string,
             "resolution":   float,
             "conversion":   float,
             "timestamps":   array,
             "comments":      string,
             "description":  string }

        *NOTE:*

        * prior to calling this method weed out recordings["stimulus"]="Model is not stimulated"
        * this method only accepts arrays

        """
        
        return {"name": model.modelname+"_stimulus",
                #"source": stimparameters["type"][1], # No longer used in NWB2.0
                "data": rec_i, "unit": "nA",
                "resolution": float(parameters["dt"]), "conversion": 1000.0, #1000=>1ms
                "timestamps": rec_t, #"starting_time": 0.0,
                #"rate": 1/parameters["dt"], # NWB suggests using Hz but frequency != rate
                "comments": "current injection, "+stimparameters["type"][1],
                "description": "whole single array of stimulus"}

    @classmethod
    def recordings_cellstimulus(cls, model, rec_t, rec_i, parameters, stimparameters):
        """Creates a time-series (response) metadata for stimulated cells. This method is called by :py:meth:`.forcellrecordings_stimulus`.

        **Arguments:**

        +-------------+------------------------------------------------------------------+
        | Argument    | Value type                                                       |
        +=============+==================================================================+
        | first       | instantiated model                                               |
        +-------------+------------------------------------------------------------------+
        | second      | array; eg: recordings["time"] = rec_t                            |
        +-------------+------------------------------------------------------------------+
        | third       | array; eg: recordings["stimulus"] = rec_i                        |
        +-------------+------------------------------------------------------------------+
        | fourth      | - dictionary for runtime parameters                              |
        |             | - keys ``"dt"``, ``"celsius"``, ``"tstop"``, ``"v_init"``        |
        |             | - Eg: {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}    |
        +-------------+------------------------------------------------------------------+
        | fifth       | - dictionary for stimulation parameters                          |
        |             | - keys ``"type"``, ``"stimlist"`` and ``"tstop"``                |
        |             | - value for ``"type"`` is a two element list of strings of       |
        |             |the form <stimulus category> <specific type of that category>     |
        |             | - the first element is ALWAYS ``<stimulus category>``            |
        |             | -  Eg: current inject on a cell ``["current", "IClamp"]``        |
        |             | - value for ``"stimlist"`` is a list with elements as dictionary |
        |             |of the form [ {}, {}, ... ]                                       |
        |             | - Eg1: [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},              |
        |             |          {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]        |
        |             | - Eg2: [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0,      |
        |             |                                                 "delay": 5.0},   |
        |             |          {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0,      |
        |             |                                                 "delay": 10.0},  |
        |             |          {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0,      |
        |             |                                                 "delay": 15.0},  |
        |             |          {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0,      |
        |             |                                                 "delay": 20.0} ] |
        |             | - value for ``"tstop"`` is a number, time for generating the last|
        |             |epoch. Therefore, ``"tstop": parameters["tstop"]``.               |
        +-------------+------------------------------------------------------------------+

        **Returned value:** See :py:meth:`.recordings_cell_currentstimulus`.

        *NOTE:*
        
        * this function is meant for generic stimulation of a cell
        * present release only supports current injection so this function may appear to be exactly the same as :py:meth:`.recordings_cell_currentstimulus`.

        """
        if stimparameters["type"][0]=="current":
            return cls.recordings_cell_currentstimulus(model, rec_t, rec_i,
                                                  parameters, stimparameters)

    @classmethod
    def forcellrecordings_nostimulus(cls, chosenmodel, recordings, runtimeparameters):
        """Creates time-series metadata for unstimulated cells. This method calls :py:meth:`.cellrecordings_response`. However this method is called by :py:meth:`.forcellrecording`.

        **Arguments:**

        +---------------+---------------------------------------------------------------+
        | Argument      | Value type                                                    |
        +===============+===============================================================+
        | first         | instantiated model                                            |
        +---------------+---------------------------------------------------------------+
        | second        | - dictionary of the recordings                                |
        |               | - keys: ``"time"``, ``"response"`` and ``"stimulus"``         |
        |               | - Eg: {"time": array, "response": {cellregion_a: array,       |
        |               |                                    cellregion_b: array},      |
        |               |        "stimulus": str("Model is not stimulated") or array}   |
        +---------------+---------------------------------------------------------------+
        | third         | - dictionary of the run-time parameters                       |
        |               | - keys: ``"dt"``, ``"celsius"``, ``"tstop"``, ``"v_init"``    |
        |               | - Eg: {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65} |
        +---------------+---------------------------------------------------------------+

        **Returned value:** Dictionary whose elements themselves are dictionaries. The length of the root dictionary is equal to the number of cell regions, say, a soma and an axon. The keys of the parent dictionary are the cell region names. Their respective values are themselves dictionaries, see :py:meth:`.cellrecordings_response`.

        """
        specific_rec_i = "not stimulated"
        y = {}
        for cellregion in chosenmodel.regions.keys():
            y.update( {cellregion:
                       cls.cellrecordings_response(
                                            chosenmodel, cellregion,
                                            recordings["time"], specific_rec_i,
                                            recordings["response"][cellregion],
                                            runtimeparameters )} )
        return y

    @classmethod
    def forcellrecordings_stimulus(cls, chosenmodel, recordings,
                                   runtimeparameters, stimparameters):
        """Creates time-series metadata for stimulated cells. This method calls :py:meth:`.cellrecordings_response` and also :py:meth:`.recordings_cellstimulus`. However this method is called by :py:meth:`.forcellrecording`.

        **Arguments:**

        +-------------+------------------------------------------------------------------+
        | Argument    | Value type                                                       |
        +=============+==================================================================+
        | first       | instantiated model                                               |
        +-------------+------------------------------------------------------------------+
        | second      | - dictionary of the recordings                                   |
        |             | - keys: ``"time"``, ``"response"`` and ``"stimulus"``            |
        |             | - Eg: {"time": array, "response": {cellregion_a: array,          |
        |             |                                    cellregion_b: array},         |
        |             |        "stimulus": str("Model is not stimulated") or array}      |
        +-------------+------------------------------------------------------------------+
        | third       | - dictionary of the run-time parameters                          |
        |             | - keys: ``"dt"``, ``"celsius"``, ``"tstop"``, ``"v_init"``       |
        |             | - Eg: {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}    |
        +-------------+------------------------------------------------------------------+
        | fifth       | - dictionary for stimulation parameters                          |
        |             | - keys ``"type"``, ``"stimlist"`` and ``"tstop"``                |
        |             | - value for ``"type"`` is a two element list of strings of       |
        |             |the form <stimulus category> <specific type of that category>     |
        |             | - the first element is ALWAYS ``<stimulus category>``            |
        |             | -  Eg: current inject on a cell ``["current", "IClamp"]``        |
        |             | - value for ``"stimlist"`` is a list with elements as dictionary |
        |             |of the form [ {}, {}, ... ]                                       |
        |             | - Eg1: [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},              |
        |             |          {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]        |
        |             | - Eg2: [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0,      |
        |             |                                                 "delay": 5.0},   |
        |             |          {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0,      |
        |             |                                                 "delay": 10.0},  |
        |             |          {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0,      |
        |             |                                                 "delay": 15.0},  |
        |             |          {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0,      |
        |             |                                                 "delay": 20.0} ] |
        |             | - value for ``"tstop"`` is a number, time for generating the last|
        |             |epoch. Therefore, ``"tstop": parameters["tstop"]``.               |
        +-------------+------------------------------------------------------------------+

        **Returned value:** Dictionary whose elements themselves are dictionaries. The length of the root dictionary is equal to 1 + the number of cell regions, say, a soma and an axon. The keys of the parent dictionary are "stimulus" plus the cell region names. Their respective values are themselves dictionaries, see :py:meth:`.recordings_cellstimulus` for "stimulus" key value and see :py:meth:`.cellrecordings_response` for the cell regions key values.

        """
        y = {}
        y.update( {"stimulus":
                   cls.recordings_cellstimulus(
                                            chosenmodel,
                                            recordings["time"],
                                            recordings["stimulus"],
                                            runtimeparameters, stimparameters )} )
        for cellregion in chosenmodel.regions.keys():
            y.update( {cellregion:
                       cls.cellrecordings_response(
                                            chosenmodel, cellregion,
                                            recordings["time"], recordings["stimulus"],
                                            recordings["response"][cellregion],
                                            runtimeparameters )} )
        return y

    @classmethod
    def forcellrecording( cls, chosenmodel=None, recordings=None,
                          runtimeparameters=None, stimparameters=None ):
        """Creates the `NWB <https://www.nwb.org/>`_ formatted time-series metadata for cells. This is normally not called by the :ref:`TranscribeManager`, instead it is called by :py:meth:`.forrecording`.

        **Keyword Arguments:**

        +---------------------+----------------------------------------------------------------+
        | Key                 | Value type                                                     |
        +=====================+================================================================+
        |``chosenmodel``      | instantiated model                                             |
        +---------------------+----------------------------------------------------------------+
        |``recordings``       | - dictionary with keys: ``"time"``, ``"response"`` and         |
        |                     |                                             ``"stimulus"``     |
        |                     | - Eg: {"time": array, "response": {cellregion_a: array,        |
        |                     |                                      cellregion_b: array},     |
        |                     |       "stimulus": str("Model is not stimulated") or array}     |
        +---------------------+----------------------------------------------------------------+
        |``runtimeparameters``| - dictionary with keys ``"dt"``, ``"celsius"``, ``"tstop"`` and|
        |                     |                                                   ``"v_init"`` |
        |                     | - - Eg: {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}|
        +---------------------+----------------------------------------------------------------+
        |``stimparameters``   | - dictionary with keys ``"type"``, ``"stimlist"`` and          |
        |                     |                                                ``"tstop"``     |
        |                     | - value for ``"type"`` is a two element list of strings of     |
        |                     |the form <stimulus category> <specific type of that category>   |
        |                     | - the first element is ALWAYS ``<stimulus category>``          |
        |                     | -  Eg: current inject on a cell ``["current", "IClamp"]``      |
        |                     | - value for ``"stimlist"`` is list with elements as dictionary |
        |                     |of the form [ {}, {}, ... ]                                     |
        |                     | - Eg1: [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},            |
        |                     |          {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]      |
        |                     | - Eg2: [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0,    |
        |                     |                                                 "delay": 5.0}, |
        |                     |          {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0,    |
        |                     |                                                 "delay": 10.0},|
        |                     |          {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0,    |
        |                     |                                                 "delay": 15.0},|
        |                     |          {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0,    |
        |                     |                                                 "delay": 20.0}]|
        |                     | - value for ``"tstop"`` is a number, time for generating the   |
        |                     |last epoch. Therefore, ``"tstop": parameters["tstop"]``.        |
        +---------------------+----------------------------------------------------------------+

        **Returned value:** Dictionary whose elements themselves are dictionaries. If there was not stimulus the length of the root dictionary is qual tot he number of cell regions, say, a soma and a dendrite. Their key values are themselves dictionaries, see :py:meth:`.forcellrecordings_nostimulus`. On the other hand if there was a stimulus the length of the root dictionary is equal to 1 + the number of cell regions, say, a soma and an axon. Their key values are also dictionaries, see :py:meth:`.forcellrecordings_stimulus`.

        **Use case:**

        ``>> tg = TimeseriesGenerator()``

        Get the model

        ``>> from models.cells.modelDummyTest import DummyCell``

        ``>> model = DummyCell()``

        ``>> runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}``

        Generate model response

        ``>> rec_t = [ t*runtimeparam["dt"] for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]``

        ``>> rec_i = numpy.random.rand(1,len(rec_t))[0] # stimulus``

        ``>> rec_v = numpy.random.rand(2,len(rec_t))    # response``

        This model has, ``model.regions = {'soma':0.0, 'axon':0.0}``

        For simulation without stimulation

        ``>> recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]}, "stimulus": "Model is not stimulated"}``

        ``>> respmd = tg.forcellrecording(chosenmodel = model, recordings = recordings, parameters = runtimeparam)``

        For simulation with stimulation

        ``>> stimparameters = {"type": ["current", "IClamp"], "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0}, {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ], "tstop": parameters["tstop"]}``

        ``>> recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]}, "stimulus": rec_i}``

        ``>> respmd = tg.forcellrecording(chosenmodel = model, recordings = recordings, parameters = runtimeparam, stimparameters = stimparameters)``

        *NOTE:*

        * if there is NO stimulation and ``chosenmodel.regions={"soma": 0.0, "axon": 0.0}` then ``len(respmd) = 2`` since there are two cell regions
        * also, this means ``respmd_soma = respmd["soma"]`` and ``respmd_axon = respmd["axon"]``
        * however, with stimulation there is an additional "stimulus" key ``stimulmd = respmmd["stimulus"]``

        """
        y = {}
        #if npd.equal(recordings["stimulus"], "Model is not stimulated").item((0)):
        # str because recordings has numpy array as dictionary values resulting in
        # numpy FutureWarning bug as it expects this to be an array as well
        # https://stackoverflow.com/questions/40659212/futurewarning-elementwise-comparison-failed-returning-scalar-but-in-the-futur
        if str(recordings["stimulus"])=="Model is not stimulated":
            y.update( cls.forcellrecordings_nostimulus( chosenmodel, recordings,
                                                        runtimeparameters ) )
        else: # for stimulus
            if (stimparameters is None):
                raise ValueError("for recording stimuli passing stimparameters is mandatory")
            else:
                y.update( cls.forcellrecordings_stimulus( chosenmodel, recordings,
                                              runtimeparameters, stimparameters ) )
        return y

    @classmethod
    def forrecording( cls, chosenmodel=None, recordings=None,
                      runtimeparameters=None, stimparameters=None ):
        """Creates the `NWB <https://www.nwb.org/>`_ formatted time-series metadata.

        **Keyword Arguments:**

        +---------------------+----------------------------------------------------------------+
        | Key                 | Value type                                                     |
        +=====================+================================================================+
        |``chosenmodel``      | instantiated model                                             |
        +---------------------+----------------------------------------------------------------+
        |``recordings``       | - dictionary with keys: ``"time"``, ``"response"`` and         |
        |                     |                                             ``"stimulus"``     |
        |                     | - Eg: {"time": array, "response": {cellregion_a: array,        |
        |                     |                                      cellregion_b: array},     |
        |                     |       "stimulus": str("Model is not stimulated") or array}     |
        +---------------------+----------------------------------------------------------------+
        |``runtimeparameters``| - dictionary with keys ``"dt"``, ``"celsius"``, ``"tstop"`` and|
        |                     |                                                   ``"v_init"`` |
        |                     | - Eg: {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}  |
        +---------------------+----------------------------------------------------------------+
        |    (optional)       | - dictionary with keys ``"type"``, ``"stimlist"`` and          |
        |``stimparameters``   |                                                ``"tstop"``     |
        |                     | - value for ``"type"`` is a two element list of strings of     |
        |                     |the form <stimulus category> <specific type of that category>   |
        |                     | - the first element is ALWAYS ``<stimulus category>``          |
        |                     | -  Eg: current inject on a cell ``["current", "IClamp"]``      |
        |                     | - value for ``"stimlist"`` is list with elements as dictionary |
        |                     |of the form [ {}, {}, ... ]                                     |
        |                     | - Eg1: [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},            |
        |                     |          {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]      |
        |                     | - Eg2: [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0,    |
        |                     |                                                 "delay": 5.0}, |
        |                     |          {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0,    |
        |                     |                                                 "delay": 10.0},|
        |                     |          {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0,    |
        |                     |                                                 "delay": 15.0},|
        |                     |          {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0,    |
        |                     |                                                 "delay": 20.0}]|
        |                     | - value for ``"tstop"`` is a number, time for generating the   |
        |                     |last epoch. Therefore, ``"tstop": parameters["tstop"]``.        |
        +---------------------+----------------------------------------------------------------+

        **Returned value:** Dictionary whose elements themselves are dictionaries. If there was not stimulus the length of the root dictionary is qual tot he number of cell regions, say, a soma and a dendrite. On the other hand if there was a stimulus the length of the root dictionary is equal to 1 + the number of cell regions, say, a soma and an axon. The key values are themselves dictionaries, see :py:meth:`.forcellrecording`.

        **Use case:** For ``modelscale="cells"``

        ``>> tg = TimeseriesGenerator()``

        Get dummy model

        ``>> from models.cells.modelDummyTest import DummyCell``

        ``>> model = DummyCell()``

        ``>> runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}``

        Generate model response

        ``>> rec_t = [ t*runtimeparam["dt"] for t in range( int( runtimeparam["tstop"]/runtimeparam["dt"] ) ) ]``

        ``>> rec_i = numpy.random.rand(1,len(rec_t))[0] # stimulus``

        ``>> rec_v = numpy.random.rand(2,len(rec_t))    # response``

        This model has ``model.regions = {'soma':0.0, 'axon':0.0}``

        For simulation without stimulation

        ``>> recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]}, "stimulus": "Model is not stimulated"}``

        ``>> respmd = tg.forcellrecording(chosenmodel = model, recordings = recordings, parameters = runtimeparam)``

        Simulation with stimulation

        ``>> stimparameters = {"type": ["current", "IClamp"], "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0}, {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ], "tstop": runtimeparam["tstop"]}``
        ``>> recordings = {"time": rec_t, "response": {"soma": rec_v[0], "axon": rec_v[1]}, "stimulus": rec_i}``

        ``>> respmd = tg.forcellrecording(chosenmodel = model, recordings = recordings, parameters = runtimeparam, stimparameters = stimparameters)``

        *NOTE:*

        * if there is NO stimulation and ``chosenmodel.regions={"soma": 0.0, "axon": 0.0}`` then ``len(respmd) = 2`` since there are two cell regions
        * also, this means ``respmd_soma = respmd["soma"]`` and ``respmd_axon = respmd["axon"]``
        * however, with stimulation there is an additional "stimulus" key ``stimulmd = respmmd["stimulus"]``

        """
        if (chosenmodel is None) or (recordings is None) or (runtimeparameters is None):
            raise ValueError("passing an instantiated chosenmodel, the recordings (dictionary) and runtimeparameters are  mandatory")
        elif chosenmodel.modelscale == "cells":
            return cls.forcellrecording( chosenmodel=chosenmodel,
                                          recordings=recordings,
                                          runtimeparameters=runtimeparameters,
                                          stimparameters=stimparameters )
