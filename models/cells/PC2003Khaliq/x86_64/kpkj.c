/* Created by Language version: 7.7.0 */
/* NOT VECTORIZED */
#define NRN_VECTORIZED 0
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "scoplib_ansi.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__kpkj
#define _nrn_initial _nrn_initial__kpkj
#define nrn_cur _nrn_cur__kpkj
#define _nrn_current _nrn_current__kpkj
#define nrn_jacob _nrn_jacob__kpkj
#define nrn_state _nrn_state__kpkj
#define _net_receive _net_receive__kpkj 
#define rates rates__kpkj 
#define states states__kpkj 
 
#define _threadargscomma_ /**/
#define _threadargsprotocomma_ /**/
#define _threadargs_ /**/
#define _threadargsproto_ /**/
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 static double *_p; static Datum *_ppvar;
 
#define t nrn_threads->_t
#define dt nrn_threads->_dt
#define gkbar _p[0]
#define ik _p[1]
#define m _p[2]
#define h _p[3]
#define ek _p[4]
#define Dm _p[5]
#define Dh _p[6]
#define _g _p[7]
#define _ion_ek	*_ppvar[0]._pval
#define _ion_ik	*_ppvar[1]._pval
#define _ion_dikdv	*_ppvar[2]._pval
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  -1;
 /* external NEURON variables */
 /* declaration of user functions */
 static void _hoc_htau_func(void);
 static void _hoc_mtau_func(void);
 static void _hoc_rates(void);
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static const char* nmodl_file_text;
static const char* nmodl_filename;
extern void hoc_reg_nmodl_text(int, const char*);
extern void hoc_reg_nmodl_filename(int, const char*);
#endif

 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _p = _prop->param; _ppvar = _prop->dparam;
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 "setdata_kpkj", _hoc_setdata,
 "htau_func_kpkj", _hoc_htau_func,
 "mtau_func_kpkj", _hoc_mtau_func,
 "rates_kpkj", _hoc_rates,
 0, 0
};
#define htau_func htau_func_kpkj
#define mtau_func mtau_func_kpkj
 extern double htau_func( double );
 extern double mtau_func( double );
 /* declare global and static user variables */
#define hik hik_kpkj
 double hik = 11.2;
#define hivh hivh_kpkj
 double hivh = -5.802;
#define hiA hiA_kpkj
 double hiA = 0.78;
#define hiy0 hiy0_kpkj
 double hiy0 = 0.31;
#define htau htau_kpkj
 double htau = 0;
#define hinf hinf_kpkj
 double hinf = 0;
#define mtk2 mtk2_kpkj
 double mtk2 = -23.1;
#define mtvh2 mtvh2_kpkj
 double mtvh2 = -56;
#define mtk1 mtk1_kpkj
 double mtk1 = 12.9;
#define mtvh1 mtvh1_kpkj
 double mtvh1 = 100.7;
#define mty0 mty0_kpkj
 double mty0 = 0.00012851;
#define mik mik_kpkj
 double mik = 15.4;
#define mivh mivh_kpkj
 double mivh = -24;
#define mtau mtau_kpkj
 double mtau = 0;
#define minf minf_kpkj
 double minf = 0;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "mivh_kpkj", "mV",
 "mik_kpkj", "1",
 "mtvh1_kpkj", "mV",
 "mtk1_kpkj", "1",
 "mtvh2_kpkj", "mV",
 "mtk2_kpkj", "1",
 "hivh_kpkj", "mV",
 "hik_kpkj", "1",
 "mtau_kpkj", "ms",
 "htau_kpkj", "ms",
 "gkbar_kpkj", "mho/cm2",
 "ik_kpkj", "mA/cm2",
 0,0
};
 static double delta_t = 0.01;
 static double h0 = 0;
 static double m0 = 0;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "mivh_kpkj", &mivh_kpkj,
 "mik_kpkj", &mik_kpkj,
 "mty0_kpkj", &mty0_kpkj,
 "mtvh1_kpkj", &mtvh1_kpkj,
 "mtk1_kpkj", &mtk1_kpkj,
 "mtvh2_kpkj", &mtvh2_kpkj,
 "mtk2_kpkj", &mtk2_kpkj,
 "hiy0_kpkj", &hiy0_kpkj,
 "hiA_kpkj", &hiA_kpkj,
 "hivh_kpkj", &hivh_kpkj,
 "hik_kpkj", &hik_kpkj,
 "minf_kpkj", &minf_kpkj,
 "mtau_kpkj", &mtau_kpkj,
 "hinf_kpkj", &hinf_kpkj,
 "htau_kpkj", &htau_kpkj,
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(_NrnThread*, _Memb_list*, int);
static void nrn_state(_NrnThread*, _Memb_list*, int);
 static void nrn_cur(_NrnThread*, _Memb_list*, int);
