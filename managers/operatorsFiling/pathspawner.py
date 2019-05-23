# ~/managers/operatorsFiling/pathspawner.py
import os

class PathSpawner(object):
    """
    **Available methods:**

    +-----------------------------------+----------------------+
    | Method name                       | Method type          |
    +-----------------------------------+----------------------+
    | :py:meth:`hatch_path_to_nmodl`    | static method        |
    +-----------------------------------+----------------------+
    | :py:meth:`hatch_path_to_response` | static method        |
    +-----------------------------------+----------------------+

    *NOTE*:

    * ``hatch_path_to_nmodl`` returns path/to/the/directory/mod_files and path/to/the/file/libnrnmech.so.0
    * ``hatch_path_to_response`` returns path/to/the/directory/responses/<modelscale>/<modelname>

    """

    @staticmethod
    def hatch_path_to_nmodl(modelscale=None, modelname=None):
        """Hatches path to directory "mod_files" and file ``libnrnmech.so.0``

        **Keyword Arguments:**

        +------------------+---------------------------------------------------+
        | Key              | Value type                                        |
        +------------------+---------------------------------------------------+
        | ``model_scale``  | string; egs. "cells", "microcircuits", "networks" |
        +------------------+---------------------------------------------------+
        | ``model_name``   | string; "XY2000Author"                            |
        +------------------+---------------------------------------------------+

        **Returned values:**

        * ``path/to/the/directory/mod_files``
        * ``path/to/the/file/libnrnmech.so.0``

        **Raised Exceptions:** ``ValueError`` if modelscale and modelname is empty.

        """

        if modelscale is not None and modelname is not None:
            model_path = os.getcwd() + os.sep + "models" + os.sep + modelscale + os.sep + modelname
            mod_path = model_path + os.sep + "mod_files"
            lib_path = model_path + os.sep + "x86_64" + os.sep + ".libs" + os.sep + "libnrnmech.so.0"
            return mod_path, lib_path
        else:
            raise ValueError("Give a modelscale and modelname.")

    @staticmethod
    def hatch_path_to_response(modelscale=None, modelname=None):
        """Hatches path to directory ~/responses/<modelscale>/<modelname>"

        **Keyword Arguments:**

        +------------------+---------------------------------------------------+
        | Key              | Value type                                        |
        +------------------+---------------------------------------------------+
        | ``model_scale``  | string; egs. "cells", "microcircuits", "networks" |
        +------------------+---------------------------------------------------+
        | ``model_name``   | string; "XY2000Author"                            |
        +------------------+---------------------------------------------------+

        **Returned values:** ``path/to/the/directory/responses/<modelscale>/<modelname>``

        **Raised Exceptions:** ``ValueError`` if modelscale and modelname is empty.

        """

        if modelscale is not None and modelname is not None:
            return os.getcwd() + os.sep + "responses" + os.sep + modelscale + os.sep + modelname
        else:
            raise ValueError("Give a modelscale and modelname.")
