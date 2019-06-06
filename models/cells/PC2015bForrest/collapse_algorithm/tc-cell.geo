NumSmoothDendrite=85
NumSpinyDendrite=1002

create soma, SmoothDendrite[NumSmoothDendrite], SpinyDendrite[NumSpinyDendrite]
access soma
    soma connect SmoothDendrite[0](0),1
    soma         {nseg=1 L=22 diam=22 }	      // {nseg=1 L=0.00001 diam=0.00001 }
    SmoothDendrite[0] {nseg=1 L=18 diam=4 }
 
    SmoothDendrite[0] connect SmoothDendrite[1](0),1
    SmoothDendrite[1] {nseg=1 L=39 diam=4 }
 
    SmoothDendrite[1] connect SmoothDendrite[2](0),1
    SmoothDendrite[2] {nseg=1 L=12 diam=2 }
 
    SmoothDendrite[2] connect SmoothDendrite[3](0),1
    SmoothDendrite[3] {nseg=1 L=7 diam=2 }
 
    SmoothDendrite[2] connect SmoothDendrite[4](0),1
    SmoothDendrite[4] {nseg=1 L=2 diam=2 }
 
    SmoothDendrite[4] connect SmoothDendrite[5](0),1
    SmoothDendrite[5] {nseg=1 L=10 diam=2 }

    SmoothDendrite[1] connect SmoothDendrite[6](0),1
    SmoothDendrite[6] {nseg=1 L=10 diam=5 }
 
    SmoothDendrite[6] connect SmoothDendrite[7](0),1
    SmoothDendrite[7] {nseg=1 L=37 diam=4 }
 
    SmoothDendrite[7] connect SmoothDendrite[8](0),1
    SmoothDendrite[8] {nseg=1 L=2 diam=4 }
 
    SmoothDendrite[7] connect SmoothDendrite[9](0),1
    SmoothDendrite[9] {nseg=1 L=15 diam=4 }
 
    SmoothDendrite[9] connect SmoothDendrite[10](0),1
    SmoothDendrite[10] {nseg=1 L=4 diam=2 }
 
    SmoothDendrite[9] connect SmoothDendrite[11](0),1
    SmoothDendrite[11] {nseg=1 L=2 diam=4 }
 
    SmoothDendrite[11] connect SmoothDendrite[12](0),1
    SmoothDendrite[12] {nseg=1 L=7 diam=4 }
 
    SmoothDendrite[12] connect SmoothDendrite[13](0),1
    SmoothDendrite[13] {nseg=1 L=2 diam=4 }
 
    SmoothDendrite[13] connect SmoothDendrite[14](0),1
    SmoothDendrite[14] {nseg=1 L=32 diam=4 }
 
    SmoothDendrite[14] connect SmoothDendrite[15](0),1
    SmoothDendrite[15] {nseg=1 L=11 diam=3 }
 
    SmoothDendrite[17] connect SmoothDendrite[16](0),1
    SmoothDendrite[16] {nseg=1 L=3 diam=2 }
 
    SmoothDendrite[14] connect SmoothDendrite[17](0),1
    SmoothDendrite[17] {nseg=1 L=3 diam=2 }
 
    SmoothDendrite[15] connect SmoothDendrite[18](0),1
    SmoothDendrite[18] {nseg=1 L=12 diam=3 }
 
    SmoothDendrite[18] connect SmoothDendrite[19](0),1
    SmoothDendrite[19] {nseg=1 L=8 diam=3 }
 
    SmoothDendrite[19] connect SmoothDendrite[20](0),1
    SmoothDendrite[20] {nseg=1 L=3 diam=2 }
 
    SmoothDendrite[20] connect SmoothDendrite[21](0),1
    SmoothDendrite[21] {nseg=1 L=6 diam=2 }
 
    SmoothDendrite[21] connect SmoothDendrite[22](0),1
    SmoothDendrite[22] {nseg=1 L=27 diam=2 }
 
    SmoothDendrite[22] connect SmoothDendrite[23](0),1
    SmoothDendrite[23] {nseg=1 L=5 diam=2 }
 
    SmoothDendrite[23] connect SmoothDendrite[24](0),1
    SmoothDendrite[24] {nseg=1 L=2 diam=2 }
 
    SmoothDendrite[6] connect SmoothDendrite[25](0),1
    SmoothDendrite[25] {nseg=1 L=10 diam=5 }
 
    SmoothDendrite[25] connect SmoothDendrite[26](0),1
    SmoothDendrite[26] {nseg=1 L=12 diam=2 }
 
    SmoothDendrite[26] connect SmoothDendrite[27](0),1
    SmoothDendrite[27] {nseg=1 L=2 diam=2 }
 
    SmoothDendrite[27] connect SmoothDendrite[28](0),1
    SmoothDendrite[28] {nseg=1 L=2 diam=2 }
 
    SmoothDendrite[28] connect SmoothDendrite[29](0),1
    SmoothDendrite[29] {nseg=1 L=2 diam=2 }
 
    SmoothDendrite[25] connect SmoothDendrite[30](0),1
    SmoothDendrite[30] {nseg=1 L=12 diam=5 }
 
    SmoothDendrite[30] connect SmoothDendrite[31](0),1
    SmoothDendrite[31] {nseg=1 L=6 diam=5 }

    SmoothDendrite[31] connect SmoothDendrite[32](0),1
    SmoothDendrite[32] {nseg=1 L=6 diam=2 }
 
    SmoothDendrite[32] connect SmoothDendrite[33](0),1
    SmoothDendrite[33] {nseg=1 L=13 diam=2 }
 
    SmoothDendrite[33] connect SmoothDendrite[34](0),1
    SmoothDendrite[34] {nseg=1 L=2 diam=2 }
 
    SmoothDendrite[31] connect SmoothDendrite[35](0),1
    SmoothDendrite[35] {nseg=1 L=22 diam=4 }
 
    SmoothDendrite[35] connect SmoothDendrite[36](0),1
    SmoothDendrite[36] {nseg=1 L=4 diam=2 }
 
    SmoothDendrite[35] connect SmoothDendrite[37](0),1
    SmoothDendrite[37] {nseg=1 L=4 diam=4 }
 
    SmoothDendrite[37] connect SmoothDendrite[38](0),1
    SmoothDendrite[38] {nseg=1 L=20 diam=4 }
 
    SmoothDendrite[38] connect SmoothDendrite[39](0),1
    SmoothDendrite[39] {nseg=1 L=23 diam=1 }
 
    SmoothDendrite[38] connect SmoothDendrite[40](0),1
    SmoothDendrite[40] {nseg=1 L=6 diam=4 }
 
    SmoothDendrite[40] connect SmoothDendrite[41](0),1
    SmoothDendrite[41] {nseg=1 L=4 diam=4 }
 
    SmoothDendrite[41] connect SmoothDendrite[42](0),1
    SmoothDendrite[42] {nseg=1 L=1 diam=2 }
 
    SmoothDendrite[42] connect SmoothDendrite[43](0),1
    SmoothDendrite[43] {nseg=1 L=3 diam=2 }
 
    SmoothDendrite[41] connect SmoothDendrite[44](0),1
    SmoothDendrite[44] {nseg=1 L=18 diam=3 }
 
    SmoothDendrite[44] connect SmoothDendrite[45](0),1
    SmoothDendrite[45] {nseg=1 L=2 diam=2 }
 
    SmoothDendrite[45] connect SmoothDendrite[46](0),1
    SmoothDendrite[46] {nseg=1 L=20 diam=2 }
 
    SmoothDendrite[44] connect SmoothDendrite[47](0),1
    SmoothDendrite[47] {nseg=1 L=8 diam=3 }
 
    SmoothDendrite[47] connect SmoothDendrite[48](0),1
    SmoothDendrite[48] {nseg=1 L=5 diam=3 }
 
    SmoothDendrite[48] connect SmoothDendrite[49](0),1
    SmoothDendrite[49] {nseg=1 L=9 diam=2 }
 
    SmoothDendrite[49] connect SmoothDendrite[50](0),1
    SmoothDendrite[50] {nseg=1 L=4 diam=2 }
 
    SmoothDendrite[50] connect SmoothDendrite[51](0),1
    SmoothDendrite[51] {nseg=1 L=6 diam=2 }
 
    SmoothDendrite[0] connect SmoothDendrite[52](0),1
    SmoothDendrite[52] {nseg=1 L=22 diam=4 }
 
    SmoothDendrite[52] connect SmoothDendrite[53](0),1
    SmoothDendrite[53] {nseg=1 L=2 diam=2 }
 
    SmoothDendrite[53] connect SmoothDendrite[54](0),1
    SmoothDendrite[54] {nseg=1 L=18 diam=2 }
 
    SmoothDendrite[52] connect SmoothDendrite[55](0),1
    SmoothDendrite[55] {nseg=1 L=22 diam=6 }
 
    SmoothDendrite[55] connect SmoothDendrite[56](0),1
    SmoothDendrite[56] {nseg=1 L=8 diam=2 }
 
    SmoothDendrite[55] connect SmoothDendrite[57](0),1
    SmoothDendrite[57] {nseg=1 L=2 diam=6 }
 
    SmoothDendrite[57] connect SmoothDendrite[58](0),1
    SmoothDendrite[58] {nseg=1 L=3 diam=5 }
 
    SmoothDendrite[58] connect SmoothDendrite[59](0),1
    SmoothDendrite[59] {nseg=1 L=3 diam=6 }
 
    SmoothDendrite[59] connect SmoothDendrite[60](0),1
    SmoothDendrite[60] {nseg=1 L=8 diam=2 }
 
    SmoothDendrite[59] connect SmoothDendrite[61](0),1
    SmoothDendrite[61] {nseg=1 L=14 diam=6 }
 
    SmoothDendrite[61] connect SmoothDendrite[62](0),1
    SmoothDendrite[62] {nseg=1 L=44 diam=2 }
 
    SmoothDendrite[62] connect SmoothDendrite[63](0),1
    SmoothDendrite[63] {nseg=1 L=12 diam=2 }
 
    SmoothDendrite[63] connect SmoothDendrite[64](0),1
    SmoothDendrite[64] {nseg=1 L=2 diam=2 }
 
    SmoothDendrite[62] connect SmoothDendrite[65](0),1
    SmoothDendrite[65] {nseg=1 L=2 diam=2 }
 
    SmoothDendrite[65] connect SmoothDendrite[66](0),1
    SmoothDendrite[66] {nseg=1 L=2 diam=2 }
 
    SmoothDendrite[66] connect SmoothDendrite[67](0),1
    SmoothDendrite[67] {nseg=1 L=13 diam=1 }
 
    SmoothDendrite[67] connect SmoothDendrite[68](0),1
    SmoothDendrite[68] {nseg=1 L=4 diam=1 }
 
    SmoothDendrite[61] connect SmoothDendrite[69](0),1
    SmoothDendrite[69] {nseg=1 L=10 diam=6 }
 
    SmoothDendrite[69] connect SmoothDendrite[70](0),1
    SmoothDendrite[70] {nseg=1 L=4 diam=3 }
 
    SmoothDendrite[70] connect SmoothDendrite[71](0),1
    SmoothDendrite[71] {nseg=1 L=4 diam=3 }
 
    SmoothDendrite[69] connect SmoothDendrite[72](0),1
    SmoothDendrite[72] {nseg=1 L=2 diam=6 }
 
    SmoothDendrite[72] connect SmoothDendrite[73](0),1
    SmoothDendrite[73] {nseg=1 L=24 diam=5 }
 
    SmoothDendrite[73] connect SmoothDendrite[74](0),1
    SmoothDendrite[74] {nseg=1 L=52 diam=2 }
 
    SmoothDendrite[74] connect SmoothDendrite[75](0),1
    SmoothDendrite[75] {nseg=1 L=16 diam=2 }
 
    SmoothDendrite[73] connect SmoothDendrite[76](0),1
    SmoothDendrite[76] {nseg=1 L=14 diam=4 }
 
    SmoothDendrite[76] connect SmoothDendrite[77](0),1
    SmoothDendrite[77] {nseg=1 L=2 diam=4 }
 
    SmoothDendrite[77] connect SmoothDendrite[78](0),1
    SmoothDendrite[78] {nseg=1 L=14 diam=4 }
 
    SmoothDendrite[78] connect SmoothDendrite[79](0),1
    SmoothDendrite[79] {nseg=1 L=24 diam=4 }
 
    SmoothDendrite[79] connect SmoothDendrite[80](0),1
    SmoothDendrite[80] {nseg=1 L=6 diam=2 }
 
    SmoothDendrite[79] connect SmoothDendrite[81](0),1
    SmoothDendrite[81] {nseg=1 L=8 diam=2 }
 
    SmoothDendrite[81] connect SmoothDendrite[82](0),1
    SmoothDendrite[82] {nseg=1 L=2 diam=2 }
 
    SmoothDendrite[82] connect SmoothDendrite[83](0),1
    SmoothDendrite[83] {nseg=1 L=6 diam=2 }

    SmoothDendrite[83] connect SmoothDendrite[84](0),1
    SmoothDendrite[84] {nseg=1 L=12 diam=2 }


/**** Spiny 1 ****/
    SmoothDendrite[53] connect SpinyDendrite[0](0),1
    SpinyDendrite[0] {nseg=1 L=8 diam=1 }
 

/**** Spiny 2 ****/
    SmoothDendrite[54] connect SpinyDendrite[1](0),1
    SpinyDendrite[1] {nseg=1 L=9 diam=2 }
 
    SpinyDendrite[1] connect SpinyDendrite[2](0),1
    SpinyDendrite[2] {nseg=1 L=6 diam=1.4 }
 
    SpinyDendrite[2] connect SpinyDendrite[3](0),1
    SpinyDendrite[3] {nseg=1 L=8 diam=1 }
 
    SpinyDendrite[2] connect SpinyDendrite[4](0),1
    SpinyDendrite[4] {nseg=1 L=10 diam=1 }
 
    SpinyDendrite[1] connect SpinyDendrite[5](0),1
    SpinyDendrite[5] {nseg=1 L=5 diam=1.4 }
 
    SpinyDendrite[5] connect SpinyDendrite[6](0),1
    SpinyDendrite[6] {nseg=1 L=5 diam=1.0 }
 
    SpinyDendrite[5] connect SpinyDendrite[7](0),1
    SpinyDendrite[7] {nseg=1 L=9 diam=1.0 }
 
/**** Spiny 3 ****/
    SmoothDendrite[54] connect SpinyDendrite[8](0),1
    SpinyDendrite[8] {nseg=1 L=4 diam=2 }
 
    SpinyDendrite[8] connect SpinyDendrite[9](0),1
    SpinyDendrite[9] {nseg=1 L=9 diam=1.0 }
 
    SpinyDendrite[8] connect SpinyDendrite[10](0),1
    SpinyDendrite[10] {nseg=1 L=5 diam=2.0 }
 
    SpinyDendrite[10] connect SpinyDendrite[11](0),1
    SpinyDendrite[11] {nseg=1 L=10 diam=1.0 }
 
    SpinyDendrite[10] connect SpinyDendrite[12](0),1
    SpinyDendrite[12] {nseg=1 L=2 diam=2.0 }
 
    SpinyDendrite[12] connect SpinyDendrite[13](0),1
    SpinyDendrite[13] {nseg=1 L=13 diam=1.4 }
 
    SpinyDendrite[13] connect SpinyDendrite[14](0),1
    SpinyDendrite[14] {nseg=1 L=7 diam=1.0 }
 
    SpinyDendrite[13] connect SpinyDendrite[15](0),1
    SpinyDendrite[15] {nseg=1 L=6 diam=1 }
 
    SpinyDendrite[12] connect SpinyDendrite[16](0),1
    SpinyDendrite[16] {nseg=1 L=6 diam=1.4 }
 
    SpinyDendrite[16] connect SpinyDendrite[17](0),1
    SpinyDendrite[17] {nseg=1 L=10 diam=1 }
 
    SpinyDendrite[16] connect SpinyDendrite[18](0),1
    SpinyDendrite[18] {nseg=1 L=6 diam=1.4 }
 
    SpinyDendrite[18] connect SpinyDendrite[19](0),1
    SpinyDendrite[19] {nseg=1 L=3 diam=1 }
 
    SpinyDendrite[18] connect SpinyDendrite[20](0),1
    SpinyDendrite[20] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[20] connect SpinyDendrite[21](0),1
    SpinyDendrite[21] {nseg=1 L=5 diam=1 }
 
    SpinyDendrite[20] connect SpinyDendrite[22](0),1
    SpinyDendrite[22] {nseg=1 L=3 diam=1.4 }
 
    SpinyDendrite[22] connect SpinyDendrite[23](0),1
    SpinyDendrite[23] {nseg=1 L=8 diam=1 }
 
    SpinyDendrite[22] connect SpinyDendrite[24](0),1
    SpinyDendrite[24] {nseg=1 L=2 diam=1.4 }
 
    SpinyDendrite[24] connect SpinyDendrite[25](0),1
    SpinyDendrite[25] {nseg=1 L=2 diam=1 }
 
    SpinyDendrite[24] connect SpinyDendrite[26](0),1
    SpinyDendrite[26] {nseg=1 L=4 diam=1.4 }
 
    SpinyDendrite[26] connect SpinyDendrite[27](0),1
    SpinyDendrite[27] {nseg=1 L=5 diam=1 }
 
    SpinyDendrite[26] connect SpinyDendrite[28](0),1
    SpinyDendrite[28] {nseg=1 L=4 diam=1 }


/**** Spiny 4 ****/
    SmoothDendrite[56] connect SpinyDendrite[29](0),1
    SpinyDendrite[29] {nseg=1 L=11 diam=2 }
 
    SpinyDendrite[29] connect SpinyDendrite[30](0),1
    SpinyDendrite[30] {nseg=1 L=6 diam=1.4 }
 
    SpinyDendrite[30] connect SpinyDendrite[31](0),1
    SpinyDendrite[31] {nseg=1 L=10 diam=1 }
 
    SpinyDendrite[30] connect SpinyDendrite[32](0),1
    SpinyDendrite[32] {nseg=1 L=10 diam=1 }
 
    SpinyDendrite[29] connect SpinyDendrite[33](0),1
    SpinyDendrite[33] {nseg=1 L=2 diam=2 }
 
    SpinyDendrite[33] connect SpinyDendrite[34](0),1
    SpinyDendrite[34] {nseg=1 L=18 diam=1 }
 
    SpinyDendrite[33] connect SpinyDendrite[35](0),1
    SpinyDendrite[35] {nseg=1 L=2 diam=2 }

    SpinyDendrite[35] connect SpinyDendrite[36](0),1
    SpinyDendrite[36] {nseg=1 L=2 diam=1.4 }
 
    SpinyDendrite[36] connect SpinyDendrite[37](0),1
    SpinyDendrite[37] {nseg=1 L=6 diam=1.4 }
 
    SpinyDendrite[37] connect SpinyDendrite[38](0),1
    SpinyDendrite[38] {nseg=1 L=18 diam=1 }
 
    SpinyDendrite[37] connect SpinyDendrite[39](0),1
    SpinyDendrite[39] {nseg=1 L=6 diam=1 }

    SpinyDendrite[36] connect SpinyDendrite[40](0),1
    SpinyDendrite[40] {nseg=1 L=7 diam=1 }
 
    SpinyDendrite[35] connect SpinyDendrite[41](0),1
    SpinyDendrite[41] {nseg=1 L=6 diam=2 }
 
    SpinyDendrite[41] connect SpinyDendrite[42](0),1
    SpinyDendrite[42] {nseg=1 L=8 diam=1.4 }
 
    SpinyDendrite[42] connect SpinyDendrite[43](0),1
    SpinyDendrite[43] {nseg=1 L=6 diam=1 }
 
    SpinyDendrite[42] connect SpinyDendrite[44](0),1
    SpinyDendrite[44] {nseg=1 L=6 diam=1 }
 
    SpinyDendrite[41] connect SpinyDendrite[45](0),1
    SpinyDendrite[45] {nseg=1 L=7 diam=1.4 }

    SpinyDendrite[45] connect SpinyDendrite[46](0),1
    SpinyDendrite[46] {nseg=1 L=8 diam=1 }
 
    SpinyDendrite[45] connect SpinyDendrite[47](0),1
    SpinyDendrite[47] {nseg=1 L=7 diam=1.4 }
 
    SpinyDendrite[46] connect SpinyDendrite[48](0),1
    SpinyDendrite[48] {nseg=1 L=3 diam=1 }

    SpinyDendrite[47] connect SpinyDendrite[49](0),1
    SpinyDendrite[49] {nseg=1 L=6 diam=1 }


