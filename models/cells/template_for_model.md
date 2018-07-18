# Template for adding cellular models here in cerebmodels

For uploading models in `~/cerebmodels/models/cells/` follow the manadatory steps instructed below.

## The Model Directory (NEURON)

Assuming you already have a model (NEURON), place it in a directory. The structure should be
```
directory/
    __init__.py
    Cellname.py
    mod_files/
        contains .mod files
```

Note:

    * the main `directory/` should have the `__init__.py` file and the `Cellname.py` file which is where the code for the template of the cell is located. Generally, the file name corresponds with the cell name. For instance, for Purkinje cell the file would be `Purkinje.py`. 
    * this main `directory/` may also have other associated files need for constructing the cell. This will depend on the model.
    * the naming of the main `directory/` is of the form
      ```
      &lt;UpperCaseLetters&gt;&lt;Year&gt;&lt;FirstAuthor&gt;
      ```
      such that `<UpperCaseLetters>` are PC for Purkinje Cell, GoC for Golgi Cell and GrC for Granular Cell.
---

## Cell Template

The `Cellname.py` will contain a class whose name is `Cellname`. For instance, 'Purkinje.py` contains `class Purkinje`. At the end of the template
```
### ====== STANDARDIZED FOR cerebmodels =======
### ===== mandatory for all NEURON models =====
self.rec_t = h.Vector()
self.rec_t.record(h._ref_t)
# ------- this will be the cell-regions -------
self.region_name = h.Vector()
self.region_name.record(self.soma(0.5)._ref_v)
```

Note:

    * this is usually placed at the bottom of the `__init__` method.
    * `h` implies `neuron.h`
    * the name of the cell-region is assigned by the designer. For example,
      ```
      self.vm_soma = h.Vector()
      self.vm_soma.record(self.soma(0.5)._ref_v)
      ```
    * for time being recorded the attribute name must all be named `rec_t`. This is to enforce a standard name here for cerebmodels.
---

## Model Template

The model directory will be in `~/cerebmodels/models/cells/ABYearXYZ`. In the directory above the model directory, you must have a python script (the model template). The naming structure is
```
model &lt; UpperCaseLetters &gt; &lt; Year &gt; &lt; FirstAuthor &gt;
```
Also, in the "`__init__.py`" located in "`~/cerebmodels/models/cells/__init__.py`" make sure to add
```
import model&lt;UpperCaseLetters&gt;&lt;Year&gt;&lt;FirstAuthor&gt; as &lt;UpperCaseLetters&gt;&lt;Year&gt;&lt;FirstAuthor&gt;
```

The `modelABYearXYZ.py` will contain a class whose name is `&lt;Cellname&gt;Cell`. For instance, 'modelPC2015Masoli.py` contains `class PurkinjeCell`. At the start of this template first import
```
from managers.managerSimulation import SimulationManager
from models.cells.ABYearXYZ.Cellname import Cellname
```
Then under `def __init__`
```
### =====================Instantiate the cell======================
self.cell = Cellname()
# ------specify cell-regions from with response are recorded-------
self.cell_regions = {region_name1: float, region_name2: float}
### ===============================================================
#
### =====================Essential Attributes======================
self.modelscale = "cells"
self.modelname = "ABYearXYZ"
# -----------attributed inheritance from sciunit.Model-------------
self.name = "XYZ et al. Year model of &lt;Cellname&gt;Cell"
self.description = "a brief description of the model"
### ===============================================================
#
self.sm = SimulationManager()
```

NOTE:

    * if the import was `from models.cells.PC2015Masoli.Purkinje import Purkinje` then
      ```self.cell = Purkinje()```
    * `self.cell_regions` must be a dictionary in the form key = "region-name" and its value = threshold for considering spike, i.e, value = 0.0 implies if &geq; 0.0 then spike.
    * the key name (region-name) should correspond to those used/defined within the cell template. For example, we had `vm_soma` in `~/cells/PC2015Masoli/Purkinje.py` therefore the file `~/cells/modelPC2015Masoli.py` must have
      ```
      self.cell_regions = {"vm_soma": float}
      ```
---
