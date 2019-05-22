# ../managers/managerFiling.py
import os

from managers.operatorsFiling.crawler import Crawler as cr
from managers.operatorsFiling.pathspawner import PathSpawner as ps

class FilingManager(object):
    """
    **Available methods:**

    +------------------------------------------+----------------------+
    | Method name                              | Method type          |
    +==========================================+======================+
    | :py:meth:`available_modelscales`         | static method        |
    +------------------------------------------+----------------------+
    | :py:meth:`modelscale_inventory`          | static method        |
    +------------------------------------------+----------------------+
    | :py:meth:`get_responsepath_check_create` | static method        |
    +------------------------------------------+----------------------+
    | :py:meth:`responsepath_check_create`     | class method         |
    +------------------------------------------+----------------------+

    """

    def __init__(self):
        #self.cr = Crawler()
        #self.ps = PathSpawner()
        pass

    @staticmethod
    def available_modelscales():
        """Returns a list of available model_scale.

        **Arguments:** No arguments

        **Returned value:** list of model scales (directory names)

        **Raised Exceptions:** ``ValueError`` if there are no ``model_scale``

        **Use case:**

        ``>> fm = FilingManager()``

        ``>> fm.available_modelscales()``

        """

        search_in_path = os.getcwd() + os.sep + "models"
        scale_dirs = cr.list_dirs(search_path = search_in_path)
        if not scale_dirs:
            raise ValueError("There are no model_scale")
        else:
            return scale_dirs

    @staticmethod
    def modelscale_inventory(model_scale=None):
        """Returns a list of available model for given ``model_scale``.

        **Keyword argument:**

        +-------------+--------------------------------------------------+
        | Key         | Value type                                       |
        +=============+==================================================+
        | model_scale | string; egs. "cells", "microcircuits", "networks"|
        +-------------+--------------------------------------------------+

        **Returned value:** list of model names (model directory names)

        **Raised exceptions:**

        * ``ValueError`` if the given ``model_scale`` is not listed
        * ``ValueError`` if the ``model_scale`` has no models.

        **Use case:**

        ``>> fm = FilingManager()``

        ``>> fm.modelscale_inventory(model_scale="cells")``

        """

        modelscale_path = os.getcwd() + os.sep + "models" + os.sep + model_scale
        if not os.path.isdir(modelscale_path):
            raise ValueError("This model_scale is currently not listed.")
        else:
            model_dirs = cr.list_dirs(search_path = modelscale_path)
            if not model_dirs:
                raise ValueError("There is no inventory for the given model_scale")
            else:
                return model_dirs

    @staticmethod
    def get_responsepath_check_create(list_dir_names):
        """:ref:`Crawler` operator checks for the response path (if it already exists). Otherwise a reponse path is created by the :ref:`PathSpawner` operator. Regardless, the response is returned. The path is of the form ``~/cerebmodels/responses/<model_scale>/<model_name>/``.

        **Argument:** list of string elements of the form ``["responses", "<model_scale>", "<model_name>"]``.

        *NOTE:* ``['responses', chosenmodel.modelscale, chosenmodel.modelname]`` is equivalent to ``['responses', 'cells', 'DummyModel']``.

        This is called by :py:meth: ``.responsepath_check_create()``.
        """
        try:
            path = cr.path_to_dir(dir_names = list_dir_names)
            return path
        except:
            path = ps.hatch_path_to_response(modelscale=list_dir_names[1],
                                             modelname=list_dir_names[-1])
            os.makedirs(path)
            return path

    @classmethod
    def responsepath_check_create(cls, list_dir_names=None, chosenmodel=None):
        """Returns path to the reponse.

        **Keyword argument:**

        +--------------------+----------------------------+
        | Key                | Value type                 |
        +====================+============================+
        | ``list_dir_names`` | list of three strings      |
        | **or**             |                            |
        | ``chosenmodel``    | instantiated model         |
        +--------------------+----------------------------+

        **Returned value:** path (string) `` ~/cerebmodel/responses/<model_scale>/<model_name>``

        **Raised exceptions:** ``ValueError`` if the argument ``list_dir_names`` is not of the form ``["responses", "<model_scale>", "<model_name>"]``

        **Use case:**

        ``>> fm = FilingManager()``

        Then,

        ``>> fm.responsepath_check_create(list_dir_names=["responses", "cells", "DummyModel"])``

        OR

        ``>> fm.responsepath_check_create( chosenmodel = DummyModel() )``

        """

        if ((list_dir_names is None) or (len(list_dir_names)!=3)) and (chosenmodel is None):
            raise ValueError("The argument must be a three-string list, eg ['responses', chosenmodel.modelscale, chosenmodel.modelname] OR chosenmodel must be an instantiated model.")
        elif chosenmodel is not None:
            dir_names = ['responses', chosenmodel.modelscale, chosenmodel.modelname]
            return cls.get_responsepath_check_create(dir_names)
        elif (list_dir_names is not None) or (len(list_dir_names)==3):
            return cls.get_responsepath_check_create(list_dir_names)

    @staticmethod
    def show_filenames_with_path(dir_names):
        """This is identical to ``show_files`` method of :ref:`Crawler`

        **Returned Value:** dictionary whose *key* is the filename and its filepath is the *value*.
        """
        return cr.show_files(dir_names=dir_names)