/**** Spiny 5 ****/
    SmoothDendrite[56] connect SpinyDendrite[50](0),1
    SpinyDendrite[50] {nseg=1 L=5 diam=2 }
 
    SpinyDendrite[50] connect SpinyDendrite[51](0),1
    SpinyDendrite[51] {nseg=1 L=17 diam=1 }
 
    SpinyDendrite[50] connect SpinyDendrite[52](0),1
    SpinyDendrite[52] {nseg=1 L=4 diam=2 }
 
    SpinyDendrite[52] connect SpinyDendrite[53](0),1
    SpinyDendrite[53] {nseg=1 L=16 diam=1.4 }
 
    SpinyDendrite[53] connect SpinyDendrite[54](0),1
    SpinyDendrite[54] {nseg=1 L=15 diam=1}
 
    SpinyDendrite[53] connect SpinyDendrite[55](0),1
    SpinyDendrite[55] {nseg=1 L=3 diam=1 }
 
    SpinyDendrite[52] connect SpinyDendrite[56](0),1
    SpinyDendrite[56] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[56] connect SpinyDendrite[57](0),1
    SpinyDendrite[57] {nseg=1 L=4 diam=1 }
 
    SpinyDendrite[56] connect SpinyDendrite[58](0),1
    SpinyDendrite[58] {nseg=1 L=2 diam=1.4 }
 
    SpinyDendrite[58] connect SpinyDendrite[59](0),1
    SpinyDendrite[59] {nseg=1 L=4 diam=1 }
 
    SpinyDendrite[58] connect SpinyDendrite[60](0),1
    SpinyDendrite[60] {nseg=1 L=9 diam=1.4 }
 
    SpinyDendrite[60] connect SpinyDendrite[61](0),1
    SpinyDendrite[61] {nseg=1 L=14 diam=1 }
 
    SpinyDendrite[60] connect SpinyDendrite[62](0),1
    SpinyDendrite[62] {nseg=1 L=7 diam=1 }


/**** Spiny 6 ****/
    SmoothDendrite[57] connect SpinyDendrite[63](0),1
    SpinyDendrite[63] {nseg=1 L=16 diam=1.4 }
 
    SpinyDendrite[63] connect SpinyDendrite[64](0),1
    SpinyDendrite[64] {nseg=1 L=4 diam=1 }
 
    SpinyDendrite[63] connect SpinyDendrite[65](0),1
    SpinyDendrite[65] {nseg=1 L=18 diam=1 }
 
/**** Spiny 7 ****/
    SmoothDendrite[58] connect SpinyDendrite[66](0),1
    SpinyDendrite[66] {nseg=1 L=10 diam=1.4 }
 
    SpinyDendrite[66] connect SpinyDendrite[67](0),1
    SpinyDendrite[67] {nseg=1 L=6 diam=1 }
 
    SpinyDendrite[66] connect SpinyDendrite[68](0),1
    SpinyDendrite[68] {nseg=1 L=29 diam=1 }
 

/**** Spiny 8 ****/
    SmoothDendrite[70] connect SpinyDendrite[69](0),1
    SpinyDendrite[69] {nseg=1 L=11 diam=1.4 }
 
    SpinyDendrite[69] connect SpinyDendrite[70](0),1
    SpinyDendrite[70] {nseg=1 L=12 diam=1 }
 
    SpinyDendrite[69] connect SpinyDendrite[71](0),1
    SpinyDendrite[71] {nseg=1 L=1 diam=1.4 }
 
    SpinyDendrite[71] connect SpinyDendrite[72](0),1
    SpinyDendrite[72] {nseg=1 L=12 diam=1 }
 
    SpinyDendrite[71] connect SpinyDendrite[73](0),1
    SpinyDendrite[73] {nseg=1 L=9 diam=1 }
 

/**** Spiny 9 ****/
    SmoothDendrite[71] connect SpinyDendrite[74](0),1
    SpinyDendrite[74] {nseg=1 L=2 diam=2 }
 
    SpinyDendrite[74] connect SpinyDendrite[75](0),1
    SpinyDendrite[75] {nseg=1 L=22 diam=1.4 }
 
    SpinyDendrite[75] connect SpinyDendrite[76](0),1
    SpinyDendrite[76] {nseg=1 L=4 diam=1.4 }
 
    SpinyDendrite[76] connect SpinyDendrite[77](0),1
    SpinyDendrite[77] {nseg=1 L=14 diam=1 }
 
    SpinyDendrite[76] connect SpinyDendrite[78](0),1
    SpinyDendrite[78] {nseg=1 L=8 diam=1 }
 
    SpinyDendrite[75] connect SpinyDendrite[79](0),1
    SpinyDendrite[79] {nseg=1 L=10 diam=1 }
 
    SpinyDendrite[74] connect SpinyDendrite[80](0),1
    SpinyDendrite[80] {nseg=1 L=10 diam=1.4 }

    SpinyDendrite[80] connect SpinyDendrite[81](0),1
    SpinyDendrite[81] {nseg=1 L=6 diam=1 }
 
    SpinyDendrite[80] connect SpinyDendrite[82](0),1
    SpinyDendrite[82] {nseg=1 L=5 diam=1.4 }
 
    SpinyDendrite[82] connect SpinyDendrite[83](0),1
    SpinyDendrite[83] {nseg=1 L=6 diam=1 }
 
    SpinyDendrite[82] connect SpinyDendrite[84](0),1
    SpinyDendrite[84] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[84] connect SpinyDendrite[85](0),1
    SpinyDendrite[85] {nseg=1 L=23 diam=1 }
 
    SpinyDendrite[84] connect SpinyDendrite[86](0),1
    SpinyDendrite[86] {nseg=1 L=4 diam=1.4 }
 
    SpinyDendrite[86] connect SpinyDendrite[87](0),1
    SpinyDendrite[87] {nseg=1 L=4 diam=1 }
 
    SpinyDendrite[86] connect SpinyDendrite[88](0),1
    SpinyDendrite[88] {nseg=1 L=6 diam=1 }


/**** Spiny 10 ****/
    SmoothDendrite[71] connect SpinyDendrite[89](0),1
    SpinyDendrite[89] {nseg=1 L=12 diam=2 }
 
    SpinyDendrite[89] connect SpinyDendrite[90](0),1
    SpinyDendrite[90] {nseg=1 L=7 diam=1.4 }
 
    SpinyDendrite[90] connect SpinyDendrite[91](0),1
    SpinyDendrite[91] {nseg=1 L=26 diam=1 }
 
    SpinyDendrite[90] connect SpinyDendrite[92](0),1
    SpinyDendrite[92] {nseg=1 L=12 diam=1 }
 
    SpinyDendrite[89] connect SpinyDendrite[93](0),1
    SpinyDendrite[93] {nseg=1 L=6 diam=1.4 }
 
    SpinyDendrite[93] connect SpinyDendrite[94](0),1
    SpinyDendrite[94] {nseg=1 L=14 diam=1 }
 
    SpinyDendrite[93] connect SpinyDendrite[95](0),1
    SpinyDendrite[95] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[95] connect SpinyDendrite[96](0),1
    SpinyDendrite[96] {nseg=1 L=11 diam=1 }
 
    SpinyDendrite[95] connect SpinyDendrite[97](0),1
    SpinyDendrite[97] {nseg=1 L=7 diam=1.4 }
 
    SpinyDendrite[97] connect SpinyDendrite[98](0),1
    SpinyDendrite[98] {nseg=1 L=4 diam=1 }
 
    SpinyDendrite[97] connect SpinyDendrite[99](0),1
    SpinyDendrite[99] {nseg=1 L=7 diam=1 }


/**** Spiny 11 ****/
    SmoothDendrite[72] connect SpinyDendrite[100](0),1
    SpinyDendrite[100] {nseg=1 L=4 diam=2 }
 
    SpinyDendrite[100] connect SpinyDendrite[101](0),1
    SpinyDendrite[101] {nseg=1 L=18 diam=1 }
 
    SpinyDendrite[100] connect SpinyDendrite[102](0),1
    SpinyDendrite[102] {nseg=1 L=2 diam=2 }
 
    SpinyDendrite[102] connect SpinyDendrite[103](0),1
    SpinyDendrite[103] {nseg=1 L=16 diam=1 }
 
    SpinyDendrite[102] connect SpinyDendrite[104](0),1
    SpinyDendrite[104] {nseg=1 L=13 diam=2 }
 
    SpinyDendrite[104] connect SpinyDendrite[105](0),1
    SpinyDendrite[105] {nseg=1 L=9 diam=1.4 }
 
    SpinyDendrite[105] connect SpinyDendrite[106](0),1
    SpinyDendrite[106] {nseg=1 L=10 diam=1 }

    SpinyDendrite[105] connect SpinyDendrite[107](0),1
    SpinyDendrite[107] {nseg=1 L=3 diam=1 }
 
    SpinyDendrite[104] connect SpinyDendrite[108](0),1
    SpinyDendrite[108] {nseg=1 L=3 diam=1.4 }
 
    SpinyDendrite[108] connect SpinyDendrite[109](0),1
    SpinyDendrite[109] {nseg=1 L=13 diam=1 }
 
    SpinyDendrite[108] connect SpinyDendrite[110](0),1
    SpinyDendrite[110] {nseg=1 L=23 diam=1.4 }

    SpinyDendrite[110] connect SpinyDendrite[111](0),1
    SpinyDendrite[111] {nseg=1 L=6 diam=1 }
 
    SpinyDendrite[110] connect SpinyDendrite[112](0),1
    SpinyDendrite[112] {nseg=1 L=6 diam=1 }


/**** Spiny 12 ****/
    SmoothDendrite[77] connect SpinyDendrite[113](0),1
    SpinyDendrite[113] {nseg=1 L=3 diam=2 }
 
    SpinyDendrite[113] connect SpinyDendrite[114](0),1
    SpinyDendrite[114] {nseg=1 L=4 diam=1.4 }
 
    SpinyDendrite[114] connect SpinyDendrite[115](0),1
    SpinyDendrite[115] {nseg=1 L=4 diam=1.4 }
 
    SpinyDendrite[115] connect SpinyDendrite[116](0),1
    SpinyDendrite[116] {nseg=1 L=3 diam=1.4 }
 
    SpinyDendrite[116] connect SpinyDendrite[117](0),1
    SpinyDendrite[117] {nseg=1 L=5 diam=1 }
 
    SpinyDendrite[116] connect SpinyDendrite[118](0),1
    SpinyDendrite[118] {nseg=1 L=4 diam=1 }
 
    SpinyDendrite[114] connect SpinyDendrite[119](0),1
    SpinyDendrite[119] {nseg=1 L=12 diam=1 }

    SpinyDendrite[115] connect SpinyDendrite[120](0),1
    SpinyDendrite[120] {nseg=1 L=13 diam=1 }
 
    SpinyDendrite[113] connect SpinyDendrite[121](0),1
    SpinyDendrite[121] {nseg=1 L=8 diam=2 }
 
    SpinyDendrite[121] connect SpinyDendrite[122](0),1
    SpinyDendrite[122] {nseg=1 L=10 diam=1.4 }
 
    SpinyDendrite[122] connect SpinyDendrite[123](0),1
    SpinyDendrite[123] {nseg=1 L=16 diam=1 }
 
    SpinyDendrite[122] connect SpinyDendrite[124](0),1
    SpinyDendrite[124] {nseg=1 L=10 diam=1 }
 
    SpinyDendrite[121] connect SpinyDendrite[125](0),1
    SpinyDendrite[125] {nseg=1 L=9 diam=2 }
 
    SpinyDendrite[125] connect SpinyDendrite[126](0),1
    SpinyDendrite[126] {nseg=1 L=6 diam=1.4 }
 
    SpinyDendrite[126] connect SpinyDendrite[127](0),1
    SpinyDendrite[127] {nseg=1 L=9 diam=1 }
 
    SpinyDendrite[126] connect SpinyDendrite[128](0),1
    SpinyDendrite[128] {nseg=1 L=9 diam=1 }
 
    SpinyDendrite[125] connect SpinyDendrite[129](0),1
    SpinyDendrite[129] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[129] connect SpinyDendrite[130](0),1
    SpinyDendrite[130] {nseg=1 L=5 diam=1 }
 
    SpinyDendrite[129] connect SpinyDendrite[131](0),1
    SpinyDendrite[131] {nseg=1 L=9 diam=1.4 }
 
    SpinyDendrite[131] connect SpinyDendrite[132](0),1
    SpinyDendrite[132] {nseg=1 L=15 diam=1 }
 
    SpinyDendrite[131] connect SpinyDendrite[133](0),1
    SpinyDendrite[133] {nseg=1 L=5 diam=1 }


/**** Spiny 13 ****/
    SmoothDendrite[78] connect SpinyDendrite[134](0),1
    SpinyDendrite[134] {nseg=1 L=5 diam=2 }
 
    SpinyDendrite[134] connect SpinyDendrite[135](0),1
    SpinyDendrite[135] {nseg=1 L=8 diam=1.4 }
 
    SpinyDendrite[135] connect SpinyDendrite[136](0),1
    SpinyDendrite[136] {nseg=1 L=14 diam=1 }
 
    SpinyDendrite[135] connect SpinyDendrite[137](0),1
    SpinyDendrite[137] {nseg=1 L=10 diam=1 }
 
    SpinyDendrite[134] connect SpinyDendrite[138](0),1
    SpinyDendrite[138] {nseg=1 L=8 diam=2 }
 
    SpinyDendrite[138] connect SpinyDendrite[139](0),1
    SpinyDendrite[139] {nseg=1 L=4 diam=1.4 }
 
    SpinyDendrite[139] connect SpinyDendrite[140](0),1
    SpinyDendrite[140] {nseg=1 L=24 diam=1 }

    SpinyDendrite[139] connect SpinyDendrite[141](0),1
    SpinyDendrite[141] {nseg=1 L=13 diam=1 }
 
    SpinyDendrite[138] connect SpinyDendrite[142](0),1
    SpinyDendrite[142] {nseg=1 L=10 diam=1.4 }
 
    SpinyDendrite[142] connect SpinyDendrite[143](0),1
    SpinyDendrite[143] {nseg=1 L=12 diam=1 }
 
    SpinyDendrite[142] connect SpinyDendrite[144](0),1
    SpinyDendrite[144] {nseg=1 L=10 diam=1.4 }

    SpinyDendrite[144] connect SpinyDendrite[145](0),1
    SpinyDendrite[145] {nseg=1 L=6 diam=1 }
 
    SpinyDendrite[144] connect SpinyDendrite[146](0),1
    SpinyDendrite[146] {nseg=1 L=5 diam=1.4 }
 
    SpinyDendrite[146] connect SpinyDendrite[147](0),1
    SpinyDendrite[147] {nseg=1 L=8 diam=1 }
 
    SpinyDendrite[146] connect SpinyDendrite[148](0),1
    SpinyDendrite[148] {nseg=1 L=6 diam=1 }
/**** Spiny 14 ****/
    SmoothDendrite[80] connect SpinyDendrite[149](0),1
    SpinyDendrite[149] {nseg=1 L=4 diam=2 }
 
    SpinyDendrite[149] connect SpinyDendrite[150](0),1
    SpinyDendrite[150] {nseg=1 L=8 diam=1.4 }
 
    SpinyDendrite[150] connect SpinyDendrite[151](0),1
    SpinyDendrite[151] {nseg=1 L=18 diam=1 }
 
    SpinyDendrite[150] connect SpinyDendrite[152](0),1
    SpinyDendrite[152] {nseg=1 L=8 diam=1 }
 
    SpinyDendrite[149] connect SpinyDendrite[153](0),1
    SpinyDendrite[153] {nseg=1 L=8 diam=1.4 }
 
    SpinyDendrite[153] connect SpinyDendrite[154](0),1
    SpinyDendrite[154] {nseg=1 L=18 diam=1 }
 
    SpinyDendrite[153] connect SpinyDendrite[155](0),1
    SpinyDendrite[155] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[155] connect SpinyDendrite[156](0),1
    SpinyDendrite[156] {nseg=1 L=9 diam=1}
 
    SpinyDendrite[155] connect SpinyDendrite[157](0),1
    SpinyDendrite[157] {nseg=1 L=4 diam=1.4 }
 
    SpinyDendrite[157] connect SpinyDendrite[158](0),1
    SpinyDendrite[158] {nseg=1 L=12 diam=1 }
 
    SpinyDendrite[157] connect SpinyDendrite[159](0),1
    SpinyDendrite[159] {nseg=1 L=24 diam=1 }


/**** Spiny 15 ****/
    SmoothDendrite[80] connect SpinyDendrite[160](0),1
    SpinyDendrite[160] {nseg=1 L=14 diam=2 }
 
    SpinyDendrite[160] connect SpinyDendrite[161](0),1
    SpinyDendrite[161] {nseg=1 L=12 diam=1 }
 
    SpinyDendrite[160] connect SpinyDendrite[162](0),1
    SpinyDendrite[162] {nseg=1 L=3 diam=2 }
 
    SpinyDendrite[162] connect SpinyDendrite[163](0),1
    SpinyDendrite[163] {nseg=1 L=13 diam=1 }
 
    SpinyDendrite[162] connect SpinyDendrite[164](0),1
    SpinyDendrite[164] {nseg=1 L=10 diam=2 }
 
    SpinyDendrite[164] connect SpinyDendrite[165](0),1
    SpinyDendrite[165] {nseg=1 L=12 diam=1.4 }
 
    SpinyDendrite[165] connect SpinyDendrite[166](0),1
    SpinyDendrite[166] {nseg=1 L=6 diam=1 }

    SpinyDendrite[165] connect SpinyDendrite[167](0),1
    SpinyDendrite[167] {nseg=1 L=5 diam=1 }
 
    SpinyDendrite[164] connect SpinyDendrite[168](0),1
    SpinyDendrite[168] {nseg=1 L=3 diam=1.4 }
 
    SpinyDendrite[168] connect SpinyDendrite[169](0),1
    SpinyDendrite[169] {nseg=1 L=26 diam=1 }
 
    SpinyDendrite[168] connect SpinyDendrite[170](0),1
    SpinyDendrite[170] {nseg=1 L=5 diam=1.4 }
 
    SpinyDendrite[170] connect SpinyDendrite[171](0),1
    SpinyDendrite[171] {nseg=1 L=4 diam=1 }
 
    SpinyDendrite[170] connect SpinyDendrite[172](0),1
    SpinyDendrite[172] {nseg=1 L=5 diam=1 }


