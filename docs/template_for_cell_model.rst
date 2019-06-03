Template for adding cellular models here in cerebmodels
*******************************************************
**For uploading models in `~/cerebmodels/models/cells/`, i.e., follow the manadatory steps instructed below.**

The Model Directory (NEURON)
============================
Assuming you already have a model (NEURON), place it in a directory. The structure should be

::

   model-directory/
       __init__.py
       Cellname.py
       mod_files/
           contains .mod files

The main ``model-directory/`` should have the ``__init__.py`` file and the ``Cellname.py`` file which is where the code for the template of the cell is located. This main ``model-directory/`` may also have other associated files need for constructing the cell. This will depend on the model.

*Recommendations:*

* the naming of the main ``model-directory/`` is of the form
  ``<UpperCaseLetters><Year><FirstAuthor>``
such that ``<UpperCaseLetters>`` are the initials: **PC** for Purkinje Cell, **GoC** for Golgi Cell and **GrC** for Granular Cell.'
* it is recommended that the filename ``Cellname.py`` be the name of the cell. For instance, ``Purkinje.py`` for Purkinje cell.
* the class name for ``Cellname.py`` is ``Cellname``

1. Cell Template
================
The ``Cellname.py`` will contain a class whose name is ``Cellname``. For instance, ``Purkinje.py`` contains ``class Purkinje``. The idea of having both cell template and model template is that the original model is undisturbed or minimaly edited in the 'cell template'.

*Note:*

* no setup for recording should be made here
* comment out, if the source file have lines for recording (say time and voltages). Hint: this usually takes place under ``__init__`` method.

2. Model Template
=================
The model directory will be in ``~/cerebmodels/models/cells/ABYearSmith/``.

Above the model directory (i.e., in ``~/cerebmodels/models/cells/``), there should be a python script (the model template). The naming structure is
``
model<UpperCaseLetters>< Year><FirstAuthor>.py;
``
The ``modelABYearSmith.py`` will contain a class whose name is ``<Cellname>Cell``. That is, suffix *Cell* to the <Cellname> (name of the class in the cell-template; as mentioned above the cell-template has the same name for file name and class name). For instance, 'modelPC2015Masoli.py` contains ``class PurkinjeCell``. Follow the steps below to construct the model template.

2.1 Import modules
------------------

2.1.1 Setup path to the model of interest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Assuming one is interested in the the model, i.e., model directory ``ABYearSmith/`` containing the template ``Cellname.py``, the first step is to set the path to the model.

::

   import os
   pwd = os.getcwd()
   path_to_files = pwd + os.sep + "models" + os.sep + "cells" + os.sep + <ABYearSmith> + os.sep

2.1.2 Make available modules within ``CerebModels`` needed to execute the simulation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
After setting up the path to the model libraries at the start of the ``ABYearSmith.py`` file, now import

::

   from models.cells.ABYearSmith.Cellname import Cellname
   from executive import ExecutiveControl
   from managers.simulation import SimulationManager as sm
   from managers.read import ReadManager as rm

And depending on the *capability* (see below) of the cell
``
from managers.signalprocessing import SignalProcessingManager as spm
``

2.1.3 Import `SciUnit <https://github.com/scidash/sciunit>`_ module and the particular *capability* the model will have
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   import sciunit
   from cerebunit.capabilities.cells.<capability-category> import <BrandCategory>

where ``<capability-category>`` is a category of a capability which in turn is the class ``<BrandCategory>``. Details on how to implement a capability is given below.

Note that, depending on the model it may have more than one capability.

2.1.4 Passing the capabilities into the class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Finally, our ``modelABYearSmith.py`` will have a class named ``<Cellname>Cell`` inheriting the required capabilities.
``
class <Cellname>Cell( sciunit.Model, <BrandCategory1>, <BrandCategory2> ):
``
Details on how to implement tha capability(s) is given below.

2.2 Model UUID (optional)
-------------------------
Although it is not mandatory to set a uuid, if one intends to assign a uuid it is recommended to do it above the constructor ``__init__`` method.
``
uuid = "some-12134234-id"
``
This is a mandatory step if one intends to validate the model via the `HBP Validation Framework_<https://github.com/HumanBrainProject/hbp-validation-client>`_. After the model is registered to the HBP Validation Framework Model catalog, it assigns a uuid. This generated uuid will be the value for above.

2.3 Setting up the constructor ``__init__``
-------------------------------------------

2.3.1 Descriptive attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   self.modelscale = "cells"
   self.modelname = "ABYearSmith"
   # --------------specify cell-regions from with response are recorded----------------
   self.regions = {<region_name1>: <float>, <region_name2>: <float>}
   # -------------------attribute inheritance from sciunit.Model----------------------
   self.name = "Smith et al. Year model of <Cellname>Cell"
   self.description = "a brief description of the model"

Notice that the value for the ``.modelname`` attribute is also the name of the directory ``ABYearSmith/`` which has the cell template ``<Cellname>.py``.

