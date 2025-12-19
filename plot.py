from neuron import h
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from ast import literal_eval
import dataProcessing
import seaborn as sns
from matplotlib.colors import Normalize
import matplotlib.cm as cm
import json
    

def plotLatency(data_aps, data_stim, norm=False, title=""):
    l = dataProcessing.calculateLatency(data_aps, data_stim, norm)
       
    if len(l)>0:
        plt.figure(figsize=(15,5))
        plt.scatter(l[:,0],l[:,1])
        plt.xlabel('time (s)')
        plt.ylabel('latency (ms)')
        plt.title(title)
        plt.show()


#get lower bound for channel
def lower(ion):
    return 0#because negative values don't make sense
    '''
    if ion==gKdr or ion==gNav18:
        return ion-2*ion
    else:
        return ion-4*ion
    '''
    #return ion-(0.5*ion)
    #return -4.5#beale
    #return -2*math.pi#mishra bird
    #return -10#holder
    #return -512#eggholder
    #return -100#schaffer, easom


#get upper bound for channel
def upper(ion):
    gPump=0.0047891 
    gNav17=0.10664 
    gNav18=0.24271 
    gNav19=9.4779e-05 
    gKs=0.0069733 
    gKf=0.012756 
    gH=0.0025377 
    gKdr=0.018002 
    gKna=0.00042
    
    if ion==gKdr or ion==gNav18:
        return 2*ion
    else:
        return 4*ion
    
    #return ion+(0.5*ion)
    #return 4.5#beale
    #return 2*math.pi#mishra bird
    #return 10#holder
    #return 512#eggholder
    #return 100#schaffer, easom

#plot particle positions and scores
def plotParticles(dimension, num_particles, num_iterations, name):
    gPump=0.0047891 
    gNav17=0.10664 
    gNav18=0.24271 
    gNav19=9.4779e-05 
    gKs=0.0069733 
    gKf=0.012756 
    gH=0.0025377 
    gKdr=0.018002 
    gKna=0.00042
    
    channel_names=["Pump", "Nav17", "Nav18", "Nav19", "Ks", "Kf", "h", "Kdr", "Kna"]
    ions=[gPump, gNav17, gNav18, gNav19, gKs, gKf, gH, gKdr, gKna]
    
    '''
    colors=['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                      'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                      'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
    '''
    
    #get particles 
    for j in range(dimension):
        for i in range(num_particles):
            filename='Results/'+str(name)+'/'+str(name)+'particle'+str(i)+'.csv'
            data = pd.read_csv(filename)

            data['Position'] = data['Position'].apply(literal_eval)#make string to list
            
            #weights = np.arange(1, len(data["Position"])+1)
            #plt.scatter(data["Score"], data["Position"].apply(lambda x: x[j]), marker='.', c=weights, cmap=colors[i])
            
            #plt.plot(data["Score"], data["Position"].apply(lambda x: x[j]), marker='.')
            plt.plot(data["Position"].apply(lambda x: x[j]), data["Score"], marker='.')
        
        plt.xlim(lower(ions[j]), upper(ions[j]))
        #plt.xlim(0,2)
        plt.title(channel_names[j])
        plt.ylabel("Score")
        plt.xlabel("conduction")
        plt.show()

