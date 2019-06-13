# ~/models/microcircuits/VOR2014Clopath/VOR.py
#
# This is the Python template of VOR.m
# Conversion by Lungsi 2019
#
"""
+--------------------------------------+------------+---------------+
|Parameter(p); variable(v)             | VOR.m      | VOR.py        |
+======================================+============+===============+
|mean eye movement (p)                 | Dmean      | d_mean        |
+--------------------------------------+------------+---------------+
|simulation start time (p)             | previous_t | t_start       |
+--------------------------------------+------------+---------------+
|stimulation time (p) [unit of cycles] | Simul_t    | t_simul       |
+--------------------------------------+------------+---------------+
|time of a cycle [ms]                  | T_pat      | T_ms          |
+--------------------------------------+------------+---------------+
|light condition (p)                   | light      | light         |
+--------------------------------------+------------+---------------+
|target gain (p)                       | gain       | gain          |
+--------------------------------------+------------+---------------+
|number of GrC (p)                     | N_inp      | num_GrC       |
+--------------------------------------+------------+---------------+
|vestibular component (ratio) in CF (p)| cf_vest    | vest_CF       |
+--------------------------------------+------------+---------------+
|initial wt GrC to PC (p)              | win        | w_ini_GrCPC   |
+--------------------------------------+------------+---------------+
|weights from GrC to PC (v)            | w_GP       | w_GrCPC       |
+--------------------------------------+------------+---------------+
|weight from the In to PC (p)          | w_IP       | w_InPC        |
+--------------------------------------+------------+---------------+
|weight from MF to D (MVN cell) (p)    | w_MD       | w_MFD         |
+--------------------------------------+------------+---------------+
|learning rate for w_GrCPC (p)         | alphai     | alpha_l_GrCPC |
+--------------------------------------+------------+---------------+
|forgetting rate for w_GrCPC (p)       | alphaf     | alpha_f_GrCPC |
+--------------------------------------+------------+---------------+
|learning rate for w_MFD (p)           | alphad     | alpha_l_MFD   |
+--------------------------------------+------------+---------------+
|lower bound plasticity GrC to PC (p)  | BL         | low_GrCPC     |
+--------------------------------------+------------+---------------+
|upper bound plasticity GrC to PC (p)  | BH         | up_GrCPC      |
+--------------------------------------+------------+---------------+
|firing rates of GrC (v)               | G          | GrC           |
+--------------------------------------+------------+---------------+
|firing rate of In (p)                 | In         | In            |
+--------------------------------------+------------+---------------+
|baseline firing rate of PC (p)        | Pmean      | PCmean        |
+--------------------------------------+------------+---------------+
|mean firing rate of MF (p)            | Mmean      | MFmean        |
+--------------------------------------+------------+---------------+
|firing rate of MF (p)                 | MF         | MF            |
+--------------------------------------+------------+---------------+
|mean firing rate of D (p)             | Dmean      | Dmean         |
+--------------------------------------+------------+---------------+
|delay in firing rate of CF (p) [ms]   | delay      | delay_CF      |
+--------------------------------------+------------+---------------+
|noise in firing rate of CF (p)        | noise      | noise_CF      |
+--------------------------------------+------------+---------------+
|time of night (p) [unit of cycles]    | nit        | t_of_night    |
+--------------------------------------+------------+---------------+

"""
import numpy as np

