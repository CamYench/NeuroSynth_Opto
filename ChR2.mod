NEURON {
    SUFFIX ChR2
    USEION na READ ena WRITE ina
    USEION k READ ek WRITE ik
    NONSPECIFIC_CURRENT iopto
    RANGE gmax, iopto, light_on
}

UNITS {
    (mV) = (millivolt)
    (mA) = (milliamp)
    (S) = (siemens)
    (um) = (micron)
}

PARAMETER {
    gmax = 0.001 (S/cm2)  : Maximum conductance of ChR2
    light_on = 0 (1)      : Light activation flag (0 = off, 1 = on)
    tau_rise = 1 (ms)     : Rise time constant
    tau_decay = 10 (ms)   : Decay time constant
    v (mV)
    ena = 50 (mV)
    ek = -90 (mV)
}

ASSIGNED {
    iopto (mA/cm2)    : Optogenetic current
    ina (mA/cm2)
    ik (mA/cm2)
    gopto (S/cm2)     : Conductance
}

STATE {
    o              : Fraction of open channels
}

INITIAL {
    o = 0
    gopto = 0
    iopto = 0
}

BREAKPOINT {
    SOLVE states METHOD cnexp
    gopto = gmax * o
    iopto = gopto * (v - ena)  : Optogenetic current, sodium contribution (modify as needed)
    ina = iopto
    ik = gopto * (v - ek)      : If ChR2 passes potassium, include this component
}

DERIVATIVE states {
    LOCAL light_factor
    light_factor = light_on
    o' = light_factor * (1 - o) / tau_rise - o / tau_decay
}