'''    
def plotParticles2D(dimension, num_particles, num_iterations, name, showInf, scoreCutoff=float('inf')):
    gPump=0.0047891 
    gNav17=0.10664 
    gNav18=0.24271 
    gNav19=9.4779e-05 
    gKs=0.0069733 
    gKf=0.012756 
    gH=0.0025377 
    gKdr=0.018002 
    gKna=0.00042

    gCav12=0.000188 
    gCav22=0.000361 
    gNacx=0.009242 
    gBk=0.002016
    gSk=0.000755

    vRest=-55
    
    channel_names=["Pump", "Nav17", "Nav17P", "Nav18", "Nav18P", "Nav19", "Ks", "Kf", "h", "Kdr", "Kna", "Cav12", "Cav22", "Nacx", "Bk", "Sk", "RMP"]
    ions=[gPump, gNav17, gNav17, gNav18, gNav18, gNav19, gKs, gKf, gH, gKdr, gKna, gCav12, gCav22, gNacx, gBk, gSk, vRest]
    
    filename='Results/'+str(name)+'/'+str(name)+'_bestParticles.csv'
    dataBest = pd.read_csv(filename)
    dataBest['Position'] = dataBest['Position'].apply(literal_eval)#make string to list
    
    allData=[]
    for i in range(num_particles):
        filename='Results/'+str(name)+'/'+str(name)+'particle'+str(i)+'.csv'
        data = pd.read_csv(filename)
        data['Position'] = data['Position'].apply(literal_eval)#make string to list
        data=data[0:num_iterations]
        
        
        if scoreCutoff!=float('inf'):
            data = data[data['Score'] < scoreCutoff]#only data with score < scoreCutoff
            data=data.reset_index()

        if showInf:
            data.replace([np.inf, -np.inf], 1500, inplace=True)
        allData.append(data)
        
    figure, axis = plt.subplots(dimension, dimension, figsize=(25, 25))
    #get particles 
    
    maxScore=0
    # getting the original colormap using cm.get_cmap() function
    orig_map=plt.cm.get_cmap('YlGnBu')
    # reversing the original colormap using reversed() function
    reversed_map = orig_map.reversed()
    
    for p1 in range(dimension):
        for p2 in range(dimension):
            dataHist=[]
            for i in range(num_particles):
                if p2<p1:
                    im=axis[p1,p2].scatter(allData[i]["Position"].apply(lambda x: x[p2]), allData[i]["Position"].apply(lambda x: x[p1]), c=allData[i]["Score"], cmap=reversed_map, marker=".")
                    
                    #find max score
                    #print("allData[i]")
                    #print(allData[i])
                    #print("#################################################################")
                    if not allData[i].empty:
                        maxi = np.where(np.isinf(allData[i]["Score"]),-np.Inf,allData[i]["Score"]).max()
                        if maxScore<maxi:
                            maxScore=maxi
                    #print(allData[i]["Position"].apply(lambda x: x[p2]))
                    #print(allData[i]["Position"].apply(lambda x: x[p1]))
                    #print(allData[i]["Score"])
                    #print(dataBest["Position"][num_iterations-1])
                    axis[p1,p2].plot(dataBest["Position"][num_iterations-1][p2], dataBest["Position"][num_iterations-1][p1], c="Red", zorder=100, markersize=10, marker="*")
                    axis[p1,p2].plot(ions[p2], ions[p1], c="green", zorder=100, markersize=10, marker="*")#original value
                elif p1==p2:
                    dataHist.append(allData[i]["Position"].apply(lambda x: x[p1]))

            if p1==p2:
                axis[p1,p2].hist(dataHist, bins=20)

            axis[p1,0].set_ylabel(channel_names[p1])
            axis[dimension-1,p2].set_xlabel(channel_names[p2])
    
    
    if maxScore>scoreCutoff:
        maxScore=scoreCutoff
    print(maxScore)    
    normalizer=Normalize(0,maxScore)
    im=cm.ScalarMappable(norm=normalizer, cmap=reversed_map)
    figure.colorbar(im, ax=axis.ravel().tolist())
    
    #figure.subplots_adjust(right=0.8)
    #cbar_ax = figure.add_axes([0.85, 0.15, 0.05, 0.7])
    #figure.colorbar(im, cax=cbar_ax)
'''


def plotParticles2D(dimension, num_particles, num_iterations, name, showInf, scoreCutoff=float('inf'), replaceInf=30000):
    ions = np.array([
        0.0047891, 0.10664, 0.10664, 0.24271, 0.24271, 9.4779e-05, 0.0069733, 
        0.012756, 0.0025377, 0.018002, 0.00042, 0.000188, 0.000361, 0.009242, 0.002016, 0.000755, -55
    ])
    
    channel_names = [
        "Pump", "Nav17", "Nav17P", "Nav18", "Nav18P", "Nav19", "Ks", "Kf", "h", "Kdr", 
        "Kna", "Cav12", "Cav22", "Nacx", "Bk", "Sk", "RMP"
    ]

    # Best Particle Daten einlesen (mit effizienter JSON-Parsing-Methode)
    best_file = f'Results/{name}/{name}_bestParticles.csv'
    dataBest = pd.read_csv(best_file)
    dataBest['Position'] = dataBest['Position'].map(json.loads)  # JSON ist effizienter als eval

    # Daten für alle Partikel laden
    allData = []
    for i in range(num_particles):
        file = f'Results/{name}/{name}particle{i}.csv'
        data = pd.read_csv(file)
        data['Position'] = data['Position'].map(json.loads)

        if scoreCutoff != float('inf'):
            data = data[data['Score'] < scoreCutoff]

        if showInf:
            data.replace([np.inf, -np.inf], replaceInf, inplace=True)

        allData.append(data)

    # Plot erstellen
    figure, axis = plt.subplots(dimension, dimension, figsize=(25, 25))
    maxScore = 0

    # Farbmap umkehren
    reversed_map = plt.cm.get_cmap('YlGnBu').reversed()

    # Haupt-Plot-Schleife
    for p1 in range(dimension):
        for p2 in range(dimension):
            if p2 < p1:
                # Positions- und Score-Daten für Scatterplot vorbereiten
                x_vals, y_vals, scores = [], [], []
                for data in allData:
                    x_vals.extend([pos[p2] for pos in data["Position"]])
                    y_vals.extend([pos[p1] for pos in data["Position"]])
                    scores.extend(data["Score"])

                im = axis[p1, p2].scatter(x_vals, y_vals, c=scores, cmap=reversed_map, marker=".", s=1)

                # Bestes Partikel & Originalwert plotten
                axis[p1, p2].plot(dataBest["Position"].iloc[num_iterations-1][p2], 
                                  dataBest["Position"].iloc[num_iterations-1][p1], 
                                  c="red", markersize=10, marker="*")
                axis[p1, p2].plot(ions[p2], ions[p1], c="green", markersize=10, marker="*")

                # Maximalen Score für Normalisierung bestimmen
                maxScore = max(maxScore, np.nanmax(np.where(np.isinf(scores), -np.inf, scores)))

            elif p1 == p2:
                # Histogramm der Parameterwerte erstellen
                param_vals = [pos[p1] for data in allData for pos in data["Position"]]
                axis[p1, p2].hist(param_vals, bins=20)

            axis[p1, 0].set_ylabel(channel_names[p1])
            axis[dimension - 1, p2].set_xlabel(channel_names[p2])

    # Colorbar für alle Achsen
    print(maxScore)
    normalizer = Normalize(0, min(maxScore, scoreCutoff))
    im = plt.cm.ScalarMappable(norm=normalizer, cmap=reversed_map)
    figure.colorbar(im, ax=axis.ravel().tolist())

    plt.show()



