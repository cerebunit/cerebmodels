# ~/models/layers/modelGL2011Souza.py
import os
pwd = os.getcwd() # record root directory path ~/cerebmodels
path_to_files = pwd + os.sep + "models" + os.sep + "layers" + os.sep + \
                "GL2011Souza" + os.sep # record path to this model/folder

from models.layers.GL2011Souza.Granule import Granule
from executive import ExecutiveControl

import sciunit

class GranuleLayer( sciunit.Model, ):
    """Text
    """

    # AFTER the model is in the HBP Validation Framework Model Catalog, set the generated uuid
    # for e.g. uuuid = "22dc8fd3-c62b-4e07-9e47-f5829e038d6d"

    def __init__(self):
        ### ===================== Descriptive Attributes ======================
        self.modelscale = "layers"
        self.modelname = "GL2011Souza"
        # ------specify regions from which response are recorded-------
        self.regions = {"GrC": "soma", "GoC": "soma", "MF": "spiketimes"}
        # -----------attributed inheritance from sciunit.Model--------------
        self.name = "Souza & Schutter 2011 model of Granule Layer"
        self.description = "Souza & Schutter 2011 model of Granule Layer (GL) and published in 10.1186/2042-1001-1-7 This model comprises 8100 GrCs, 225 GoCs and 900 MFs. This model is the SciUnit wrapped version of the NEURON model in modelDB accession # 139646."
        #
        ### =================== Instantiate cell template ====================
        sm.lock_and_load_model_libraries(modelscale=self.modelscale,
                                         modelname=self.modelname)
        os.chdir(path_to_files)
        self.layer = Granule()
        os.chdir(pwd)
        #
        self.produce_spike_train = self.produce_voltage_response()

    def produce_voltage_response(self):
        return "DummyTest model just finished run for produce_voltage_response"

    def produce_spike_train(self):
        return "DummyTest model just finished run for produce_spike_train"