/**** Spiny 16 ****/
    SmoothDendrite[81] connect SpinyDendrite[173](0),1
    SpinyDendrite[173] {nseg=1 L=2 diam=1.4 }
 
    SpinyDendrite[173] connect SpinyDendrite[174](0),1
    SpinyDendrite[174] {nseg=1 L=18 diam=1 }
 
    SpinyDendrite[173] connect SpinyDendrite[175](0),1
    SpinyDendrite[175] {nseg=1 L=6 diam=1 }


/**** Spiny 17 ****/
    SmoothDendrite[84] connect SpinyDendrite[176](0),1
    SpinyDendrite[176] {nseg=1 L=8 diam=2 }
 
    SpinyDendrite[176] connect SpinyDendrite[177](0),1
    SpinyDendrite[177] {nseg=1 L=40 diam=1 }
 
    SpinyDendrite[176] connect SpinyDendrite[178](0),1
    SpinyDendrite[178] {nseg=1 L=9 diam=2 }
 
    SpinyDendrite[178] connect SpinyDendrite[179](0),1
    SpinyDendrite[179] {nseg=1 L=11 diam=1.4 }
 
    SpinyDendrite[179] connect SpinyDendrite[180](0),1
    SpinyDendrite[180] {nseg=1 L=10 diam=1.4 }
 
    SpinyDendrite[180] connect SpinyDendrite[181](0),1
    SpinyDendrite[181] {nseg=1 L=17 diam=1 }
 
    SpinyDendrite[180] connect SpinyDendrite[182](0),1
    SpinyDendrite[182] {nseg=1 L=5 diam=1 }

    SpinyDendrite[179] connect SpinyDendrite[183](0),1
    SpinyDendrite[183] {nseg=1 L=10 diam=1 }
 
    SpinyDendrite[178] connect SpinyDendrite[184](0),1
    SpinyDendrite[184] {nseg=1 L=1 diam=1.4 }
 
    SpinyDendrite[184] connect SpinyDendrite[185](0),1
    SpinyDendrite[185] {nseg=1 L=22 diam=1 }
 
    SpinyDendrite[184] connect SpinyDendrite[186](0),1
    SpinyDendrite[186] {nseg=1 L=10 diam=1.4 }

    SpinyDendrite[186] connect SpinyDendrite[187](0),1
    SpinyDendrite[187] {nseg=1 L=6 diam=1 }
 
    SpinyDendrite[186] connect SpinyDendrite[188](0),1
    SpinyDendrite[188] {nseg=1 L=6 diam=1 }


/**** Spiny 18 ****/
    SmoothDendrite[84] connect SpinyDendrite[189](0),1
    SpinyDendrite[189] {nseg=1 L=4 diam=2 }
 
    SpinyDendrite[189] connect SpinyDendrite[190](0),1
    SpinyDendrite[190] {nseg=1 L=7 diam=1.4 }
 
    SpinyDendrite[190] connect SpinyDendrite[191](0),1
    SpinyDendrite[191] {nseg=1 L=9 diam=1 }
 
    SpinyDendrite[190] connect SpinyDendrite[192](0),1
    SpinyDendrite[192] {nseg=1 L=14 diam=1 }
 
    SpinyDendrite[189] connect SpinyDendrite[193](0),1
    SpinyDendrite[193] {nseg=1 L=1 diam=1.4 }
 
    SpinyDendrite[193] connect SpinyDendrite[194](0),1
    SpinyDendrite[194] {nseg=1 L=4 diam=1 }
 
    SpinyDendrite[193] connect SpinyDendrite[195](0),1
    SpinyDendrite[195] {nseg=1 L=10 diam=1.4 }

    SpinyDendrite[195] connect SpinyDendrite[196](0),1
    SpinyDendrite[196] {nseg=1 L=6 diam=1 }
 
    SpinyDendrite[195] connect SpinyDendrite[197](0),1
    SpinyDendrite[197] {nseg=1 L=15 diam=1.4 }
 
    SpinyDendrite[197] connect SpinyDendrite[198](0),1
    SpinyDendrite[198] {nseg=1 L=4 diam=1 }
 
    SpinyDendrite[197] connect SpinyDendrite[199](0),1
    SpinyDendrite[199] {nseg=1 L=9 diam=1 }


/**** Spiny 19 ****/
    SmoothDendrite[83] connect SpinyDendrite[200](0),1
    SpinyDendrite[200] {nseg=1 L=19 diam=1.4 }
 
    SpinyDendrite[200] connect SpinyDendrite[201](0),1
    SpinyDendrite[201] {nseg=1 L=12 diam=1 }
 
    SpinyDendrite[200] connect SpinyDendrite[202](0),1
    SpinyDendrite[202] {nseg=1 L=11 diam=1 }
 

/**** Spiny 20 ****/
    SmoothDendrite[82] connect SpinyDendrite[203](0),1
    SpinyDendrite[203] {nseg=1 L=1 diam=1.4 }
 
    SpinyDendrite[203] connect SpinyDendrite[204](0),1
    SpinyDendrite[204] {nseg=1 L=12 diam=1 }
 
    SpinyDendrite[203] connect SpinyDendrite[205](0),1
    SpinyDendrite[205] {nseg=1 L=8 diam=1.4 }
 
    SpinyDendrite[205] connect SpinyDendrite[206](0),1
    SpinyDendrite[206] {nseg=1 L=15 diam=1 }
 
    SpinyDendrite[205] connect SpinyDendrite[207](0),1
    SpinyDendrite[207] {nseg=1 L=14 diam=1 }
 

/**** Spiny 21 ****/
    SmoothDendrite[76] connect SpinyDendrite[208](0),1
    SpinyDendrite[208] {nseg=1 L=28 diam=2 }
 
    SpinyDendrite[208] connect SpinyDendrite[209](0),1
    SpinyDendrite[209] {nseg=1 L=4 diam=1.4 }
 
    SpinyDendrite[209] connect SpinyDendrite[210](0),1
    SpinyDendrite[210] {nseg=1 L=8 diam=1 }
 
    SpinyDendrite[209] connect SpinyDendrite[211](0),1
    SpinyDendrite[211] {nseg=1 L=9 diam=1 }
 
    SpinyDendrite[208] connect SpinyDendrite[212](0),1
    SpinyDendrite[212] {nseg=1 L=4 diam=1.4 }
 
    SpinyDendrite[212] connect SpinyDendrite[213](0),1
    SpinyDendrite[213] {nseg=1 L=2 diam=1 }
 
    SpinyDendrite[212] connect SpinyDendrite[214](0),1
    SpinyDendrite[214] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[214] connect SpinyDendrite[215](0),1
    SpinyDendrite[215] {nseg=1 L=3 diam=1}
 
    SpinyDendrite[214] connect SpinyDendrite[216](0),1
    SpinyDendrite[216] {nseg=1 L=6 diam=1}
 

/**** Spiny 22 ****/
    SmoothDendrite[75] connect SpinyDendrite[217](0),1
    SpinyDendrite[217] {nseg=1 L=4 diam=2 }
 
    SpinyDendrite[217] connect SpinyDendrite[218](0),1
    SpinyDendrite[218] {nseg=1 L=6 diam=1.4 }
 
    SpinyDendrite[218] connect SpinyDendrite[219](0),1
    SpinyDendrite[219] {nseg=1 L=13 diam=1.4 }
 
    SpinyDendrite[219] connect SpinyDendrite[220](0),1
    SpinyDendrite[220] {nseg=1 L=4 diam=1.4 }
 
    SpinyDendrite[220] connect SpinyDendrite[221](0),1
    SpinyDendrite[221] {nseg=1 L=6 diam=1}
 
    SpinyDendrite[220] connect SpinyDendrite[222](0),1
    SpinyDendrite[222] {nseg=1 L=6 diam=1}
 
    SpinyDendrite[218] connect SpinyDendrite[223](0),1
    SpinyDendrite[223] {nseg=1 L=10 diam=1}

    SpinyDendrite[219] connect SpinyDendrite[224](0),1
    SpinyDendrite[224] {nseg=1 L=5 diam=1}
 
    SpinyDendrite[217] connect SpinyDendrite[225](0),1
    SpinyDendrite[225] {nseg=1 L=6 diam=2 }
 
    SpinyDendrite[225] connect SpinyDendrite[226](0),1
    SpinyDendrite[226] {nseg=1 L=7 diam=1.4 }
 
    SpinyDendrite[226] connect SpinyDendrite[227](0),1
    SpinyDendrite[227] {nseg=1 L=3 diam=1 }

    SpinyDendrite[226] connect SpinyDendrite[228](0),1
    SpinyDendrite[228] {nseg=1 L=15 diam=1 }
 
    SpinyDendrite[225] connect SpinyDendrite[229](0),1
    SpinyDendrite[229] {nseg=1 L=3 diam=2 }

    SpinyDendrite[229] connect SpinyDendrite[230](0),1
    SpinyDendrite[230] {nseg=1 L=18 diam=1 }
 
    SpinyDendrite[229] connect SpinyDendrite[231](0),1
    SpinyDendrite[231] {nseg=1 L=3 diam=2 }

    SpinyDendrite[231] connect SpinyDendrite[232](0),1
    SpinyDendrite[232] {nseg=1 L=6 diam=1.4 }
 
    SpinyDendrite[232] connect SpinyDendrite[233](0),1
    SpinyDendrite[233] {nseg=1 L=8 diam=1 }
 
    SpinyDendrite[232] connect SpinyDendrite[234](0),1
    SpinyDendrite[234] {nseg=1 L=2 diam=1 }
 
    SpinyDendrite[231] connect SpinyDendrite[235](0),1
    SpinyDendrite[235] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[235] connect SpinyDendrite[236](0),1
    SpinyDendrite[236] {nseg=1 L=6 diam=1}
 
    SpinyDendrite[235] connect SpinyDendrite[237](0),1
    SpinyDendrite[237] {nseg=1 L=10 diam=1 }


/**** Spiny 23 ****/
    SmoothDendrite[75] connect SpinyDendrite[238](0),1
    SpinyDendrite[238] {nseg=1 L=6 diam=2 }
 
    SpinyDendrite[238] connect SpinyDendrite[239](0),1
    SpinyDendrite[239] {nseg=1 L=25 diam=1.4 }
 
    SpinyDendrite[239] connect SpinyDendrite[240](0),1
    SpinyDendrite[240] {nseg=1 L=13 diam=1.4 }
 
    SpinyDendrite[240] connect SpinyDendrite[241](0),1
    SpinyDendrite[241] {nseg=1 L=18 diam=1.4 }
 
    SpinyDendrite[241] connect SpinyDendrite[242](0),1
    SpinyDendrite[242] {nseg=1 L=2 diam=1.4 }
 
    SpinyDendrite[242] connect SpinyDendrite[243](0),1
    SpinyDendrite[243] {nseg=1 L=4 diam=1 }
 
    SpinyDendrite[242] connect SpinyDendrite[244](0),1
    SpinyDendrite[244] {nseg=1 L=8 diam=1 }

    SpinyDendrite[239] connect SpinyDendrite[245](0),1
    SpinyDendrite[245] {nseg=1 L=6 diam=1 }
 
    SpinyDendrite[240] connect SpinyDendrite[246](0),1
    SpinyDendrite[246] {nseg=1 L=5 diam=1 }
 
    SpinyDendrite[241] connect SpinyDendrite[247](0),1
    SpinyDendrite[247] {nseg=1 L=14 diam=1 }
 
    SpinyDendrite[238] connect SpinyDendrite[248](0),1
    SpinyDendrite[248] {nseg=1 L=9 diam=1.4 }

    SpinyDendrite[248] connect SpinyDendrite[249](0),1
    SpinyDendrite[249] {nseg=1 L=6 diam=1 }
 
    SpinyDendrite[248] connect SpinyDendrite[250](0),1
    SpinyDendrite[250] {nseg=1 L=17 diam=1.4 }
 
    SpinyDendrite[250] connect SpinyDendrite[251](0),1
    SpinyDendrite[251] {nseg=1 L=10 diam=1 }
 
    SpinyDendrite[250] connect SpinyDendrite[252](0),1
    SpinyDendrite[252] {nseg=1 L=12 diam=1.4 }
 
    SpinyDendrite[252] connect SpinyDendrite[253](0),1
    SpinyDendrite[253] {nseg=1 L=10 diam=1 }
 
    SpinyDendrite[252] connect SpinyDendrite[254](0),1
    SpinyDendrite[254] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[254] connect SpinyDendrite[255](0),1
    SpinyDendrite[255] {nseg=1 L=6 diam=1 }
 
    SpinyDendrite[254] connect SpinyDendrite[256](0),1
    SpinyDendrite[256] {nseg=1 L=2 diam=1.4 }
 
    SpinyDendrite[256] connect SpinyDendrite[257](0),1
    SpinyDendrite[257] {nseg=1 L=8 diam=1 }
 
    SpinyDendrite[256] connect SpinyDendrite[258](0),1
    SpinyDendrite[258] {nseg=1 L=11 diam=1.4 }

    SpinyDendrite[258] connect SpinyDendrite[259](0),1
    SpinyDendrite[259] {nseg=1 L=6 diam=1 }
 
    SpinyDendrite[258] connect SpinyDendrite[260](0),1
    SpinyDendrite[260] {nseg=1 L=2 diam=1.4 }
 
    SpinyDendrite[260] connect SpinyDendrite[261](0),1
    SpinyDendrite[261] {nseg=1 L=17 diam=1 }
 
    SpinyDendrite[260] connect SpinyDendrite[262](0),1
    SpinyDendrite[262] {nseg=1 L=2 diam=1.4 }
 
    SpinyDendrite[262] connect SpinyDendrite[263](0),1
    SpinyDendrite[263] {nseg=1 L=8 diam=1 }
 
    SpinyDendrite[262] connect SpinyDendrite[264](0),1
    SpinyDendrite[264] {nseg=1 L=10 diam=1 }


/**** Spiny 24 ****/
    SmoothDendrite[74] connect SpinyDendrite[265](0),1
    SpinyDendrite[265] {nseg=1 L=8 diam=1.4 }
 
    SpinyDendrite[265] connect SpinyDendrite[266](0),1
    SpinyDendrite[266] {nseg=1 L=6 diam=1 }

    SpinyDendrite[265] connect SpinyDendrite[267](0),1
    SpinyDendrite[267] {nseg=1 L=5 diam=1 }


/**** Spiny 25 ****/
    SmoothDendrite[64] connect SpinyDendrite[268](0),1
    SpinyDendrite[268] {nseg=1 L=14 diam=2 }
 
    SpinyDendrite[268] connect SpinyDendrite[269](0),1
    SpinyDendrite[269] {nseg=1 L=16 diam=1 }

    SpinyDendrite[268] connect SpinyDendrite[270](0),1
    SpinyDendrite[270] {nseg=1 L=12 diam=2 }

    SpinyDendrite[270] connect SpinyDendrite[271](0),1
    SpinyDendrite[271] {nseg=1 L=14 diam=1 }

    SpinyDendrite[270] connect SpinyDendrite[272](0),1
    SpinyDendrite[272] {nseg=1 L=2 diam=2 }

    SpinyDendrite[272] connect SpinyDendrite[273](0),1
    SpinyDendrite[273] {nseg=1 L=11 diam=1 }

    SpinyDendrite[272] connect SpinyDendrite[274](0),1
    SpinyDendrite[274] {nseg=1 L=3 diam=2 }

    SpinyDendrite[274] connect SpinyDendrite[275](0),1
    SpinyDendrite[275] {nseg=1 L=7 diam=1 }

    SpinyDendrite[274] connect SpinyDendrite[276](0),1
    SpinyDendrite[276] {nseg=1 L=7 diam=2 }

    SpinyDendrite[276] connect SpinyDendrite[277](0),1
    SpinyDendrite[277] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[277] connect SpinyDendrite[278](0),1
    SpinyDendrite[278] {nseg=1 L=4 diam=1 }

    SpinyDendrite[277] connect SpinyDendrite[279](0),1
    SpinyDendrite[279] {nseg=1 L=6 diam=1 }

    SpinyDendrite[276] connect SpinyDendrite[280](0),1
    SpinyDendrite[280] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[280] connect SpinyDendrite[281](0),1
    SpinyDendrite[281] {nseg=1 L=7 diam=1 }

    SpinyDendrite[280] connect SpinyDendrite[282](0),1
    SpinyDendrite[282] {nseg=1 L=12 diam=1.4 }

    SpinyDendrite[282] connect SpinyDendrite[283](0),1
    SpinyDendrite[283] {nseg=1 L=7 diam=1 }

    SpinyDendrite[282] connect SpinyDendrite[284](0),1
    SpinyDendrite[284] {nseg=1 L=5 diam=1 }


/**** Spiny 26 ****/
    SmoothDendrite[64] connect SpinyDendrite[285](0),1
    SpinyDendrite[285] {nseg=1 L=5 diam=2 }
 
    SpinyDendrite[285] connect SpinyDendrite[286](0),1
    SpinyDendrite[286] {nseg=1 L=22 diam=1 }

    SpinyDendrite[285] connect SpinyDendrite[287](0),1
    SpinyDendrite[287] {nseg=1 L=6 diam=2 }

    SpinyDendrite[287] connect SpinyDendrite[288](0),1
    SpinyDendrite[288] {nseg=1 L=7 diam=1.4 }

    SpinyDendrite[288] connect SpinyDendrite[289](0),1
    SpinyDendrite[289] {nseg=1 L=1 diam=1.4 }

    SpinyDendrite[289] connect SpinyDendrite[290](0),1
    SpinyDendrite[290] {nseg=1 L=10 diam=1 }

    SpinyDendrite[289] connect SpinyDendrite[291](0),1
    SpinyDendrite[291] {nseg=1 L=8 diam=1 }

    SpinyDendrite[288] connect SpinyDendrite[292](0),1
    SpinyDendrite[292] {nseg=1 L=6 diam=1 }

    SpinyDendrite[287] connect SpinyDendrite[293](0),1
    SpinyDendrite[293] {nseg=1 L=15 diam=1.4 }

    SpinyDendrite[293] connect SpinyDendrite[294](0),1
    SpinyDendrite[294] {nseg=1 L=10 diam=1 }

    SpinyDendrite[293] connect SpinyDendrite[295](0),1
    SpinyDendrite[295] {nseg=1 L=16 diam=1.4 }

    SpinyDendrite[295] connect SpinyDendrite[296](0),1
    SpinyDendrite[296] {nseg=1 L=15 diam=1 }

    SpinyDendrite[295] connect SpinyDendrite[297](0),1
    SpinyDendrite[297] {nseg=1 L=8 diam=1 }


/**** Spiny 27 ****/
    SmoothDendrite[63] connect SpinyDendrite[298](0),1
    SpinyDendrite[298] {nseg=1 L=12 diam=1 }
 

