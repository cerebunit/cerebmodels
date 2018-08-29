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

The `modelABYearXYZ.py` will contain a class whose name is `<Cellname>Cell`. That is, the word 'Cell' appended at the end of the <Cellname> of the cell-template. For instance, 'modelPC2015Masoli.py` contains `class PurkinjeCell`. At the start of this template first setup the path for loading the libraries of the model.
```
import os
pwd = os.getcwd()
path_to_files = pwd + os.sep + "models" + os.sep + "cells" + os.sep + \
                <ABYearXYZ> + os.sep
```
Notice that `modelABYearXYZ.py` contains the model/class `ABYearXYZ`. The cell template is located in the directory with same name as the class name. For instance, 'modelPC2015Masoli.py` with the model class name 'PC2015Masoli()` must load the model libraries located in '~/cerebmodels/models/cells/PC2015Masoli/`.

After setting up the path to the model libraries at the start of the 'modelPC2015Masoli.py` file, now import
```
from managers.managerSimulation import SimulationManager
from models.cells.ABYearXYZ.Cellname import Cellname

sm = SimulationManager()
```
Then under `def __init__`
```
### ==============================Essential Attributes==============================
# --------------specify cell-regions from with response are recorded----------------
self.regions = {<region_name1>: <float>, <region_name2>: <float>}
#
self.modelscale = "cells"
self.modelname = "ABYearXYZ"
# -------------------attributed inheritance from sciunit.Model----------------------
self.name = "XYZ et al. Year model of <Cellname>Cell"
self.description = "a brief description of the model"
### ================================================================================
#
### =============================Instantiate the cell===============================
sm.si.lock_and_load_nmodl(modelscale=self.modelscale, modelname=self.modelname)
os.chdir(path_to_files) # temporarily change directory to model directory
self.cell = Cellname()  # instantiate the model
os.chdir(pwd)           # revert back to default directory ~/cerebmodels
### ================================================================================
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
  self.regions = {'soma': 0.0, 'axon': 0.0}
  ```
Notice that dendrite is not a region because it is not in the cell-template. However, `self.regions` does not have to include all the the NEURON sections. For instance it is prefectly fine for the `self.regions` in the model-template `~/cells/modelDummyTest.py` to be like
  ```
  self.regions = {'soma': 0.0}
  ```
Its upto the user what he/she wants to do with the model.
* it is good practice to have both the name of the section (eg soma inside `h.Section('soma'`) and name of the cell attribute be the same (eg, soma in `self.soma`). The keys in `self.regions` are the cell attribute name. Therefore, the key 'soma' in `self.regions` corresponds to 'soma' of `self.soma` NOT 'soma' in `h.Section('soma').
* generally, `float=0.0` which means that the membrane voltage taken from the respective `self.regions` 'whenever' required to transform them to spike-trains (zeros & ones) takes 0.0mV as the threshold for considering spike.
* The SimulationManager is deployed from the model template so as to load the `nmodl` files before instantiating the cell-template.
* If the cell-template requires loading custom files (generally located in same directory as the cell-template) required for its constructing then you must temporarily change the current working directory to the directory location of the cell-template. Then instantiate the cell-template and once done return to default working directory. Therefore, this change of directory is not necessary if the cell-template does not require loading any configuration files for its template.
---
