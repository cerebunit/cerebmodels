A Quick Start Guide To Running Models in Cerebmodels
****************************************************

Before proceeding it should be pointed out that CerebUnit is based on Python3 and no longer supports Python2.7.

1. Set-up
=========

1.1. Getting cerebmodels and cerebunit (cerebtests)
---------------------------------------------------

* For obvious reasons getting `cerebmodels <https://github.com/cerebunit/cerebmodels>`_ is essential for following the steps given below.
* To get cerebmodels do ``git clone https://github.com/cerebunit/cerebmodels.git``.
* Although, not essential to install `cerebunit <https://github.com/cerebunit/cerebtests>`_ especially if you have not intention to run validation tests it is **recommended to install cerebunit**.
* To install cerebunit do ``pip install git+https://github.com/cerebunit/cerebtests.git``.

1.2. Set working directory to the root of ``~/cerebmodels/``
------------------------------------------------------------

* To do this in console terminal or jupyter notebook do ``cd cerebmodels``.

1.3. Import ``ExecutiveControl`` of cerebmodels
-----------------------------------------------

``from executive import ExecutiveControl as ec``

2. Search for models and picking a model
========================================

Apart from going through the sub-directories of cerebmodels and searching for models, the ``ExecutiveControl`` can provide them to you.

2.1. Get model scales
---------------------

Models available in cerebmodels ranges across various modelling scales, from sub-cellular models, cellular models to network models. So, to see the modelling scales available in the current cerebmodels do

::

   ec.list_modelscale()

2.2. Get available models for a particular scale
------------------------------------------------

Based on the model scale currently available within cerebmodels one can get the list of available model for that particular scale with

::

   ec.list_models( modelscale = <string> )

For example ``ec.list_models( mdoelscale = "cells" )`` will return the list of available models for "cells."

2.3. Picking a desired model
----------------------------

To choose a desired model for a particular model scale, one has to call

::

   ec.choose_model( modelscale = <string>, modelname = <string> )

An example is ``desired_model = ec.choose_model( modelscale = "cells", modelname = "PC2003Khaliq" )``.

3. Launching (executing) the desired model
==========================================


3.1. Setting the parameters
---------------------------

Let us consider three scenarios:

1. launch without stimulation
2. launch with stimulation
3. launch with capability

The first two examples will be demonstrated with "raw" launch, i.e., launching without capability. The third example with "capability"; note that it may also be launched with or without stimulation, but with capability. Here, capability with stimulation will be the example.

3.1.1. Parameters for case-1 (without stimulation)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Only one set of parameter is needed for this scenario, the run-time parameters. Say,

``runtimeparam_c1 = { "dt": 0.025, "celsius": 37, "tstop": 500, "v_init": -65 }``

3.2. Executing the model
------------------------

The following commands for respective three scenarios

for scenario 1

::

   exc1 = ExecutiveControl()
   desired_model_c1 = exc1.launch_model( parameters = runtimeparam_c1,
                                         onmodel = desired_model )

which is the same as

::

   desired_model_c1 = exc1.launch_model( parameters = runtimeparam_c1,
                                         onmodel = desired_model,
u                                        mode = "raw" )
`ram_c1 = { "dt": 0.025, "celsius": 37, "tstop": 500, "v_init": -65 }`exc = ExecutiveControl``


for scenario 2

::

   exc2 = ExecutiveControl()
   desired_model_c2 = exc2.launch_model( parameters = runtimeparam_c2,
                                         onmodel = desired_model,
                                         stimparameters = stimparam,
                                         stimloc = desired_model.soma )

for scenario 3

::

   exc3 = ExecutiveControl()
   desired_model_c3 = exc3.launch_model( parameters = runtimeparam_c3,
                                         onmodel = desired_model,
                                         stimparameters = stimparam,
                                         stimloc = desired_model.soma,
                                         capabilities = {"model": "produce_soma_restVm",
                                                         "vtest": ProducesEphysMeasurement},
                                         mode = "capability" )

3.3. Saving the responses
-------------------------

The ``ExecutiveControl`` for cerebmodels can also save response. It saves it in a `HDF5 file (.h5 extension) <https://www.hdfgroup.org/solutions/hdf5/>`_. The file is saved based on `NWB 2.0 <https://www.nwb.org/how-to-use/>`_ scheme.

To save response the required response is ``excN.save_response()``. Thus, for the each of the above three scenarios just replace the ``N`` with 1, 2 or 3 as shown below

* ``desired_model_c1.fullfilename = exc1.save_response()``
* ``desired_model_c2.fullfilename = exc2.save_response()``
* ``desired_model_c3.fullfilename = exc3.save_response()``

4. Visualizing the response
===========================

4.1. List available model regions
---------------------------------

::

   ec.list_modelregions( chosenmodel = desired_model )

4.2. Visualize all events (defined by epochs)
---------------------------------------------

::

   ec.visualize_all( chosenmodel = desired_model, roi = "soma v" )

4.3. Visualize all events in one plot
-------------------------------------

::

   ec.visualize_aio( chosenmodel = desired_model, roi = "soma v" )
