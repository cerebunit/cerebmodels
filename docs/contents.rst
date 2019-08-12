Available models
****************
.. toctree::
   :maxdepth: 1
   :caption: Contents:

   models/available_models.rst

How to add models in cerebmodels
********************************
.. toctree::
   :maxdepth: 1
   :caption: Contents:

   template_for_cell_model.rst

How to run models in cerebmodels
********************************
.. toctree::
   :maxdepth: 1
   :caption: Contents:

   quickstart_guide_to_run_model.rst
   notebooks/executing_models_no_stimulation_case1.ipynb
   notebooks/executing_models_stimulation_case2.ipynb
   notebooks/executing_models_capability_case3.ipynb

Code Documentation
******************

ExecutiveControl
================
.. automodule:: executive
   :members:

Code Documentation: Lower level functions
*****************************************

For filing tasks
================

Manager
-------
.. toctree::
   :maxdepth: 1
   :caption: Contents:

   managers/filing.rst

Operators
---------
.. toctree::
   :maxdepth: 1
   :caption: Contents:

   managers/operatorsFiling/crawler.rst
   managers/operatorsFiling/pathspawner.rst

For simulation
==============

Manager
-------
.. toctree::
   :maxdepth: 1
   :caption: Contents:

   managers/simulation.rst

Operators
---------
.. toctree::
   :maxdepth: 1
   :caption: Contents:

   managers/operatorsSimaudit/assembler.rst
   managers/operatorsSimaudit/hardware.rst
   managers/operatorsSimaudit/inspector.rst
   managers/operatorsSimaudit/stimulator.rst

For recording
=============

Manager
-------
.. toctree::
   :maxdepth: 1
   :caption: Contents:

   managers/record.rst

Operators
---------
.. toctree::
   :maxdepth: 1
   :caption: Contents:

   managers/operatorsYield/recorder.rst

For signal processing
=====================

Manager
-------
.. toctree::
   :maxdepth: 1
   :caption: Contents:

   managers/signalprocessing.rst

Operators
---------
.. toctree::
   :maxdepth: 1
   :caption: Contents:

   managers/operatorsSignaling/converter.rst
   managers/operatorsSignaling/reconstructer.rst

For transcribing
================

Manager
-------
.. toctree::
   :maxdepth: 1
   :caption: Contents:

   managers/transcribe.rst

Operators
---------
.. toctree::
   :maxdepth: 1
   :caption: Contents:

   managers/operatorsTranscribe/metadata_filegenerator.rst
   managers/operatorsTranscribe/metadata_timeseriesgenerator.rst
   managers/operatorsTranscribe/metadata_epochgenerator.rst
   managers/operatorsTranscribe/fabricator.rst

For reading saved file (NWB)
============================

Manager
-------
.. toctree::
   :maxdepth: 1
   :caption: Contents:

   managers/read.rst

Operators
---------
.. toctree::
   :maxdepth: 1
   :caption: Contents:

   managers/operatorsReadNWB/epoch_unraveller.rst

Quick reference
===============

+--------------------------------------------+-----------------------------------------+
| Managers                                   | Operators                               |
+============================================+=========================================+
| :ref:`FilingManager`                       | - :ref:`Crawler`                        |
|                                            | - :ref:`PathSpawner`                    |
+--------------------------------------------+-----------------------------------------+
| :ref:`SimulationManager`                   | - :ref:`SimAssembler`                   |
|                                            | - :ref:`HardwareConfigurator`           |
|                                            | - :ref:`SimInspector`                   |
|                                            | - :ref:`Stimulator`                     |
+--------------------------------------------+-----------------------------------------+
| :ref:`RecordManager`                       | - :ref:`Recorder`                       |
+--------------------------------------------+-----------------------------------------+
| :ref:`SignalProcessingManager`             | - :ref:`Converter`                      |
|                                            | - :ref:`Reconstructer`                  |
+--------------------------------------------+-----------------------------------------+
| :ref:`TranscribeManager`                   | - :ref:`FileGenerator`                  |
|                                            | - :ref:`TimeseriesGenerator`            |
|                                            | - :ref:`EpochGenerator`                 |
|                                            | - :ref:`Fabricator`                     |
+--------------------------------------------+-----------------------------------------+
| :ref:`ReadManager`                         | - :ref:`EpochUnraveller`                |
+--------------------------------------------+-----------------------------------------+

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