class VOR(object):

    def __init__( self, runtimeparams=None, populparams=None,
                  signalparams=None, weightparams=None ):
        # DEFAULT PARAMETERS
        #self.T_ms = int( np.floor(1000/0.6) )
        self.T_ms = int(runtimeparam["T_ms"]) 
        # Initialize
        # initial weight from Granule cells to Purkinje cells
        self.w_ini_GrCPC = 1.85/populparam["num_GrC"]
        # weights from Granule cells to Purkinje cells, num_GrC x 1
        self.w_GrCPC = self.w_in * np.ones( (populparam["num_GrC"], 1) )
        #
        # Granule cells, num_GrC x T_ms
        GrC = np.zeros( (int(populparam["num_GrC"]), int(runtimeparam["T_ms"])) )
        self.GrC = self._generate_firing_rate_GrC( GrC )
        #
        # weight from Interneuron to Purkinje cells 1 x 1 
        self.w_InPC = np.array(weightparam["w_InPC"]).reshape(1,1)
        #
        # Interneuron 1 x T_ms
        In = (2.5/populparam["num_GrC"]) * np.sum(self.GrC, axis=0) # T_ms x 0
        self.In = (In - np.mean(In) + 0.85).reshape(1, len(In))
        #
        # Purkinje cells (baseline firing rate)
        self.PCmean = (self.w_GrCPC.conj().T @ self.GrC) - (self.w_InPC.conj().T @ self.In)
        #
        # Mossy fibers 1 x T_ms
        self.MFmean = signalparam["MFmean"]
        self.MF = ( 0.25 *
                    np.cos( np.arange( 1+self.T_ms*3/4, (self.T_ms+self.T_ms*3/4)+1 )
                            * 2*np.pi/self.T_ms ) + self.MFmean ).reshape(1, int(self.T_ms))
        #
        # weight from initial MF to MVN
        self.w_MFD = weightparam["w_MFD"]
        #
        # mean firing rate of MVN cell
        #self.Dmean = signalparam["Dmean"]
        #

    def _generate_firing_rate_GrC(self, GrC):
        "Private function called during initialization"
        num_GrC = len(GrC)
        # distribution of GrC firing at certain phases num_GrC x 0
        dist = 0.1886 * np.cos( np.arange( 1+num_GrC, 2*num_GrC + 1 )
                                * 2*np.pi/num_GrC ) \
               + ( np.arange( 1, num_GrC+1 ) * 2*np.pi/num_GrC )
        for i in range(len(self.GrC)):
            GrC[i,:] = np.cos( np.arange( 1+self.T_ms, 2*self.T_ms+1 )
                               * 2*np.pi/self.T_ms - dist[i] ) + 1 # T_ms x 0
        return GrC # num_GrC x T_ms

    def run(self, runtimeparams=None, populparams=None, signalparams=None, weightparams=None):
        "Tuneable parameters:

        - runtimeparams['t_start'], runtimeparams['t_simul'],
        - runtimeparams['light'], runtimeparams['gain']
        - populparams['vest_CF']
        - signalparams['Dmean'], signalparams['delay_CF'], signalparams['noise_CF']
        - weightparams['alpha_l_GrCPC'], weightparams['alpha_f_GrCPC']
        - weightparams['low_GrCPC'], weightparams['up_GrCPC']
        - weightparams['alpha_l_MFD']
        "
        t_start = int(runtimeparams["t_start"])
        t_stop = t_start + int( runtimeparams["t_simul"] )
        # Target MVN output, target D 1 x T_ms
        Dt = (runtimeparams["gain"] * 0.25 * \
              np.cos( np.arange( 1+self.T_ms*3/4, (self.T_ms+self.T_ms*3/4)+1 )
                      * 2*np.pi/self.T_ms ) + 1).reshape(1, int(self.T_ms))
        #
        for t in range( t_start, t_stop + 1 ): # +1 to include t_stop
            # Purkinje cells 1 x T_ms
            PC = (self.w_GrCPC.conj().T @ self.GrC) + (self.w_InPC.con().T @ self.In)
            # MVN, medial vestibular nuclei cells 1 x T_ms
            D = self.w_MFD * 2*(self.MF - self.MFmean) + signalparams["Dmean"] - self.MF - PC
            # Climbing fibers 1 x T_ms
            CF = runtimeparams["light"] * (Dt - D) \
                 +  populparams["vest_CF"] * (self.MF - self.Mmean)
            CF = np.roll( CF, [0, signalparams["delay_CF"]] )
            self.w_GrCPC = self._GrC_to_PC_plasticity( CF, weightparams, signalparams )
            self.w_MFD   = self._MF_to_D_plasticity( PC, weightparams )

    def _GrC_to_PC_plasticity(self, CF, weightparams, signalparams):
        "Private function called during running the model"
        num_GrC = len(w_GrCPC)
        w_GrCPC = self.w_GrCPC + \
                  (weightparams["alpha_l_GrCPC"] * (-1) *
                    np.sum(
                       ( ( np.ones((num_GrC, 1)) @ CF ) +
                         ( signalparam["noise_CF"] * np.random.rand(num_GrC, self.T_ms) ) )
                       * self.GrC , 1 ) # axis=1 => sum across columns
                   ).reshape(num_GrC,1) # reshape to maintain num_GrC x 1
        w_GrCPC = (w_GrCPC - weightparams["low_GrCPC"]/num_GrC) * \
                  ((w_GrCPC - weightparams["low_GrCPC"]/num_GrC) < 0).astype(int) + \
                  weightparams["low_GrCPC"]/num_GrC
        w_GrCPC = (w_GrCPC - weightparams["up_GrCPC"]/num_GrC) * \
                  ((w_GrCPC - weightparams["up_GrCPC"]/num_GrC) < 0).astype(int) + \
                  weightparams["up_GrCPC"]/num_GrC
        w_GrCPC = w_GrCPC + \
                  weightparams["alpha_f_GrCPC"] * (self.w_ini_GrCPC - w_GrCPC)
        return w_GrCPC.reshape(num_GrC,1) # num_GrC x 1

    def _MF_to_D_plasticity(self, PC, weightparams):
        "Private function called during running the model"
        w_MFD = self.w_MFD + \
                weightparams["alpha_l_MFD"] * np.sum( (-self.MF + self.MFmean)
                                                      * (PC - self.PCmean) )
        w_MFD = w_MFD * (w_MFD > 0).astype(int)
        return w_MFD # scalar
