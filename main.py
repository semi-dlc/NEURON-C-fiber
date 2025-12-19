from neuron import h
import numpy as np
import csv
import time
import math
import os
from os import path
from defineCell import *
from stimulationProtocols import *
import dataProcessing
from itertools import zip_longest
#import fasteners


#prot: stimulation protocol number or filename
#gPump: conductance of pump
#gNav17: conductance of Nav 1.7
#gNav18: conductance of Nav 1.8
#dt: step size in time, if set to zero, CVode is activated
#previousStim: sets a pre stimulation before the regular stimulation protocol, if the protocol is loaded from file
def run(prot=1, path="Results", scalingFactor=1,  dt=0, previousStim=False, tempBranch=32, tempParent=37, 
        gPump=-0.0047891, gNav17=0.10664, gNav17Parent=0.10664, gNav18=0.24271, gNav18Parent=0.24271, gNav19=9.4779e-05, 
        gKs=0.0069733, gKf=0.012756, gH=0.0025377, gKdr=0.018002, gKna=0.00042, 
        gCav12=0.000188, gCav22=0.000361, gNacx=0.009242, gBk=0.002016, gSk=0.000755, 
        vRest=-55, sine=False, ampSine=0.1, particleNr=0, iterationNr=0):
    
    #start timer
    #tic = time.perf_counter()
    
    #define morphology as in Tigerholm
    axon=[0,0,0,0,0,0]
    
    axon[0] = h.Section(name='extra1')
    axon[0].nseg = round(10*scalingFactor)
    axon[0].diam = 0.25
    axon[0].L = 100*scalingFactor
    
    axon[1] = h.Section(name='branch')
    axon[1].diam = 0.25
    axon[1].L = 20000*scalingFactor
    axon[1].nseg = round(400*scalingFactor)
        
    axon[2] = h.Section(name='branchPoint')
    h.pt3dadd(h.Vector([0,5000*scalingFactor]), h.Vector([0,0]), h.Vector([0,0]), h.Vector([0.25,1]), sec=axon[2])
    axon[2].nseg = round(100*scalingFactor)
        
    axon[3] = h.Section(name='parent')
    axon[3].diam = 1
    axon[3].L = 100000*scalingFactor
    axon[3].nseg = round(10*200*scalingFactor)
        
    axon[4] = h.Section(name='extra2')
    axon[4].nseg = round(10*scalingFactor)
    axon[4].diam = 1
    axon[4].L = 100*scalingFactor
    
    axon[5] = h.Section(name='extra3')
    axon[5].nseg = round(10*scalingFactor)
    axon[5].diam = 1
    axon[5].L = 100*scalingFactor
    
    for i in range(6):
        axon[i].Ra = 35.5
        axon[i].cm = 1
        #axon[i].eca=126.1
        #h.ion_style("ca_ion", einit=0, eadvance=0, sec=axon[i])
    
    #connect parts
    axon[1].connect(axon[0])
    axon[2].connect(axon[1])
    axon[3].connect(axon[2])
    axon[4].connect(axon[3])
    axon[5].connect(axon[4])

    '''
    #print all axon information to check if everything is right
    for i in range(6):
        print(axon[i].psection())
    '''
    '''
    h.topology()
    ps = h.PlotShape(False)  # False tells h.PlotShape not to use NEURON's gui
    ps.plot(plt)
    plt.show(0)
    '''
    
    for i in range(6):
        condFactor=1
        if i==0 or i==5:#extra1 and extra3
            #set conduction low at the beginning and end of the axon for action potential to fade out
            condFactor=1e-5
        if i==3:#parent
            insertChannels(axon[i], condFactor, gPump, gNav17Parent, gNav18Parent, gNav19, gKs, gKf, gH, gKdr, gKna, gCav12, gCav22, gNacx, gBk, gSk)
        else:
            insertChannels(axon[i], condFactor, gPump, gNav17, gNav18, gNav19, gKs, gKf, gH, gKdr, gKna, gCav12, gCav22, gNacx, gBk, gSk)
    
    if dt==0:
        #variable time step integration method
        cvode = h.CVode()
        cvode.active(1)
        #print("CVode active")
        cvode.atolscale("cai", 1e-7) #worked with 1e-7
    else:
        h.dt=dt

    if sine:
        stim, delay, vec = setStimulationSine(axon[0], prot, ampSine)
        #print("Stimulation: Sine Wave")
    else:
        stim, delay, vec = setStimulationProtocol(axon[0], prot, previousStim)
        #print("Stimulation: Square Pulse")
    
    '''
    spTimes = h.Vector()
    apc = h.APCount(axon[1](0))
    apc.thresh = -10
    apc.record(spTimes)

    spTimes2 = h.Vector() 
    apc2 = h.APCount(axon[1](0.25))
    apc2.thresh = -10
    apc2.record(spTimes2)
    
    spTimes3 = h.Vector() 
    apc3 = h.APCount(axon[1](0.5))
    apc3.thresh = -10
    apc3.record(spTimes3)
    
    spTimes4 = h.Vector() 
    apc4 = h.APCount(axon[1](0.75))
    apc4.thresh = -10
    apc4.record(spTimes4)
    '''
    spTimes5 = h.Vector() 
    apc5 = h.APCount(axon[1](1))
    apc5.thresh = -10
    apc5.record(spTimes5)
    '''
    spTimes6 = h.Vector() 
    apc6 = h.APCount(axon[3](0))
    apc6.thresh = -10
    apc6.record(spTimes6)
    
    spTimes7 = h.Vector() 
    apc7 = h.APCount(axon[3](0.25))
    apc7.thresh = -10
    apc7.record(spTimes7)
    
    spTimes8 = h.Vector() 
    apc8 = h.APCount(axon[3](0.5))
    apc8.thresh = -10
    apc8.record(spTimes8)
    
    spTimes9 = h.Vector() 
    apc9 = h.APCount(axon[3](0.75))
    apc9.thresh = -10
    apc9.record(spTimes9)
    '''
    spTimes10 = h.Vector() 
    apc10 = h.APCount(axon[3](1))
    apc10.thresh = -10
    apc10.record(spTimes10)
    
    if prot==1:#only one pulse
        t = h.Vector().record(h._ref_t)
        potential = h.Vector().record(axon[3](1)._ref_v)
        potential_1 = h.Vector().record(axon[1](1)._ref_v)
        

    #simulation
    Vrest=vRest
    h.finitialize(Vrest)

    tempCelsius1 = tempBranch
    tempCelsius2 = tempParent
    setTemp(axon[0], tempCelsius1)    
    setTemp(axon[1], tempCelsius1)
    setTemp(axon[2], (tempCelsius1+tempCelsius2)/2)
    setTemp(axon[3], tempCelsius2)
    setTemp(axon[4], tempCelsius2)
    setTemp(axon[5], tempCelsius2)

    h.fcurrent()
    
    scoreBalance=0
    for i in range(6):
        balance(axon[i], Vrest)
        scoreBalance+=checkBalance(axon[i])
    #myPrint("ScoreBalance",scoreBalance)
    
    #create folder
    if not os.path.exists(path):
        os.makedirs(path)
    
    #create filename
    if isinstance(prot, str) and "/" in prot:
        prot = prot.split("/", 2)
        prot = prot[2]
    
    fileSuffix = dataProcessing.getFileSuffix(prot, particleNr, iterationNr)
         
    #start simulation
    tstop = delay
    #h.continuerun(tstop)
    while(h.t<tstop):      
        #step     
        #t_before = time.perf_counter()
        try:
            h.fadvance()
        except Exception as e:
            scoreBalance=float('inf')
            break
        #t_after = time.perf_counter()

        #if t_after-t_before>0.02:
            #scoreBalance=float('inf')
            #break
    
    #save stimulation times
    fileStim = str(path)+'/stim'+'_Prot'+str(prot)+'.csv'
    #if file does not exist, create it
    if not os.path.isfile(fileStim):
        #with fasteners.InterProcessLock(fileStim):
        with open(fileStim,'w', newline='') as f:
            csv.writer(f).writerow(["StimTime"])
            if len(vec)>1:
                csv.writer(f).writerows([[x] for x in vec])
            else:
                csv.writer(f).writerow(vec)

    #save spikes
    fileSpikes = str(path)+'/spikes'+fileSuffix
    with open(fileSpikes,'w', newline='') as f:
        '''
        csv.writer(f).writerow(["Axon 1 0", "Axon 1 0.25", "Axon 1 0.5", "Axon 1 0.75", "Axon 1 1", "Axon 3 0", "Axon 3 0.25", "Axon 3 0.5","Axon 3 0.75","Axon 3 1"])
        '''
        csv.writer(f).writerow(["Axon 1 1", "Axon 3 1"])
        for data in zip_longest(spTimes5, spTimes10, fillvalue=float('nan')):
            print(*data, file=f, sep=",")     
        
    if prot==1:#only one pulse
        #save membrane potential
        filename = str(path)+'/potential'+fileSuffix

        #creates file, deletes content, if file already exists
        with open(filename,'w', newline='') as f:
            csv.writer(f).writerow(["Time", "Axon 1 1", "Axon 3 1"])
            csv.writer(f).writerows(zip(t, potential_1, potential))
        #print("saved potential, path: ", filename) 
    
    #toc = time.perf_counter()
    #print(f"Simulation time Main: {(toc - tic)/60:0.4f} min")
    
    return scoreBalance


