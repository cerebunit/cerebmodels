#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _bkpkj_reg(void);
extern void _cadiff_reg(void);
extern void _cap_reg(void);
extern void _ihpkj_reg(void);
extern void _kpkj_reg(void);
extern void _kpkj2_reg(void);
extern void _kpkjslow_reg(void);
extern void _pkjlk_reg(void);
extern void _rsg_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," \"mod_files/bkpkj.mod\"");
    fprintf(stderr," \"mod_files/cadiff.mod\"");
    fprintf(stderr," \"mod_files/cap.mod\"");
    fprintf(stderr," \"mod_files/ihpkj.mod\"");
    fprintf(stderr," \"mod_files/kpkj.mod\"");
    fprintf(stderr," \"mod_files/kpkj2.mod\"");
    fprintf(stderr," \"mod_files/kpkjslow.mod\"");
    fprintf(stderr," \"mod_files/pkjlk.mod\"");
    fprintf(stderr," \"mod_files/rsg.mod\"");
    fprintf(stderr, "\n");
  }
  _bkpkj_reg();
  _cadiff_reg();
  _cap_reg();
  _ihpkj_reg();
  _kpkj_reg();
  _kpkj2_reg();
  _kpkjslow_reg();
  _pkjlk_reg();
  _rsg_reg();
}
