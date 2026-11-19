import("stdfaust.lib");
// Faust violinModel (R. Michon, physmodels.lib) driven for a cello-range string.
// Output 0: string at the bridge without the body resonance; output 1: with pm.violinBody.
freq = hslider("freq",130.8,30,1000,0.01) : si.smoo;
pres = hslider("pressure",0.8,0,1,0.001) : si.smoo;
vel0 = hslider("velocity",0,0,1,0.001) : si.smoo;
pos  = hslider("position",0.85,0,1,0.001) : si.smoo;
nz   = hslider("noise",0,0,1,0.001) : si.smoo;
vel  = vel0*(1 + nz*(no.noise : fi.lowpass(1,2500)));
stringL = pm.f2l(freq) - 12*pm.speedOfSound/ma.SR;
raw  = pm.endChain(pm.chain(pm.violinNuts : pm.violinBowedString(stringL,pres,vel,pos) : pm.violinBridge : pm.out));
body = pm.endChain(pm.chain(pm.violinNuts : pm.violinBowedString(stringL,pres,vel,pos) : pm.violinBridge : pm.violinBody : pm.out));
process = raw, body;
