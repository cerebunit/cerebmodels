# ../managers/managerSimulate.py
import os

from operatorsFiling.crawler import Crawler

class SimManager(object):

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

        """

        search_in_path = os.getcwd() + os.sep + "models"
        scale_dirs = self.cr.list_dirs(search_path = search_in_path)
        if not scale_dirs:
            raise ValueError("There are no model_scale")
        else:
            return scale_dirs
