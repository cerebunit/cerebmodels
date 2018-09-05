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

import os, sys
pwd = os.getcwd()
rootwd = os.path.dirname(pwd)
#sys.path.append(os.path.dirname(pwd))

#from managers.managerFiling import FilingManager
from executive import ExecutiveControl

ec = ExecutiveControl()

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
        #print new
        #print modelscales_select.value
        #print menu_list
        #print menu_list[0]

    def update_global_model( attr, old, new ):
        ec = ExecutiveControl()
        menu_list = new.split()
        modelscale = menu_list[0] # update global modelscale
        modelname = menu_list[1]  # update glocal modelname
        #print modelscale, modelname 
        chosenmodel = ec.choose_model( modelscale=modelscale,
                                       modelname=modelname )
        #print chosenmodel
        modeltitle.text = chosenmodel.name
        modeldescr.text = chosenmodel.description
        #
        runmodel.disabled = False
        modeltitle.disabled = False
        modeldescr.disabled = False
        #print new
        #print new.split()
        #pass

    def update_stimulation_parameters_input_status( attr, old, new ):
        if new=="no":
            stim_type_input.disabled = True
            stim_list_input.disabled = True
        else:
            stim_type_input.disabled = False
            stim_list_input.disabled = False

    def update_plot( attr, old, new ):
        pass

    #def makeplot( response ):
    #    if response=="test1.txt":
    #        data
    #    else:
    #        data

    def myplot():
        # Create a blank figure with labels
        p = figure(plot_width = 600, plot_height = 600, 
                   title = 'Example Glyphs',
                   x_axis_label = 'X', y_axis_label = 'Y')

        # Example data
        squares_x = [1, 3, 4, 5, 8]
        squares_y = [8, 7, 3, 1, 10]
        circles_x = [9, 12, 4, 3, 15]
        circles_y = [8, 4, 11, 6, 10]

        # Add squares glyph
        p.square(squares_x, squares_y, size = 12, color = 'navy', alpha = 0.6)
        # Add circle glyph
        p.circle(circles_x, circles_y, size = 12, color = 'red')

        return p

    def simulate( attr, old, new ):
        if modelscales_select.value == "No_Models":
            pass
        else:
            modelscale_with_models= [''.join(list(modelscales_select.value))]
            models_with_scale = [''.join(list(models_select.value))]
            modelscale = modelscale_with_models[0]
            modelname = models_with_scale[1]
            chosenmodel = ec.choose_model(modelscale=modelscale, modelname=modelname)
            parameters = ast.literal_eval(runtime_input.value)
            #stimparam = ast.literal_eval(stim_input.value)
            ec.launch_model( parameters = parameters, onmodel = chosenmodel )
                             #stimparameters = stimparam, stimloc = stimloc )
            ec.save_response()
    #
    ### +++++++++++++++++++GENERATE DATA FOR THE OPTIONS MENU++++++++++++++++++
    # available_modelscales -- list
    # scale_and_models -- dictionary with list as key value
    # models_with_filenames -- dictionary with list as key value
    # responses_with_filepaths -- dictionary with string as key value
    ec = ExecutiveControl()
    # Generate Model Info
    #os.chdir("..") # line required for calling ~/managers/bokehtest.py
    #available_modelscales = fm.available_modelscales()
    #os.chdir(rootwd) # for running it from ~/managers
    print rootwd
    available_modelscales = ec.list_modelscales()
    scale_and_models = {}
    for modelscale in available_modelscales: # get list of models in each scale
        try:
            #modelslist = fm.modelscale_inventory(model_scale=modelscale)
            modelslist = ec.list_models(modelscale=modelscale)
        except:
            modelslist = ["No_Models"]
        scale_and_models.update( {modelscale: modelslist} )
    #os.chdir(pwd) # for running it from ~/managers
    #print scale_and_models
    ### ++++++++++++++++++++END GENERATE DATA FOR THE OPTIONS++++++++++++++++++
    #
    ec = ExecutiveControl()
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
    runtime_input = TextInput(value="{'dt': 0.01, 'celsius': 30, 'tstop': 100, 'v_init': 65}",
                           title="Runtime Parameters:")
    print runtime_input.value
    print type(runtime_input.value)
    #
    stimulation_menu = [("No", "no"), None, ("Yes", "yes")]
    stimulation = Dropdown(label="Stimulation Yes/No", button_type="warning",
                           menu=stimulation_menu)
    stim_type_input = TextInput(value="{'type': ['current', 'IClamp']}",
                                title="Stimulation Parameters (Stimulation Type):")
    stim_list_input = TextInput(value="[{'amp': 0.5, 'dur': 10.0, 'delay': 5.0}, "
                                      " {'amp': 1.0, 'dur': 20.0, 'delay': 15.0}]",
                                title="Stimulation Parameters (Stimuli):")
    # disable stimulation by DEFAULT
    stim_type_input.disabled = True
    stim_list_input.disabled = True
    #
    runmodel = Button(label="Run Simulation", button_type="success")
    #
    modeltitle = Div(text="""No Model has been selected yet.""", width=290, height=20)
    modeldescr = Paragraph(text="""Your text is initialized with the 'text' argument.  The remaining Paragraph arguments are 'width' and 'height'. For this example, those values are 200 and 100 respectively. Your text is initialieze with the 'text' argument. The remaining Paragraph arguments are 'width' and 'height'. For this example, those values are 290 and 100 respectively. """, width=290, height=100)
    # disable the model texts by DEFAULT
    modeltitle.disabled = True
    modeldescr.disabled = True
    #
    # INTERACTION
    modelscales_select.on_change("value", update_models_list)
    models_select.on_change("value", update_global_model)
    #responses_select.on_change("value", update_plot)
    stimulation.on_change("value", update_stimulation_parameters_input_status)

    # Put controls in a single element
    #controls = WidgetBox(modelscales_select, models_select, runtime_input, stim_input, runmodel, div)
    #displays = WidgetBox(div)

    p = myplot()
    prof = Profiler()
    rprof = ResourceProfiler()
    # Create a row layout
    #mylayout = row(controls, p)
    #mylayout = row(controls, p)
    #mylayout = layout([[controls, displays]], sizing_mode="stretch_both")
    #modeloptions = WidgetBox(modelscales_select, models_select, runtime_input, stim_input, runmodel)
    #choicedisplay = WidgetBox(div, div, div, div, div)
    #mylayout = row(WidgetBox(modelscales_select, models_select),
    #               WidgetBox(runtime_input, stim_input),
    #               WidgetBox(runmodel, div))
    runmodel.disabled = True
    mylayout = row(WidgetBox(modelscales_select, models_select, runtime_input,
                             stimulation, stim_type_input, stim_list_input, runmodel),
                   WidgetBox(modeltitle, modeldescr),
                   row(visualize([prof, rprof])))
    #mylayout = row(WidgetBox(modelscales_select, models_select, runtime_input, stim_input, runmodel),
    #               WidgetBox(modelscales_select, models_select, runtime_input, stim_input, runmodel))
    #mylayout = row(WidgetBox(modelscales_select, models_select, runtime_input, stim_input, runmodel),
    #               WidgetBox(div, div))

    # Make a tab with the layout
    tab = Panel(child=mylayout, title = 'Choose Model')

    return tab