# Daten effizient laden
def load_data_parallel(name, num_particles, num_iterations):
    all_data = []
    
    for i in range(num_particles):
        filename = f'Results/{name}/{name}particle{i}.csv'
        data = pd.read_csv(filename, dtype={'Position': str})  # Schnellere Einlesung

        # Position direkt als Liste speichern
        data['Position'] = data['Position'].map(literal_eval)  
        all_data.append(data.iloc[:num_iterations])  # Nur benötigte Zeilen
        
    return all_data

#show only particles with Score=inf or particles with a score below a certain threshold
def plotParticles2D_Heatmap_Relative(dimension, num_particles, num_iterations, name, score="inf"):
    
    channel_names=["Pump", "Nav17", "Nav17P", "Nav18", "Nav18P", "Nav19", "Ks", "Kf", "h", "Kdr", "Kna", "Cav12", "Cav22", "Nacx", "Bk", "Sk", "RMP"]
    
    allData=load_data_parallel(name, num_particles, num_iterations)
    
    figure, axis = plt.subplots(dimension, dimension, figsize=(25, 25))

    orig_map = plt.cm.get_cmap('YlGnBu').reversed()  # Colormap vorbereiten

    for p1 in range(dimension):
        for p2 in range(dimension):
            x_vals, y_vals, inf_mask = [], [], []

            # Daten vorbereiten
            for i in range(num_particles):
                pos = np.array(allData[i]['Position'].tolist())  # Schneller als .apply
                scores = allData[i]['Score'].to_numpy()
                if score == "inf":
                    mask = (scores == "inf") | (scores == float("inf"))
                else:
                    mask = scores <= score

                x_vals.append(pos[:, p2])
                y_vals.append(pos[:, p1])
                inf_mask.append(mask)

            # In `numpy` umwandeln für schnelleren Zugriff
            x_vals = np.concatenate(x_vals)
            y_vals = np.concatenate(y_vals)
            inf_mask = np.concatenate(inf_mask)
            
            if p2 < p1:
                # Scatterplot: Inf-Punkte rot
                #axis[p1, p2].scatter(x_vals[inf_mask], y_vals[inf_mask], color="red", edgecolor="black", marker=".")

                heatmap1, xedges1, yedges1 = np.histogram2d(x_vals, y_vals, bins=50)
                print(heatmap1)
                # Zählen der Positionen für Heatmap (Inf-Werte)
                heatmap, xedges, yedges = np.histogram2d(x_vals[inf_mask], y_vals[inf_mask], bins=50)
                print(heatmap)
                relative_heatmap = np.divide(heatmap, heatmap1, out=np.zeros_like(heatmap, dtype=float), where=heatmap1 > 0)
                # Heatmap anzeigen
                im = axis[p1, p2].imshow(relative_heatmap.T, origin='lower', cmap=orig_map, aspect='auto', interpolation='nearest')

                # Achsen anpassen, um die korrekten Werte darzustellen
                x_tick_positions = np.linspace(0, len(xedges) - 1, 4)
                y_tick_positions = np.linspace(0, len(yedges) - 1, 4)
            
                axis[p1, p2].set_xticks(x_tick_positions)
                axis[p1, p2].set_xticklabels(np.round(xedges[x_tick_positions.astype(int)], 3))
                axis[p1, p2].set_yticks(y_tick_positions)
                axis[p1, p2].set_yticklabels(np.round(yedges[y_tick_positions.astype(int)], 3))
                
                #figure.colorbar(im, ax=axis[p1, p2])  # Colorbar für jede Heatmap hinzufügen

            elif p1==p2:
                axis[p1, p2].hist(x_vals, bins=50, alpha=0.7, color="red", label="all particles")
                axis[p1, p2].hist(x_vals[inf_mask], bins=50, alpha=0.7, zorder=3, label=str(score))
                axis[p1, p2].legend(loc='upper left', bbox_to_anchor=(1, 1))

            axis[p1, 0].set_ylabel(channel_names[p1])
            axis[dimension - 1, p2].set_xlabel(channel_names[p2])

    figure.subplots_adjust(right=0.8)
    cbar_ax = figure.add_axes([0.82, 0.15, 0.02, 0.7])
    cbar=figure.colorbar(im, cax=cbar_ax)
    cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel('relative number of particles', rotation=270)
    #plt.legend()
    plt.show()

