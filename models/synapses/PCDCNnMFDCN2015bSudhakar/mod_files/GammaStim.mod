COMMENT

Modification by Johannes Luthman of the built-in NetStim.mod of NEURON 6.1.
NB, this code has not been used with CVode.

Changes from NetStim:
    The output events can be set to follow gamma distributions of order 1-6,
    where 1 corresponds to the original Poisson process generated by NetStim.mod.
    The gamma process is generated in the same way as that given by timetable.c
    in GENESIS 2.3.
    A refractory period has been added.
    The output length is determined by duration in ms instead of number of events.

Parameters:
    interval: 	mean time between spikes (ms)
    start:      start of first spike (ms)
    noise:      amount of randomness in the spike train [0-1], where 0 generates
                fully regular spiking with isi given by parameter interval.
    duration:   length in ms of the spike train.
    order:      Integers [1-6] giving the order of gamma distribution.
    refractoryPeriod (ms)

ENDCOMMENT

NEURON  {
    ARTIFICIAL_CELL GammaStim
    RANGE interval, start, duration, order, noise, refractoryPeriod
}

PARAMETER {
    interval = 10 (ms) <1e-9,1e9>	: time between spikes (msec)
    start = 1 (ms)       		    : start of first spike
    noise = 0 <0,1>       		    : amount of randomness (0.0 - 1.0) in spike timing.
    duration = 1000 (ms)		    : input duration
    order = 1 <1,6>                 : order of gamma distribution. 1=pure poisson process.
    refractoryPeriod = 0 (ms)
}

ASSIGNED {
    event (ms)
    on
    end (ms)
}

PROCEDURE seed(x) {
    set_seed(x) : Calling .seed() from hoc affects the event streams
                : generated by all NetStims, see http://www.neuron.yale.edu/phpBB2/viewtopic.php?p=3285&sid=511cb3101cc8f4c12d47299198ed40c2
}

INITIAL {

    on = 0 : off
    if (order < 1 || order > 6) {
        order = 1
    }
    if (noise < 0) {
        noise = 0
    }
    if (noise > 1) {
        noise = 1
    }
    if (start >= 0) {
        : randomize the first spike so on average it occurs at
        : start + noise*interval
        event = start + invl(interval) - interval*(1. - noise)
        : but not earlier than 0
        if (event < 0) {
            event = 0
        }
        net_send(event, 3)
    }
}

PROCEDURE init_sequence(t(ms)) {
    on = 1
    event = t
    end = t + 1e-6 + duration
}

FUNCTION invl(mean (ms)) (ms) {

    : This function returns spiking interval

    if (mean <= 0.) {
        mean = .01 (ms)
    }
    if (noise == 0) {
        invl = mean
    }else{
        invl = (1. - noise)*mean + noise*meanRndGamma(order, refractoryPeriod, mean)
    }
}

PROCEDURE event_time() {
    event = event + invl(interval)
    if (event > end) {
        on = 0
    }
}

NET_RECEIVE (w) {
    if (flag == 0) { : external event
        if (w > 0 && on == 0) { : turn on spike sequence
            init_sequence(t)
            net_send(0, 1): net_send args: duration of event, flag to a NET_RECEIVE block,
                    : see The NEURON book ch 10 p343
        }else if (w < 0 && on == 1) { : turn off spiking
            on = 0
        }
    }
    if (flag == 3) { : from INITIAL
        if (on == 0) {
            init_sequence(t)
            net_send(0, 1)
        }
    }
    if (flag == 1 && on == 1) {
        net_event(t) : See NEURON book p. 345. Sum: net_event tells NetCon something has happened.
        event_time()
        if (on == 1) {
            net_send(event - t, 1)
        }
        net_send(.1, 2)
    }
}

FUNCTION meanRndGamma(gammaOrder(1), refractoryPeriod(ms), mean(ms)) (1) {

    : Code translated from the timetable object of GENESIS 2.3.

	LOCAL x

	x = 1.0
	FROM i = 0 TO gammaOrder-1 {
	    x = x * scop_random()
    }
	x = -log(x) * (interval - refractoryPeriod) / gammaOrder
	meanRndGamma = x + refractoryPeriod
}