/**** Spiny 28 ****/
    SmoothDendrite[66] connect SpinyDendrite[299](0),1
    SpinyDendrite[299] {nseg=1 L=32 diam=1.4 }
 
    SpinyDendrite[299] connect SpinyDendrite[300](0),1
    SpinyDendrite[300] {nseg=1 L=10 diam=1 }

    SpinyDendrite[299] connect SpinyDendrite[301](0),1
    SpinyDendrite[301] {nseg=1 L=4 diam=1 }


/**** Spiny 29 ****/
    SmoothDendrite[67] connect SpinyDendrite[302](0),1
    SpinyDendrite[302] {nseg=1 L=14 diam=1.4 }
 
    SpinyDendrite[302] connect SpinyDendrite[303](0),1
    SpinyDendrite[303] {nseg=1 L=12 diam=1 }

    SpinyDendrite[302] connect SpinyDendrite[304](0),1
    SpinyDendrite[304] {nseg=1 L=5 diam=1 }


/**** Spiny 30 ****/
    SmoothDendrite[68] connect SpinyDendrite[305](0),1
    SpinyDendrite[305] {nseg=1 L=6 diam=2 }
 
    SpinyDendrite[305] connect SpinyDendrite[306](0),1
    SpinyDendrite[306] {nseg=1 L=4 diam=1 }

    SpinyDendrite[305] connect SpinyDendrite[307](0),1
    SpinyDendrite[307] {nseg=1 L=12 diam=2 }

    SpinyDendrite[307] connect SpinyDendrite[308](0),1
    SpinyDendrite[308] {nseg=1 L=8 diam=1.4 }

    SpinyDendrite[308] connect SpinyDendrite[309](0),1
    SpinyDendrite[309] {nseg=1 L=3 diam=1 }

    SpinyDendrite[308] connect SpinyDendrite[310](0),1
    SpinyDendrite[310] {nseg=1 L=6 diam=1 }

    SpinyDendrite[309] connect SpinyDendrite[311](0),1
    SpinyDendrite[311] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[311] connect SpinyDendrite[312](0),1
    SpinyDendrite[312] {nseg=1 L=7 diam=1 }

    SpinyDendrite[311] connect SpinyDendrite[313](0),1
    SpinyDendrite[313] {nseg=1 L=9 diam=1 }


/**** Spiny 31 ****/
    SmoothDendrite[68] connect SpinyDendrite[314](0),1
    SpinyDendrite[314] {nseg=1 L=5 diam=2 }
 
    SpinyDendrite[314] connect SpinyDendrite[315](0),1
    SpinyDendrite[315] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[315] connect SpinyDendrite[316](0),1
    SpinyDendrite[316] {nseg=1 L=1 diam=1.4 }

    SpinyDendrite[316] connect SpinyDendrite[317](0),1
    SpinyDendrite[317] {nseg=1 L=14 diam=1 }

    SpinyDendrite[316] connect SpinyDendrite[318](0),1
    SpinyDendrite[318] {nseg=1 L=11 diam=1 }

    SpinyDendrite[315] connect SpinyDendrite[319](0),1
    SpinyDendrite[319] {nseg=1 L=5 diam=1 }

    SpinyDendrite[314] connect SpinyDendrite[320](0),1
    SpinyDendrite[320] {nseg=1 L=2 diam=2 }

    SpinyDendrite[320] connect SpinyDendrite[321](0),1
    SpinyDendrite[321] {nseg=1 L=11 diam=1.4 }

    SpinyDendrite[321] connect SpinyDendrite[322](0),1
    SpinyDendrite[322] {nseg=1 L=12diam=1 }

    SpinyDendrite[321] connect SpinyDendrite[323](0),1
    SpinyDendrite[323] {nseg=1 L=3 diam=1 }

    SpinyDendrite[320] connect SpinyDendrite[324](0),1
    SpinyDendrite[324] {nseg=1 L=14 diam=1.4 }

    SpinyDendrite[324] connect SpinyDendrite[325](0),1
    SpinyDendrite[325] {nseg=1 L=8 diam=1 }

    SpinyDendrite[324] connect SpinyDendrite[326](0),1
    SpinyDendrite[326] {nseg=1 L=6 diam=1 }


/**** Spiny 32 ****/
    SmoothDendrite[65] connect SpinyDendrite[327](0),1
    SpinyDendrite[327] {nseg=1 L=2 diam=2 }
 
    SpinyDendrite[327] connect SpinyDendrite[328](0),1
    SpinyDendrite[328] {nseg=1 L=7 diam=1.4 }

    SpinyDendrite[328] connect SpinyDendrite[329](0),1
    SpinyDendrite[329] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[329] connect SpinyDendrite[330](0),1
    SpinyDendrite[330] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[330] connect SpinyDendrite[331](0),1
    SpinyDendrite[331] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[331] connect SpinyDendrite[332](0),1
    SpinyDendrite[332] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[332] connect SpinyDendrite[333](0),1
    SpinyDendrite[333] {nseg=1 L=10 diam=1 }

    SpinyDendrite[332] connect SpinyDendrite[334](0),1
    SpinyDendrite[334] {nseg=1 L=9 diam=1 }

    SpinyDendrite[328] connect SpinyDendrite[335](0),1
    SpinyDendrite[335] {nseg=1 L=10 diam=1 }

    SpinyDendrite[329] connect SpinyDendrite[336](0),1
    SpinyDendrite[336] {nseg=1 L=4 diam=1 }

    SpinyDendrite[330] connect SpinyDendrite[337](0),1
    SpinyDendrite[337] {nseg=1 L=6 diam=1 }

    SpinyDendrite[331] connect SpinyDendrite[338](0),1
    SpinyDendrite[338] {nseg=1 L=8 diam=1 }

    SpinyDendrite[327] connect SpinyDendrite[339](0),1
    SpinyDendrite[339] {nseg=1 L=2 diam=2 }

    SpinyDendrite[339] connect SpinyDendrite[340](0),1
    SpinyDendrite[340] {nseg=1 L=8 diam=1 }

    SpinyDendrite[339] connect SpinyDendrite[341](0),1
    SpinyDendrite[341] {nseg=1 L=6 diam=2 }

    SpinyDendrite[341] connect SpinyDendrite[342](0),1
    SpinyDendrite[342] {nseg=1 L=11 diam=1 }

    SpinyDendrite[341] connect SpinyDendrite[343](0),1
    SpinyDendrite[343] {nseg=1 L=2 diam=2 }

    SpinyDendrite[343] connect SpinyDendrite[344](0),1
    SpinyDendrite[344] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[344] connect SpinyDendrite[345](0),1
    SpinyDendrite[345] {nseg=1 L=7 diam=1 }

    SpinyDendrite[344] connect SpinyDendrite[346](0),1
    SpinyDendrite[346] {nseg=1 L=7 diam=1 }

    SpinyDendrite[343] connect SpinyDendrite[347](0),1
    SpinyDendrite[347] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[347] connect SpinyDendrite[348](0),1
    SpinyDendrite[348] {nseg=1 L=15 diam=1 }

    SpinyDendrite[347] connect SpinyDendrite[349](0),1
    SpinyDendrite[349] {nseg=1 L=4 diam=1 }


/**** Spiny 33 ****/
    SmoothDendrite[60] connect SpinyDendrite[350](0),1
    SpinyDendrite[350] {nseg=1 L=3 diam=2 }
 
    SpinyDendrite[350] connect SpinyDendrite[351](0),1
    SpinyDendrite[351] {nseg=1 L=10 diam=1.4 }

    SpinyDendrite[351] connect SpinyDendrite[352](0),1
    SpinyDendrite[352] {nseg=1 L=5 diam=1 }

    SpinyDendrite[351] connect SpinyDendrite[353](0),1
    SpinyDendrite[353] {nseg=1 L=5 diam=1 }

    SpinyDendrite[350] connect SpinyDendrite[354](0),1
    SpinyDendrite[354] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[354] connect SpinyDendrite[355](0),1
    SpinyDendrite[355] {nseg=1 L=13 diam=1 }

    SpinyDendrite[354] connect SpinyDendrite[356](0),1
    SpinyDendrite[356] {nseg=1 L=10 diam=1.4 }

    SpinyDendrite[356] connect SpinyDendrite[357](0),1
    SpinyDendrite[357] {nseg=1 L=7 diam=1 }

    SpinyDendrite[356] connect SpinyDendrite[358](0),1
    SpinyDendrite[358] {nseg=1 L=6 diam=1 }


/**** Spiny 34 ****/
    SmoothDendrite[60] connect SpinyDendrite[359](0),1
    SpinyDendrite[359] {nseg=1 L=5 diam=2 }
 
    SpinyDendrite[359] connect SpinyDendrite[360](0),1
    SpinyDendrite[360] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[360] connect SpinyDendrite[361](0),1
    SpinyDendrite[361] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[361] connect SpinyDendrite[362](0),1
    SpinyDendrite[362] {nseg=1 L=10 diam=1 }

    SpinyDendrite[361] connect SpinyDendrite[363](0),1
    SpinyDendrite[363] {nseg=1 L=14 diam=1 }

    SpinyDendrite[360] connect SpinyDendrite[364](0),1
    SpinyDendrite[364] {nseg=1 L=15 diam=1 }

    SpinyDendrite[359] connect SpinyDendrite[365](0),1
    SpinyDendrite[365] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[365] connect SpinyDendrite[366](0),1
    SpinyDendrite[366] {nseg=1 L=5 diam=1 }

    SpinyDendrite[365] connect SpinyDendrite[367](0),1
    SpinyDendrite[367] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[367] connect SpinyDendrite[368](0),1
    SpinyDendrite[368] {nseg=1 L=8 diam=1 }

    SpinyDendrite[367] connect SpinyDendrite[369](0),1
    SpinyDendrite[369] {nseg=1 L=8 diam=1.4 }

    SpinyDendrite[369] connect SpinyDendrite[370](0),1
    SpinyDendrite[370] {nseg=1 L=4 diam=1 }

    SpinyDendrite[369] connect SpinyDendrite[371](0),1
    SpinyDendrite[371] {nseg=1 L=5 diam=1 }


/**** Spiny 35 ****/
    SmoothDendrite[27] connect SpinyDendrite[372](0),1
    SpinyDendrite[372] {nseg=1 L=6 diam=1.4 }
 
    SpinyDendrite[372] connect SpinyDendrite[373](0),1
    SpinyDendrite[373] {nseg=1 L=16 diam=1 }

    SpinyDendrite[372] connect SpinyDendrite[374](0),1
    SpinyDendrite[374] {nseg=1 L=1 diam=1 }


/**** Spiny 36 ****/
    SmoothDendrite[29] connect SpinyDendrite[375](0),1
    SpinyDendrite[375] {nseg=1 L=2 diam=2 }
 
    SpinyDendrite[375] connect SpinyDendrite[376](0),1
    SpinyDendrite[376] {nseg=1 L=4 diam=1 }

    SpinyDendrite[375] connect SpinyDendrite[377](0),1
    SpinyDendrite[377] {nseg=1 L=2 diam=2 }

    SpinyDendrite[377] connect SpinyDendrite[378](0),1
    SpinyDendrite[378] {nseg=1 L=6 diam=1 }

    SpinyDendrite[377] connect SpinyDendrite[379](0),1
    SpinyDendrite[379] {nseg=1 L=2 diam=2 }

    SpinyDendrite[379] connect SpinyDendrite[380](0),1
    SpinyDendrite[380] {nseg=1 L=6 diam=1 }

    SpinyDendrite[379] connect SpinyDendrite[381](0),1
    SpinyDendrite[381] {nseg=1 L=6 diam=2 }

    SpinyDendrite[381] connect SpinyDendrite[382](0),1
    SpinyDendrite[382] {nseg=1 L=11 diam=1 }

    SpinyDendrite[381] connect SpinyDendrite[383](0),1
    SpinyDendrite[383] {nseg=1 L=2 diam=2 }

    SpinyDendrite[383] connect SpinyDendrite[384](0),1
    SpinyDendrite[384] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[384] connect SpinyDendrite[385](0),1
    SpinyDendrite[385] {nseg=1 L=7 diam=1 }

    SpinyDendrite[384] connect SpinyDendrite[386](0),1
    SpinyDendrite[386] {nseg=1 L=11 diam=1 }

    SpinyDendrite[383] connect SpinyDendrite[387](0),1
    SpinyDendrite[387] {nseg=1 L=8 diam=1.4 }

    SpinyDendrite[387] connect SpinyDendrite[388](0),1
    SpinyDendrite[388] {nseg=1 L=15 diam=1 }

    SpinyDendrite[387] connect SpinyDendrite[389](0),1
    SpinyDendrite[389] {nseg=1 L=6 diam=1 }


/**** Spiny 37 ****/
    SmoothDendrite[29] connect SpinyDendrite[390](0),1
    SpinyDendrite[390] {nseg=1 L=8 diam=2 }
 
    SpinyDendrite[390] connect SpinyDendrite[391](0),1
    SpinyDendrite[391] {nseg=1 L=7 diam=1.4 }

    SpinyDendrite[391] connect SpinyDendrite[392](0),1
    SpinyDendrite[392] {nseg=1 L=13 diam=1.4 }

    SpinyDendrite[392] connect SpinyDendrite[393](0),1
    SpinyDendrite[393] {nseg=1 L=18 diam=1 }

    SpinyDendrite[392] connect SpinyDendrite[394](0),1
    SpinyDendrite[394] {nseg=1 L=14 diam=1 }

    SpinyDendrite[391] connect SpinyDendrite[395](0),1
    SpinyDendrite[395] {nseg=1 L=8 diam=1 }

    SpinyDendrite[390] connect SpinyDendrite[396](0),1
    SpinyDendrite[396] {nseg=1 L=2 diam=2 }

    SpinyDendrite[396] connect SpinyDendrite[397](0),1
    SpinyDendrite[397] {nseg=1 L=22 diam=1 }

    SpinyDendrite[396] connect SpinyDendrite[398](0),1
    SpinyDendrite[398] {nseg=1 L=11 diam=2 }

    SpinyDendrite[398] connect SpinyDendrite[399](0),1
    SpinyDendrite[399] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[399] connect SpinyDendrite[400](0),1
    SpinyDendrite[400] {nseg=1 L=7 diam=1 }

    SpinyDendrite[399] connect SpinyDendrite[401](0),1
    SpinyDendrite[401] {nseg=1 L=5 diam=1 }

    SpinyDendrite[398] connect SpinyDendrite[402](0),1
    SpinyDendrite[402] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[402] connect SpinyDendrite[403](0),1
    SpinyDendrite[403] {nseg=1 L=16 diam=1 }

    SpinyDendrite[402] connect SpinyDendrite[404](0),1
    SpinyDendrite[404] {nseg=1 L=12 diam=1.4 }

    SpinyDendrite[404] connect SpinyDendrite[405](0),1
    SpinyDendrite[405] {nseg=1 L=7 diam=1 }

    SpinyDendrite[404] connect SpinyDendrite[406](0),1
    SpinyDendrite[406] {nseg=1 L=6 diam=1 }


/**** Spiny 38 ****/
    SmoothDendrite[28] connect SpinyDendrite[407](0),1
    SpinyDendrite[407] {nseg=1 L=16 diam=1.4 }
 
    SpinyDendrite[407] connect SpinyDendrite[408](0),1
    SpinyDendrite[408] {nseg=1 L=5 diam=1 }

    SpinyDendrite[407] connect SpinyDendrite[409](0),1
    SpinyDendrite[409] {nseg=1 L=11 diam=1 }


/**** Spiny 39 ****/
    SmoothDendrite[26] connect SpinyDendrite[410](0),1
    SpinyDendrite[410] {nseg=1 L=14 diam=1.4 }
 
    SpinyDendrite[410] connect SpinyDendrite[411](0),1
    SpinyDendrite[411] {nseg=1 L=4 diam=1 }

    SpinyDendrite[410] connect SpinyDendrite[412](0),1
    SpinyDendrite[412] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[412] connect SpinyDendrite[413](0),1
    SpinyDendrite[413] {nseg=1 L=2 diam=1 }

    SpinyDendrite[412] connect SpinyDendrite[414](0),1
    SpinyDendrite[414] {nseg=1 L=7 diam=1.4 }

    SpinyDendrite[414] connect SpinyDendrite[415](0),1
    SpinyDendrite[415] {nseg=1 L=8 diam=1 }

    SpinyDendrite[414] connect SpinyDendrite[416](0),1
    SpinyDendrite[416] {nseg=1 L=15 diam=1 }


/**** Spiny 40 ****/
    SmoothDendrite[30] connect SpinyDendrite[417](0),1
    SpinyDendrite[417] {nseg=1 L=6 diam=2 }
 
    SpinyDendrite[417] connect SpinyDendrite[418](0),1
    SpinyDendrite[418] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[418] connect SpinyDendrite[419](0),1
    SpinyDendrite[419] {nseg=1 L=6 diam=1 }

    SpinyDendrite[418] connect SpinyDendrite[420](0),1
    SpinyDendrite[420] {nseg=1 L=5 diam=1 }

    SpinyDendrite[417] connect SpinyDendrite[421](0),1
    SpinyDendrite[421] {nseg=1 L=8 diam=2 }

    SpinyDendrite[421] connect SpinyDendrite[422](0),1
    SpinyDendrite[422] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[422] connect SpinyDendrite[423](0),1
    SpinyDendrite[423] {nseg=1 L=11 diam=1 }

    SpinyDendrite[422] connect SpinyDendrite[424](0),1
    SpinyDendrite[424] {nseg=1 L=14 diam=1 }

    SpinyDendrite[421] connect SpinyDendrite[425](0),1
    SpinyDendrite[425] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[425] connect SpinyDendrite[426](0),1
    SpinyDendrite[426] {nseg=1 L=3 diam=1 }

    SpinyDendrite[425] connect SpinyDendrite[427](0),1
    SpinyDendrite[427] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[427] connect SpinyDendrite[428](0),1
    SpinyDendrite[428] {nseg=1 L=11 diam=1 }

    SpinyDendrite[427] connect SpinyDendrite[429](0),1
    SpinyDendrite[429] {nseg=1 L=12 diam=1 }


/**** Spiny 41 ****/
    SmoothDendrite[32] connect SpinyDendrite[430](0),1
    SpinyDendrite[430] {nseg=1 L=1 diam=2 }
 
    SpinyDendrite[430] connect SpinyDendrite[431](0),1
    SpinyDendrite[431] {nseg=1 L=10 diam=1 }

    SpinyDendrite[430] connect SpinyDendrite[432](0),1
    SpinyDendrite[432] {nseg=1 L=1 diam=2 }

    SpinyDendrite[432] connect SpinyDendrite[433](0),1
    SpinyDendrite[433] {nseg=1 L=9 diam=1 }

    SpinyDendrite[432] connect SpinyDendrite[434](0),1
    SpinyDendrite[434] {nseg=1 L=2 diam=2 }

    SpinyDendrite[434] connect SpinyDendrite[435](0),1
    SpinyDendrite[435] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[435] connect SpinyDendrite[436](0),1
    SpinyDendrite[436] {nseg=1 L=4 diam=1 }

    SpinyDendrite[435] connect SpinyDendrite[437](0),1
    SpinyDendrite[437] {nseg=1 L=6 diam=1 }

    SpinyDendrite[434] connect SpinyDendrite[438](0),1
    SpinyDendrite[438] {nseg=1 L=3 diam=1.4 }
 
    SpinyDendrite[438] connect SpinyDendrite[439](0),1
    SpinyDendrite[439] {nseg=1 L=12 diam=1 }

    SpinyDendrite[438] connect SpinyDendrite[440](0),1
    SpinyDendrite[440] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[440] connect SpinyDendrite[441](0),1
    SpinyDendrite[441] {nseg=1 L=4 diam=1 }

    SpinyDendrite[440] connect SpinyDendrite[442](0),1
    SpinyDendrite[442] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[442] connect SpinyDendrite[443](0),1
    SpinyDendrite[443] {nseg=1 L=12 diam=1 }

    SpinyDendrite[442] connect SpinyDendrite[444](0),1
    SpinyDendrite[444] {nseg=1 L=10 diam=1 }


