# ~/managers/operatorsTranscribe/metadata_epochgenerator.py
from managers.operatorsYield.regionparser import RegionParser as rp

class EpochGenerator(object):
    """
    **Available Methods:**

    +------------------------------------------------+---------------+
    | Method name                                    | Method type   |
    +================================================+===============+
    | :py:meth:`.epochcontainer`                     | class method  |
    +------------------------------------------------+---------------+
    | :py:meth:`.anepoch` DEPRECIATED                | class method  |
    +------------------------------------------------+---------------+
    | :py:meth:`.forepoch` DEPRECIATED               | class method  |
    +------------------------------------------------+---------------+
    | :py:meth:`.compute_totalepochs_per_cellregion` | static method |
    +------------------------------------------------+---------------+
    | :py:meth:`.epoch_times_list`                   | static method |
    +------------------------------------------------+---------------+
    | :py:meth:`.epochcontainer_for_regionbodies`    | static method |
    +------------------------------------------------+---------------+
    | :py:meth:`.epochcontainer_for_compartments`    | static method |
    +------------------------------------------------+---------------+
    | :py:meth:`.an_epoch_stimulus_window`DEPRECIATED| static method |
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
        #if "stimlist" in parameters:
        #    no_of_stimulus = len(parameters["stimlist"])
            #last_t = parameters["stimlist"][-1]["delay"]+parameters["stimlist"][-1]["dur"]
            #if last_t == parameters["tstop"]:
            #    n = 0
            #else:
            #    n = 1
        #else:
        #    no_of_stimulus = 0
            #n = 0
        #return 1+no_of_stimulus#+n
        if "stimlist" in parameters:
            no_of_stimulus = len(parameters["stimlist"])
            if parameters["type"][0]=="current":
                if (parameters["stimlist"][0]["delay"] != 0):
                    n = 1 + no_of_stimulus
                else:# first delay = 0 => first stimulus at t = 0.0
                    n = no_of_stimulus
            elif parameters["type"][0]=="voltage":
                n = 1+no_of_stimulus
        else:
            n = 1
        return n

    @staticmethod
    def epoch_times_list(parameters):
        dur = (lambda volttype, indx:\
                  "dur"+str(indx+1) if volttype=="SEClamp" else "dur")
        start_ts = [0.0]
        if "stimlist" in parameters:
            if parameters["type"][0]=="current":
                if parameters["stimlist"][0]["delay"] != 0.0:
                    stop_ts = [ parameters["stimlist"][0]["delay"] ]
                    i0 = 0
                else: # epoch0 is also when first stimulus was given
                    stop_ts = [ parameters["stimlist"][0]["dur"] ]
                    i0 = 1
                for i in range( i0, len(parameters["stimlist"]) ):
                    start_ts.append( parameters["stimlist"][i]["delay"] )
                    stop_ts.append( parameters["stimlist"][i]["delay"] +
                                    parameters["stimlist"][i]["dur"] )
            elif parameters["type"][0]=="voltage":
                volttype = parameters["type"][1]
                stop_ts = [ parameters["stimlist"][0][dur(volttype,0)] ]
                for i in range( 1, len(parameters["stimlist"]) ):
                    start_ts.append( parameters["stimlist"][ i-1 ][ dur(volttype,i-1) ] )
                    stop_ts.append( parameters["stimlist"][ i ][ dur(volttype,i) ] )
            # Finally
            if stop_ts[-1] < parameters["tstop"]:
                start_ts.append( stop_ts[-1] )
                stop_ts.append( parameters["tstop"] )
        else:
            stop_ts = [ parameters["tstop"] ]
        return start_ts, stop_ts
 
    @staticmethod
    def epochcontainer_for_regionbodies(model, no_of_epochs, start_ts, stop_ts):
        regionlist = rp.get_regionlist(model)
        x = {}
        for a_region_name in regionlist:
            [ x.update({"epoch"+str(i)+a_region_name: {}})
              for i in range(no_of_epochs) ]
            no_of_rec = len(model.regions[a_region_name])
            for ith_rec_type in range(no_of_rec):
                rec_of = model.regions[a_region_name][ith_rec_type]
                [ x["epoch"+str(i)+a_region_name].update(
                    {rec_of:
                        {"start_time": start_ts[i],
                         "stop_time": stop_ts[i],
                         "tags": ( str(no_of_epochs)+"_epoch_response",# 0 number of epochs
                                   str(i),                        # 1 epochID
                                   a_region_name +" "+ rec_of,    # 2 [ region, recsite ]
                                   " ".join(model.regions[a_region_name]),#3 all rec sites
                                   model.modelname, model.modelscale,# 4modelname, 5scale
                                   "epoch"+str(i)+a_region_name +" "+ rec_of )} # 6 dict keys
                    } ) for i in range(no_of_epochs) ]
        return x

    @staticmethod
    def epochcontainer_for_components(model, no_of_epochs, start_ts, stop_ts):
        componentgrouplist = rp.get_componentgrouplist(model)
        x = {}
        for epochID in range(no_of_epochs):
            for compgroup_name in componentgrouplist:
                its_regionlist = rp.get_regionlist_of_componentgroup(model, compgroup_name)
                ans2 = {}
                for a_region_name in its_regionlist:
                    complist = rp.get_componentlist(model, compgroup_name, a_region_name)
                    ans1 = {}
                    for a_comp_name in complist:
                        no_of_rec = \
                          len(model.regions[compgroup_name][a_region_name][a_comp_name])
                        ans0 = {}
                        for ith_rec_type in range(no_of_rec):
                            rec_of = model.regions[compgroup_name][a_region_name]\
                                                  [a_comp_name][ith_rec_type]
                            ans0.update({rec_of:
                              {"start_time": start_ts[ epochID ],
                               "stop_time": stop_ts[ epochID ],
                               "tags": ( str(no_of_epochs)+"_epoch_response",# 0 #epochs
                                         str( epochID ), # 1 epochID
                                         compgroup_name +" "+ a_region_name +" "+
                                          a_comp_name +" "+ rec_of,# 2[gp, reg, comp, rec]
                                         " ".join(model.regions[compgroup_name][a_region_name][a_comp_name]),#3 all rec sites
                                         model.modelname, model.modelscale,# 4, 5 indices
                                         "epoch"+str(epochID)+compgroup_name +" "+
                                         a_region_name +" "+ a_comp_name +" "+
                                         rec_of )} }) # 6 dict keys
                        ans1.update( {a_comp_name: ans0} )
                    ans2.update( {a_region_name: ans1} )
                x.update( {"epoch"+str(epochID)+compgroup_name: ans2} )
        return x

    @classmethod
    def epochcontainer(cls, chosenmodel = None, parameters = None):
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

        ::

           { "epoch0soma": {"tags": ("3_epoch_responses", "0", "soma", modelname, modelscale,
                                     "epoch0soma", "soma axon") },
             "epoch1soma": {"tags": ("3_epoch_responses", "1", "soma", modelname, modelscale,
                                     "epoch1soma", "soma axon") },
             "epoch2soma": {"tags": ("3_epoch_responses", "2", "soma", modelname, modelscale,
                                     "epoch2soma", "soma axon") },
             "epoch0axon": {"tags": ("3_epoch_responses", "0", "axon", modelname, modelscale,
                                     "epoch0axon", "soma axon")},
             "epoch1axon": {"tags": ("3_epoch_responses", "1", "soma", modelname, modelscale,
                                     "epoch1axon", "soma axon")},
             "epoch2axon": {"tags": ("3_epoch_responses", "2", "soma", modelname, modelscale,
                                     "epoch2axon", "soma axon")} }

        However without stimulation, number of epochs per region = 1 (i.e, only epoch0) and the dictionary will look like

        ::

           { "epoch0soma": {"tags": ("1_epoch_responses", "0", "soma", modelname, modelscale,
                                     "epoch0soma", "soma axon") },
             "epoch0axon": {"tags": ("1_epoch_responses", "0", "soma", modelname, modelscale,
                                     "epoch0axon", "soma axon") } }

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
        #x = {}
        #lst = []
        #no_of_epochs_per_region = cls.compute_totalepochs_per_cellregion(parameters)
        #for cellregion in chosenmodel.regions.keys():
        #    [ x.update({"epoch"+str(i)+cellregion: {}})
        #                           for i in range(no_of_epochs_per_region) ]
        #    [ x["epoch"+str(i)+cellregion].update(
        #                    {"tags":
        #                          ( str(no_of_epochs_per_region)+"_epoch_responses",
        #                            str(i), cellregion,
        #                            chosenmodel.modelname, chosenmodel.modelscale,
        #                            "epoch"+str(i)+cellregion,
        #                            ' '.join( chosenmodel.regions.keys() ) )}) # space separated string
        #         for i in range(no_of_epochs_per_region) ]
        #return x
        no_of_epochs = cls.compute_totalepochs_per_cellregion( parameters )
        [start_ts, stop_ts] = cls.epoch_times_list( parameters )
        x = cls.epochcontainer_for_regionbodies( chosenmodel,
                                          no_of_epochs, start_ts, stop_ts )
        componentgrouplist = rp.get_componentgrouplist(chosenmodel)
        if len(componentgrouplist)!=0:
            y = cls.epochcontainer_for_components( chosenmodel,
                                          no_of_epochs, start_ts, stop_ts )
            return {**x, **y}
        else:
            return x

    @staticmethod
    def epochs_allstimuli(stimparameters, no_of_epochs):
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
        # Current amplitudes
        ic_amps = (lambda ic_stimlist: [ ic_stimlist[i]["amp"] \
                                         for i in range(len(ic_stimlist)) ])
        ir_amps = (lambda ir_stimlist: [ ir_stimlist[i]["amp_initial"] \
                                         for i in range(len(ir_stimlist)) ])
        i_amps = (lambda stimparameters: \
            ic_amps(stimparameters["stimlist"]) if stimparameters["type"][1]=="IClamp"\
            else ( ir_amps(stimparameters["stimlist"]) if stimparameters["type"][1]=="IRamp"\
                   else [] ) )
        # Current times
        i_times = (lambda i_stimlist: [ i_stimlist[i]["delay"] \
                                        for i in range(len(i_stimlist)) ])
        # Current description
        curr_descrip = (lambda stimparameters: \
                stimparameters["type"][1]+" stimulation of model with amplitude = "+\
                str( i_amps(stimparameters) )+" nA starting at times = "+\
                str( i_times(stimparameters) ))
        # Voltage amplitudes
        sec_amps = (lambda sec_stimlist: [ sec_stimlist[i]["amp"+str(i+1)] \
                                           for i in range(len(sec_stimlist)) ])
        v_amps = (lambda stimparameters: \
            sec_amps(stimparameters["stimlist"]) if stimparameters["type"][1]=="SEClamp"\
            else ic_amps(stimparameters["stimlist"]) ) # note key for VClamp same as ic
        # Voltages times
        v_times = (lambda stimparameters: \
            [ stimparameters["stimlist"][i]["dur"+str(i+1)]
              for i in range(len(stimparameters["stimlist"]))] \
            if stimparameters["type"][1]=="SEClamp"\
            else [ stimparameters["stimlist"][i]["dur"]
                   for i in range(len(stimparameters["stimlist"]))] )
        # Voltage description
        volt_descrip = (lambda stimparameters: \
                stimparameters["type"][1]+" stimulation of model with amplitude = "+\
                str( v_amps(stimparameters) )+" mV stopping at times = "+\
                str( v_times(stimparameters) ))
        # Main Description
        if stimparameters["type"][0]=="current":
            descrip = curr_descrip( stimparameters )
        else:
            descrip = volt_descrip( stimparameters )
        #
        curr_t0_tf = ( lambda epochID, stimlist: \
                [ 0.0, float(stimlist[epochID]["delay"]) ] if epochID==0 \
                else [ float(stimlist[epochID]["delay"]),
                       float(stimlist[epochID]["delay"] + stimlist[epochID]["dur"]) ] )
        #
        #sec_t0_tf = ( lambda epochID, stimlist: \
        #        [ 0.0, float(stimlist[epochID]["dur"+str(epochID+1)]) ]
        #        if epochID==0 \
        #        else [ float(stimlist[epochID-1]["dur"+str(epochID)]),
        #               float(stimlist[epochID]["dur"+str(epochID))] ] )
        #
        #
        #x = {}
        #for i in range(no_of_epochs):
        #    key = "epoch"+str(i)+"stimulus"
        #    src = stimparameters["type"][1]
        #    if i==0:
        #        t0 = 0.0
        #        tf = 
        #i = epoch_no_per_region - 1
        #stimlist = parameters["stimlist"]
        #if parameters["type"][1]=="IClamp":
        #    descrip = "IClamp stimulation of model with amplitude = " + \
        #              str(stimlist[i]["amp"]) + " nA"
        #else:
        #    descrip = "IRamp stimulation of model with amplitudes from " + \
        #              str(stimlist[i]["amp_initial"]) + " to " + \
        #              str(stimlist[i]["amp_final"]) + " nA"
        #return {"source": theregion,
        #        "start_time": float(stimlist[i]["delay"]),
        #        "stop_time": float(stimlist[i]["delay"] + stimlist[i]["dur"]),
        #        "description": descrip}

    @staticmethod
    def an_epoch_stimulus_window(epoch_no_per_region, theregion, stimparameters):
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

        ::

           { 
             "epoch0soma": {"source": "soma", "start_time": float, "stop_time": float,
                            "description": string,
                            "tags": ( No_epoch_responses, epochID, this_region, modelname,
                                      modelscale, epochs<index>region, all_regions ) },
             "epoch1soma": {"source": "soma", "start_time": float, "stop_time": float,
                            "description": string,
                            "tags": ( string, string, string, string, string, string,
                                      space separated string ) }
             "epoch0axon": {"source": "axon", "start_time": float, "stop_time": float,
                            "description": string,
                            "tags": ( string, string, string, string, string, string,
                                      space separated string ) },
             "epoch1axon": {"source": "axon", "start_time": float, "stop_time": float,
                            "description": string,
                            "tags": ( string, string, string, string, string, string,
                                      space separated string ) },
             "epoch_tags": ('2_epoch_responses',) }

        However without stimulation, number of epochs per region = 1 (i.e, only epoch0) resulting in

        ::

           { "epoch0soma": {"source": "soma", "start_time": float, "stop_time": float,
                            "description": string,
                            "tags": ( No_epoch_responses, epochID, this_region, modelname,
                                      modelscale, epochs<index>retion, all_regions ) },
             "epoch0axon": {"source": "axon", "start_time": float, "stop_time": float,
                            "description": string,
                            "tags": ( string, string, string, string, string, string,
                                      space separated string ) },
             "epoch_tags": ('1_epoch_responses',) }

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
