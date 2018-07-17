# ~/models/cells/modelDummyTest.py

class DummyTest(object):

    def __init__(self):
        self.modelscale = "cells"
        self.modelname = "DummyTest"

    def produce_voltage_response(self):
        return "DummyTest model just finished run for produce_voltage_response"

    def produce_spike_train(self):
        return "DummyTest model just finished run for produce_spike_train"