static void  nrn_jacob(_NrnThread*, _Memb_list*, int);
 
static int _ode_count(int);
static void _ode_map(int, double**, double**, double*, Datum*, double*, int);
static void _ode_spec(_NrnThread*, _Memb_list*, int);
static void _ode_matsol(_NrnThread*, _Memb_list*, int);
 
#define _cvode_ieq _ppvar[3]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"kpkj",
 "gkbar_kpkj",
 0,
 "ik_kpkj",
 0,
 "m_kpkj",
 "h_kpkj",
 0,
 0};
 static Symbol* _k_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 8, _prop);
 	/*initialize range parameters*/
 	gkbar = 0.004;
 	_prop->param = _p;
 	_prop->param_size = 8;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 4, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_k_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0]._pval = &prop_ion->param[0]; /* ek */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* ik */
 	_ppvar[2]._pval = &prop_ion->param[4]; /* _ion_dikdv */
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _kpkj_reg() {
	int _vectorized = 0;
  _initlists();
 	ion_reg("k", -10000.);
 	_k_sym = hoc_lookup("k_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 8, 4);
  hoc_register_dparam_semantics(_mechtype, 0, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 kpkj /home/cereb/cerebmodels/models/cells/PC2003Khaliq/mod_files/kpkj.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int rates(double);
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[2], _dlist1[2];
 static int states(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 () {_reset=0;
 {
   rates ( _threadargscomma_ v ) ;
   Dm = ( minf - m ) / mtau ;
   Dh = ( hinf - h ) / htau ;
   }
 return _reset;
}
 static int _ode_matsol1 () {
 rates ( _threadargscomma_ v ) ;
 Dm = Dm  / (1. - dt*( ( ( ( - 1.0 ) ) ) / mtau )) ;
 Dh = Dh  / (1. - dt*( ( ( ( - 1.0 ) ) ) / htau )) ;
  return 0;
}
 /*END CVODE*/
 static int states () {_reset=0;
 {
   rates ( _threadargscomma_ v ) ;
    m = m + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / mtau)))*(- ( ( ( minf ) ) / mtau ) / ( ( ( ( - 1.0 ) ) ) / mtau ) - m) ;
    h = h + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / htau)))*(- ( ( ( hinf ) ) / htau ) / ( ( ( ( - 1.0 ) ) ) / htau ) - h) ;
   }
  return 0;
}
 
static int  rates (  double _lVm ) {
   double _lv ;
 _lv = _lVm + 11.0 ;
   minf = 1.0 / ( 1.0 + exp ( - ( _lv - mivh ) / mik ) ) ;
   mtau = ( 1000.0 ) * mtau_func ( _threadargscomma_ _lv ) ;
   hinf = hiy0 + hiA / ( 1.0 + exp ( ( _lv - hivh ) / hik ) ) ;
   htau = 1000.0 * htau_func ( _threadargscomma_ _lv ) ;
    return 0; }
 
static void _hoc_rates(void) {
  double _r;
   _r = 1.;
 rates (  *getarg(1) );
 hoc_retpushx(_r);
}
 
double mtau_func (  double _lv ) {
   double _lmtau_func;
 if ( _lv < - 35.0 ) {
     _lmtau_func = ( 3.4225e-5 + .00498 * exp ( - _lv / - 28.29 ) ) * 3.0 ;
     }
   else {
     _lmtau_func = ( mty0 + 1.0 / ( exp ( ( _lv + mtvh1 ) / mtk1 ) + exp ( ( _lv + mtvh2 ) / mtk2 ) ) ) ;
     }
   
return _lmtau_func;
 }
 
static void _hoc_mtau_func(void) {
  double _r;
   _r =  mtau_func (  *getarg(1) );
 hoc_retpushx(_r);
}
 
double htau_func (  double _lVm ) {
   double _lhtau_func;
 if ( _lVm > 0.0 ) {
     _lhtau_func = .0012 + .0023 * exp ( - .141 * _lVm ) ;
     }
   else {
     _lhtau_func = 1.2202e-05 + .012 * exp ( - pow( ( ( _lVm - ( - 56.3 ) ) / 49.6 ) , 2.0 ) ) ;
     }
   
return _lhtau_func;
 }
 