/**** Spiny 42 ****/
    SmoothDendrite[33] connect SpinyDendrite[445](0),1
    SpinyDendrite[445] {nseg=1 L=18 diam=1 }
 

/**** Spiny 43 ****/
    SmoothDendrite[34] connect SpinyDendrite[446](0),1
    SpinyDendrite[446] {nseg=1 L=2 diam=2 }
 
    SpinyDendrite[446] connect SpinyDendrite[447](0),1
    SpinyDendrite[447] {nseg=1 L=17 diam=1 }

    SpinyDendrite[446] connect SpinyDendrite[448](0),1
    SpinyDendrite[448] {nseg=1 L=1 diam=2 }

    SpinyDendrite[448] connect SpinyDendrite[449](0),1
    SpinyDendrite[449] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[449] connect SpinyDendrite[450](0),1
    SpinyDendrite[450] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[450] connect SpinyDendrite[451](0),1
    SpinyDendrite[451] {nseg=1 L=9 diam=1.4 }

    SpinyDendrite[451] connect SpinyDendrite[452](0),1
    SpinyDendrite[452] {nseg=1 L=8 diam=1 }

    SpinyDendrite[451] connect SpinyDendrite[453](0),1
    SpinyDendrite[453] {nseg=1 L=3 diam=1 }

    SpinyDendrite[449] connect SpinyDendrite[454](0),1
    SpinyDendrite[454] {nseg=1 L=19 diam=1 }

    SpinyDendrite[450] connect SpinyDendrite[455](0),1
    SpinyDendrite[455] {nseg=1 L=14 diam=1 }

    SpinyDendrite[448] connect SpinyDendrite[456](0),1
    SpinyDendrite[456] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[456] connect SpinyDendrite[457](0),1
    SpinyDendrite[457] {nseg=1 L=5 diam=1 }

    SpinyDendrite[456] connect SpinyDendrite[458](0),1
    SpinyDendrite[458] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[458] connect SpinyDendrite[459](0),1
    SpinyDendrite[459] {nseg=1 L=11 diam=1 }

    SpinyDendrite[458] connect SpinyDendrite[460](0),1
    SpinyDendrite[460] {nseg=1 L=7 diam=1.4 }

    SpinyDendrite[460] connect SpinyDendrite[461](0),1
    SpinyDendrite[461] {nseg=1 L=8 diam=1 }

    SpinyDendrite[460] connect SpinyDendrite[462](0),1
    SpinyDendrite[462] {nseg=1 L=6 diam=1 }


/**** Spiny 44 ****/
    SmoothDendrite[34] connect SpinyDendrite[463](0),1
    SpinyDendrite[463] {nseg=1 L=5 diam=2 }

    SpinyDendrite[463] connect SpinyDendrite[464](0),1
    SpinyDendrite[464] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[464] connect SpinyDendrite[465](0),1
    SpinyDendrite[465] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[465] connect SpinyDendrite[466](0),1
    SpinyDendrite[466] {nseg=1 L=6 diam=1 }

    SpinyDendrite[465] connect SpinyDendrite[467](0),1
    SpinyDendrite[467] {nseg=1 L=4 diam=1 }

    SpinyDendrite[464] connect SpinyDendrite[468](0),1
    SpinyDendrite[468] {nseg=1 L=2 diam=1 }

    SpinyDendrite[463] connect SpinyDendrite[469](0),1
    SpinyDendrite[469] {nseg=1 L=6 diam=2 }

    SpinyDendrite[469] connect SpinyDendrite[470](0),1
    SpinyDendrite[470] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[470] connect SpinyDendrite[471](0),1
    SpinyDendrite[471] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[471] connect SpinyDendrite[472](0),1
    SpinyDendrite[472] {nseg=1 L=4 diam=1 }

    SpinyDendrite[471] connect SpinyDendrite[473](0),1
    SpinyDendrite[473] {nseg=1 L=5 diam=1 }

    SpinyDendrite[470] connect SpinyDendrite[474](0),1
    SpinyDendrite[474] {nseg=1 L=10 diam=1 }

    SpinyDendrite[469] connect SpinyDendrite[475](0),1
    SpinyDendrite[475] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[475] connect SpinyDendrite[476](0),1
    SpinyDendrite[476] {nseg=1 L=20 diam=1 }

    SpinyDendrite[475] connect SpinyDendrite[477](0),1
    SpinyDendrite[477] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[477] connect SpinyDendrite[478](0),1
    SpinyDendrite[478] {nseg=1 L=8 diam=1 }

    SpinyDendrite[477] connect SpinyDendrite[479](0),1
    SpinyDendrite[479] {nseg=1 L=16 diam=1.4 }

    SpinyDendrite[479] connect SpinyDendrite[480](0),1
    SpinyDendrite[480] {nseg=1 L=8 diam=1 }

    SpinyDendrite[479] connect SpinyDendrite[481](0),1
    SpinyDendrite[481] {nseg=1 L=8 diam=1 }


/**** Spiny 45 ****/
    SmoothDendrite[43] connect SpinyDendrite[482](0),1
    SpinyDendrite[482] {nseg=1 L=7 diam=2 }

    SpinyDendrite[482] connect SpinyDendrite[483](0),1
    SpinyDendrite[483] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[483] connect SpinyDendrite[484](0),1
    SpinyDendrite[484] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[484] connect SpinyDendrite[485](0),1
    SpinyDendrite[485] {nseg=1 L=17 diam=1 }

    SpinyDendrite[484] connect SpinyDendrite[486](0),1
    SpinyDendrite[486] {nseg=1 L=19 diam=1 }

    SpinyDendrite[483] connect SpinyDendrite[487](0),1
    SpinyDendrite[487] {nseg=1 L=9 diam=1 }

    SpinyDendrite[482] connect SpinyDendrite[488](0),1
    SpinyDendrite[488] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[488] connect SpinyDendrite[489](0),1
    SpinyDendrite[489] {nseg=1 L=8 diam=1}

    SpinyDendrite[488] connect SpinyDendrite[490](0),1
    SpinyDendrite[490] {nseg=1 L=2 diam=1.4}

    SpinyDendrite[490] connect SpinyDendrite[491](0),1
    SpinyDendrite[491] {nseg=1 L=11 diam=1 }

    SpinyDendrite[490] connect SpinyDendrite[492](0),1
    SpinyDendrite[492] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[492] connect SpinyDendrite[493](0),1
    SpinyDendrite[493] {nseg=1 L=5 diam=1 }

    SpinyDendrite[492] connect SpinyDendrite[494](0),1
    SpinyDendrite[494] {nseg=1 L=8 diam=1 }
 

/**** Spiny 46 ****/
    SmoothDendrite[43] connect SpinyDendrite[495](0),1
    SpinyDendrite[495] {nseg=1 L=6 diam=2 }

    SpinyDendrite[495] connect SpinyDendrite[496](0),1
    SpinyDendrite[496] {nseg=1 L=14 diam=1.4 }

    SpinyDendrite[496] connect SpinyDendrite[497](0),1
    SpinyDendrite[497] {nseg=1 L=7 diam=1 }

    SpinyDendrite[496] connect SpinyDendrite[498](0),1
    SpinyDendrite[498] {nseg=1 L=4 diam=1 }

    SpinyDendrite[495] connect SpinyDendrite[499](0),1
    SpinyDendrite[499] {nseg=1 L=19 diam=1.4 }

    SpinyDendrite[499] connect SpinyDendrite[500](0),1
    SpinyDendrite[500] {nseg=1 L=9 diam=1 }

    SpinyDendrite[499] connect SpinyDendrite[501](0),1
    SpinyDendrite[501] {nseg=1 L=6 diam=1 }


/**** Spiny 47 ****/
    SmoothDendrite[42] connect SpinyDendrite[502](0),1
    SpinyDendrite[502] {nseg=1 L=1 diam=2 }

    SpinyDendrite[502] connect SpinyDendrite[503](0),1
    SpinyDendrite[503] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[503] connect SpinyDendrite[504](0),1
    SpinyDendrite[504] {nseg=1 L=30 diam=1 }

    SpinyDendrite[503] connect SpinyDendrite[505](0),1
    SpinyDendrite[505] {nseg=1 L=18 diam=1 }

    SpinyDendrite[502] connect SpinyDendrite[506](0),1
    SpinyDendrite[506] {nseg=1 L=8 diam=2 }

    SpinyDendrite[506] connect SpinyDendrite[507](0),1
    SpinyDendrite[507] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[507] connect SpinyDendrite[508](0),1
    SpinyDendrite[508] {nseg=1 L=4 diam=1 }

    SpinyDendrite[507] connect SpinyDendrite[509](0),1
    SpinyDendrite[509] {nseg=1 L=5 diam=1 }

    SpinyDendrite[506] connect SpinyDendrite[510](0),1
    SpinyDendrite[510] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[510] connect SpinyDendrite[511](0),1
    SpinyDendrite[511] {nseg=1 L=5 diam=1 }

    SpinyDendrite[510] connect SpinyDendrite[512](0),1
    SpinyDendrite[512] {nseg=1 L=7 diam=1.4 }

    SpinyDendrite[512] connect SpinyDendrite[513](0),1
    SpinyDendrite[513] {nseg=1 L=17 diam=1 }

    SpinyDendrite[512] connect SpinyDendrite[514](0),1
    SpinyDendrite[514] {nseg=1 L=6 diam=1 }
 

/**** Spiny 48 ****/
    SmoothDendrite[49] connect SpinyDendrite[515](0),1
    SpinyDendrite[515] {nseg=1 L=10 diam=1.4 }

    SpinyDendrite[515] connect SpinyDendrite[516](0),1
    SpinyDendrite[516] {nseg=1 L=13 diam=1 }

    SpinyDendrite[515] connect SpinyDendrite[517](0),1
    SpinyDendrite[517] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[517] connect SpinyDendrite[518](0),1
    SpinyDendrite[518] {nseg=1 L=7 diam=1 }

    SpinyDendrite[517] connect SpinyDendrite[519](0),1
    SpinyDendrite[519] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[519] connect SpinyDendrite[520](0),1
    SpinyDendrite[520] {nseg=1 L=12 diam=1 }

    SpinyDendrite[519] connect SpinyDendrite[521](0),1
    SpinyDendrite[521] {nseg=1 L=5 diam=1 }


/**** Spiny 49 ****/
    SmoothDendrite[50] connect SpinyDendrite[522](0),1
    SpinyDendrite[522] {nseg=1 L=14 diam=1 }


/**** Spiny 50 ****/
    SmoothDendrite[51] connect SpinyDendrite[523](0),1
    SpinyDendrite[523] {nseg=1 L=5 diam=2 }

    SpinyDendrite[523] connect SpinyDendrite[524](0),1
    SpinyDendrite[524] {nseg=1 L=8 diam=1.4 }

    SpinyDendrite[524] connect SpinyDendrite[525](0),1
    SpinyDendrite[525] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[525] connect SpinyDendrite[526](0),1
    SpinyDendrite[526] {nseg=1 L=22 diam=1 }

    SpinyDendrite[525] connect SpinyDendrite[527](0),1
    SpinyDendrite[527] {nseg=1 L=8 diam=1 }

    SpinyDendrite[524] connect SpinyDendrite[528](0),1
    SpinyDendrite[528] {nseg=1 L=14 diam=1 }

    SpinyDendrite[523] connect SpinyDendrite[529](0),1
    SpinyDendrite[529] {nseg=1 L=8 diam=2 }

    SpinyDendrite[529] connect SpinyDendrite[530](0),1
    SpinyDendrite[530] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[530] connect SpinyDendrite[531](0),1
    SpinyDendrite[531] {nseg=1 L=9 diam=1 }

    SpinyDendrite[530] connect SpinyDendrite[532](0),1
    SpinyDendrite[532] {nseg=1 L=18 diam=1 }

    SpinyDendrite[529] connect SpinyDendrite[533](0),1
    SpinyDendrite[533] {nseg=1 L=25 diam=2 }

    SpinyDendrite[533] connect SpinyDendrite[534](0),1
    SpinyDendrite[534] {nseg=1 L=8 diam=1 }

    SpinyDendrite[533] connect SpinyDendrite[535](0),1
    SpinyDendrite[535] {nseg=1 L=10 diam=2 }

    SpinyDendrite[535] connect SpinyDendrite[536](0),1
    SpinyDendrite[536] {nseg=1 L=9 diam=1 }

    SpinyDendrite[535] connect SpinyDendrite[537](0),1
    SpinyDendrite[537] {nseg=1 L=2 diam=2 }

    SpinyDendrite[537] connect SpinyDendrite[538](0),1
    SpinyDendrite[538] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[538] connect SpinyDendrite[539](0),1
    SpinyDendrite[539] {nseg=1 L=13 diam=1 }

    SpinyDendrite[538] connect SpinyDendrite[540](0),1
    SpinyDendrite[540] {nseg=1 L=7 diam=1 }

    SpinyDendrite[537] connect SpinyDendrite[541](0),1
    SpinyDendrite[541] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[541] connect SpinyDendrite[542](0),1
    SpinyDendrite[542] {nseg=1 L=8 diam=1 }

    SpinyDendrite[541] connect SpinyDendrite[543](0),1
    SpinyDendrite[543] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[543] connect SpinyDendrite[544](0),1
    SpinyDendrite[544] {nseg=1 L=14 diam=1 }

    SpinyDendrite[543] connect SpinyDendrite[545](0),1
    SpinyDendrite[545] {nseg=1 L=14 diam=1 }


/**** Spiny 51 ****/
    SmoothDendrite[51] connect SpinyDendrite[546](0),1
    SpinyDendrite[546] {nseg=1 L=7 diam=2 }

    SpinyDendrite[546] connect SpinyDendrite[547](0),1
    SpinyDendrite[547] {nseg=1 L=10 diam=1.4 }

    SpinyDendrite[547] connect SpinyDendrite[548](0),1
    SpinyDendrite[548] {nseg=1 L=8 diam=1 }

    SpinyDendrite[547] connect SpinyDendrite[549](0),1
    SpinyDendrite[549] {nseg=1 L=10 diam=1 }

    SpinyDendrite[546] connect SpinyDendrite[550](0),1
    SpinyDendrite[550] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[550] connect SpinyDendrite[551](0),1
    SpinyDendrite[551] {nseg=1 L=14 diam=1 }

    SpinyDendrite[550] connect SpinyDendrite[552](0),1
    SpinyDendrite[552] {nseg=1 L=9 diam=1.4 }

    SpinyDendrite[552] connect SpinyDendrite[553](0),1
    SpinyDendrite[553] {nseg=1 L=29 diam=1 }

    SpinyDendrite[552] connect SpinyDendrite[554](0),1
    SpinyDendrite[554] {nseg=1 L=30 diam=1 }


/**** Spiny 52 ****/
    SmoothDendrite[48] connect SpinyDendrite[555](0),1
    SpinyDendrite[555] {nseg=1 L=4 diam=2 }

    SpinyDendrite[555] connect SpinyDendrite[556](0),1
    SpinyDendrite[556] {nseg=1 L=20 diam=1.4 }

    SpinyDendrite[556] connect SpinyDendrite[557](0),1
    SpinyDendrite[557] {nseg=1 L=9 diam=1 }

    SpinyDendrite[556] connect SpinyDendrite[558](0),1
    SpinyDendrite[558] {nseg=1 L=12 diam=1 }

    SpinyDendrite[555] connect SpinyDendrite[559](0),1
    SpinyDendrite[559] {nseg=1 L=5 diam=2 }

    SpinyDendrite[559] connect SpinyDendrite[560](0),1
    SpinyDendrite[560] {nseg=1 L=7 diam=1 }

    SpinyDendrite[559] connect SpinyDendrite[561](0),1
    SpinyDendrite[561] {nseg=1 L=9 diam=2 }

    SpinyDendrite[561] connect SpinyDendrite[562](0),1
    SpinyDendrite[562] {nseg=1 L=6 diam=1 }

    SpinyDendrite[561] connect SpinyDendrite[563](0),1
    SpinyDendrite[563] {nseg=1 L=4 diam=2 }

    SpinyDendrite[563] connect SpinyDendrite[564](0),1
    SpinyDendrite[564] {nseg=1 L=7 diam=1 }

    SpinyDendrite[563] connect SpinyDendrite[565](0),1
    SpinyDendrite[565] {nseg=1 L=10 diam=2 }

    SpinyDendrite[565] connect SpinyDendrite[566](0),1
    SpinyDendrite[566] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[566] connect SpinyDendrite[567](0),1
    SpinyDendrite[567] {nseg=1 L=5 diam=1 }
 
    SpinyDendrite[566] connect SpinyDendrite[568](0),1
    SpinyDendrite[568] {nseg=1 L=20 diam=1 }

    SpinyDendrite[565] connect SpinyDendrite[569](0),1
    SpinyDendrite[569] {nseg=1 L=10 diam=1.4 }

    SpinyDendrite[569] connect SpinyDendrite[570](0),1
    SpinyDendrite[570] {nseg=1 L=3 diam=1 }

    SpinyDendrite[569] connect SpinyDendrite[571](0),1
    SpinyDendrite[571] {nseg=1 L=5 diam=1.4 }
 
    SpinyDendrite[571] connect SpinyDendrite[572](0),1
    SpinyDendrite[572] {nseg=1 L=5 diam=1 }

    SpinyDendrite[571] connect SpinyDendrite[573](0),1
    SpinyDendrite[573] {nseg=1 L=4 diam=1 }
 

/**** Spiny 53 ****/
    SmoothDendrite[47] connect SpinyDendrite[574](0),1
    SpinyDendrite[574] {nseg=1 L=16 diam=1 }


/**** Spiny 54 ****/
    SmoothDendrite[45] connect SpinyDendrite[575](0),1
    SpinyDendrite[575] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[575] connect SpinyDendrite[576](0),1
    SpinyDendrite[576] {nseg=1 L=8 diam=1 }

    SpinyDendrite[575] connect SpinyDendrite[577](0),1
    SpinyDendrite[577] {nseg=1 L=12 diam=1.4 }

    SpinyDendrite[577] connect SpinyDendrite[578](0),1
    SpinyDendrite[578] {nseg=1 L=16 diam=1 }

    SpinyDendrite[577] connect SpinyDendrite[579](0),1
    SpinyDendrite[579] {nseg=1 L=3 diam=1 }


