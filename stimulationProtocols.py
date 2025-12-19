from neuron import h
import numpy as np

def setStimulationProtocol(axon, prot, previousStim=False):
    i=0
    iclamps = []
    vec = []
    delay = 0
    if prot == -1:
        for i in range(1,6):
            vec.append(i*8000)
        lastPulse=5*8000
        delay=lastPulse+500

    elif prot == 0:#Test protocol (10 pulses, 500 ms)
        vec = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500]
        delay = 5000

    elif prot == 1:#single pulse after 2 ms
        vec = [2]
        delay = 250
    
    elif prot == 5:#Test protocol (10 pulses, 1000 ms)
        vec = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
        delay = 10000
 
    elif prot==10:#elID
        #20 pulses at 0.125 Hz -> one pulse every 8 seconds
        for i in range(1,21):
            vec.append(i*8000)
        lastPulse=20*8000
        #20 pulses at 0.25 Hz -> one pulse every 4 seconds
        for i in range(1,21):
            vec.append(lastPulse+i*4000)
        lastPulse=lastPulse+20*4000
        #30 pulses at 0.5 Hz -> one pulse every 2 seconds
        for i in range(1,31):
            vec.append(lastPulse+i*2000)
        delay=lastPulse+30*2000+1000

    elif prot==11:#elID with recovery
        #20 pulses at 0.125 Hz -> one pulse every 8 seconds
        for i in range(1,21):
            vec.append(i*8000)
        lastPulse=20*8000
        #20 pulses at 0.25 Hz -> one pulse every 4 seconds
        for i in range(1,21):
            vec.append(lastPulse+i*4000)
        lastPulse=lastPulse+20*4000
        #30 pulses at 0.5 Hz -> one pulse every 2 seconds
        for i in range(1,31):
            vec.append(lastPulse+i*2000)
        lastPulse=lastPulse+30*2000
        #10 pulses at 0.25 Hz -> one pulse every 4 seconds
        for i in range(1,11):
            vec.append(lastPulse+i*4000)
        delay=lastPulse+10*4000+1000

    elif prot=="ELID_Short":#beginning of ELID protocols
        #20 pulses at 0.125 Hz -> one pulse every 8 seconds
        for i in range(1,6):
            vec.append(i*8000)
        lastPulse=5*8000
        delay=lastPulse+100

    elif prot==15:#2 Hz, 3min
        #2 Hz -> two pulses every second
        offset=0
        for i in range(1,361):
            vec.append(offset+i*500)
        lastPulse=360*500
        #recovery: 10 pulses at 1/4 Hz -> one pulse every 4 seconds
        for i in range(1,11):
            vec.append(lastPulse+i*4000)
        delay=lastPulse+10*4000+100

    elif prot=="2Hz_Short":#2 Hz, only beginning
        #2 Hz -> two pulses every second
        offset=0
        for i in range(1,11):
            vec.append(offset+i*500)
        lastPulse=10*500
        delay=lastPulse+100
    
    elif prot=="DP":#old Doppelpuls
        #20 pulses at 0.25 Hz -> one pulse every 4 seconds
        #to stabilize latency
        offset=0
        for i in range(1,21):
            vec.append(offset+i*4000)
        lastPulse=offset+20*4000
        extras=[2000, 1000, 500, 250, 150, 100, 50, 40, 30, 20, 15]#distance to next regular puls
        numReg=5#number of regular pulses
        for e in extras:
            #one extra pulse
            vec.append(lastPulse+4000-e)
            #regular pulses
            for i in range(1,numReg+1):
                vec.append(lastPulse+i*4000)
            lastPulse=lastPulse+numReg*4000
        delay=lastPulse+1000
    
    elif prot=="FF_5Hz":#following frequency - 5Hz
        offset=100
        numbersRepetition=3
        for j in range(numbersRepetition):
            numberOfPulses=25
            for i in range(numberOfPulses):
                vec.append(offset+i*200)
            lastPulse=offset+(numberOfPulses-1)*200
            offset=10000+lastPulse #10s
        delay=lastPulse+1000
    
    elif prot=="FF_10Hz":#following frequency - 10Hz
        offset=100
        numbersRepetition=3
        for j in range(numbersRepetition):
            numberOfPulses=25
            for i in range(numberOfPulses):
                vec.append(offset+i*100)
            lastPulse=offset+(numberOfPulses-1)*100
            offset=10000+lastPulse #10s
        delay=lastPulse+1000
    
    elif prot=="FF_20Hz":#following frequency - 20Hz
        offset=100
        numbersRepetition=3
        for j in range(numbersRepetition):
            numberOfPulses=25
            for i in range(numberOfPulses):
                vec.append(offset+i*50)
            lastPulse=offset+(numberOfPulses-1)*50
            offset=10000+lastPulse #10s
        delay=lastPulse+1000
    
    elif prot=="FF_50Hz":#following frequency - 50Hz
        numberOfPulses=4
        numberOfBursts=6
        lastPulse=0
        offset=100
        numbersRepetition=3
        for k in range(numbersRepetition):
            for j in range(1, numberOfBursts+1):
                for i in range(numberOfPulses):
                    vec.append(offset+lastPulse+i*20)
                lastPulse=vec[-1]
                offset=200
            offset=10000 #10s
        delay=lastPulse+1000
    
    elif prot=="FF_100Hz":#following frequency - 100Hz
        numberOfPulses=4
        numberOfBursts=6
        lastPulse=0
        offset=100
        numbersRepetition=3
        for k in range(numbersRepetition):
            for j in range(1, numberOfBursts+1):
                for i in range(numberOfPulses):
                    vec.append(offset+lastPulse+i*10)
                lastPulse=vec[-1]
                offset=200
            offset=10000 #10s
        delay=lastPulse+1000
    
    elif prot=="FF2_50Hz":#following frequency - 20Hz
        offset=100
        numbersRepetition=1
        for j in range(numbersRepetition):
            numberOfPulses=25
            for i in range(numberOfPulses):
                vec.append(offset+i*20)
            lastPulse=offset+(numberOfPulses-1)*20
            offset=10000+lastPulse #10s
        delay=lastPulse+1000
    
    elif prot=="FF2_100Hz":#following frequency - 100Hz
        offset=100
        numbersRepetition=1
        for j in range(numbersRepetition):
            numberOfPulses=25
            for i in range(numberOfPulses):
                vec.append(offset+i*10)
            lastPulse=offset+(numberOfPulses-1)*10
            offset=10000+lastPulse #10s
        delay=lastPulse+1000
        
    else:#Get protocol from file
        vec, delay = getProtFromFile(prot)
        
        vecPrevious =[]
        if previousStim==True:
            #set stimulation of 2Hz (one pulse every 0.5 seconds)for 3min/180s 
            for i in range(0, 1800, 5):
                vecPrevious.append(i*100)
            #print(vecPrevious)
            #set stimulation of 0.25Hz (one pulse every 4 seconds) for 3min/180s 
            for i in range(180, 360, 4):
                vecPrevious.append(i*1000)
            #print(vecPrevious)
            
            #offset for vec
            for i in range(len(vec)):
                vec[i]=vec[i]+360*1000
            
            #put previous stimulation in front of vec
            vec = vecPrevious + vec
            delay = delay+360*1000
        
    #print("Stimulation: "+str(vec))
    #print("Duration: "+str(delay))
    
    for t in vec:
        #current clamp
        i = h.IClamp(axon(1))
        i.delay = t # ms
        #working
        #i.dur = 0.2 # ms
        #i.amp = 2.5 # nA
        #like MNG
        i.dur = 0.5 # ms
        i.amp = 0.1 # nA: threshold for model with sacling=0.1: 0.05nA, stim:0.1nA
        #i.amp = 0.075 # to make APs more likely to fail
        #i.amp = 0.14 # nA: threshold for model with sacling=0.5: 0.07nA, stim: 0.14nA
        #i.amp = 0.18 # nA: threshold for model with sacling=1: 0.09nA, stim: 0.18nA
        
        #working
        #i.dur = 5 # ms 
        #i.amp = 0.02 # nA
        #not working
        #i.dur = 5 # Tigerholm
        #i.amp = 0.01 #Tigerholm

        iclamps.append(i)
            
    return iclamps, delay, vec