def plotParticles2D_Heatmap(dimension, num_particles, num_iterations, name, score="inf", bins=50):
    
    channel_names=["Pump", "Nav17", "Nav17P", "Nav18", "Nav18P", "Nav19", "Ks", "Kf", "h", "Kdr", "Kna", "Cav12", "Cav22", "Nacx", "Bk", "Sk", "RMP"]
    
    allData=load_data_parallel(name, num_particles, num_iterations)
    
    figure, axis = plt.subplots(dimension, dimension, figsize=(25, 25))

    orig_map = plt.cm.get_cmap('YlGnBu').reversed()  # Colormap vorbereiten

    for p1 in range(dimension):
        for p2 in range(dimension):
            x_vals, y_vals, inf_mask = [], [], []

            # Daten vorbereiten
            for i in range(num_particles):
                pos = np.array(allData[i]['Position'].tolist())  # Schneller als .apply
                scores = allData[i]['Score'].to_numpy()
                if score == "inf":
                    mask = (scores == "inf") | (scores == float("inf"))
                else:
                    mask = scores <= score

                x_vals.append(pos[:, p2])
                y_vals.append(pos[:, p1])
                inf_mask.append(mask)

            # In `numpy` umwandeln für schnelleren Zugriff
            x_vals = np.concatenate(x_vals)
            y_vals = np.concatenate(y_vals)
            inf_mask = np.concatenate(inf_mask)
            
            if p2 < p1:
                # Scatterplot: Inf-Punkte rot
                #axis[p1, p2].scatter(x_vals[inf_mask], y_vals[inf_mask], color="red", edgecolor="black", marker=".")

                # Zählen der Positionen für Heatmap (Inf-Werte)
                heatmap, xedges, yedges = np.histogram2d(x_vals[inf_mask], y_vals[inf_mask], bins=bins)
                # Heatmap anzeigen
                im = axis[p1, p2].imshow(heatmap.T, origin='lower', cmap=orig_map, aspect='auto', interpolation='nearest')

                # Achsen anpassen, um die korrekten Werte darzustellen
                x_tick_positions = np.linspace(0, len(xedges) - 1, 4)
                y_tick_positions = np.linspace(0, len(yedges) - 1, 4)
            
                axis[p1, p2].set_xticks(x_tick_positions)
                axis[p1, p2].set_xticklabels(np.round(xedges[x_tick_positions.astype(int)], 3))
                axis[p1, p2].set_yticks(y_tick_positions)
                axis[p1, p2].set_yticklabels(np.round(yedges[y_tick_positions.astype(int)], 3))
                
                #figure.colorbar(im, ax=axis[p1, p2])  # Colorbar für jede Heatmap hinzufügen

            elif p1==p2:
                axis[p1, p2].hist(x_vals, bins=bins, alpha=0.7, color="red", label="all particles")
                axis[p1, p2].hist(x_vals[inf_mask], bins=bins, alpha=0.7, zorder=3, label=str(score))
                axis[p1, p2].legend(loc='upper left', bbox_to_anchor=(1, 1))

            axis[p1, 0].set_ylabel(channel_names[p1])
            axis[dimension - 1, p2].set_xlabel(channel_names[p2])

    figure.subplots_adjust(right=0.8)
    cbar_ax = figure.add_axes([0.82, 0.15, 0.02, 0.7])
    cbar=figure.colorbar(im, cax=cbar_ax)
    cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel('number of particles', rotation=270)
    #plt.legend()
    plt.show()


