# Template for adding cellular models here in cerebmodels

For uploading models in `~/cerebmodels/models/cells/` follow the manadatory steps instructed below.

## The Model Directory (NEURON)

Assuming you already have a model (NEURON), place it in a directory. The structure should be
```
model-directory/
    __init__.py
    Cellname.py
    mod_files/
        contains .mod files
```

Note:

* usually, the filename <Cellname> is as suggested the name of the cell. For instance, `Purkinje.py` for Purkinje cell.
* the class name of `Cellname.py` is `Cellname`
* the main `model-directory/` should have the `__init__.py` file and the `Cellname.py` file which is where the code for the template of the cell is located. Generally, the file name corresponds with the cell name. For instance, for Purkinje cell the file would be `Purkinje.py`. 
* this main `model-directory/` may also have other associated files need for constructing the cell. This will depend on the model.
* the naming of the main `model-directory/` is of the form
  ```<UpperCaseLetters><Year><FirstAuthor>```
such that `<UpperCaseLetters>` are PC for Purkinje Cell, GoC for Golgi Cell and GrC for Granular Cell.
---

## Cell Template

The `Cellname.py` will contain a class whose name is `Cellname`. For instance, 'Purkinje.py` contains `class Purkinje`. The idea of having both cell template and model template is that the original model is undisturbed or minimaly edited in the 'cell template'.

Note:

* no setup for recording should be made here
* comment out, if the source file have lines for recording (say time and voltages). Hint: this usually takes place under `__init__` method.
---

## Model Template

The model directory will be in `~/cerebmodels/models/cells/ABYearXYZ`. In the directory above the model directory, you must have a python script (the model template). The naming structure is
```
model<UpperCaseLetters>< Year><FirstAuthor>.py;
```
Also, in the "`__init__.py`" located in "`~/cerebmodels/models/cells/__init__.py`" make sure to add
```
import model<UpperCaseLetters><Year><FirstAuthor> as <UpperCaseLetters><Year><FirstAuthor>
```

The `modelABYearXYZ.py` will contain a class whose name is `<Cellname>Cell`. That is, the word 'Cell' appended at the end of the <Cellname> of the cell-template. For instance, 'modelPC2015Masoli.py` contains `class PurkinjeCell`. At the start of this template first import
```
from managers.managerSimulation import SimulationManager
from models.cells.ABYearXYZ.Cellname import Cellname
```
Then under `def __init__`
```
### =====================Instantiate the cell======================
self.cell = Cellname()
# ------specify cell-regions from with response are recorded-------
self.regions = {<region_name1>: <float>, <region_name2>: <float>}
### ===============================================================
#
### =====================Essential Attributes======================
self.modelscale = "cells"
self.modelname = "ABYearXYZ"
# -----------attributed inheritance from sciunit.Model-------------
self.name = "XYZ et al. Year model of <Cellname>Cell"
self.description = "a brief description of the model"
### ===============================================================
#
self.sm = SimulationManager()
```

NOTE:

* if the import was `from models.cells.PC2015Masoli.Purkinje import Purkinje` then
  ```self.cell = Purkinje()```
* `self.regions` must be a dictionary in the form key = "region-name" and its value = threshold for considering spike, i.e, value = 0.0 implies if &geq; 0.0 then spike.
* the key name (region-name) should correspond to those used/defined within the cell template. For instance, in the cell-template `~/cells/DummyTest/Dummy.py` we have
  ```
  self.soma = h.Section('soma')
  self.axon = h.Section('axon')
  #self.dendrite = h.Section('dendrite')
  ```
Therefore, the `self.regions` in the corresponding model-template `~/cells/modelDummyTest.py` will look like
  ```
  self.regions = {self.cell.soma: 0.0, self.cell.axon: 0.0}
  ```
Notice that dendrite is not a region because it is not in the cell-template. However, `self.regions` does not have to include all the the NEURON sections. For instance it is prefectly fine for the `self.regions` in the model-template `~/cells/modelDummyTest.py` to be like
  ```
  self.regions = {self.cell.soma: 0.0}
  ```
Its upto the user what he/she wants to do with the model.
* generally, `float=0.0` which means that the membrane voltage taken from the respective `self.regions` 'whenever' required to transform them to spike-trains (zeros & ones) takes 0.0mV as the threshold for considering spike.
---
