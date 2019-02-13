TITLE Electrode for sinusoidal current clamping

COMMENT
	Author: A. Fontana
	Last revised: 13.2.2018 (by Lungsi)
ENDCOMMENT

NEURON {
	POINT_PROCESS GrC_Sine
	RANGE delay, dur, amp, i, freq, phase
	ELECTRODE_CURRENT i
}
UNITS {
	(nA) = (nanoamp)
}

PARAMETER {
	PI = 3.141592
	delay (ms)
	dur (ms)	
	amp = 0.006 (nA)
	freq = 4 (1/ms)
	phase = 0
}
ASSIGNED { i (nA) }

INITIAL {
	i = 0
}

BREAKPOINT {
	at_time(delay)
	at_time(delay+dur)

	if (t < delay + dur && t > delay) {

		
		i = amp*sin(2*PI*freq*t/1000)


	}else{
		i = 0
	}
}
