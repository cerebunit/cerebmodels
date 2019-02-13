Code Changes for cerebmodels:
- all the mod files are moved to the created /mod_file directory
- Granule.py is the python translation of grc.hoc
- For the sake of consistency 'del' in Grc_sine.mod is changed to
  'delay'.

Readme file for the model associated with

D'Angelo E, Nieus T, Maffei A, Armano S, Rossi P, Taglietti V, 
Fontana A, Naldi G (2001) Theta-frequency bursting and resonance 
in cerebellar granule cells: experimental evidence and modeling
of a slow k+-dependent mechanism. J Neurosci 21:759-70

Abstract:
Neurons process information in a highly nonlinear manner,
generating oscillations, bursting, and resonance, enhancing
responsiveness at preferential frequencies. It has been proposed
that slow repolarizing currents could be responsible for
both oscillation/burst termination and for high-pass filtering
that causes resonance (Hutcheon and Yarom, 2000). However,
different mechanisms, including electrotonic effects (Mainen
and Sejinowski, 1996), the expression of resurgent currents
(Raman and Bean, 1997), and network feedback, may also be
important. In this study we report theta-frequency (3-12 Hz)
bursting and resonance in rat cerebellar granule cells and show
that these neurons express a previously unidentified slow repolarizing
K1 current (IK-slow ). Our experimental and modeling
results indicate that IK-slow was necessary for both bursting and
resonance. A persistent (and potentially a resurgent) Na current
exerted complex amplifying actions on bursting and resonance,
whereas electrotonic effects were excluded by the compact
structure of the granule cell. Theta-frequency bursting and
resonance in granule cells may play an important role in determining
synchronization, rhythmicity, and learning in the
cerebellum.

Key words: bursting; resonance; M-current; cerebellum;
granule cell; modeling

Basic Model Use:
Expand archive file.  Use mknrndll (windows, mac) or nrnivmodl (unix)
to compile the mod files.  Start nrngui and load the mosinit.hoc
file to see a couple of traces from figure 6A in the paper.

Clicking on the Kinetics, Cell, or Electrodes buttons allow the
changing of these simulation parameters.
