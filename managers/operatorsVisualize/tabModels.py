# ~/managers/operatorsVisualize/tabModels.py
from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool, 
			  ColumnDataSource, Panel, 
			  FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider,
                                  Dropdown, Select, Button, TextInput, Div, Paragraph,
				  Tabs, CheckboxButtonGroup, 
				  TableColumn, DataTable, Select)
from bokeh.layouts import column, row, WidgetBox, layout
from bokeh.palettes import Category20_16

from dask.diagnostics import Profiler, ResourceProfiler, CacheProfiler, visualize
from dask.callbacks import Callback
from dask.distributed import Client, LocalCluster

import os, sys
pwd = os.getcwd()
rootwd = os.path.dirname(pwd)
#sys.path.append(os.path.dirname(pwd))

from executive import ExecutiveControl

import ast

def TabModels():
    """available_modelscales = ['cells', 'microcircuit', 'network']
    """
    def get_select_menu( menu_type, menu_list ):
        if menu_type=="modelscales":
            title = "Modeling Scale Options"
        elif menu_type=="models":
            title = "Choose a model name"
        elif menu_type=="responses":
            title = "Choose a response (file)"
        return Select( title=title, value=menu_list[0][0], options=menu_list )

    def get_menu_modelscales():
        #NOTE: available_modelscale & scale_and_models are global variables
        menu = [("None", "None")]
        for modelscale in available_modelscales:
            # tag the modelscale as first element in the value = modellist
            modellist = ' '.join( [modelscale] + scale_and_models[modelscale] )
            menu.append( (modellist, modelscale) ) # tuple (string of models, scale)
        return menu

    def get_menu_models(modellist):
        #NOTE: models_with_filenames is a global variable
        menu = [("None", "Below are available models")]
        if modellist[1]=="No_Models": #modellist[0]=modelname
            menu[0] = ( modellist[1], modellist[1].replace("_"," ") )#tuple (scale, string of models)
        else:
            for modelname in modellist[1:]:
                # tag modelscale & modelname as 1st-two elements in the value
                itsvalue = ' '.join( [modellist[0], modelname] )
                menu.append( (itsvalue, modelname) ) # tuple (string of models, scale)
        return menu

    def update_models_list( attr, old, new ):
        if new == "No_Models":
            menu_list = [''.join(list(new))] # ["No Models"]
        else:
            menu_list = new.split()
        models_select.options = get_menu_models(menu_list)
        runmodel.disabled = True
        #print new
        #print modelscales_select.value
        #print menu_list
        #print menu_list[0]

    def update_global_model( attr, old, new ):
        menu_list = new.split()
        modelscale = menu_list[0] # update global modelscale
        modelname = menu_list[1]  # update glocal modelname
        #print modelscale, modelname
        sys.path.append(pwd) # uncomment only when using executiveViz
        chosenmodel = ExecutiveControl.choose_model( modelscale=str(modelscale),
                                                     modelname=str(modelname) )
        modeltitle.text = chosenmodel.name
        modeldescr.text = chosenmodel.description
        modelregions.text = "Potential stimulation sites: "+str(chosenmodel.regions)
        runmodel.disabled = False

    def update_stimulation_parameters_input_status( attr, old, new ):
        if new=="no":
            stim_type_input.disabled = True
            stim_list_input.disabled = True
            stim_loc_input.disabled = True
        else:
            stim_type_input.disabled = False
            stim_list_input.disabled = False
            stim_loc_input.disabled = False

    def simulate():
        #if modelscales_select.value == "No_Models":
            #print modelscales_select.value
        #else:
            #print modelscales_select.value
        sys.path.append(pwd) # uncomment only when using executiveViz
        ec = ExecutiveControl()
        modelscale = models_select.value.split()[0]
        modelname =  models_select.value.split()[1]
        chosenmodel = ec.choose_model(modelscale=modelscale, modelname=modelname)
        parameters = ast.literal_eval(runtime_input.value)
        #print parameters
        #print stimulation.value
        if stimulation.value=="yes":
            stimparameters = ast.literal_eval(stim_type_input.value)
            stimparameters.update( {"stimlist": ast.literal_eval(stim_list_input.value)} )
            with Profiler() as prof, ResourceProfiler() as rprof:
                ec.launch_model ( parameters=parameters, onmodel=chosenmodel,
                                  stimparameters=stimparameters, stimloc=stim_loc_input.value )
        else:
            with Profiler() as prof, ResourceProfiler() as rprof:
                ec.launch_model( parameters=parameters, onmodel=chosenmodel )
            #myplot = visualize([prof, rprof])
        ec.save_response()
        #viz_source.data['diagnostic'][0] = prof
        #viz_source.data['diagnostic'][1] = rprof
        viz_source.data['diagnostic'] = [prof, rprof]
        #viz_source.data['diagnostic'][0].results[0] = prof.results[0]
        #myplot.data['diagplots'][0] = visualize([prof, rprof])
        
        #return visualize([prof, rprof])
    #
    ### +++++++++++++++++++GENERATE DATA FOR THE OPTIONS MENU++++++++++++++++++
    # available_modelscales -- list
    # scale_and_models -- dictionary with list as key value
    # models_with_filenames -- dictionary with list as key value
    # responses_with_filepaths -- dictionary with string as key value
    # Generate Model Info
    #os.chdir("..") # line required for calling ~/managers/bokehtest.py
    #available_modelscales = fm.available_modelscales()
    #os.chdir(rootwd) # for running it from ~/managers
    available_modelscales = ExecutiveControl.list_modelscales()
    scale_and_models = {}
    for modelscale in available_modelscales: # get list of models in each scale
        try:
            #modelslist = fm.modelscale_inventory(model_scale=modelscale)
            modelslist = ExecutiveControl.list_models(modelscale=modelscale)
        except:
            modelslist = ["No_Models"]
        scale_and_models.update( {modelscale: modelslist} )
    #os.chdir(pwd) # for running it from ~/managers
    #print scale_and_models
    ### ++++++++++++++++++++END GENERATE DATA FOR THE OPTIONS++++++++++++++++++
    #
    modelscale = None
    modelname = None
    chosenmodel = None
    #
    menu = get_menu_modelscales()
    modelscales_select = get_select_menu( "modelscales", menu )
    #
    dummy_model_menu = [('None', "First select a model scale")]
    models_select = get_select_menu( "models", dummy_model_menu )
    #
    runtime_input = TextInput(value="{'dt': 0.1, 'celsius': 30, 'tstop': 10, 'v_init': 65}",
                           title="Runtime Parameters:")
    #print runtime_input.value
    #print type(runtime_input.value)
    #
    stimulation_menu = [("No", "no"), None, ("Yes", "yes")]
    stimulation = Dropdown(label="Stimulation Yes/No", button_type="warning",
                           menu=stimulation_menu)
    stim_type_input = TextInput(value="{'type': ['current', 'IClamp']}",
                                title="Stimulation Parameters (Stimulation Type):")
    stim_list_input = TextInput(value="[{'amp': 0.5, 'dur': 10.0, 'delay': 5.0}, "
                                      " {'amp': 1.0, 'dur': 20.0, 'delay': 15.0}]",
                                title="Stimulation Parameters (Stimuli):")
    stim_loc_input = TextInput(value='soma', title="Stimulation location:")
    # disable stimulation by DEFAULT
    stim_type_input.disabled = True
    stim_list_input.disabled = True
    stim_loc_input.disabled = True
    #
    runmodel = Button(label="Run Simulation", button_type="success")
    runmodel.disabled = True
    #
    modeltitle = Div(text="""No Model has been selected yet.""", width=290, height=40)
    modeldescr = Paragraph(text="""There is no Model Description.""", width=290, height=200)
    modelregions = Div(text="""Main Locations within the model for stimulation""", width=290, height=50)
    # disable the model texts by DEFAULT
    modeltitle.disabled = True
    modeldescr.disabled = True
    modelregions.disabled = True

    def viz():
        return visualize(viz_source.data['diagnostic'])
    # Put controls in a single element
    viz_source = ColumnDataSource(data={'diagnostic': [Profiler(), ResourceProfiler()]})
    myplot = viz()
    #diagplot = visualize( viz_source.data['diagnostic'] )
    #myplot = ColumnDataSource(data={'diagplots': [diagplot]})
    #myplot = ColumnDataSource(data={'diagplots': [visualize([Profiler(), ResourceProfiler()])]})
    
    

    # INTERACTION
    modelscales_select.on_change("value", update_models_list)
    models_select.on_change("value", update_global_model)
    #responses_select.on_change("value", update_plot)
    stimulation.on_change("value", update_stimulation_parameters_input_status)
    runmodel.on_click(simulate)

    # Create a row layout
    mylayout = row(WidgetBox(modelscales_select, models_select, runtime_input,
                             stimulation, stim_type_input, stim_list_input,
                             stim_loc_input, runmodel),
                   WidgetBox(modeltitle, modeldescr, modelregions),
                   #row(viz_source.data['diagnostic'][0].visualize()))
                   #row(myplot.data['diagplots'][0]))
                   row(myplot))
    # Make a tab with the layout
    tab = Panel(child=mylayout, title = 'Choose Model')

    return tab