def setStimulationSine(axon, prot=0, amplitude=0.1):
    i=0
    iclamps = []
    vec = []
    delay = 0
        
    if prot==0:#single sine wave after 2ms
        vec = [2]
        delay = 600
        #current clamp for sine wave
        i = h.SinClamp(axon(1))
        i.delay = 2 # ms #starttime
        i.dur = 250 # ms #duration
        i.pkamp = amplitude # nA #amplitude
        i.freq = 4 #Hz, frequency
        iclamps.append(i)
    if prot==1:#multiple sine waves
        vec = [2]
        delay = 500*5
        #current clamp for sine wave
        i = h.SinClamp(axon(1))
        i.delay = 2 # ms #starttime
        i.dur = 250*5 # ms #duration -> 5 sine waves of 250ms duration
        i.pkamp = amplitude # nA #amplitude
        i.freq = 4 #Hz, frequency
        iclamps.append(i)
        
    return iclamps, delay, vec

        
def getProtFromFile(filename):    
    lines = open(filename).readlines()
    #lines = open("TestProt.txt").readlines()
    vec =[]
    for l in lines:
        l = float(l.replace("\n",""))*1000
        vec.append(l)
    vec.sort()
    delay = float(vec[len(vec)-1])+100
    return vec, delay

def getProtFromFile2(filename):    
    lines = open(filename).readlines()
    #lines = open("TestProt.txt").readlines()
    if isinstance(lines[0], str):
        lines.pop(0)#remove first element if text
    vec =[]
    for l in lines:
        split_string = l.split(",", 1)
        substring = split_string[0]
        f = float(substring.replace("\n",""))*1000
        vec.append(f)
    delay = float(vec[len(vec)-1])+100
    return vec, delay

def test():
    vec1, d1 = getProtFromFile2('Protocols/AE1/20_05_13_U1b_reg.txt')
    vec2, d2 = getProtFromFile2('Protocols/AE1/20_05_13_U1b_extra.txt')
    l = list(np.array(vec1) - np.array(vec2))
    return l
        
        
        
        