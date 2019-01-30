# ~/managers/operatorsVisualize/tabModelResponses.py
from bokeh.plotting import figure
from bokeh.models import (ColumnDataSource, Panel)
from bokeh.models.widgets import (Dropdown, Select, Tabs)
from bokeh.layouts import row, WidgetBox

import os, sys

sys.path.append(os.getcwd()) # when run from ~/cerebmodels

from managers.managerFiling import FilingManager as fm
from reader import Reader

def TabModelResponses():
    ## ==================== Initiator =======================
    def initiate_select_menu(menutype, menulist):
        """initiates Select widgets
        """
        if menutype=="modelscales":
            title = "Modeling Scale Options"
        elif menutype=="modelnames":
            title = "Choose a model"
        elif menutype=="modelresponses":
            title = "Choose a response (file)"
        elif menutype=="modelregions":
            title = "Pick a region"
        elif menutype=="responseepochs":
            title = "Pick an epoch"
        return Select( title=title, value=menulist[0][0], options=menulist )
    ## ====================== END =========================
    #
    ## ==================== Getters =======================
    def get_menu_modelscales():
        menu = [("None", "None")]
        for modelscale in available_modelscales:
            # tag the modelscale as first element in the value = modellist
            modellist = ' '.join( [modelscale] + scale_and_models[modelscale] )
            menu.append( ( modellist, modelscale ) ) # tuple(list of models, scale)
        return menu

    def extract_filenames(modelscale, modelname):
        files = []
        dir_names = ["responses", modelscale, modelname]
        responsepath = fm.responsepath_check_create(list_dir_names=dir_names)
        filesdictionary = fm.show_filenames_with_path(dir_names=dir_names)
        if filesdictionary=="There are no files in the current path.":
            files.append("There_are_no_files")
        else:
            for filename, filepath in filesdictionary.iteritems():
                files.append(filename)
        return files

    def get_menu_models(modellist):
        menu = [("None", "Below are available models")]
        if modellist[1]=="No_Models": #modellist[0]=modelname
            menu[0] = ( 'func call', modellist[1].replace("_"," ") ) #tuple(value, str)
        else:
            for modelname in modellist[1:]:
                extract_filenames( modellist[0], modelname )
                # tag modelscale & modelname as 1st-two elements in value=responselist
                responselist = ' '.join( [modellist[0], modelname] +
                                          extract_filenames(modellist[0],modelname) )
                menu.append( (responselist, modelname) )
        return menu

    def get_menu_responses(responselist):
        menu = [("None", "Below are available responses")]
        if responselist[2]=="There_are_no_files":
            menu[0] = ('func call', responselist[2].replace("_"," "))#tuple(value, str)
        else:
            dir_names = ["responses", responselist[0], responselist[1]]
            for response in responselist[2:]:
                filesdictionary = fm.show_filenames_with_path(dir_names=dir_names)
                # tag modelscale, modelname, filename as 1st-three elements in value=responsepath
                responsepath = ' '.join( [responselist[0], responselist[1],
                                          response, filesdictionary[response]] )
                menu.append( (responsepath, response[20:]) )
        return menu

    def get_menu_regions():
        pass
    def get_menu_epochs():
        pass
    ## ====================== END =========================
    #
    ## ==================== Updaters ======================
    def update_modelslist( attr, old, new ):
        if new=="No_Models":
            model_list = [''.join(list(new))] # ["No Models"]
        else:
            model_list = new.split()
        #print model_list
        models_select.options = get_menu_models(model_list)
        regions_select.disabled = True
        epoch_select.diabled = True

    def update_responseslist( attr, old, new ):
        if new=="There_are_no_files":
            responselist = [''.join(list(new))] # ["There are no files"]
        else:
            responselist = new.split()
        responses_select.options = get_menu_responses(responselist)
        regions_select.disabled = True
        epoch_select.disabled = True

    def update_regionslist_epochslist():
        pass
    def update_epoch_visibility():
        pass
    def update_plotsource():
        pass
    ## ====================== END =========================
    #
    ## ===================== Plot =========================
    def responseplot():
        pass
    def myplot():
        p = figure(plot_width = 600, plot_height = 600,
                   title = 'Example Glyphs',
                   x_axis_label = 'X', y_axis_label = 'Y')
        #squares_x = [1, 3, 4, 5, 8]
        #squares_y = [8, 7, 3, 1, 10]
        #p.square(squares_x, squares_y, size=12)
        return p
    ## ====================== END =========================
    #
    ## ================== Generate Data ===================
    available_modelscales = fm.available_modelscales()
    scale_and_models = {}
    for modelscale in available_modelscales: # get list of models in each scale
        try:
            modelslist = fm.modelscale_inventory(model_scale=modelscale)
        except:
            modelslist = ["No_Models"]
        scale_and_models.update( {modelscale: modelslist} )
    ## ====================== END =========================
    #
    ## ========= Generate Global Data For Plotting ========
    global load_file_params
    load_file_params = {"all_files": None, "all_files_with_paths": None,
                        "filepath": None, "all_regions": None, "picked_regions": None,
                        "total_epochid": None, "picked_epochid": None}
    plotsource = ColumnDataSource(data = {"x_axis": range(10), "y_axis": range(10)})
    ## ====================== END =========================
    #
    ## ================ Initiate Widgets ==================
    modelscales_select = initiate_select_menu( "modelscales", get_menu_modelscales() )
    #
    dummy_model_menu = [('None', "First select a model scale")]
    models_select = initiate_select_menu( "modelnames", dummy_model_menu )
    #
    dummy_response_menu = [('None', "First select a model scale")]
    responses_select = initiate_select_menu( "modelresponses", dummy_response_menu )
    #
    dummy_region_menu = [('None', "Pick a region")]
    regions_select = initiate_select_menu( "modelregions", dummy_region_menu )
    #
    dummy_epoch_menu = [('None', "Select an epoch")]
    epochs_select = initiate_select_menu( "responseepochs", dummy_epoch_menu )
    #
    # DISABLE by DEFAULT
    regions_select.disabled = True
    epochs_select.disabled = True
    ## ====================== END =========================
    #
    ## ================ Widget Interaction ================
    modelscales_select.on_change("value", update_modelslist)
    models_select.on_change("value", update_responseslist)
    #responses_select.on_change("value", update_regionslist_epochslist)
    #regions_select.on_change("value", update_epoch_visibility)
    #epochs_select.on_change("value", update_plotsource)
    ## ====================== END =========================
    #
    ## Setup Controls
    controls = WidgetBox( modelscales_select, models_select, responses_select,
                          regions_select, epochs_select )
    ## Generate Plot
    p = myplot()
    ## Make a tab and return it
    return Panel( child = row(controls, p), title = "Model Responses" )