/**** Spiny 55 ****/
    SmoothDendrite[46] connect SpinyDendrite[580](0),1
    SpinyDendrite[580] {nseg=1 L=20 diam=2 }

    SpinyDendrite[580] connect SpinyDendrite[581](0),1
    SpinyDendrite[581] {nseg=1 L=25 diam=1 }

    SpinyDendrite[580] connect SpinyDendrite[582](0),1
    SpinyDendrite[582] {nseg=1 L=4 diam=2 }

    SpinyDendrite[582] connect SpinyDendrite[583](0),1
    SpinyDendrite[583] {nseg=1 L=6 diam=1 }

    SpinyDendrite[582] connect SpinyDendrite[584](0),1
    SpinyDendrite[584] {nseg=1 L=16 diam=2 }

    SpinyDendrite[584] connect SpinyDendrite[585](0),1
    SpinyDendrite[585] {nseg=1 L=13 diam=1 }

    SpinyDendrite[584] connect SpinyDendrite[586](0),1
    SpinyDendrite[586] {nseg=1 L=3 diam=2 }

    SpinyDendrite[586] connect SpinyDendrite[587](0),1
    SpinyDendrite[587] {nseg=1 L=15 diam=1.4 }

    SpinyDendrite[587] connect SpinyDendrite[588](0),1
    SpinyDendrite[588] {nseg=1 L=16 diam=1 }

    SpinyDendrite[587] connect SpinyDendrite[589](0),1
    SpinyDendrite[589] {nseg=1 L=14 diam=1 }

    SpinyDendrite[586] connect SpinyDendrite[590](0),1
    SpinyDendrite[590] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[590] connect SpinyDendrite[591](0),1
    SpinyDendrite[591] {nseg=1 L=6 diam=1 }

    SpinyDendrite[590] connect SpinyDendrite[592](0),1
    SpinyDendrite[592] {nseg=1 L=10 diam=1.4 }

    SpinyDendrite[592] connect SpinyDendrite[593](0),1
    SpinyDendrite[593] {nseg=1 L=16 diam=1 }

    SpinyDendrite[592] connect SpinyDendrite[594](0),1
    SpinyDendrite[594] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[594] connect SpinyDendrite[595](0),1
    SpinyDendrite[595] {nseg=1 L=16 diam=1 }

    SpinyDendrite[594] connect SpinyDendrite[596](0),1
    SpinyDendrite[596] {nseg=1 L=6 diam=1 }


/**** Spiny 56 ****/
    SmoothDendrite[46] connect SpinyDendrite[597](0),1
    SpinyDendrite[597] {nseg=1 L=4 diam=2 }

    SpinyDendrite[597] connect SpinyDendrite[598](0),1
    SpinyDendrite[598] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[598] connect SpinyDendrite[599](0),1
    SpinyDendrite[599] {nseg=1 L=14 diam=1.4 }

    SpinyDendrite[599] connect SpinyDendrite[600](0),1
    SpinyDendrite[600] {nseg=1 L=10 diam=1.4 }

    SpinyDendrite[600] connect SpinyDendrite[601](0),1
    SpinyDendrite[601] {nseg=1 L=17 diam=1.4 }

    SpinyDendrite[601] connect SpinyDendrite[602](0),1
    SpinyDendrite[602] {nseg=1 L=10 diam=1 }

    SpinyDendrite[601] connect SpinyDendrite[603](0),1
    SpinyDendrite[603] {nseg=1 L=22 diam=1 }

    SpinyDendrite[598] connect SpinyDendrite[604](0),1
    SpinyDendrite[604] {nseg=1 L=8 diam=1 }

    SpinyDendrite[599] connect SpinyDendrite[605](0),1
    SpinyDendrite[605] {nseg=1 L=30 diam=1 }

    SpinyDendrite[600] connect SpinyDendrite[606](0),1
    SpinyDendrite[606] {nseg=1 L=14 diam=1 }

    SpinyDendrite[597] connect SpinyDendrite[607](0),1
    SpinyDendrite[607] {nseg=1 L=3 diam=2 }

    SpinyDendrite[607] connect SpinyDendrite[608](0),1
    SpinyDendrite[608] {nseg=1 L=2 diam=1 }

    SpinyDendrite[607] connect SpinyDendrite[609](0),1
    SpinyDendrite[609] {nseg=1 L=1 diam=2 }
 
    SpinyDendrite[609] connect SpinyDendrite[610](0),1
    SpinyDendrite[610] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[610] connect SpinyDendrite[611](0),1
    SpinyDendrite[611] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[611] connect SpinyDendrite[612](0),1
    SpinyDendrite[612] {nseg=1 L=25 diam=1 }

    SpinyDendrite[611] connect SpinyDendrite[613](0),1
    SpinyDendrite[613] {nseg=1 L=4 diam=1 }

    SpinyDendrite[610] connect SpinyDendrite[614](0),1
    SpinyDendrite[614] {nseg=1 L=6 diam=1 }

    SpinyDendrite[609] connect SpinyDendrite[615](0),1
    SpinyDendrite[615] {nseg=1 L=4 diam=2 }

    SpinyDendrite[615] connect SpinyDendrite[616](0),1
    SpinyDendrite[616] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[616] connect SpinyDendrite[617](0),1
    SpinyDendrite[617] {nseg=1 L=4 diam=1 }

    SpinyDendrite[616] connect SpinyDendrite[618](0),1
    SpinyDendrite[618] {nseg=1 L=9 diam=1 }

    SpinyDendrite[615] connect SpinyDendrite[619](0),1
    SpinyDendrite[619] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[619] connect SpinyDendrite[620](0),1
    SpinyDendrite[620] {nseg=1 L=10 diam=1 }

    SpinyDendrite[619] connect SpinyDendrite[621](0),1
    SpinyDendrite[621] {nseg=1 L=8 diam=1 }


/**** Spiny 57 ****/
    SmoothDendrite[40] connect SpinyDendrite[622](0),1
    SpinyDendrite[622] {nseg=1 L=3 diam=2 }

    SpinyDendrite[622] connect SpinyDendrite[623](0),1
    SpinyDendrite[623] {nseg=1 L=9 diam=1.4 }

    SpinyDendrite[623] connect SpinyDendrite[624](0),1
    SpinyDendrite[624] {nseg=1 L=27 diam=1 }

    SpinyDendrite[623] connect SpinyDendrite[625](0),1
    SpinyDendrite[625] {nseg=1 L=11 diam=1 }

    SpinyDendrite[622] connect SpinyDendrite[626](0),1
    SpinyDendrite[626] {nseg=1 L=4 diam=2 }

    SpinyDendrite[626] connect SpinyDendrite[627](0),1
    SpinyDendrite[627] {nseg=1 L=1 diam=1.4 }

    SpinyDendrite[627] connect SpinyDendrite[628](0),1
    SpinyDendrite[628] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[628] connect SpinyDendrite[629](0),1
    SpinyDendrite[629] {nseg=1 L=5 diam=1 }

    SpinyDendrite[628] connect SpinyDendrite[630](0),1
    SpinyDendrite[630] {nseg=1 L=25 diam=1 }

    SpinyDendrite[627] connect SpinyDendrite[631](0),1
    SpinyDendrite[631] {nseg=1 L=16 diam=1 }

    SpinyDendrite[626] connect SpinyDendrite[632](0),1
    SpinyDendrite[632] {nseg=1 L=18 diam=2 }

    SpinyDendrite[632] connect SpinyDendrite[633](0),1
    SpinyDendrite[633] {nseg=1 L=10 diam=1.4 }

    SpinyDendrite[633] connect SpinyDendrite[634](0),1
    SpinyDendrite[634] {nseg=1 L=8 diam=1 }
 
    SpinyDendrite[633] connect SpinyDendrite[635](0),1
    SpinyDendrite[635] {nseg=1 L=6 diam=1 }

    SpinyDendrite[632] connect SpinyDendrite[636](0),1
    SpinyDendrite[636] {nseg=1 L=12 diam=1.4 }

    SpinyDendrite[636] connect SpinyDendrite[637](0),1
    SpinyDendrite[637] {nseg=1 L=18 diam=1 }

    SpinyDendrite[636] connect SpinyDendrite[638](0),1
    SpinyDendrite[638] {nseg=1 L=8 diam=1 }

 
/**** Spiny 58 ****/
    SmoothDendrite[39] connect SpinyDendrite[639](0),1
    SpinyDendrite[639] {nseg=1 L=4 diam=2 }

    SpinyDendrite[639] connect SpinyDendrite[640](0),1
    SpinyDendrite[640] {nseg=1 L=10 diam=1 }

    SpinyDendrite[639] connect SpinyDendrite[641](0),1
    SpinyDendrite[641] {nseg=1 L=2 diam=2 }

    SpinyDendrite[641] connect SpinyDendrite[642](0),1
    SpinyDendrite[642] {nseg=1 L=9 diam=1 }

    SpinyDendrite[641] connect SpinyDendrite[643](0),1
    SpinyDendrite[643] {nseg=1 L=2 diam=2 }

    SpinyDendrite[643] connect SpinyDendrite[644](0),1
    SpinyDendrite[644] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[644] connect SpinyDendrite[645](0),1
    SpinyDendrite[645] {nseg=1 L=18 diam=1 }

    SpinyDendrite[644] connect SpinyDendrite[646](0),1
    SpinyDendrite[646] {nseg=1 L=9 diam=1 }

    SpinyDendrite[643] connect SpinyDendrite[647](0),1
    SpinyDendrite[647] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[647] connect SpinyDendrite[648](0),1
    SpinyDendrite[648] {nseg=1 L=16 diam=1 }

    SpinyDendrite[647] connect SpinyDendrite[649](0),1
    SpinyDendrite[649] {nseg=1 L=8 diam=1 }


/**** Spiny 59 ****/
    SmoothDendrite[39] connect SpinyDendrite[650](0),1
    SpinyDendrite[650] {nseg=1 L=1 diam=2 }

    SpinyDendrite[650] connect SpinyDendrite[651](0),1
    SpinyDendrite[651] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[651] connect SpinyDendrite[652](0),1
    SpinyDendrite[652] {nseg=1 L=13 diam=1.4 }

    SpinyDendrite[652] connect SpinyDendrite[653](0),1
    SpinyDendrite[653] {nseg=1 L=22 diam=1 }

    SpinyDendrite[652] connect SpinyDendrite[654](0),1
    SpinyDendrite[654] {nseg=1 L=4 diam=1 }

    SpinyDendrite[651] connect SpinyDendrite[655](0),1
    SpinyDendrite[655] {nseg=1 L=7 diam=1 }

    SpinyDendrite[650] connect SpinyDendrite[656](0),1
    SpinyDendrite[656] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[656] connect SpinyDendrite[657](0),1
    SpinyDendrite[657] {nseg=1 L=10 diam=1 }

    SpinyDendrite[656] connect SpinyDendrite[658](0),1
    SpinyDendrite[658] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[658] connect SpinyDendrite[659](0),1
    SpinyDendrite[659] {nseg=1 L=4 diam=1 }

    SpinyDendrite[658] connect SpinyDendrite[660](0),1
    SpinyDendrite[660] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[660] connect SpinyDendrite[661](0),1
    SpinyDendrite[661] {nseg=1 L=11 diam=1 }

    SpinyDendrite[660] connect SpinyDendrite[662](0),1
    SpinyDendrite[662] {nseg=1 L=2 diam=1.4 }
 
    SpinyDendrite[662] connect SpinyDendrite[663](0),1
    SpinyDendrite[663] {nseg=1 L=11 diam=1 }

    SpinyDendrite[662] connect SpinyDendrite[664](0),1
    SpinyDendrite[664] {nseg=1 L=24 diam=1 }
 

/**** Spiny 60 ****/
    SmoothDendrite[37] connect SpinyDendrite[665](0),1
    SpinyDendrite[665] {nseg=1 L=24 diam=1 }


/**** Spiny 61 ****/
    SmoothDendrite[36] connect SpinyDendrite[666](0),1
    SpinyDendrite[666] {nseg=1 L=10 diam=2 }

    SpinyDendrite[666] connect SpinyDendrite[667](0),1
    SpinyDendrite[667] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[667] connect SpinyDendrite[668](0),1
    SpinyDendrite[668] {nseg=1 L=19 diam=1 }

    SpinyDendrite[667] connect SpinyDendrite[669](0),1
    SpinyDendrite[669] {nseg=1 L=4 diam=1 }

    SpinyDendrite[666] connect SpinyDendrite[670](0),1
    SpinyDendrite[670] {nseg=1 L=9 diam=2 }

    SpinyDendrite[670] connect SpinyDendrite[671](0),1
    SpinyDendrite[671] {nseg=1 L=12 diam=1.4 }

    SpinyDendrite[671] connect SpinyDendrite[672](0),1
    SpinyDendrite[672] {nseg=1 L=12 diam=1 }

    SpinyDendrite[671] connect SpinyDendrite[673](0),1
    SpinyDendrite[673] {nseg=1 L=8 diam=1 }

    SpinyDendrite[670] connect SpinyDendrite[674](0),1
    SpinyDendrite[674] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[674] connect SpinyDendrite[675](0),1
    SpinyDendrite[675] {nseg=1 L=7 diam=1 }

    SpinyDendrite[674] connect SpinyDendrite[676](0),1
    SpinyDendrite[676] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[676] connect SpinyDendrite[677](0),1
    SpinyDendrite[677] {nseg=1 L=10 diam=1 }

    SpinyDendrite[676] connect SpinyDendrite[678](0),1
    SpinyDendrite[678] {nseg=1 L=8 diam=1 }
 

/**** Spiny 62 ****/
    SmoothDendrite[36] connect SpinyDendrite[679](0),1
    SpinyDendrite[679] {nseg=1 L=4 diam=2 }

    SpinyDendrite[679] connect SpinyDendrite[680](0),1
    SpinyDendrite[680] {nseg=1 L=8 diam=1 }

    SpinyDendrite[679] connect SpinyDendrite[681](0),1
    SpinyDendrite[681] {nseg=1 L=7 diam=2 }

    SpinyDendrite[681] connect SpinyDendrite[682](0),1
    SpinyDendrite[682] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[682] connect SpinyDendrite[683](0),1
    SpinyDendrite[683] {nseg=1 L=5 diam=1 }

    SpinyDendrite[682] connect SpinyDendrite[684](0),1
    SpinyDendrite[684] {nseg=1 L=9 diam=1 }

    SpinyDendrite[681] connect SpinyDendrite[685](0),1
    SpinyDendrite[685] {nseg=1 L=4 diam=2 }

    SpinyDendrite[685] connect SpinyDendrite[686](0),1
    SpinyDendrite[686] {nseg=1 L=11 diam=1.4 }

    SpinyDendrite[686] connect SpinyDendrite[687](0),1
    SpinyDendrite[687] {nseg=1 L=16 diam=1 }

    SpinyDendrite[686] connect SpinyDendrite[688](0),1
    SpinyDendrite[688] {nseg=1 L=12 diam=1 }

    SpinyDendrite[685] connect SpinyDendrite[689](0),1
    SpinyDendrite[689] {nseg=1 L=8 diam=2 }

    SpinyDendrite[689] connect SpinyDendrite[690](0),1
    SpinyDendrite[690] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[690] connect SpinyDendrite[691](0),1
    SpinyDendrite[691] {nseg=1 L=7 diam=1 }
 
    SpinyDendrite[690] connect SpinyDendrite[692](0),1
    SpinyDendrite[692] {nseg=1 L=8 diam=1 }

    SpinyDendrite[689] connect SpinyDendrite[693](0),1
    SpinyDendrite[693] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[693] connect SpinyDendrite[694](0),1
    SpinyDendrite[694] {nseg=1 L=4 diam=1 }

    SpinyDendrite[693] connect SpinyDendrite[695](0),1
    SpinyDendrite[695] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[695] connect SpinyDendrite[696](0),1
    SpinyDendrite[696] {nseg=1 L=11 diam=1 }

    SpinyDendrite[695] connect SpinyDendrite[697](0),1
    SpinyDendrite[697] {nseg=1 L=8 diam=1.4 }

    SpinyDendrite[697] connect SpinyDendrite[698](0),1
    SpinyDendrite[698] {nseg=1 L=9 diam=1 }

    SpinyDendrite[697] connect SpinyDendrite[699](0),1
    SpinyDendrite[699] {nseg=1 L=6 diam=1 }


/**** Spiny 63 ****/
    SmoothDendrite[12] connect SpinyDendrite[700](0),1
    SpinyDendrite[700] {nseg=1 L=12 diam=1 }


/**** Spiny 64 ****/
    SmoothDendrite[13] connect SpinyDendrite[701](0),1
    SpinyDendrite[701] {nseg=1 L=6 diam=2 }

    SpinyDendrite[701] connect SpinyDendrite[702](0),1
    SpinyDendrite[702] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[702] connect SpinyDendrite[703](0),1
    SpinyDendrite[703] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[703] connect SpinyDendrite[704](0),1
    SpinyDendrite[704] {nseg=1 L=5 diam=1 }

    SpinyDendrite[703] connect SpinyDendrite[705](0),1
    SpinyDendrite[705] {nseg=1 L=5 diam=1 }

    SpinyDendrite[702] connect SpinyDendrite[706](0),1
    SpinyDendrite[706] {nseg=1 L=11 diam=1 }

    SpinyDendrite[701] connect SpinyDendrite[707](0),1
    SpinyDendrite[707] {nseg=1 L=7 diam=2 }

    SpinyDendrite[707] connect SpinyDendrite[708](0),1
    SpinyDendrite[708] {nseg=1 L=10 diam=1.4 }

    SpinyDendrite[708] connect SpinyDendrite[709](0),1
    SpinyDendrite[709] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[709] connect SpinyDendrite[710](0),1
    SpinyDendrite[710] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[710] connect SpinyDendrite[711](0),1
    SpinyDendrite[711] {nseg=1 L=10 diam=1.4 }

    SpinyDendrite[711] connect SpinyDendrite[712](0),1
    SpinyDendrite[712] {nseg=1 L=14 diam=1 }

    SpinyDendrite[711] connect SpinyDendrite[713](0),1
    SpinyDendrite[713] {nseg=1 L=5 diam=1 }
 
    SpinyDendrite[708] connect SpinyDendrite[714](0),1
    SpinyDendrite[714] {nseg=1 L=7 diam=1 }

    SpinyDendrite[709] connect SpinyDendrite[715](0),1
    SpinyDendrite[715] {nseg=1 L=6 diam=1 }

    SpinyDendrite[710] connect SpinyDendrite[716](0),1
    SpinyDendrite[716] {nseg=1 L=10 diam=1 }

    SpinyDendrite[707] connect SpinyDendrite[717](0),1
    SpinyDendrite[717] {nseg=1 L=4 diam=2 }

    SpinyDendrite[717] connect SpinyDendrite[718](0),1
    SpinyDendrite[718] {nseg=1 L=7 diam=1.4 }

    SpinyDendrite[718] connect SpinyDendrite[719](0),1
    SpinyDendrite[719] {nseg=1 L=15 diam=1 }

    SpinyDendrite[718] connect SpinyDendrite[720](0),1
    SpinyDendrite[720] {nseg=1 L=18 diam=1 }

    SpinyDendrite[717] connect SpinyDendrite[721](0),1
    SpinyDendrite[721] {nseg=1 L=9 diam=1.4 }

    SpinyDendrite[721] connect SpinyDendrite[722](0),1
    SpinyDendrite[722] {nseg=1 L=10 diam=1 }

    SpinyDendrite[721] connect SpinyDendrite[723](0),1
    SpinyDendrite[723] {nseg=1 L=10 diam=1.4 }

    SpinyDendrite[723] connect SpinyDendrite[724](0),1
    SpinyDendrite[724] {nseg=1 L=8 diam=1 }

    SpinyDendrite[723] connect SpinyDendrite[725](0),1
    SpinyDendrite[725] {nseg=1 L=6 diam=1 }


