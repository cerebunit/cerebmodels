# ~/managers/operatorsTranscribe/metadata_epochgenerator.py

class EpochGenerator(object):
    """
    **Available Methods:**

    +------------------------------------------------+---------------+
    | Method name                                    | Method type   |
    +================================================+===============+
    | :py:meth:`.epochcontainer`                     | class method  |
    +------------------------------------------------+---------------+
    | :py:meth:`.anepoch`                            | class method  |
    +------------------------------------------------+---------------+
    | :py:meth:`.forepoch`                           | class method  |
    +------------------------------------------------+---------------+
    | :py:meth:`.compute_totalepochs_per_cellregion` | static method |
    +------------------------------------------------+---------------+
    | :py:meth:`.an_epoch_stimulus_window`           | static method |
    +------------------------------------------------+---------------+

    """

    @staticmethod
    def compute_totalepochs_per_cellregion(parameters):
        """Returns the "total" number of epochs. Here "total" stands for **A** region, NOT all regions.

        **Argument:**

        +----------+---------------------------------------------------------------+
        | Argument | Value type                                                    |
        +==========+===============================================================+
        | only one | - dictionary for **either** of the two parameters             |
        |          | - for run time parameters dictionary has keys ``"dt"``,       |
        |          |``"celsius"``, ``"tstop"``, ``"v_init"``                       |
        |          | - Eg: {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65} |
        |          | - the run time parameter argument is used for cases without   |	
        |          |stimulation.                                                   |
        |          | - for stimulation parameters dictionary has keys ``"type"``,  |
        |          |``"stimlist"`` and ``"tstop"``                                 |
        |          | - ``"type"`` key value is a two element list of strings       |
        |          |``<stimulus category> <specific type of that category>``       |
        |          |The first element is ALWAYS ``<stimulus category>``            |
        |          | - Eg: for injecting cell current ``["current", "IClamp"]``    |
        |          | - ``"stimlist"`` key value is a list with elements as         |
        |          |dictionary in the form [ {}, {}, ... ]                         |
        |          | - Eg: [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},            |
        |          |         {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]      |
        |          | - Eg: [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0,    |
        |          |                                              "delay": 5.0},   |
        |          |         {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0,    |
        |          |                                              "delay": 10.0},  |
        |          |         {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0,    |
        |          |                                              "delay": 15.0},  |
        |          |         {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0,    |
        |          |                                              "delay": 20.0} ] |
        |          | - ``"tstop"`` key value `` = runtimeparameters["tstop"]``     |
        |          |hence, for the last epoch                                      |
        +----------+---------------------------------------------------------------+

        *NOTE:*

        * ``no_of_regions = len(list(chosenmodel.regions.keys()))``
        * ``no_of_stimulus = 2``
        * ``no_of_epochs_per_region = 1 + no_of_stimulus``. Thus it includes period/epoch pre-first stimulus
        * ``total number of epochs = no_of_regions * no_of_epochs_per_regions``

        """
        if "stimlist" in parameters:
            no_of_stimulus = len(parameters["stimlist"])
            last_t = parameters["stimlist"][-1]["delay"]+parameters["stimlist"][-1]["dur"]
            if last_t == parameters["tstop"]:
                n = 0
            else:
                n = 1
        else:
            no_of_stimulus = 0
            n = 0
        return 1+no_of_stimulus+n

    @classmethod
    def epochcontainer(cls, chosenmodel, parameters):
        """Creates the container for `NWB <https://www.nwb.org/>`_ formatted epoch metadata.

        **Arguments:**

        +-----------+---------------------------------------------------------------+
        | Arguments | Value type                                                    |
        +===========+===============================================================+
        | first     | instantiated model                                            |
        +-----------+---------------------------------------------------------------+
        | second    | - dictionary for **either** of the two parameters             |
        |           | - for run time parameters dictionary has keys ``"dt"``,       |
        |           |``"celsius"``, ``"tstop"``, ``"v_init"``                       |
        |           | - Eg: {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65} |
        |           | - the run time parameter argument is used for cases without   |	
        |           |stimulation.                                                   |
        |           | - for stimulation parameters dictionary has keys ``"type"``   |
        |           |and ``"stimlist"``                                             |
        |           | - ``"type"`` key value is a two element list of strings       |
        |           |``<stimulus category> <specific type of that category>``       |
        |           |The first element is ALWAYS ``<stimulus category>``            |
        |           | - Eg: for injecting cell current ``["current", "IClamp"]``    |
        |           | - ``"stimlist"`` key value is a list with elements as         |
        |           |dictionary in the form [ {}, {}, ... ]                         |
        |           | - Eg: [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},            |
        |           |         {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]      |
        |           | - Eg: [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0,    |
        |           |                                              "delay": 5.0},   |
        |           |         {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0,    |
        |           |                                              "delay": 10.0},  |
        |           |         {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0,    |
        |           |                                              "delay": 15.0},  |
        |           |         {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0,    |
        |           |                                              "delay": 20.0} ] |
        |           | - ``"tstop"`` key value `` = runtimeparameters["tstop"]``     |
        |           |hence, for the last epoch                                      |
        +-----------+---------------------------------------------------------------+

        **Returned Value:** Assuming ``chosenmodel.regions = {'soma': 0.0, 'axon': 0.0}`` and the number of epochs per region = 3 (i.e initial state regardless of stimulus is epoch0), then the returned value is a dictionary of the form

        .. code-block:: python

           { "epoch0soma":
                {'tags': ('3_epoch_responses', "0", "soma", modelname, modelscale, "epoch0soma", "soma axon")},
             "epoch1soma":
                {'tags': ('3_epoch_responses', "1", "soma", modelname, modelscale, "epoch1soma", "soma axon")},
             "epoch2soma":
                {'tags': ('3_epoch_responses', "2", "soma", modelname, modelscale, "epoch2soma", "soma axon"])},
             "epoch0axon":
                {'tags': ('3_epoch_responses', "0", "axon", modelname, modelscale, "epoch0axon", "soma axon"])},
             "epoch1axon":
                {'tags': ('3_epoch_responses', "1", "soma", modelname, modelscale, "epoch1axon", "soma axon")},
             "epoch2axon":
                {'tags': ('3_epoch_responses', "2", "soma", modelname, modelscale, "epoch2axon", "soma axon")} }

        However without stimulation, number of epochs per region = 1 (i.e, only epoch0) and the dictionary will look like

        .. code-block:: python

           { "epoch0soma":
                {'tags': ('1_epoch_responses', "0", "soma", modelname, modelscale, "epoch0soma", "soma axon")},
             "epoch0axon":
                {'tags': ('1_epoch_responses', "0", "soma", modelname, modelscale, "epoch0axon", "soma axon")} }

        *NOTE:*

        * ``no_of_regions = len(list(chosenmodel.regions.keys()))``
        * ``no_of_stimulus = 2``
        * ``no_of_epochs_per_region = 1 + no_of_stimulus`` Thus it includes period/epoch pre-first stimulus
        * ``total number of epochs = no_of_regions * no_of_epochs_per_regions``
        * and tuple

          ``"tags": ( No_epoch_responses, epochID, this_cellregion, modelname, modelscale, epoch<index>cellregion, all_cellregions )``

        * elements of the ``tags`` tuple are "all strings"
        * the first element of the tuple will always be of the form <No>_epoch_responses the only difference is the <No>, standing for number of epoch responses for this cell regions. It should be pointed out that it does not stand for the total overall number of epochs (for all the regions).
        * the last element is a string of space separated region names

        """
        x = {}
        lst = []
        no_of_epochs_per_region = cls.compute_totalepochs_per_cellregion(parameters)
        for cellregion in chosenmodel.regions.keys():
            [ x.update({"epoch"+str(i)+cellregion: {}})
                                   for i in range(no_of_epochs_per_region) ]
            [ x["epoch"+str(i)+cellregion].update(
                            {"tags":
                                  ( str(no_of_epochs_per_region)+"_epoch_responses",
                                    str(i), cellregion,
                                    chosenmodel.modelname, chosenmodel.modelscale,
                                    "epoch"+str(i)+cellregion,
                                    ' '.join( chosenmodel.regions.keys() ) )}) # space separated string
                 for i in range(no_of_epochs_per_region) ]
        return x

    @staticmethod
    def an_epoch_stimulus_window(epoch_no_per_region, theregion, parameters):
        """Returns a dictionary focusing on the stimulation for an epoch.

        **Arguments:**

        +-----------+---------------------------------------------------------------+
        | Arguments | Value type                                                    |
        +===========+===============================================================+
        | first     | number of epochs per region                                   |
        +-----------+---------------------------------------------------------------+
        | second    | string for the region name,                                   |
        |           |i.e, key of chosenmodel.regions = {"soma": 0.0, "axon": 0.0}   |
        +-----------+---------------------------------------------------------------+
        | third     | - dictionary for stimulation parameters dictionary            |
        |           | - ``"type"`` key value is a two element list of strings       |
        |           |``<stimulus category> <specific type of that category>``       |
        |           |The first element is ALWAYS ``<stimulus category>``            |
        |           | - Eg: for injecting cell current ``["current", "IClamp"]``    |
        |           | - ``"stimlist"`` key value is a list with elements as         |
        |           |dictionary in the form [ {}, {}, ... ]                         |
        |           | - Eg: [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},            |
        |           |         {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]      |
        |           | - Eg: [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0,    |
        |           |                                              "delay": 5.0},   |
        |           |         {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0,    |
        |           |                                              "delay": 10.0},  |
        |           |         {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0,    |
        |           |                                              "delay": 15.0},  |
        |           |         {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0,    |
        |           |                                              "delay": 20.0} ] |
        |           | - ``"tstop"`` key value `` = runtimeparameters["tstop"]``     |
        |           |hence, for the last epoch                                      |
        +-----------+---------------------------------------------------------------+

        **Returned value:** This is a dictionary with the keys ``"source"``, ``"start_time"``, ``"stop_time"`` and ``"description"``.

        """
        i = epoch_no_per_region - 1
        stimlist = parameters["stimlist"]
        if parameters["type"][1]=="IClamp":
            descrip = "IClamp stimulation of model with amplitude = " + \
                      str(stimlist[i]["amp"]) + " nA"
        else:
            descrip = "IRamp stimulation of model with amplitudes from " + \
                      str(stimlist[i]["amp_initial"]) + " to " + \
                      str(stimlist[i]["amp_final"]) + " nA"
        return {"source": theregion,
                "start_time": float(stimlist[i]["delay"]),
                "stop_time": float(stimlist[i]["delay"] + stimlist[i]["dur"]),
                "description": descrip}

    @classmethod
    def an_epoch( cls, epoch_no_per_region, theregion, parameters ):
        """Creates the value for one epoch, i.e, value for one of the epoch-key in the container.

        **Arguments:**

        +-----------+---------------------------------------------------------------+
        | Arguments | Value type                                                    |
        +===========+===============================================================+
        | first     | integer for number of epochs per region                       |
        +-----------+---------------------------------------------------------------+
        | second    | string for the region name,                                   |
        |           |i.e, key of chosenmodel.regions = {"soma": 0.0, "axon": 0.0}   |
        +-----------+---------------------------------------------------------------+
        | third     | - dictionary for **either** of the two parameters             |
        |           | - for run time parameters dictionary has keys ``"dt"``,       |
        |           |``"celsius"``, ``"tstop"``, ``"v_init"``                       |
        |           | - Eg: {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65} |
        |           | - the run time parameter argument is used for cases without   |	
        |           |stimulation.                                                   |
        |           | - for stimulation parameters dictionary has keys ``"type"``   |
        |           |and ``"stimlist"``                                             |
        |           | - ``"type"`` key value is a two element list of strings       |
        |           |``<stimulus category> <specific type of that category>``       |
        |           |The first element is ALWAYS ``<stimulus category>``            |
        |           | - Eg: for injecting cell current ``["current", "IClamp"]``    |
        |           | - ``"stimlist"`` key value is a list with elements as         |
        |           |dictionary in the form [ {}, {}, ... ]                         |
        |           | - Eg: [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},            |
        |           |         {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]      |
        |           | - Eg: [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0,    |
        |           |                                              "delay": 5.0},   |
        |           |         {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0,    |
        |           |                                              "delay": 10.0},  |
        |           |         {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0,    |
        |           |                                              "delay": 15.0},  |
        |           |         {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0,    |
        |           |                                              "delay": 20.0} ] |
        |           | - ``"tstop"`` key value `` = runtimeparameters["tstop"]``     |
        |           |hence, for the last epoch                                      |
        +-----------+---------------------------------------------------------------+

        **Returned Value:** Assuming ``chosenmodel.regions = {'soma': 0.0, 'axon': 0.0}`` the epoch metadata for a region, say ``"soma"`` is a dictionary of the form

        ``{"source": "soma", "start_time": float, "stop_time": float, "description": string, "tags": ( No_epoch_responses, epochID, this_region, modelname, modelscale, epochs<index>region, all_regions ) }``

        *NOTE:*

        * the returned value has these same four-keys regardless of with or without stimulus

        """
        if "stimlist" not in parameters:
            return {"source": theregion, "start_time": 0.0, "stop_time": float(parameters["tstop"]),
                    "description": "there is no stimulation of the model"}
        elif parameters["type"][0]=="current":
            stimlist = parameters["stimlist"]
            if epoch_no_per_region==0: # initial no stimulation region
                return {"source": theregion,
                        "start_time": 0.0,
                        "stop_time": 0.0 + stimlist[0]["delay"],
                        "description": "first, no stimulus"}
            elif epoch_no_per_region>len(stimlist):
                last_t = float( stimlist[-1]["delay"]+stimlist[-1]["dur"] )
                return {"source": theregion,
                        "start_time": last_t,
                        "stop_time": float(parameters["tstop"]),
                        "description": "last, no stimulus"}
            else:
                return cls.an_epoch_stimulus_window(epoch_no_per_region,
                                                    theregion, parameters)

    @classmethod
    def forepoch( cls, chosenmodel=None, parameters=None ):
        """Creates the `NWB <https://www.nwb.org/>`_ formatted metadata forfile.

        **Keyword arguments:**

        +-----------------+---------------------------------------------------------------+
        | Key             | Value type                                                    |
        +=================+===============================================================+
        | ``chosenmodel`` | instantiated model                                            |
        +-----------------+---------------------------------------------------------------+
        | ``parameters``  | - dictionary for **either** of the two parameters             |
        |                 | - for run time parameters dictionary has keys ``"dt"``,       |
        |                 |``"celsius"``, ``"tstop"``, ``"v_init"``                       |
        |                 | - Eg: {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65} |
        |                 | - the run time parameter argument is used for cases without   |	
        |                 |stimulation.                                                   |
        |                 | - for stimulation parameters dictionary has keys ``"type"``   |
        |                 |and ``"stimlist"``                                             |
        |                 | - ``"type"`` key value is a two element list of strings       |
        |                 |``<stimulus category> <specific type of that category>``       |
        |                 |The first element is ALWAYS ``<stimulus category>``            |
        |                 | - Eg: for injecting cell current ``["current", "IClamp"]``    |
        |                 | - ``"stimlist"`` key value is a list with elements as         |
        |                 |dictionary in the form [ {}, {}, ... ]                         |
        |                 | - Eg: [ {"amp": 0.5, "dur": 100.0, "delay": 10.0},            |
        |                 |         {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ]      |
        |                 | - Eg: [ {"amp_initial": 0.0, "amp_final": 0.5, "dur": 5.0,    |
        |                 |                                              "delay": 5.0},   |
        |                 |         {"amp_initial": 0.5, "amp_final": 1.0, "dur": 5.0,    |
        |                 |                                              "delay": 10.0},  |
        |                 |         {"amp_initial": 1.0, "amp_final": 0.5, "dur": 5.0,    |
        |                 |                                              "delay": 15.0},  |
        |                 |         {"amp_initial": 0.5, "amp_final": 0.0, "dur": 5.0,    |
        |                 |                                              "delay": 20.0} ] |
        |                 | - ``"tstop"`` key value `` = runtimeparameters["tstop"]``     |
        |                 |hence, for the last epoch                                      |
        +-----------------+---------------------------------------------------------------+

        **Returned Value:** Assuming ``chosenmodel.regions = {'soma': 0.0, 'axon': 0.0}`` and number of epochs per region = 2 (i.e initial state regardless of stimulus is epoch0), the returned value is a dictionary of the form

        | ``{"epoch0soma": {"source": "soma", "start_time": float, "stop_time": float, "description": string, "tags": ( No_epoch_responses, epochID, this_region, modelname, modelscale, epochs<index>region, all_regions ) },``
        |  ``"epoch1soma": {"source": "soma", "start_time": float, "stop_time": float, "description": string}, "tags": ( string, string, string, string, string, string, space separated string ) }``
        |  ``"epoch0axon": {"source": "axon", "start_time": float, "stop_time": float, "description": string, "tags": ( string, string, string, string, string, string, space separated string ) },``
        |  ``"epoch1axon": {"source": "axon", "start_time": float, "stop_time": float, "description": string, "tags": ( string, string, string, string, string, string, space separated string ) },``
        | ``"epoch_tags": ('2_epoch_responses',)}``

        However without stimulation, number of epochs per region = 1 (i.e, only epoch0) resulting in
        | ``{"epoch0soma": {"source": "soma", "start_time": float, "stop_time": float, "description": string, "tags": ( No_epoch_responses, epochID, this_region, modelname, modelscale, epochs<index>retion, all_regions ) },``
        |  ``"epoch0axon": {"source": "axon", "start_time": float, "stop_time": float, "description": string, "tags": ( string, string, string, string, string, string, space separated string )},``
        |  ``"epoch_tags": ('1_epoch_responses',)}``

        *NOTE:*

        * the first element of the ``"tags"`` tuple is always of the form <No>_epoch_responses, such that <No> may vary, representing the total available epochs for this chosen region. It does not stand for the overall number of epochs (for all the regions).
       

        **Use case:**

        ``>> eg = EpochGenerator()``

        ``>> model = Xyz()``

        ``>> runtimeparam = {"dt": 0.01, "celsius": 30, "tstop": 100, "v_init": 65}``

        For simulation without stimulation

        ``>> epochmd = eg.forepoch(chosenmodel = model, parameters = runtimeparam)``

        For simulation with stimulation

        ``>> stimparameters = {"type": ["current", "IClamp"], "stimlist": [ {"amp": 0.5, "dur": 100.0, "delay": 10.0}, {"amp": 1.0, "dur": 50.0, "delay": 10.0+100.0} ], "tstop": runtimeparam["tstop"]}``

        ``>> epochmd = eg.forepoch(chosenmodel = model, parameters = stimparameters)``

        """

        if (chosenmodel is None) or (parameters is None):
            raise ValueError("passing an instantiated chosenmodel and parameters (for runtime or stimulation) are  mandatory")
        else:
            x = cls.epochcontainer( chosenmodel, parameters )
            no_of_epochs_per_region = cls.compute_totalepochs_per_cellregion(parameters)
            for cellregion in chosenmodel.regions.keys():
                for i in range(no_of_epochs_per_region):
                    epoch = "epoch"+str(i)+cellregion
                    x[epoch].update( cls.an_epoch( i, cellregion, parameters ) )
            return x
