# ../managers/managerFiling.py
import os

from managers.operatorsFiling.crawler import Crawler
from managers.operatorsFiling.pathspawner import PathSpawner

class FilingManager(object):

    def __init__(self):
        self.cr = Crawler()
        self.ps = PathSpawner()

    def available_modelscales(self):
        """method that returns a list of available model_scale.

        Arguments:
        No arguments

        Returned value:
        list of model scales (directory names)

        Raised Exceptions:
        ValueError if there are no model_scale

        Use case:
        fm = FilingManager()
        fm.available_modelscales()

        """

        search_in_path = os.getcwd() + os.sep + "models"
        scale_dirs = self.cr.list_dirs(search_path = search_in_path)
        if not scale_dirs:
            raise ValueError("There are no model_scale")
        else:
            return scale_dirs

    def modelscale_inventory(self, model_scale=None):
        """method that returns a list of available model for given model_scale.

        Keyword arguments:
        model_scale -- string; egs. "cells", "microcircuits", "networks"

        Returned value:
        list of model names (model directory names)

        Raised exceptions:
        ValueError if the given model_scale is not listed
        ValueError if the model_scale has no models.

        Use case:
        fm = FilingManager()
        fm.modelscale_inventory(model_scale="cells")

        """

        modelscale_path = os.getcwd() + os.sep + "models" + os.sep + model_scale
        if not os.path.isdir(modelscale_path):
            raise ValueError("This model_scale is currently not listed.")
        else:
            model_dirs = self.cr.list_dirs(search_path = modelscale_path)
            if not model_dirs:
                raise ValueError("There is no inventory for the given model_scale")
            else:
                return model_dirs

    def get_responsepath_check_create(self, list_dir_names):
        """this method is called by responsepath_check_create() below.
        """
        try:
            path = self.cr.path_to_dir(dir_names = list_dir_names)
            return path
        except:
            path = self.ps.hatch_path_to_response(modelscale=list_dir_names[1],
                                                  modelname=list_dir_names[-1])
            os.makedirs(path)
            return path

    def responsepath_check_create(self, list_dir_names=None, chosenmodel=None):
        """method that returns path to the reponse.

        Keyword argument: list_dir_names OR chosenmodel
        list_dir_names -- list of three string;
                          Eg. ['responses', chosenmodel.modelscale, chosenmodel.modelname]
                          this is equivalent to
                              ['responses', 'cells', 'DummyTest']
        chosenmodel -- instantiated model

        Returned value:
        path (string) -- ~/cerebmodel/responses/cells/DummyTest

        Raised exceptions:
        ValueError if the argument list_dir_names is not of the form ['responses', 'cells', 'DummyTest']

        Use case:
        fm = FilingManager()
        fm.responsepath_check_create(list_dir_names=['responses', 'cells', 'DummyTest'])
        OR
        fm.responsepath_check_create( chosenmodel = DummyTest() )

        """

        if ((list_dir_names is None) or (len(list_dir_names)!=3)) and (chosenmodel is None):
            raise ValueError("The argument must be a three-string list, eg ['responses', chosenmodel.modelscale, chosenmodel.modelname] OR chosenmodel must be an instantiated model.")
        elif chosenmodel is not None:
            dir_names = ['responses', chosenmodel.modelscale, chosenmodel.modelname]
            return self.get_responsepath_check_create(dir_names)
        elif (list_dir_names is not None) or (len(list_dir_names)==3):
            return self.get_responsepath_check_create(list_dir_names)