/**** Spiny 65 ****/
    SmoothDendrite[18] connect SpinyDendrite[726](0),1
    SpinyDendrite[726] {nseg=1 L=8 diam=2 }

    SpinyDendrite[726] connect SpinyDendrite[727](0),1
    SpinyDendrite[727] {nseg=1 L=11 diam=1 }

    SpinyDendrite[726] connect SpinyDendrite[728](0),1
    SpinyDendrite[728] {nseg=1 L=2 diam=2 }

    SpinyDendrite[728] connect SpinyDendrite[729](0),1
    SpinyDendrite[729] {nseg=1 L=25 diam=1 }

    SpinyDendrite[728] connect SpinyDendrite[730](0),1
    SpinyDendrite[730] {nseg=1 L=12 diam=2 }

    SpinyDendrite[730] connect SpinyDendrite[731](0),1
    SpinyDendrite[731] {nseg=1 L=13 diam=1.4 }

    SpinyDendrite[731] connect SpinyDendrite[732](0),1
    SpinyDendrite[732] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[732] connect SpinyDendrite[733](0),1
    SpinyDendrite[733] {nseg=1 L=9 diam=1 }

    SpinyDendrite[732] connect SpinyDendrite[734](0),1
    SpinyDendrite[734] {nseg=1 L=7 diam=1 }

    SpinyDendrite[731] connect SpinyDendrite[735](0),1
    SpinyDendrite[735] {nseg=1 L=10 diam=1 }

    SpinyDendrite[730] connect SpinyDendrite[736](0),1
    SpinyDendrite[736] {nseg=1 L=7 diam=1.4 }

    SpinyDendrite[736] connect SpinyDendrite[737](0),1
    SpinyDendrite[737] {nseg=1 L=11 diam=1 }

    SpinyDendrite[736] connect SpinyDendrite[738](0),1
    SpinyDendrite[738] {nseg=1 L=24 diam=1.4 }
 
    SpinyDendrite[738] connect SpinyDendrite[739](0),1
    SpinyDendrite[739] {nseg=1 L=10 diam=1 }

    SpinyDendrite[738] connect SpinyDendrite[740](0),1
    SpinyDendrite[740] {nseg=1 L=3 diam=1 }


/**** Spiny 66 ****/
    SmoothDendrite[19] connect SpinyDendrite[741](0),1
    SpinyDendrite[741] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[741] connect SpinyDendrite[742](0),1
    SpinyDendrite[742] {nseg=1 L=26 diam=1 }

    SpinyDendrite[741] connect SpinyDendrite[743](0),1
    SpinyDendrite[743] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[743] connect SpinyDendrite[744](0),1
    SpinyDendrite[744] {nseg=1 L=16 diam=1 }

    SpinyDendrite[743] connect SpinyDendrite[745](0),1
    SpinyDendrite[745] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[745] connect SpinyDendrite[746](0),1
    SpinyDendrite[746] {nseg=1 L=22 diam=1 }

    SpinyDendrite[745] connect SpinyDendrite[747](0),1
    SpinyDendrite[747] {nseg=1 L=11 diam=1.4 }

    SpinyDendrite[747] connect SpinyDendrite[748](0),1
    SpinyDendrite[748] {nseg=1 L=18 diam=1 }

    SpinyDendrite[747] connect SpinyDendrite[749](0),1
    SpinyDendrite[749] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[749] connect SpinyDendrite[750](0),1
    SpinyDendrite[750] {nseg=1 L=17 diam=1 }

    SpinyDendrite[749] connect SpinyDendrite[751](0),1
    SpinyDendrite[751] {nseg=1 L=8 diam=1 }


/**** Spiny 67 ****/
    SmoothDendrite[23] connect SpinyDendrite[752](0),1
    SpinyDendrite[752] {nseg=1 L=15 diam=2 }

    SpinyDendrite[752] connect SpinyDendrite[753](0),1
    SpinyDendrite[753] {nseg=1 L=24 diam=1.4 }

    SpinyDendrite[753] connect SpinyDendrite[754](0),1
    SpinyDendrite[754] {nseg=1 L=16 diam=1 }

    SpinyDendrite[753] connect SpinyDendrite[755](0),1
    SpinyDendrite[755] {nseg=1 L=8 diam=1 }

    SpinyDendrite[752] connect SpinyDendrite[756](0),1
    SpinyDendrite[756] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[756] connect SpinyDendrite[757](0),1
    SpinyDendrite[757] {nseg=1 L=12 diam=1 }

    SpinyDendrite[756] connect SpinyDendrite[758](0),1
    SpinyDendrite[758] {nseg=1 L=12 diam=1.4 }

    SpinyDendrite[758] connect SpinyDendrite[759](0),1
    SpinyDendrite[759] {nseg=1 L=4 diam=1 }

    SpinyDendrite[758] connect SpinyDendrite[760](0),1
    SpinyDendrite[760] {nseg=1 L=14 diam=1 }


/**** Spiny 68 ****/
    SmoothDendrite[24] connect SpinyDendrite[761](0),1
    SpinyDendrite[761] {nseg=1 L=8 diam=2 }

    SpinyDendrite[761] connect SpinyDendrite[762](0),1
    SpinyDendrite[762] {nseg=1 L=13 diam=1.4 }

    SpinyDendrite[762] connect SpinyDendrite[763](0),1
    SpinyDendrite[763] {nseg=1 L=12 diam=1.4 }

    SpinyDendrite[763] connect SpinyDendrite[764](0),1
    SpinyDendrite[764] {nseg=1 L=20 diam=1 }

    SpinyDendrite[763] connect SpinyDendrite[765](0),1
    SpinyDendrite[765] {nseg=1 L=25 diam=1 }

    SpinyDendrite[762] connect SpinyDendrite[766](0),1
    SpinyDendrite[766] {nseg=1 L=24 diam=1 }

    SpinyDendrite[761] connect SpinyDendrite[767](0),1
    SpinyDendrite[767] {nseg=1 L=4 diam=2 }

    SpinyDendrite[767] connect SpinyDendrite[768](0),1
    SpinyDendrite[768] {nseg=1 L=12 diam=1.4 }

    SpinyDendrite[768] connect SpinyDendrite[769](0),1
    SpinyDendrite[769] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[769] connect SpinyDendrite[770](0),1
    SpinyDendrite[770] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[770] connect SpinyDendrite[771](0),1
    SpinyDendrite[771] {nseg=1 L=8 diam=1 }

    SpinyDendrite[770] connect SpinyDendrite[772](0),1
    SpinyDendrite[772] {nseg=1 L=48 diam=1 }

    SpinyDendrite[768] connect SpinyDendrite[773](0),1
    SpinyDendrite[773] {nseg=1 L=14 diam=1 }
 
    SpinyDendrite[769] connect SpinyDendrite[774](0),1
    SpinyDendrite[774] {nseg=1 L=12 diam=1 }

    SpinyDendrite[767] connect SpinyDendrite[775](0),1
    SpinyDendrite[775] {nseg=1 L=22 diam=2 }

    SpinyDendrite[775] connect SpinyDendrite[776](0),1
    SpinyDendrite[776] {nseg=1 L=28 diam=1 }

    SpinyDendrite[775] connect SpinyDendrite[777](0),1
    SpinyDendrite[777] {nseg=1 L=3 diam=2 }

    SpinyDendrite[777] connect SpinyDendrite[778](0),1
    SpinyDendrite[778] {nseg=1 L=23 diam=1.4 }

    SpinyDendrite[778] connect SpinyDendrite[779](0),1
    SpinyDendrite[779] {nseg=1 L=4 diam=1 }
 
    SpinyDendrite[778] connect SpinyDendrite[780](0),1
    SpinyDendrite[780] {nseg=1 L=7 diam=1 }

    SpinyDendrite[777] connect SpinyDendrite[781](0),1
    SpinyDendrite[781] {nseg=1 L=15 diam=1.4 }

    SpinyDendrite[781] connect SpinyDendrite[782](0),1
    SpinyDendrite[782] {nseg=1 L=17 diam=1 }

    SpinyDendrite[781] connect SpinyDendrite[783](0),1
    SpinyDendrite[783] {nseg=1 L=9 diam=1.4 }
 
    SpinyDendrite[783] connect SpinyDendrite[784](0),1
    SpinyDendrite[784] {nseg=1 L=8 diam=1 }

    SpinyDendrite[783] connect SpinyDendrite[785](0),1
    SpinyDendrite[785] {nseg=1 L=10 diam=1.4 }

    SpinyDendrite[785] connect SpinyDendrite[786](0),1
    SpinyDendrite[786] {nseg=1 L=5 diam=1 }

    SpinyDendrite[785] connect SpinyDendrite[787](0),1
    SpinyDendrite[787] {nseg=1 L=4 diam=1 }
 

/**** Spiny 69 ****/
    SmoothDendrite[24] connect SpinyDendrite[788](0),1
    SpinyDendrite[788] {nseg=1 L=6 diam=2 }

    SpinyDendrite[788] connect SpinyDendrite[789](0),1
    SpinyDendrite[789] {nseg=1 L=10 diam=1 }

    SpinyDendrite[788] connect SpinyDendrite[790](0),1
    SpinyDendrite[790] {nseg=1 L=16 diam=2 }

    SpinyDendrite[790] connect SpinyDendrite[791](0),1
    SpinyDendrite[791] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[791] connect SpinyDendrite[792](0),1
    SpinyDendrite[792] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[792] connect SpinyDendrite[793](0),1
    SpinyDendrite[793] {nseg=1 L=14 diam=1 }

    SpinyDendrite[792] connect SpinyDendrite[794](0),1
    SpinyDendrite[794] {nseg=1 L=12 diam=1 }

    SpinyDendrite[791] connect SpinyDendrite[795](0),1
    SpinyDendrite[795] {nseg=1 L=26 diam=1 }

    SpinyDendrite[790] connect SpinyDendrite[796](0),1
    SpinyDendrite[796] {nseg=1 L=13 diam=1.4 }

    SpinyDendrite[796] connect SpinyDendrite[797](0),1
    SpinyDendrite[797] {nseg=1 L=17 diam=1 }

    SpinyDendrite[796] connect SpinyDendrite[798](0),1
    SpinyDendrite[798] {nseg=1 L=10 diam=1.4 }

    SpinyDendrite[798] connect SpinyDendrite[799](0),1
    SpinyDendrite[799] {nseg=1 L=5 diam=1 }

    SpinyDendrite[798] connect SpinyDendrite[800](0),1
    SpinyDendrite[800] {nseg=1 L=5 diam=1.4 }
 
    SpinyDendrite[800] connect SpinyDendrite[801](0),1
    SpinyDendrite[801] {nseg=1 L=14 diam=1 }

    SpinyDendrite[800] connect SpinyDendrite[802](0),1
    SpinyDendrite[802] {nseg=1 L=10 diam=1 }


/**** Spiny 70 ****/
    SmoothDendrite[22] connect SpinyDendrite[803](0),1
    SpinyDendrite[803] {nseg=1 L=12 diam=1 }


/**** Spiny 71 ****/
    SmoothDendrite[21] connect SpinyDendrite[804](0),1
    SpinyDendrite[804] {nseg=1 L=4 diam=2 }

    SpinyDendrite[804] connect SpinyDendrite[805](0),1
    SpinyDendrite[805] {nseg=1 L=14 diam=1 }

    SpinyDendrite[804] connect SpinyDendrite[806](0),1
    SpinyDendrite[806] {nseg=1 L=11 diam=2 }

    SpinyDendrite[806] connect SpinyDendrite[807](0),1
    SpinyDendrite[807] {nseg=1 L=16 diam=1.4 }

    SpinyDendrite[807] connect SpinyDendrite[808](0),1
    SpinyDendrite[808] {nseg=1 L=9 diam=1 }

    SpinyDendrite[807] connect SpinyDendrite[809](0),1
    SpinyDendrite[809] {nseg=1 L=13 diam=1 }

    SpinyDendrite[806] connect SpinyDendrite[810](0),1
    SpinyDendrite[810] {nseg=1 L=14 diam=1.4 }

    SpinyDendrite[810] connect SpinyDendrite[811](0),1
    SpinyDendrite[811] {nseg=1 L=5 diam=1 }

    SpinyDendrite[810] connect SpinyDendrite[812](0),1
    SpinyDendrite[812] {nseg=1 L=9 diam=1 }


/**** Spiny 72 ****/
    SmoothDendrite[20] connect SpinyDendrite[813](0),1
    SpinyDendrite[813] {nseg=1 L=8 diam=2 }

    SpinyDendrite[813] connect SpinyDendrite[814](0),1
    SpinyDendrite[814] {nseg=1 L=21 diam=1 }

    SpinyDendrite[813] connect SpinyDendrite[815](0),1
    SpinyDendrite[815] {nseg=1 L=4 diam=2 }

    SpinyDendrite[815] connect SpinyDendrite[816](0),1
    SpinyDendrite[816] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[816] connect SpinyDendrite[817](0),1
    SpinyDendrite[817] {nseg=1 L=7 diam=1 }

    SpinyDendrite[816] connect SpinyDendrite[818](0),1
    SpinyDendrite[818] {nseg=1 L=14 diam=1 }

    SpinyDendrite[815] connect SpinyDendrite[819](0),1
    SpinyDendrite[819] {nseg=1 L=11 diam=1.4 }

    SpinyDendrite[819] connect SpinyDendrite[820](0),1
    SpinyDendrite[820] {nseg=1 L=27 diam=1 }

    SpinyDendrite[819] connect SpinyDendrite[821](0),1
    SpinyDendrite[821] {nseg=1 L=7 diam=1.4 }

    SpinyDendrite[821] connect SpinyDendrite[822](0),1
    SpinyDendrite[822] {nseg=1 L=10 diam=1 }

    SpinyDendrite[821] connect SpinyDendrite[823](0),1
    SpinyDendrite[823] {nseg=1 L=3 diam=1 }


/**** Spiny 73 ****/
    SmoothDendrite[15] connect SpinyDendrite[824](0),1
    SpinyDendrite[824] {nseg=1 L=20 diam=1 }


/**** Spiny 74 ****/
    SmoothDendrite[17] connect SpinyDendrite[825](0),1
    SpinyDendrite[825] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[825] connect SpinyDendrite[826](0),1
    SpinyDendrite[826] {nseg=1 L=13 diam=1 }

    SpinyDendrite[825] connect SpinyDendrite[827](0),1
    SpinyDendrite[827] {nseg=1 L=17 diam=1 }


/**** Spiny 75 ****/
    SmoothDendrite[16] connect SpinyDendrite[828](0),1
    SpinyDendrite[828] {nseg=1 L= diam=2 }

    SpinyDendrite[828] connect SpinyDendrite[829](0),1
    SpinyDendrite[829] {nseg=1 L= diam=1.4 }

    SpinyDendrite[829] connect SpinyDendrite[830](0),1
    SpinyDendrite[830] {nseg=1 L= diam=1.4 }

    SpinyDendrite[830] connect SpinyDendrite[831](0),1
    SpinyDendrite[831] {nseg=1 L= diam=1 }

    SpinyDendrite[830] connect SpinyDendrite[832](0),1
    SpinyDendrite[832] {nseg=1 L= diam=1 }

    SpinyDendrite[829] connect SpinyDendrite[833](0),1
    SpinyDendrite[833] {nseg=1 L= diam=1 }

    SpinyDendrite[828] connect SpinyDendrite[834](0),1
    SpinyDendrite[834] {nseg=1 L= diam=1.4 }

    SpinyDendrite[834] connect SpinyDendrite[835](0),1
    SpinyDendrite[835] {nseg=1 L= diam=1 }

    SpinyDendrite[834] connect SpinyDendrite[836](0),1
    SpinyDendrite[836] {nseg=1 L= diam=1.4 }

    SpinyDendrite[836] connect SpinyDendrite[837](0),1
    SpinyDendrite[837] {nseg=1 L= diam=1 }

    SpinyDendrite[836] connect SpinyDendrite[838](0),1
    SpinyDendrite[838] {nseg=1 L= diam=1.4 }

    SpinyDendrite[838] connect SpinyDendrite[839](0),1
    SpinyDendrite[839] {nseg=1 L= diam=1 }

    SpinyDendrite[838] connect SpinyDendrite[840](0),1
    SpinyDendrite[840] {nseg=1 L= diam=1 }


 /**** Spiny 76 ****/
    SmoothDendrite[16] connect SpinyDendrite[841](0),1
    SpinyDendrite[841] {nseg=1 L=6 diam=2 }

    SpinyDendrite[841] connect SpinyDendrite[842](0),1
    SpinyDendrite[842] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[842] connect SpinyDendrite[843](0),1
    SpinyDendrite[843] {nseg=1 L=5 diam=1 }

    SpinyDendrite[842] connect SpinyDendrite[844](0),1
    SpinyDendrite[844] {nseg=1 L=4 diam=1 }

    SpinyDendrite[841] connect SpinyDendrite[845](0),1
    SpinyDendrite[845] {nseg=1 L=7 diam=1.4 }

    SpinyDendrite[845] connect SpinyDendrite[846](0),1
    SpinyDendrite[846] {nseg=1 L=22 diam=1 }

    SpinyDendrite[845] connect SpinyDendrite[847](0),1
    SpinyDendrite[847] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[847] connect SpinyDendrite[848](0),1
    SpinyDendrite[848] {nseg=1 L=17 diam=1 }

    SpinyDendrite[847] connect SpinyDendrite[849](0),1
    SpinyDendrite[849] {nseg=1 L=5 diam=1 }


/**** Spiny 77 ****/
    SmoothDendrite[11] connect SpinyDendrite[850](0),1
    SpinyDendrite[850] {nseg=1 L=2 diam=2 }

    SpinyDendrite[850] connect SpinyDendrite[851](0),1
    SpinyDendrite[851] {nseg=1 L=16 diam=1.4 }

    SpinyDendrite[851] connect SpinyDendrite[852](0),1
    SpinyDendrite[852] {nseg=1 L=6 diam=1 }

    SpinyDendrite[851] connect SpinyDendrite[853](0),1
    SpinyDendrite[853] {nseg=1 L=14 diam=1 }

    SpinyDendrite[850] connect SpinyDendrite[854](0),1
    SpinyDendrite[854] {nseg=1 L=2 diam=2 }

    SpinyDendrite[854] connect SpinyDendrite[855](0),1
    SpinyDendrite[855] {nseg=1 L=5 diam=1 }

    SpinyDendrite[854] connect SpinyDendrite[856](0),1
    SpinyDendrite[856] {nseg=1 L=1 diam=2 }

    SpinyDendrite[856] connect SpinyDendrite[857](0),1
    SpinyDendrite[857] {nseg=1 L=40 diam=1 }

    SpinyDendrite[856] connect SpinyDendrite[858](0),1
    SpinyDendrite[858] {nseg=1 L=12 diam=2 }

    SpinyDendrite[858] connect SpinyDendrite[859](0),1
    SpinyDendrite[859] {nseg=1 L=8 diam=1.4 }

    SpinyDendrite[859] connect SpinyDendrite[860](0),1
    SpinyDendrite[860] {nseg=1 L=3 diam=1 }

    SpinyDendrite[859] connect SpinyDendrite[861](0),1
    SpinyDendrite[861] {nseg=1 L=6 diam=1 }

    SpinyDendrite[858] connect SpinyDendrite[862](0),1
    SpinyDendrite[862] {nseg=1 L=2 diam=1.4 }
 
    SpinyDendrite[862] connect SpinyDendrite[863](0),1
    SpinyDendrite[863] {nseg=1 L=12 diam=1 }

    SpinyDendrite[862] connect SpinyDendrite[864](0),1
    SpinyDendrite[864] {nseg=1 L=19 diam=1 }


