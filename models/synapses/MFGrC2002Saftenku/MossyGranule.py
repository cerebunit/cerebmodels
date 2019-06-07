#Template of the Mossy fiber to Granule cell (soma), Saftenku 2002
#Templating by Lungsi 2019 based on ~/MFGrC2002Saftenku/start.hoc, ltpd.hoc and mossy.hoc
from neuron import h
#from pdb import set_trace as breakpoint

class MossyGranule(object):
    """Single compartment Granule soma connected to 4 Mossy fibre
    """
    def __init__(self):
        h("objref cvode")    # initialize multiple order variable time step
        h("cvode = new CVode()") # integration method as it is called in hoc file
        h.xopen("start.hoc")

        # nsyn1 = 4 at line 11
        # ncells = 1 at line 79
        # nmossy = 4 at line 80
        # Notice that one should try to have nmossy = nsyn1 =/= NumSyn (synapse/MF)
        self.cell = h.GrCell[0] # len(h.GrCell) -> 1
        self.mossy = h.Mossy    # len(h.Mossy) -> 4

        # ========================== How to Access ============================
        # xxxxxxxxxx FOR RECORDING
        # ---- Soma Voltage
        # self.cell.soma, and
        # self.cell.soma.v
        # ---- Autophosphorylation protein levels
        # self.cell.ltp1[0].Np for LTP or h.GrCell[0].ltp1[0].Np
        # self.cell.ltp1[0].Nd for LTD or h.GrCell[0].ltp1[0].Nd
        #self.autophos_protein_level_ltp = self.cell.ltp1[0].Np
        #self.autophos_protein_level_ltd = self.cell.ltp1[0].Nd
        # ---- Mossy spikes (inputs for GrC soma)
        # self.mossy[i].pp.y
        #
        # xxxxxxxxxx FOR PARAMETERS
        # ---- LTP/D settings                                defaults
        # h.LTP_gamma    -for-> h.GrCell[0].ltp1[0].gamma    0.34 /ms
        # h.LTP_eta      -for-> h.GrCell[0].ltp1[0].eta      0.003 /ms
        # h.LTP_nu1      -for-> h.GrCell[0].ltp1[0].nu1      0.065 /ms
        # h.LTP_nu2      -for-> h.GrCell[0].ltp1[0].nu2      0.065 /ms
        # h.LTP_pp       -for-> h.GrCell[0].ltp1[0].pp       9.5e-6 /ms
        # h.LTP_pd       -for-> h.GrCell[0].ltp1[0].pd       0.00019 /ms
        # h.LTP_gdel1    -for-> h.GrCell[0].ltp1[0].gdel1    2.4 /nA /ms
        # h.LTP_gdel2    -for-> h.GrCell[0].ltp1[0].gdel2    2.4 /nA /ms
        # h.LTP_Mp       -for-> h.GrCell[0].ltp1[0].Mp       3e-5 nA /ms
        # h.LTP_Md       -for-> h.GrCell[0].ltp1[0].Md       0.0003 nA /ms
        # h.LTP_Ap       -for-> h.GrCell[0].ltp1[0].Ap       1.625 nA^2
        # h.LTP_Ad       -for-> h.GrCell[0].ltp1[0].Ad       0.55 nA^2
        # h.ampa_freqdel -for-> h.GrCell[0].ampa[0].freqdel  0.579 /nA
        # h.nmda_freqdel -for-> h.GrCell[0].nmda[0].freqdel  0.579 /nA
        # h.Tau_rec      -for-> h.GrCell[0].syn1[0].taurec   3 ms
        # h.Tau_facil    -for-> h.GrCell[0].syn1[0].taufacil 800 ms
        # h.Tau_1        -for-> h.GrCell[0].syn1[0].tauin     20 ms
        # WHENEVER you make any of the above changes RUN h.UpDateLTP()
        # UpDateLTP() is a function defined in ltpd.hoc loaded in start.hoc
        #
        # ---- Mossy spike settings                     meaning            defaults
        # h.t01     -for-> h.Mossy[i].pp.t01            first spike        20
        # h.t02     -for-> h.Mossy[i].pp.t02            last spike         4.2e5
        # h.InSpike -for-> h.Mossy[i].pp.fast_freq      inter-spike freq   100 Hz
        # h.InBurst -for-> h.Mossy[i].pp.slow_freq      inter-burst freq   4 Hz
        # h.Spikes  -for-> h.Mossy[i].pp.APinburst      spikes/burst       10
        # h.StartIn -for-> h.Mossy[i].pp.startbursting  Start at time      2000 ms
        # h.EndIn   -for-> h.Mossy[i].pp.endbursting    End at time        3000 ms
        # h.Noise   -for-> h.Mossy[i].pp.noise          Poisson noise      0 (=> No)
        #                  h.NumSyn                     no.synapse/MF      2
        # These will be set for all MF (nmossy = 4), to do this
        # you MUST RUN h.UpDateMossy(). This function is defined in mossy.hoc
        # also loaded in start.hoc
