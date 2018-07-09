# ~/executive.py
import importlib

from managers.managerAccount import AccountManager

class ExecutiveControl(object):

    def __init__(self):
        self.am = AccountManager()
        self.modelscale = None
        self.modelname = None

    def list_modelscales(self):
        return self.am.available_modelscales()

    def list_models(self, modelscale=None):
        return self.am.modelscale_inventory(model_scale=modelscale)
