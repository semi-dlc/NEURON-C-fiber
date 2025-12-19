import pandas as pd
import numpy as np
import os

#filename can't be too long, full path can't be more than 255 characters
#therefore values are rounded!
def getFileSuffix(prot=1, particleNr=0, iterationNr=0):
   
    fileSuffix=('_Prot'+str(prot)
                    +'_particle'+str(particleNr)
                    +'_iteration'+str(iterationNr)
                    +'.csv')
    return fileSuffix

#filetype can be "potential", "spikes" or "stim"
def getFilename(path="Results", filetype="potential", prot=1,  nr=0):
    
    #print("GetFilename")
    if filetype=="stim":
        fileSuffix = '_Prot'+str(prot)+'.csv'
    else:
        fileSuffix = getFileSuffix(prot, nr)
    
    #fileSuffix="particle"+str(nr)+".csv"
    
    filename = path+'/'+filetype+fileSuffix
    return filename

#filetype can be "potential", "spikes" or "stim"
def getData(path="Results", filetype="potential", prot=1, nr=0):
    #print("getData")
    filename=getFilename(path, filetype, prot, nr)
    print(filename)
    if os.path.exists(filename):
        data = pd.read_csv(filename)#, index_col=0)#, parse_dates=True, header=None)
        return data
    return None


def calculateLatency(data_aps, data_stim, norm=True):
    l = np.zeros((len(data_stim),2))
    j=0
    i=0
    k=0
    while i < len(data_stim):
        if j < len(data_aps):
            point = data_aps["Axon 3 1"][j]-data_stim["StimTime"][i]
            #print(point)
            if not np.isnan(point):
                if point>0 and point < 200:#normal AP
                    l[k][0]=data_stim["StimTime"][i]/1000
                    l[k][1]=point
                    j=j+1
                    i=i+1
                    k=k+1
                elif point <0:#AP belongs to next stimulation pulse
                    j=j+1
                elif point>200:#AP does not exist
                    l[k][0]=data_stim["StimTime"][i]/1000
                    l[k][1]=float('Nan')
                    i=i+1
                    k=k+1
            else:#AP does not exist
                l[k][0]=data_stim["StimTime"][i]/1000
                l[k][1]=float('Nan')
                i=i+1
                k=k+1     
        else:#no more APs
            l[k][0]=data_stim["StimTime"][i]/1000
            l[k][1]=float('Nan')
            i=i+1
            k=k+1
    #print(l)
    #normalize
    if norm:
        first=l[0][1]
        j=0
        for i in l:
            l[j][1]=(i[1]/first-1)*100
            j=j+1
    return l

def calculateLatency2(data_aps, data_stim, norm=True):
    l = np.zeros((len(data_stim),2))
    j=0
    i=0
    k=0
    while i < len(data_stim):
        if j < len(data_aps):
            point = data_aps[j]-data_stim[i]
            #print(point)
            if point>0 and point < 400:
                l[k][0]=data_stim[i]/1000
                l[k][1]=point
                j=j+1
                i=i+1
                k=k+1
            elif point <0:
                j=j+1
            
            elif point>400:
                l[k][0]=data_stim[i]/1000
                l[k][1]=-1
                i=i+1
                k=k+1
            
        else:
            break
    #normalize
    if norm:
        first=l[0][1]
        j=0
        for i in l:
            l[j][1]=(i[1]/first-1)*100
            j=j+1
    return l

#for ELID and Serra
def getRealData(filename):
    
    data2 = pd.read_excel(filename, index_col=None, header=4)  

    data2 =data2.drop(1)
    data2 =data2.drop("fiber id",1)

    CM=[]
    CMi=[]
    VHT=[]
    for column in data2:
        #sort cm/cmi
        if data2.at[0,column] == "cm":
            CM.append(column)
        elif data2.at[0,column] == "cmi":
            CMi.append(column)
        elif data2.at[0,column] == "vht":
            VHT.append(column)

    data2= data2.drop(0)

    for column in data2:
        #normalize
        first=data2.at[2,column]
        for row in data2.index:
            data2.at[row,column]=(data2.at[row,column]/first-1)*100

    return data2, CM, CMi, VHT
    
    
def getRealDataODP(filename):
    data = pd.read_excel(filename, index_col=None, header=0)  

    CM=[]
    CMi=[]
    VHT=[]
    for index, row in data.iterrows():
        #sort cm/cmi
        if row['unit class'] == "cm":
            CM.append(index)
        elif row['unit class'] == "cmi":
            CMi.append(index)
        elif row['unit class'] == "vht":
            VHT.append(index)

    data=data.drop(columns=['unit class', 'unit type'])
    
    return data, CM, CMi, VHT
    