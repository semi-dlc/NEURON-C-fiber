from neuron import h

def insertChannels(axon,condFactor, gPump, gNav17, gNav18, gNav19, gKs, gKf, gH, gKdr, gKna, gCav12, gCav22, gNacx, gBk, gSk):
    axon.insert('ks')
    axon.insert('kf')
    axon.insert('h')
    
    axon.insert('nattxs')
    axon.insert('nav1p8')
    axon.insert('nav1p9')
    
    axon.insert('nakpump')
   
    axon.insert('kdr')
    axon.insert('kna')
    
    axon.insert('extrapump')
    axon.insert('leak')
    axon.insert('nakdyn')

    #add calcium
    axon.insert('cav12')
    axon.insert('cav22')
    
    axon.insert('caextscale')
    axon.insert('caintscale')
    
    axon.insert('nacx')
    axon.insert('bk')
    axon.insert('sk')
    axon.insert('capump')
    

    for seg in axon:
        seg.ks.gbar = gKs*condFactor
        seg.kf.gbar = gKf*condFactor
        seg.h.gbar = gH*condFactor
        seg.nattxs.gbar = gNav17*condFactor
        seg.nav1p8.gbar = gNav18*condFactor
        seg.nav1p9.gbar = gNav19*condFactor
        seg.nakpump.smalla = gPump*condFactor
        seg.kdr.gbar = gKdr*condFactor
        seg.kna.gbar = gKna*condFactor
        
        seg.cav12.gbar=gCav12*condFactor
        seg.cav22.gbar=gCav22*condFactor
        
        seg.caextscale.nseg=axon.nseg
        seg.caextscale.L=axon.L

        seg.caintscale.nseg=axon.nseg
        seg.caintscale.L=axon.L
        
        seg.nacx.gbar=gNacx*condFactor
        seg.bk.gbar=gBk*condFactor
        seg.sk.gbar=gSk*condFactor
        
    h.theta_nakdyn = 0.029


def setTemp(axon, tempCelsius):
    for seg in axon:
        seg.ks.celsiusT = tempCelsius
        seg.kf.celsiusT = tempCelsius
        seg.h.celsiusT = tempCelsius
        seg.nattxs.celsiusT = tempCelsius
        seg.nav1p8.celsiusT = tempCelsius
        seg.nav1p9.celsiusT = tempCelsius
        seg.nakpump.celsiusT = tempCelsius
        seg.kdr.celsiusT = tempCelsius

        seg.cav12.celsiusT = tempCelsius
        seg.cav22.celsiusT = tempCelsius
        
        seg.nacx.celsiusT = tempCelsius
        seg.bk.celsiusT = tempCelsius
        seg.sk.celsiusT = tempCelsius
        seg.capump.celsiusT = tempCelsius
        


#calculates the maximum conductances of the sodium and potassium leak (balancing) currents to achieve their target rest potential (Grill)
def balance(axon, Vrest):
    inaSum=-axon.ina
    if (inaSum/(Vrest-axon.ena))<0:
        axon.pumpina_extrapump=inaSum
    else:
        #axon.gnaleak_leak = inaSum/(Vrest-axon.ena)
        axon.gnaleak_leak = inaSum

    ikSum = -axon.ik
    if (ikSum/(Vrest-axon.ek))<0:
        axon.pumpik_extrapump=ikSum
    else:
        #axon.gkleak_leak = ikSum/(Vrest-axon.ek)
        axon.gkleak_leak = ikSum
    
    icaSum = -axon.ica
    if (icaSum/(Vrest-axon.eca))<0:
        axon.pumpica_extrapump=icaSum
    else:
        #axon.gkleak_leak = ikSum/(Vrest-axon.ek)
        axon.gcaleak_leak = icaSum
    
    
def checkBalance(axon):
    #Natrium
    #check extrapump
    scoreExtraNa = max(axon.ina_nattxs, axon.ina_nav1p9, axon.ina_nav1p8, axon.ina_h, axon.ina_nakpump)-axon.pumpina_extrapump# should be >0
    if scoreExtraNa < 0:#extrapump is larger than max current
        scoreExtraNa=abs(scoreExtraNa)# the larger the difference. the larger the score
    else:
        scoreExtraNa=0
    
    #check leak
    scoreLeakNa = max(axon.ina_nattxs, axon.ina_nav1p9, axon.ina_nav1p8, axon.ina_h, axon.ina_nakpump)-axon.gnaleak_leak# should be >0
    if scoreLeakNa < 0:#extrapump is larger than max current
        scoreLeakNa=abs(scoreLeakNa)# the larger the difference. the larger the score
    else:
        scoreLeakNa=0

    #Kalium
    #check extrapump
    scoreExtraK = max(axon.ik_ks, axon.ik_kf, axon.ik_h, axon.ik_kdr, axon.ik_nakpump, axon.ik_kna)-axon.pumpik_extrapump# should be >0
    if scoreExtraK < 0:#extrapump is larger than max current
        scoreExtraK=abs(scoreExtraK)# the larger the difference. the larger the score
    else:
        scoreExtraK=0
    
    #check leak
    scoreLeakK = max(axon.ik_ks, axon.ik_kf, axon.ik_h, axon.ik_kdr, axon.ik_nakpump, axon.ik_kna)-axon.gkleak_leak# should be >0
    if scoreLeakK < 0:#extrapump is larger than max current
        scoreLeakK=abs(scoreLeakK)# the larger the difference. the larger the score
    else:
        scoreLeakK=0
    
    #Calcium   
    #check extrapump
    scoreExtraCa=0
    scoreLeakCa=0
    
    scoreExtraCa = max(axon.ica_cav12, axon.ica_cav22, axon.ica_nacx, axon.ica_capump)-axon.pumpica_extrapump# should be >0
    if scoreExtraCa < 0:#extrapump is larger than max current
        scoreExtraCa=abs(scoreExtraCa)# the larger the difference. the larger the score
    else:
        scoreExtraCa=0
    
    #check leak
    scoreLeakCa = max(axon.ica_cav12, axon.ica_cav22, axon.ica_nacx, axon.ica_capump)-axon.gcaleak_leak# should be >0
    if scoreLeakCa < 0:#extrapump is larger than max current
        scoreLeakCa=abs(scoreLeakCa)# the larger the difference. the larger the score
    else:
        scoreLeakCa=0
    
    score=(scoreExtraNa+scoreLeakNa+scoreExtraK+scoreLeakK+scoreExtraCa+scoreLeakCa)/6
    
    return score
    
    
    
    
    
    
    