#plots 2d marginals of particles as a heatmap, and 1d marginals as histogram 
#dimension: number of dimensions of particle
#num_particles: number of particles
#num_iterations: number of iterations
#name: filename 
#replaceInf: replace infinite values with number
#scoreCutoff: only plot particles with scores below cutoff
#nBins: number of bins shown in heatmap
def plotParticles2DMarginal(dimension, num_particles, num_iterations, name, replaceInf=float('inf'), scoreCutoff=float('inf'), nBins=10):
    gPump=0.0047891 
    gNav17=0.10664 
    gNav18=0.24271 
    gNav19=9.4779e-05 
    gKs=0.0069733 
    gKf=0.012756 
    gH=0.0025377 
    gKdr=0.018002 
    gKna=0.00042
    
    channel_names=["Pump", "Nav17", "Nav18", "Nav19", "Ks", "Kf", "h", "Kdr", "Kna"]
    ions=[gPump, gNav17, gNav18, gNav19, gKs, gKf, gH, gKdr, gKna]
    
    #get best particles
    filename='Results/'+str(name)+'/'+str(name)+'_bestParticles.csv'
    dataBest = pd.read_csv(filename)
    dataBest['Position'] = dataBest['Position'].apply(literal_eval)#make string to list
    
    #get all particles 
    allData=[]
    for i in range(num_particles):
        filename='Results/'+str(name)+'/'+str(name)+'particle'+str(i)+'.csv'
        data = pd.read_csv(filename)
        data['Position'] = data['Position'].apply(literal_eval)#make string to list
        data=data[0:num_iterations]
        
        if scoreCutoff!=float('inf'):
            data = data[data['Score'] < scoreCutoff]#only data with score < scoreCutoff
            data = data.reset_index()
                
        if replaceInf!=float('inf'):
            data.replace([np.inf, -np.inf], replaceInf, inplace=True)#replace infinite values with number
        allData.append(data)
                
    maxScore=0
    # getting the original colormap using cm.get_cmap() function
    orig_map=plt.cm.get_cmap('YlGnBu')
    # reversing the original colormap using reversed() function
    reversed_map = orig_map.reversed()
    
    figure, axis = plt.subplots(dimension, dimension, figsize=(25, 25))
    for p1 in range(dimension):
        for p2 in range(dimension):
            dataHist=[]
            
            if p2<p1:
                gridFinal = np.zeros_like(allData[0]["Score"], shape=(nBins+1, nBins+1))
                countFinal = np.zeros_like(allData[0]["Score"], shape=(nBins+1, nBins+1))

                #set step size
                if ions[p1]==gKdr or ions[p1]==gNav18:
                    xstep=ions[p1]*2/nBins
                else:
                    xstep=ions[p1]*4/nBins
                #print(xstep)

                if ions[p2]==gKdr or ions[p2]==gNav18:
                    ystep=ions[p2]*2/nBins
                else:
                    ystep=ions[p2]*4/nBins
                #print(ystep)
 
            for i in range(num_particles):
                if p2<p1:
                    x=allData[i]["Position"].apply(lambda x: x[p1])#Nav17
                    y=allData[i]["Position"].apply(lambda x: x[p2])#pump
                    #print(x)
                    #print(y)
                    
                    #calculate bins
                    xbin = ((x) // xstep).astype(int)
                    ybin = ((y) // ystep).astype(int) 
                    #print(xbin)
                    #print(ybin)
                    
                    grid = np.zeros_like(allData[i]["Score"], shape=(nBins+1, nBins+1))
                    count = np.zeros_like(allData[i]["Score"], shape=(nBins+1, nBins+1))
                    np.add.at(grid, (xbin, ybin), allData[i]["Score"])# add scores
                    #print(grid)
                    np.add.at(count, (xbin, ybin), 1)#number of values in each field
                    #print("Count")
                    #print(count)
                    
                    #print("Grid")
                    #print(grid)
                    gridFinal+=grid
                    countFinal+=count

                elif p1==p2:
                    dataHist.append(allData[i]["Position"].apply(lambda x: x[p1]))
                 
            if p2<p1:              
                gridFinal=gridFinal/countFinal#get mean score
                #print("GridFinal")
                #print(gridFinal)
                
                #print("CountFinal")
                #print(countFinal)
                
                #find max score
                #maxi = np.where(np.isinf(gridFinal),-np.Inf, gridFinal).argmax()
                test=np.where(np.isinf(gridFinal),-np.Inf, gridFinal)
                maxi = np.nanmax(test)
                #maxi = max(map(max, gridFinal))
                if maxScore<maxi:
                    maxScore=maxi

                axis[p1,p2].imshow(gridFinal, cmap=reversed_map, origin='lower')
                
                #set labels
                if ions[p1]==gKdr or ions[p1]==gNav18:
                    xstepL=ions[p1]*2/5
                else:
                    xstepL=ions[p1]*4/5
                #print(xstep)

                if ions[p2]==gKdr or ions[p2]==gNav18:
                    ystepL=ions[p2]*2/3
                else:
                    ystepL=ions[p2]*4/3
                
                labelX = np.array([round(xstepL*i,4) for i in range(1,6)])
                labelY = np.array([round(ystepL*i,3) for i in range(1,4)])

                axis[p1,p2].set_xticks(np.arange(0,nBins, nBins/3))
                axis[p1,p2].set_yticks(np.arange(0,nBins, nBins/5))
                axis[p1,p2].set_xticklabels(labels=labelY)
                axis[p1,p2].set_yticklabels(labels='')
                #axis[0,p2].set_xticklabels(labels=labelY)
                axis[p1,0].set_yticklabels(labels=labelX)

                #mark best position
                y=dataBest["Position"][num_iterations-1][p2]
                x=dataBest["Position"][num_iterations-1][p1]

                xbin = ((x) // xstep)
                ybin = ((y) // ystep)

                #axis[p1,p2].plot(dataBest["Position"][num_iterations-1][p2], dataBest["Position"][num_iterations-1][p1], c="Red", zorder=100, markersize=10, marker="*")
                axis[p1,p2].plot(ybin, xbin, c="Red", zorder=100, markersize=10, marker="*")
                
            if p1==p2:
                axis[p1,p2].hist(dataHist)
                    
            axis[p1,0].set_ylabel(channel_names[p1])
            axis[dimension-1,p2].set_xlabel(channel_names[p2])
    
    if maxScore>scoreCutoff:
        maxScore=scoreCutoff
    #print(maxScore)    
    normalizer=Normalize(0,maxScore)
    im=cm.ScalarMappable(norm=normalizer, cmap=reversed_map)
    figure.colorbar(im, ax=axis.ravel().tolist())
       
    
def plotParticles2Dindividual(dimension, partcileNr, num_iterations, name):
    gPump=0.0047891 
    gNav17=0.10664 
    gNav18=0.24271 
    gNav19=9.4779e-05 
    gKs=0.0069733 
    gKf=0.012756 
    gH=0.0025377 
    gKdr=0.018002 
    gKna=0.00042

    gCav12=0.000188 
    gCav22=0.000361 
    gNacx=0.009242 
    gBk=0.002016
    gSk=0.000755

    vRest=-55
    
    channel_names=["Pump", "Nav17", "Nav17P", "Nav18", "Nav18P", "Nav19", "Ks", "Kf", "h", "Kdr", "Kna", "Cav12", "Cav22", "Nacx", "Bk", "Sk", "RMP"]
    ions=[gPump, gNav17, gNav17, gNav18, gNav18, gNav19, gKs, gKf, gH, gKdr, gKna, gCav12, gCav22, gNacx, gBk, gSk, vRest]

    #get particles 
    #for i in range(num_particles):
    figure, axis = plt.subplots(dimension, dimension, figsize=(25, 25))
    for p1 in range(dimension):
        for p2 in range(dimension):
            dataHist=[]

            filename='Results/'+str(name)+'/'+str(name)+'particle'+str(partcileNr)+'.csv'
            data = pd.read_csv(filename)
            data['Position'] = data['Position'].apply(literal_eval)#make string to list
            data=data[0:num_iterations]

            if p2<p1:
                # Standardfarbe: Zeilennummer für die Farbskala
                colors = np.array(data.index, dtype=float)

                # Prüfen, ob "inf" als String oder float gespeichert ist
                inf_mask = (data["Score"] == "inf") | (data["Score"] == float("inf"))
                
                # Hauptplot (alle Punkte mit Farbskala)
                im = axis[p1, p2].scatter(
                    data["Position"].apply(lambda x: x[p2]), 
                    data["Position"].apply(lambda x: x[p1]), 
                    c=colors, 
                    cmap="Blues"
                )

                red_colors = colors[inf_mask]
                # Separate Plot-Anweisung für rote Punkte
                im2 = axis[p1, p2].scatter(
                    data.loc[inf_mask, "Position"].apply(lambda x: x[p2]),
                    data.loc[inf_mask, "Position"].apply(lambda x: x[p1]),
                    c=red_colors,
                    cmap="Reds",
                    zorder=3  # Damit diese Punkte über den blauen liegen
                )

            elif p1==p2:
                #w=upper(ions[p1])/len(data["Score"])
                #axis[p1,p2].bar(data["Position"].apply(lambda x: x[p1]), data["Score"], width=w, color='c')
                #b=np.arange(upper(ions[p1]), step=upper(ions[p1])/10)
                #print(b)
                dataHist.append(data["Position"].apply(lambda x: x[p1]))
            

            if p1==p2:
                #print(dataHist)
                axis[p1,p2].hist(dataHist)


            #axis[p1,p2].set_xlim(lower(ions[p2]), upper(ions[p2]))
            #axis[p1,p2].set_ylim(lower(ions[p1]), upper(ions[p1]))
            #plt.xlim(0,2)
            axis[p1,0].set_ylabel(channel_names[p1])
            axis[dimension-1,p2].set_xlabel(channel_names[p2])
    figure.subplots_adjust(right=0.8)
    cbar_ax = figure.add_axes([0.85, 0.15, 0.05, 0.7])
    cbar_ax2 = figure.add_axes([0.95, 0.15, 0.05, 0.7])
    figure.colorbar(im, cax=cbar_ax, label="Iteration number (blue)")
    plt.colorbar(im2, cax=cbar_ax2, label="Iteration number (red)")
        
        
def plotRecoveryCycle(data_aps, data_stim, norm):
    l = dataProcessing.calculateLatency(data_aps, data_stim, norm)
    recoveryCycle=[]
    #extras=[2000, 1750, 1500, 1250, 1000, 750, 500, 250, 150, 100, 75, 50, 40, 30, 20, 10]#distance to next regular puls
    extras=[2000, 1000, 500, 250, 150, 100, 50, 40, 30, 20, 15]#distance to next regular puls
    extrasFinal=[]
    
    numberOfExtra=len(extras)#total number of extra pulses
    numRegPulses=6#number of regular pulses in between extra pulses
    for i in range(numberOfExtra):
        l1=l[20+i*numRegPulses][1]#latency of first extra pulse
        l2=l[21+i*numRegPulses][1]#latency of next regular pulse
        if l1!=-1 and l2!=-1:
            recoveryCycle.append(l2-l1)
            extrasFinal.append(extras[i])
    print(recoveryCycle)
    print(extrasFinal)
    
    plt.plot(extrasFinal, recoveryCycle, marker=".", label="Simulation")
    realDataCMi=[0.324487317, 0.249044214, -0.176721166, 0.452664143, 1.463325936, 1.798056359, 3.110076518, 2.838785715, 3.442295076, 3.763976836,  3.681834103]
    plt.plot(extras, realDataCMi, marker=".", label="CMi")
    realDataCM=[0.240241491, 0.252928694, 0.296115416, 0.546602641, 1.450783851, 2.515537532, 3.780695111, 4.167464007, 4.516383778, 4.916885365, 5.386598886]
    plt.plot(extras, realDataCM, marker=".", label="CM")
    plt.legend()
    plt.xlabel("interspike interval")
    plt.ylabel("slowing/speeding")
    

def plotRealData(filename):
    
    data2, CM, CMi, VHT = dataProcessing.getRealData(filename)

    mean=data2[CMi].mean(axis=1)
    std=data2[CMi].sem(axis=1)

    plt.errorbar(range(len(mean)),mean, std, linestyle='None', marker='.', label="CMi")
    mean=data2[CM].mean(axis=1)
    std=data2[CM].sem(axis=1)
    plt.errorbar(range(len(mean)),mean, std, linestyle='None', marker='.', label="CM")
    mean=data2[VHT].mean(axis=1)
    std=data2[VHT].sem(axis=1)
    plt.errorbar(range(len(mean)),mean, std, linestyle='None', marker='.', label="VHT")
    plt.legend()

#for ELID und Serra
def plotRealSim(filenameReal, data_aps, data_stim, fiberType, norm=False):
    
    data2, CM, CMi, VHT = dataProcessing.getRealData(filenameReal)
    
    plt.figure(figsize=(15,5))
    
    if fiberType=="CM":
        mean=data2[CM].mean(axis=1)
        std=data2[CM].sem(axis=1)
        plt.errorbar(range(len(mean)),mean, std, linestyle='None', marker='.', label="CM", color="black", ecolor="grey")
    elif fiberType=="CMi":
        mean=data2[CMi].mean(axis=1)
        std=data2[CMi].sem(axis=1)
        plt.errorbar(range(len(mean)),mean, std, linestyle='None', marker='.', label="CMi", color="black", ecolor="grey")
    elif fiberType=="VHT":
        mean=data2[VHT].mean(axis=1)
        std=data2[VHT].sem(axis=1)
        plt.errorbar(range(len(mean)),mean, std, linestyle='None', marker='.', label="VHT", color="black", ecolor="grey")
        
    l = dataProcessing.calculateLatency(data_aps, data_stim, norm)
       
    if len(l)>0:
        plt.scatter(range(len(l)),l[:,1], label="Simulation", color="red")
        plt.xlabel('time (s)')
        plt.ylabel('latency (ms)')
        plt.title('Latency')
        plt.legend()
        plt.show()
    
def plotRealSimODP(filenameReal, pathSim, scalingFactor, norm, particle, fibertype="CMi"):
    fig, ax=plt.subplots(figsize=(15,5))

    data2, CM, CMi, VHT=dataProcessing.getRealDataODP(filenameReal)

    if fibertype=="CMi":
        mean=data2.iloc[CMi].mean()
        sem=data2.iloc[CMi].sem()
    elif fibertype=="CM":
        mean=data2.iloc[CM].mean()
        sem=data2.iloc[CM].sem()
    elif fibertype=="VHT":
        mean=data2.iloc[VHT].mean()
        sem=data2.iloc[VHT].sem()
    plt.errorbar(range(len(mean)),mean.iloc[::-1], sem.iloc[::-1], linestyle='None', marker='.', label="in-vivo", color="red", ecolor="red")

    data_aps=dataProcessing.getData(path=pathSim, filetype="spikes", prot='DP', nr=particle)
    data_stim=pd.read_csv(str(pathSim)+"/stim_ProtDP.csv")

    l=dataProcessing.calculateLatency(data_aps, data_stim, norm=norm)

    recoveryCycle=[]
    for i in range(19,len(l)-2,6):
        recoveryCycle.append(l[i+2][1]-l[i][1])
        #print("Shift")
        #print(i)
        #print(i+2)


    plt.scatter(range(len(recoveryCycle)), recoveryCycle[::-1], label="in-silico", color="darkblue")
    ax.set_xticks(range(11))
    labels=["2000", "1000", "500", "250", "150", "100", "50", "40", "30", "20", "15"]
    ax.set_xticklabels(labels[::-1])
    plt.xlabel("interstimulus interval in ms")
    if norm:
        plt.ylabel('slowing (%)')
    else:
        plt.ylabel('slowing (ms)')
    plt.title("Recovery Cycle")
    plt.legend()
    #plt.savefig("Figures/Optimization-RecoveryCycle", bbox_inches='tight', dpi=300)
                
def plotRealSimFF(pathSim, scalingFactor, freq, particle):
    gPump, gNav17, gNav18, gNav19, gKs, gKf, gH, gKdr, gKna=particle
    
    fig, ax=plt.subplots(figsize=(15,5))

    #Werte von Vivien
    if freq==10:
        #10HZ,CMi, 2-4-8
        mean=[0.92, 2.26, 4.52]
        sem=[0.56, 0.97, 1.56]
    elif freq==20:
        mean=[1.42,3.07,5.48]
        sem=[0.2, 0.16, 1.35]
    elif freq==50:
        mean=[1.27,2.47,4.57]
        sem=[0.27,0.64,1.78]
    elif freq==100:
        mean=[0.84, 0.91,0.99]
        sem=[0.64,0.69,0.57]
        
    plt.errorbar(range(len(mean)),mean, sem, linestyle='None', marker='.', label="CMi", color="black", ecolor="grey")

    data_aps=dataProcessing.getData(path=pathSim, filetype="spikes", prot='FF_'+str(freq)+'Hz_ADS', scalingFactor=scalingFactor, gPump=-gPump, gNav17=gNav17, gNav18=gNav18, gNav19=gNav19, gKs=gKs, gKf=gKf, gH=gH, gKdr=gKdr, gKna=gKna)
    data_stim=dataProcessing.getData(path=pathSim, filetype="stim", prot='FF_'+str(freq)+'Hz_ADS', scalingFactor=scalingFactor, gPump=-gPump, gNav17=gNav17, gNav18=gNav18, gNav19=gNav19, gKs=gKs, gKf=gKf, gH=gH, gKdr=gKdr, gKna=gKna)

    if data_aps is not None:
        l=dataProcessing.calculateLatency(data_aps, data_stim, norm=True)

        a=np.where(l[:,0] == 80)
        b=np.where(l[:,0] == 84)

        c=np.where(l[:,0] == 120)
        d=np.where(l[:,0] == 124)

        e=np.where(l[:,0] == 160)
        f=np.where(l[:,0] == 164)

        ff=[l[b][0,1]-l[a][0,1], l[d][0,1]-l[c][0,1], l[f][0,1]-l[e][0,1]]

        plt.scatter(range(len(ff)), ff, label="Simulation", color="red")
    
    ax.set_xticks(range(3))
    labels=[2,4,8]
    ax.set_xticklabels(labels)
    plt.xlabel("number of extra pulses")
    plt.ylabel("slowing in %")
    plt.title("Following Frequencies - "+str(freq)+"Hz")
    plt.legend()
        
def plotGating(data, title=""):
    data["Nav1.7_m"].plot()
    data["Nav1.7_h"].plot()
    data["Nav1.7_s"].plot()
    plt.legend()
    plt.title(title)
    plt.show()

    data["Nav1.8_m"].plot()
    data["Nav1.8_h"].plot()
    data["Nav1.8_s"].plot()
    data["Nav1.8_u"].plot()
    plt.legend()
    plt.title(title)
    plt.show()

    data["Nav1.9_m"].plot()
    data["Nav1.9_h"].plot()
    data["Nav1.9_s"].plot()
    plt.legend()
    plt.title(title)
    plt.show()

    data["Ks_nf"].plot()
    data["Ks_ns"].plot()
    plt.legend()
    plt.title(title)
    plt.show()

    data["Kf_m"].plot()
    data["Kf_h"].plot()
    plt.legend()
    plt.title(title)
    plt.show()

    data["Kdr_n"].plot()
    plt.legend()
    plt.title(title)
    plt.show()

    data["h_nf"].plot()
    data["h_ns"].plot()
    plt.legend()
    plt.title(title)
    plt.show()                
        
        
        
        