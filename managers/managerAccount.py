# ../managers/managerAccount.py
import os

from managers.operatorsFiling.crawler import Crawler

class AccountManager(object):

    def __init__(self):
        self.cr = Crawler()

    def available_modelscales(self):
        """method that returns a list of available model_scale.

        Arguments:
        No arguments

        Returned value:
        list of model scales (directory names)

        Raised Exceptions:
        ValueError if there are no model_scale

        Use case:
        am = AccountManager()
        am.available_modelscales()

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
        sm = SimManager()
        sm.modelscale_inventory(model_scale="cells")

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