/**** Spiny 78 ****/
    SmoothDendrite[10] connect SpinyDendrite[865](0),1
    SpinyDendrite[865] {nseg=1 L=10 diam=2 }

    SpinyDendrite[865] connect SpinyDendrite[866](0),1
    SpinyDendrite[866] {nseg=1 L=5 diam=1 }

    SpinyDendrite[865] connect SpinyDendrite[867](0),1
    SpinyDendrite[867] {nseg=1 L=6 diam=2 }

    SpinyDendrite[867] connect SpinyDendrite[868](0),1
    SpinyDendrite[868] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[868] connect SpinyDendrite[869](0),1
    SpinyDendrite[869] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[869] connect SpinyDendrite[870](0),1
    SpinyDendrite[870] {nseg=1 L=9 diam=1 }

    SpinyDendrite[869] connect SpinyDendrite[871](0),1
    SpinyDendrite[871] {nseg=1 L=6 diam=1 }

    SpinyDendrite[868] connect SpinyDendrite[872](0),1
    SpinyDendrite[872] {nseg=1 L=4 diam=1 }

    SpinyDendrite[867] connect SpinyDendrite[873](0),1
    SpinyDendrite[873] {nseg=1 L=2 diam=2 }

    SpinyDendrite[873] connect SpinyDendrite[874](0),1
    SpinyDendrite[874] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[874] connect SpinyDendrite[875](0),1
    SpinyDendrite[875] {nseg=1 L=5 diam=1 }

    SpinyDendrite[874] connect SpinyDendrite[876](0),1
    SpinyDendrite[876] {nseg=1 L=6 diam=1 }

    SpinyDendrite[873] connect SpinyDendrite[877](0),1
    SpinyDendrite[877] {nseg=1 L=8 diam=1.4 }
 
    SpinyDendrite[877] connect SpinyDendrite[878](0),1
    SpinyDendrite[878] {nseg=1 L=7 diam=1 }

    SpinyDendrite[877] connect SpinyDendrite[879](0),1
    SpinyDendrite[879] {nseg=1 L=6 diam=1 }


/**** Spiny 79 ****/
    SmoothDendrite[10] connect SpinyDendrite[880](0),1
    SpinyDendrite[880] {nseg=1 L=10 diam=2 }

    SpinyDendrite[880] connect SpinyDendrite[881](0),1
    SpinyDendrite[881] {nseg=1 L=7 diam=1.4 }

    SpinyDendrite[881] connect SpinyDendrite[882](0),1
    SpinyDendrite[882] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[882] connect SpinyDendrite[883](0),1
    SpinyDendrite[883] {nseg=1 L=3 diam=1 }

    SpinyDendrite[882] connect SpinyDendrite[884](0),1
    SpinyDendrite[884] {nseg=1 L=4 diam=1 }

    SpinyDendrite[881] connect SpinyDendrite[885](0),1
    SpinyDendrite[885] {nseg=1 L=5 diam=1 }

    SpinyDendrite[880] connect SpinyDendrite[886](0),1
    SpinyDendrite[886] {nseg=1 L=10 diam=2 }

    SpinyDendrite[886] connect SpinyDendrite[887](0),1
    SpinyDendrite[887] {nseg=1 L=8 diam=1.4 }

    SpinyDendrite[887] connect SpinyDendrite[888](0),1
    SpinyDendrite[888] {nseg=1 L=2 diam=1 }

    SpinyDendrite[887] connect SpinyDendrite[889](0),1
    SpinyDendrite[889] {nseg=1 L=6 diam=1 }

    SpinyDendrite[886] connect SpinyDendrite[890](0),1
    SpinyDendrite[890] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[890] connect SpinyDendrite[891](0),1
    SpinyDendrite[891] {nseg=1 L=10 diam=1 }

    SpinyDendrite[890] connect SpinyDendrite[892](0),1
    SpinyDendrite[892] {nseg=1 L=12 diam=1 }


/**** Spiny 80 ****/
    SmoothDendrite[8] connect SpinyDendrite[893](0),1
    SpinyDendrite[893] {nseg=1 L=7 diam=2 }

    SpinyDendrite[893] connect SpinyDendrite[894](0),1
    SpinyDendrite[894] {nseg=1 L=7 diam=1.4 }

    SpinyDendrite[894] connect SpinyDendrite[895](0),1
    SpinyDendrite[895] {nseg=1 L=13 diam=1 }

    SpinyDendrite[894] connect SpinyDendrite[896](0),1
    SpinyDendrite[896] {nseg=1 L=6 diam=1 }

    SpinyDendrite[893] connect SpinyDendrite[897](0),1
    SpinyDendrite[897] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[897] connect SpinyDendrite[898](0),1
    SpinyDendrite[898] {nseg=1 L=12 diam=1 }

    SpinyDendrite[897] connect SpinyDendrite[899](0),1
    SpinyDendrite[899] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[899] connect SpinyDendrite[900](0),1
    SpinyDendrite[900] {nseg=1 L=12 diam=1 }

    SpinyDendrite[899] connect SpinyDendrite[901](0),1
    SpinyDendrite[901] {nseg=1 L=10 diam=1 }


/**** Spiny 81 ****/
    SmoothDendrite[8] connect SpinyDendrite[902](0),1
    SpinyDendrite[902] {nseg=1 L=4 diam=2 }

    SpinyDendrite[902] connect SpinyDendrite[903](0),1
    SpinyDendrite[903] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[903] connect SpinyDendrite[904](0),1
    SpinyDendrite[904] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[904] connect SpinyDendrite[905](0),1
    SpinyDendrite[905] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[905] connect SpinyDendrite[906](0),1
    SpinyDendrite[906] {nseg=1 L=2 diam=1 }

    SpinyDendrite[905] connect SpinyDendrite[907](0),1
    SpinyDendrite[907] {nseg=1 L=2 diam=1 }

    SpinyDendrite[903] connect SpinyDendrite[908](0),1
    SpinyDendrite[908] {nseg=1 L=8 diam=1 }

    SpinyDendrite[904] connect SpinyDendrite[909](0),1
    SpinyDendrite[909] {nseg=1 L=3 diam=1 }

    SpinyDendrite[902] connect SpinyDendrite[910](0),1
    SpinyDendrite[910] {nseg=1 L=5 diam=2 }

    SpinyDendrite[910] connect SpinyDendrite[911](0),1
    SpinyDendrite[911] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[911] connect SpinyDendrite[912](0),1
    SpinyDendrite[912] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[912] connect SpinyDendrite[913](0),1
    SpinyDendrite[913] {nseg=1 L=5 diam=1 }

    SpinyDendrite[912] connect SpinyDendrite[914](0),1
    SpinyDendrite[914] {nseg=1 L=5 diam=1 }
 
    SpinyDendrite[911] connect SpinyDendrite[915](0),1
    SpinyDendrite[915] {nseg=1 L=4 diam=1 }

    SpinyDendrite[910] connect SpinyDendrite[916](0),1
    SpinyDendrite[916] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[916] connect SpinyDendrite[917](0),1
    SpinyDendrite[917] {nseg=1 L=14 diam=1 }

    SpinyDendrite[916] connect SpinyDendrite[918](0),1
    SpinyDendrite[918] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[918] connect SpinyDendrite[919](0),1
    SpinyDendrite[919] {nseg=1 L=4 diam=1 }

    SpinyDendrite[918] connect SpinyDendrite[920](0),1
    SpinyDendrite[920] {nseg=1 L=5 diam=1.4 }
 
    SpinyDendrite[920] connect SpinyDendrite[921](0),1
    SpinyDendrite[921] {nseg=1 L=14 diam=1 }

    SpinyDendrite[920] connect SpinyDendrite[922](0),1
    SpinyDendrite[922] {nseg=1 L=7 diam=1 }


/**** Spiny 82 ****/
    SmoothDendrite[4] connect SpinyDendrite[923](0),1
    SpinyDendrite[923] {nseg=1 L=28 diam=1.4 }

    SpinyDendrite[923] connect SpinyDendrite[924](0),1
    SpinyDendrite[924] {nseg=1 L=18 diam=1 }

    SpinyDendrite[923] connect SpinyDendrite[925](0),1
    SpinyDendrite[925] {nseg=1 L=12 diam=1.4 }

    SpinyDendrite[925] connect SpinyDendrite[926](0),1
    SpinyDendrite[926] {nseg=1 L=10 diam=1 }

    SpinyDendrite[925] connect SpinyDendrite[927](0),1
    SpinyDendrite[927] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[927] connect SpinyDendrite[928](0),1
    SpinyDendrite[928] {nseg=1 L=5 diam=1 }

    SpinyDendrite[927] connect SpinyDendrite[929](0),1
    SpinyDendrite[929] {nseg=1 L=13 diam=1.4 }

    SpinyDendrite[929] connect SpinyDendrite[930](0),1
    SpinyDendrite[930] {nseg=1 L=4 diam=1 }

    SpinyDendrite[929] connect SpinyDendrite[931](0),1
    SpinyDendrite[931] {nseg=1 L=4 diam=1 }


/**** Spiny 83 ****/
    SmoothDendrite[5] connect SpinyDendrite[932](0),1
    SpinyDendrite[932] {nseg=1 L=5 diam=2 }

    SpinyDendrite[932] connect SpinyDendrite[933](0),1
    SpinyDendrite[933] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[933] connect SpinyDendrite[934](0),1
    SpinyDendrite[934] {nseg=1 L=10 diam=1 }

    SpinyDendrite[933] connect SpinyDendrite[935](0),1
    SpinyDendrite[935] {nseg=1 L=5 diam=1 }

    SpinyDendrite[932] connect SpinyDendrite[936](0),1
    SpinyDendrite[936] {nseg=1 L=1 diam=2 }

    SpinyDendrite[936] connect SpinyDendrite[937](0),1
    SpinyDendrite[937] {nseg=1 L=1 diam=1.4 }

    SpinyDendrite[937] connect SpinyDendrite[938](0),1
    SpinyDendrite[938] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[938] connect SpinyDendrite[939](0),1
    SpinyDendrite[939] {nseg=1 L=4 diam=1 }

    SpinyDendrite[938] connect SpinyDendrite[940](0),1
    SpinyDendrite[940] {nseg=1 L=10 diam=1 }

    SpinyDendrite[937] connect SpinyDendrite[941](0),1
    SpinyDendrite[941] {nseg=1 L=7 diam=1 }

    SpinyDendrite[936] connect SpinyDendrite[942](0),1
    SpinyDendrite[942] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[942] connect SpinyDendrite[943](0),1
    SpinyDendrite[943] {nseg=1 L=5 diam=1 }

    SpinyDendrite[942] connect SpinyDendrite[944](0),1
    SpinyDendrite[944] {nseg=1 L=4 diam=1.4 }
 
    SpinyDendrite[944] connect SpinyDendrite[945](0),1
    SpinyDendrite[945] {nseg=1 L=4 diam=1 }

    SpinyDendrite[944] connect SpinyDendrite[946](0),1
    SpinyDendrite[946] {nseg=1 L=10 diam=1 }


/**** Spiny 84 ****/
    SmoothDendrite[5] connect SpinyDendrite[947](0),1
    SpinyDendrite[947] {nseg=1 L=8 diam=2 }

    SpinyDendrite[947] connect SpinyDendrite[948](0),1
    SpinyDendrite[948] {nseg=1 L=13 diam=1.4 }

    SpinyDendrite[948] connect SpinyDendrite[949](0),1
    SpinyDendrite[949] {nseg=1 L=5 diam=1 }

    SpinyDendrite[948] connect SpinyDendrite[950](0),1
    SpinyDendrite[950] {nseg=1 L=4 diam=1 }

    SpinyDendrite[947] connect SpinyDendrite[951](0),1
    SpinyDendrite[951] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[951] connect SpinyDendrite[952](0),1
    SpinyDendrite[952] {nseg=1 L=8 diam=1 }

    SpinyDendrite[951] connect SpinyDendrite[953](0),1
    SpinyDendrite[953] {nseg=1 L=11 diam=1 }


/**** Spiny 85 ****/
    SmoothDendrite[3] connect SpinyDendrite[954](0),1
    SpinyDendrite[954] {nseg=1 L=2 diam=2 }

    SpinyDendrite[954] connect SpinyDendrite[955](0),1
    SpinyDendrite[955] {nseg=1 L=16 diam=1 }

    SpinyDendrite[954] connect SpinyDendrite[956](0),1
    SpinyDendrite[956] {nseg=1 L=2 diam=2 }

    SpinyDendrite[956] connect SpinyDendrite[957](0),1
    SpinyDendrite[957] {nseg=1 L=10 diam=1.4 }

    SpinyDendrite[957] connect SpinyDendrite[958](0),1
    SpinyDendrite[958] {nseg=1 L=17 diam=1.4 }

    SpinyDendrite[958] connect SpinyDendrite[959](0),1
    SpinyDendrite[959] {nseg=1 L=8 diam=1.4 }

    SpinyDendrite[959] connect SpinyDendrite[960](0),1
    SpinyDendrite[960] {nseg=1 L=3 diam=1 }

    SpinyDendrite[959] connect SpinyDendrite[961](0),1
    SpinyDendrite[961] {nseg=1 L=4 diam=1 }

    SpinyDendrite[957] connect SpinyDendrite[962](0),1
    SpinyDendrite[962] {nseg=1 L=15 diam=1 }

    SpinyDendrite[958] connect SpinyDendrite[963](0),1
    SpinyDendrite[963] {nseg=1 L=2 diam=1 }

    SpinyDendrite[956] connect SpinyDendrite[964](0),1
    SpinyDendrite[964] {nseg=1 L=5 diam=1.4 }

    SpinyDendrite[964] connect SpinyDendrite[965](0),1
    SpinyDendrite[965] {nseg=1 L=14 diam=1 }

    SpinyDendrite[964] connect SpinyDendrite[966](0),1
    SpinyDendrite[966] {nseg=1 L=3 diam=1.4 }
 
    SpinyDendrite[966] connect SpinyDendrite[967](0),1
    SpinyDendrite[967] {nseg=1 L=13 diam=1 }

    SpinyDendrite[966] connect SpinyDendrite[968](0),1
    SpinyDendrite[968] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[968] connect SpinyDendrite[969](0),1
    SpinyDendrite[969] {nseg=1 L=11 diam=1 }

    SpinyDendrite[968] connect SpinyDendrite[970](0),1
    SpinyDendrite[970] {nseg=1 L=4 diam=1.4 }

    SpinyDendrite[970] connect SpinyDendrite[971](0),1
    SpinyDendrite[971] {nseg=1 L=12 diam=1 }

    SpinyDendrite[970] connect SpinyDendrite[972](0),1
    SpinyDendrite[972] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[972] connect SpinyDendrite[973](0),1
    SpinyDendrite[973] {nseg=1 L=8 diam=1 }

    SpinyDendrite[972] connect SpinyDendrite[974](0),1
    SpinyDendrite[974] {nseg=1 L=4 diam=1.4 }
 
    SpinyDendrite[974] connect SpinyDendrite[975](0),1
    SpinyDendrite[975] {nseg=1 L=8 diam=1 }

    SpinyDendrite[974] connect SpinyDendrite[976](0),1
    SpinyDendrite[976] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[976] connect SpinyDendrite[977](0),1
    SpinyDendrite[977] {nseg=1 L=10 diam=1 }

    SpinyDendrite[976] connect SpinyDendrite[978](0),1
    SpinyDendrite[978] {nseg=1 L=3 diam=1 }


/**** Spiny 86 ****/
    SmoothDendrite[3] connect SpinyDendrite[979](0),1
    SpinyDendrite[979] {nseg=1 L=4 diam=2 }

    SpinyDendrite[979] connect SpinyDendrite[980](0),1
    SpinyDendrite[980] {nseg=1 L=6 diam=1.4 }

    SpinyDendrite[980] connect SpinyDendrite[981](0),1
    SpinyDendrite[981] {nseg=1 L=6 diam=1 }

    SpinyDendrite[980] connect SpinyDendrite[982](0),1
    SpinyDendrite[982] {nseg=1 L=2 diam=1 }

    SpinyDendrite[979] connect SpinyDendrite[983](0),1
    SpinyDendrite[983] {nseg=1 L=10 diam=2 }

    SpinyDendrite[983] connect SpinyDendrite[984](0),1
    SpinyDendrite[984] {nseg=1 L=2 diam=1.4 }

    SpinyDendrite[984] connect SpinyDendrite[985](0),1
    SpinyDendrite[985] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[985] connect SpinyDendrite[986](0),1
    SpinyDendrite[986] {nseg=1 L=5 diam=1 }

    SpinyDendrite[985] connect SpinyDendrite[987](0),1
    SpinyDendrite[987] {nseg=1 L=4 diam=1 }

    SpinyDendrite[984] connect SpinyDendrite[988](0),1
    SpinyDendrite[988] {nseg=1 L=2 diam=1 }

    SpinyDendrite[983] connect SpinyDendrite[989](0),1
    SpinyDendrite[989] {nseg=1 L=7 diam=2 }

    SpinyDendrite[989] connect SpinyDendrite[990](0),1
    SpinyDendrite[990] {nseg=1 L=8 diam=1 }

    SpinyDendrite[989] connect SpinyDendrite[991](0),1
    SpinyDendrite[991] {nseg=1 L=6 diam=2 }
 
    SpinyDendrite[991] connect SpinyDendrite[992](0),1
    SpinyDendrite[992] {nseg=1 L=2 diam=1 }

    SpinyDendrite[991] connect SpinyDendrite[993](0),1
    SpinyDendrite[993] {nseg=1 L=2 diam=2 }

    SpinyDendrite[993] connect SpinyDendrite[994](0),1
    SpinyDendrite[994] {nseg=1 L=8 diam=1.4 }

    SpinyDendrite[994] connect SpinyDendrite[995](0),1
    SpinyDendrite[995] {nseg=1 L=8 diam=1 }
 
    SpinyDendrite[994] connect SpinyDendrite[996](0),1
    SpinyDendrite[996] {nseg=1 L=4 diam=1 }

    SpinyDendrite[993] connect SpinyDendrite[997](0),1
    SpinyDendrite[997] {nseg=1 L=3 diam=1.4 }

    SpinyDendrite[997] connect SpinyDendrite[998](0),1
    SpinyDendrite[998] {nseg=1 L=4 diam=1 }

    SpinyDendrite[997] connect SpinyDendrite[999](0),1
    SpinyDendrite[999] {nseg=1 L=7 diam=1.4 }
 
    SpinyDendrite[999] connect SpinyDendrite[1000](0),1
    SpinyDendrite[1000] {nseg=1 L=11 diam=1 }

    SpinyDendrite[999] connect SpinyDendrite[1001](0),1
    SpinyDendrite[1001] {nseg=1 L=5 diam=1 }