2.3.2 Instantiating the cell template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   ### =============================Instantiate the cell===============================
   sm.lock_and_load_model_libraries(modelscale=self.modelscale, modelname=self.modelname)
   os.chdir(path_to_files) # temporarily change directory to model directory
   self.cell = Cellname()  # instantiate the model
   os.chdir(pwd)           # revert back to default directory ~/cerebmodels

2.3.3 Prediction attribute
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   self.fullfilename = "nil"
   self.prediction = "nil"

2.4 Defining model capability method(s)
---------------------------------------
Following the constructor method a model template can have any number of desired methods, each representing a capability of the model. For e.g., ``produce_voltage_response``. What is critical is that the **__method name__ should be same as the method in its corresponding <BrandCategory>**.

Once the method name is consistent with the inherited ``<BrandCategory>`` capability one may write it however one wants, tailored to the validation test in `CerebUnit <https://github.com/myHBPwork/cerebunit>`_ that would call it.

However, below is a template for how might go about writing it.

2.4.1 An independent method
~~~~~~~~~~~~~~~~~~~~~~~~~~~
For cases when the capability is not dependent on another capability of the same model, e.g., ``produce_voltage_response``.

::

   def capability_a(self, **kwargs):
       emode="capability")c = ExecutiveControl() # only works when in ~/cerebmodels
       model = ec.launch_model( parameters = kwargs["parameters"],
                                stimparameters = kwargs["stimparameters"],
                                stimloc = kwargs["stimloc"],
                                onmodel = kwargs["onmodel"], mode = "raw" )
       model.fullfilename = ec.save_response()
       # setattr(model, "fullfilename", ec.save_response()) # alternative
       return model

Note that the method passes the argument ``mode = "raw"``. Also, notice that variable keyword arguments are passes. This is due to the implementation of ``lock_and_loac_capability()`` in :ref:`SimulationManager`. Among the keyword arguments, ``"parameters"`` and ``"onmodel"`` keys are mandatory.

2.4.2 A dependent method
~~~~~~~~~~~~~~~~~~~~~~~~

::

   def capability_b(self, **kwargs):
       ec = ExecutiveControl() # only works when in ~/cerebmodels
       model = ec.launch_model( parameters = kwargs["parameters"],
                                stimparameters = kwargs["stimparameters"],
                                stimloc = kwargs["stimloc"], onmodel = kwargs["onmodel"],
                                capabilities = {"model": "capability_a",
                                                "vtest": ProducesElectricalResponse},
                                mode="capability" )
       # Perform processing here
       nwbfile = rm.load_nwbfile(model.fullfilename)
       ...
       some_measure = spm.<some_method>( <corresponding_argument(s)> )
       setattr(model, "prediction", some_measure)
       #
       return model

Unlike ``capability_a``, the argument ``mode = "capability"`` is used (because ``launch_model`` will be invoking another capability). The comments on keyword arguments made above also applies here. Note that since most of the work of actually simulating the model is performed by the capability that this (capability) is depending on, ``ec.save_response()`` is not invoked here.


COMMENTS
--------

* if the import was ``from models.cells.PC2015Masoli.Purkinje import Purkinje`` then
  ``self.cell = Purkinje()``
* ``self.regions`` must be a dictionary in the form key = "region-name" and its value = threshold for considering spike, i.e, value = 0.0 implies if &geq; 0.0 then spike.
* the key name (region-name) should correspond to those used/defined within the cell template. For instance, in the cell-template ``~/cells/DummyTest/Dummy.py`` we have
  
  ::

     self.soma = h.Section('soma')
     self.axon = h.Section('axon')
     #self.dendrite = h.Section('dendrite')

Therefore, the ``self.regions`` in the corresponding model-template ``~/cells/modelDummyTest.py`` will look like
  ``
  self.regions = {'soma': 0.0, 'axon': 0.0}
  ``
Notice that dendrite is not a region because it is not in this cell-template. However, ``self.regions`` does not have to include all the the NEURON sections. For instance it is prefectly fine for the ``self.regions`` in the model-template ``~/cells/modelDummyTest.py`` to be like
  ``
  self.regions = {'soma': 0.0}
  ``
Its upto the user what he/she wants to do with the model.

* it is good practice to have both the name of the section (eg soma inside ``h.Section('soma')``) and name of the cell attribute be the same (eg, soma in ``self.soma``). The keys in ``self.regions`` are the cell attribute name. Therefore, the key 'soma' in ``self.regions`` corresponds to "soma" of ``self.soma`` NOT "soma" in ``h.Section('soma')``.
* generally, ``float=0.0`` which means that the membrane voltage taken from the respective ``self.regions`` *whenever* required to transform them to spike-trains (zeros & ones) takes 0.0mV as the threshold for considering spike.
* The :ref:`SimulationManager` is deployed from the model template so as to load the ``nmodl`` files before instantiating the cell-template. This is done by calling ``lock_and_load_model_libraries()``
* If the cell-template requires loading custom files (generally located in same directory as the cell-template) required for its constructing then you must temporarily change the current working directory to the directory location of the cell-template. Then instantiate the cell-template and once done return to default working directory. Therefore, this change of directory is not necessary if the cell-template does not require loading any configuration files for its template.
