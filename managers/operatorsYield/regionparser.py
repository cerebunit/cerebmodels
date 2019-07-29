# ~/managers/operatorsYield/regionparser.py
#import numpy as np
#from random import randint

#from neuron import h

class RegionParser(object):
    """
    ** Available methods:**

    +-------------------------------------------------+------------------------+
    | Method name                                     | Method type            |
    +=================================================+========================+
    | :py:meth:`.get_regionkeylist`                   | static method          |
    +-------------------------------------------------+------------------------+
    | :py:meth:`.get_componentgrouplist`              | static method          |
    +-------------------------------------------------+------------------------+
    | :py:meth:`.get_regionlist_of_componentgroup`    | static method          |
    +-------------------------------------------------+------------------------+
    | :py:meth:`.get_componentlist`                   | static method          |
    +-------------------------------------------------+------------------------+

    """

    @staticmethod
    def get_regionlist(chosenmodel):
        """Returns an array (NEURON's ``h.Vector``) of recorded time.

        **Arguments:** No arguments

        **Returned value:** ``h.Vector`` of recorded times (time-axis). `More about this data type. <https://www.neuron.yale.edu/neuron/static/new_doc/programming/math/vector.html>`_

        **Use case:**

        ``>> rc = Recorder()``

        ``>> rec_t = rc.time_NEURON()``

        """
        regionlist = list(chosenmodel.regions.keys())
        [ regionlist.remove(key) for key in regionlist
                                    if type(chosenmodel.regions[key]) is dict ]
        return regionlist

    @staticmethod
    def get_componentgrouplist(chosenmodel):
        """Returns an array (NEURON's ``h.Vector``) of recorded time.

        **Arguments:** No arguments

        **Returned value:** ``h.Vector`` of recorded times (time-axis). `More about this data type. <https://www.neuron.yale.edu/neuron/static/new_doc/programming/math/vector.html>`_

        **Use case:**

        ``>> rc = Recorder()``

        ``>> rec_t = rc.time_NEURON()``

        """
        componentgrouplist = list(chosenmodel.regions.keys())
        [ componentgrouplist.remove(key) for key in componentgrouplist
                                    if type(chosenmodel.regions[key]) is not dict ]
        return componentgrouplist

    @staticmethod
    def get_regionlist_of_componentgroup(chosenmodel, componentgroup_name):
        """Returns an array (NEURON's ``h.Vector``) of recorded time.

        **Arguments:** No arguments

        **Returned value:** ``h.Vector`` of recorded times (time-axis). `More about this data type. <https://www.neuron.yale.edu/neuron/static/new_doc/programming/math/vector.html>`_

        **Use case:**

        ``>> rc = Recorder()``

        ``>> rec_t = rc.time_NEURON()``

        """
        return list(chosenmodel.regions[componentgroup_name].keys())

    @staticmethod
    def get_componentlist(chosenmodel, componentgroup_name, region_name):
        return list( chosenmodel.regions[componentgroup_name][region_name].keys() )