static void _hoc_htau_func(void) {
  double _r;
   _r =  htau_func (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static int _ode_count(int _type){ return 2;}
 
static void _ode_spec(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  ek = _ion_ek;
     _ode_spec1 ();
  }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 2; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _ode_matsol1 ();
 }
 
static void _ode_matsol(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  ek = _ion_ek;
 _ode_matsol_instance1(_threadargs_);
 }}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_k_sym, _ppvar, 0, 0);
   nrn_update_ion_pointer(_k_sym, _ppvar, 1, 3);
   nrn_update_ion_pointer(_k_sym, _ppvar, 2, 4);
 }

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  h = h0;
  m = m0;
 {
   rates ( _threadargscomma_ v ) ;
   m = minf ;
   h = hinf ;
   }
  _sav_indep = t; t = _save;

}
}

static void nrn_init(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
  ek = _ion_ek;
 initmodel();
 }}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   ik = gkbar * pow( m , 3.0 ) * h * ( v - ek ) ;
   }
 _current += ik;

} return _current;
}

static void nrn_cur(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
  ek = _ion_ek;
 _g = _nrn_current(_v + .001);
 	{ double _dik;
  _dik = ik;
 _rhs = _nrn_current(_v);
  _ion_dikdv += (_dik - ik)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_ik += ik ;
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}}

static void nrn_jacob(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}}

static void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v=_v;
{
  ek = _ion_ek;
 { error =  states();
 if(error){fprintf(stderr,"at line 57 in file kpkj.mod:\n	SOLVE states METHOD cnexp\n"); nrn_complain(_p); abort_run(error);}
 } }}

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = &(m) - _p;  _dlist1[0] = &(Dm) - _p;
 _slist1[1] = &(h) - _p;  _dlist1[1] = &(Dh) - _p;
_first = 0;
}

#if NMODL_TEXT
static const char* nmodl_filename = "/home/cereb/cerebmodels/models/cells/PC2003Khaliq/mod_files/kpkj.mod";
static const char* nmodl_file_text = 
  ": HH TEA-sensitive Purkinje potassium current\n"
  ": Created 8/5/02 - nwg\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX kpkj\n"
  "	USEION k READ ek WRITE ik\n"
  "	RANGE gkbar, ik\n"
  "	GLOBAL minf, hinf, mtau, htau\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(mV) = (millivolt)\n"
  "	(mA) = (milliamp)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	v (mV)\n"
  "\n"
  "	gkbar = .004	(mho/cm2)\n"
  "\n"
  "	mivh = -24	(mV)\n"
  "	mik = 15.4	(1)\n"
  "	mty0 = .00012851 	\n"
  "	mtvh1 = 100.7	(mV)\n"
  "	mtk1 = 12.9	(1)\n"
  "	mtvh2 = -56.0	(mV)\n"
  "	mtk2 = -23.1	(1)\n"
  "	\n"
  "	hiy0 = .31	\n"
  "	hiA = .78\n"
  "	hivh = -5.802	(mV)\n"
  "	hik = 11.2	(1)\n"
  "\n"
  "	ek\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	ik		(mA/cm2)\n"
  "	minf\n"
  "	mtau		(ms)\n"
  "	hinf\n"
  "	htau		(ms)\n"
  "}\n"
  "\n"
  "STATE {\n"
  "	m\n"
  "	h\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "	rates(v)\n"
  "	m = minf\n"
  "	h = hinf\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE states METHOD cnexp\n"
  "	ik = gkbar * m^3 * h * (v - ek)\n"
  "}\n"
  "\n"
  "DERIVATIVE states {\n"
  "	rates(v)\n"
  "	m' = (minf - m) / mtau\n"
  "	h' = (hinf - h) / htau\n"
  "}\n"
  "\n"
  "PROCEDURE rates( Vm (mV)) {\n"
  "	LOCAL v\n"
  "	v = Vm + 11	: Account for Junction Potential\n"
  "	minf = 1/(1+exp(-(v-mivh)/mik))\n"
  "	mtau = (1000) * mtau_func(v)\n"
  "	hinf = hiy0 + hiA/(1+exp((v-hivh)/hik))\n"
  "	htau = 1000 * htau_func(v)\n"
  "}\n"
  "\n"
  "FUNCTION mtau_func (v (mV)) (ms) {\n"
  "	if (v < -35) {\n"
  "		mtau_func = (3.4225e-5+.00498*exp(-v/-28.29))*3\n"
  "	} else {\n"
  "		mtau_func = (mty0 + 1/(exp((v+mtvh1)/mtk1)+exp((v+mtvh2)/mtk2)))\n"
  "	}\n"
  "}\n"
  "\n"
  "FUNCTION htau_func(Vm (mV)) (ms) {\n"
  "	if ( Vm > 0) {\n"
  "		htau_func = .0012+.0023*exp(-.141*Vm)\n"
  "	} else {\n"
  "		htau_func = 1.2202e-05 + .012 * exp(-((Vm-(-56.3))/49.6)^2)\n"
  "	}\n"
  "}\n"
  "	\n"
  ;
#endif
