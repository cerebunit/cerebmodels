# ~/managers/operatorsVisualize/tabModelResponses.py
from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool, 
			  ColumnDataSource, Panel, 
			  FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider,
                                  Dropdown, Select,
				  Tabs, CheckboxButtonGroup, 
				  TableColumn, DataTable, Select)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

import os, sys
pwd = os.getcwd()
rootwd = os.path.dirname(pwd)
#sys.path.append(os.path.dirname(os.path.dirname(pwd)))

from managers.managerFiling import FilingManager as fm

def TabModelResponses():
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
            menu[0] = ( 'func call', modellist[1].replace("_"," ") )#tuple (scale, string of models)
        else:
            for modelname in modellist[1:]:
                # tag modelscale & modelname as 1st-two elements in the value = responselist
                responselist = ' '.join( [modellist[0], modelname] +
                                         responses_with_filenames[modellist[0]][modelname] )
                menu.append( (responselist, modelname) ) # tuple (string of models, scale)
        return menu

    def get_menu_responses(responselist):
        menu = [("None", "Below are available responses")]
        if responselist[2]=="There_are_no_files":
            menu[0] = ('func call', responselist[2].replace("_"," "))#tuple (scale, string of models)
        else:
            modelscale = responselist[0]
            modelname = responselist[1]
            for response in responselist[2:]:
                # tag modelscale, modelname, filename as 1st-three elements in the value
                response_value = ' '.join(
                                 [modelscale, modelname, response,
                                  responses_with_filepaths[modelscale][modelname][response]] )
                menu.append( (response_value, response) ) # tuple (scale, string of models)
                print response_value
            menu.append( ('select_all', "Sellect All") )
        return menu

    def update_models_list( attr, old, new ):
        if new == "No_Models":
            menu_list = [''.join(list(new))] # ["No Models"]
        else:
            menu_list = new.split()
        models_select.options = get_menu_models(menu_list)

    def update_responses_list( attr, old, new ):
        if new == "There_are_no_files":
            menu_list = [''.join(list(new))] # ["No Responses"]
        else:
            menu_list = new.split()
        responses_select.options = get_menu_responses(menu_list)

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

    ### +++++++++++++++++++GENERATE DATA FOR THE OPTIONS MENU++++++++++++++++++
    # available_modelscales -- list
    # scale_and_models -- dictionary with list as key value
    # models_with_filenames -- dictionary with list as key value
    # responses_with_filepaths -- dictionary with string as key value
    os.chdir(rootwd)
    # Generate Model Info
    #os.chdir("..") # line required for calling ~/managers/bokehtest.py
    available_modelscales = fm.available_modelscales()
    scale_and_models = {}
    for modelscale in available_modelscales: # get list of models in each scale
        try:
            modelslist = fm.modelscale_inventory(model_scale=modelscale)
        except:
            modelslist = ["No_Models"]
        scale_and_models.update( {modelscale: modelslist} )
    #print scale_and_models
    # Gather all the response files for respective models
    responses_with_filenames = {}
    responses_with_filepaths = {}
    files = []
    for modelscale, modellist in scale_and_models.iteritems():
        if modellist[0]=="No_Models":
            alevel1_key_value = {"No_Models": "nil"}
            blevel1_key_value = {"No_Models": "nil"}
        else:
            alevel1_key_value = {}
            blevel1_key_value = {}
            for model in modellist:
                dir_names = ["responses", modelscale, model]
                responsepath = fm.responsepath_check_create(list_dir_names=dir_names)
                filesdictionary = fm.filenames_with_path(dir_names=dir_names)
                if filesdictionary=="There are no files in the current path.":
                    alevel2_key_value = {model: ["There_are_no_files"]}
                else:
                    for filename, filepath in filesdictionary.iteritems():
                        files.append(filename)
                    alevel2_key_value = {model: files}
                alevel1_key_value.update( alevel2_key_value )
                blevel1_key_value.update( {model: filesdictionary} )
        responses_with_filenames.update( {modelscale: alevel1_key_value} )
        responses_with_filepaths.update( {modelscale: blevel1_key_value} )
        #print responses_with_filenames
        #print responses_with_filepaths
    os.chdir(pwd)
    ### ++++++++++++++++++++END GENERATE DATA FOR THE OPTIONS++++++++++++++++++
    #
    menu = get_menu_modelscales()
    modelscales_select = get_select_menu( "modelscales", menu )
    #
    dummy_model_menu = [('None', "First select a model scale")]
    models_select = get_select_menu( "models", dummy_model_menu )
    #
    dummy_response_menu = [('None', "First select a model scale")]
    responses_select = get_select_menu( "responses", dummy_response_menu )
    #
    # INTERACTION
    modelscales_select.on_change("value", update_models_list)
    models_select.on_change("value", update_responses_list)
    #responses_select.on_change("value", update_plot)

    # Put controls in a single element
    controls = WidgetBox(modelscales_select, models_select, responses_select)

    p = myplot()
    # Create a row layout
    layout = row(controls, p)

    # Make a tab with the layout
    tab = Panel(child=layout, title = 'Model Responses')

    return tab
