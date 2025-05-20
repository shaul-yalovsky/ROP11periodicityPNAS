####################################################
# FOURIER TRANSFORM AND GAUSSIAN SMOOTHING OF DATA #
# AUTHOR: Dr. Erik Gengel                          #
# THIS SCRIPT TAKES INPUT FILES AND PERFORMS:      #
# 1) SMOOTHING OVER SEVERAL ORDERED FILES 1,2,...  #
#    USING A GAUSSIAN WINDOW SMOOTHER WITH         #
#    PARAMETER kappa. kappa LARGE GIVES STRONG     #
#    SMOOTHING AND VICE VERSA.                     #
# 2) FOURIER TRANSFORM (NOT FFT) AND SMOOTHING     #
#    OF THE FT DATA AFTERWARDS                     #
# NOTE: MODES OF OPERATION ARE EITHER: FT FOR EACH #
#    DATA FILE AND SMOOTHING OVER ALL DATA COLUMNS #
#    OR FT FOR EACH DATA FILE AND SMOOTHING OVER   #
#    EACH FT DATA COLUMN.                          #
# NOTE: THE SCRIPT CAN BE ADAPTED TO USE INPUT AR- #
#    GUMENTS AS NEEDED.                            #
#                                                  #
# RAWOUTPUT: UNORDERED X, DATA   (ONE FILE)        #
# FT OUTPUT: FREQENCY, EVEN, ODD, |FT|(FREQUENCY)  #
# SMOOTHED:  AUXILIARY GRID, SMOOTHED DATA         #
#                                                  #
# THE CODE COMES WITH NO VARANTY AND CAN BE ADJUS- #
# TED FOR OWN PURPOSES.                            #
####################################################

import copy
import sys
import math
#import numpy as np

#FUNCTIONS

def Smoothing_Kernel(x,X,kappa):      #X is data position, x is auxiliary position, kappa is smoothing parameter
    return 1.0/(math.sqrt(math.pi)*kappa)*math.exp(-(X-x)*(X-x)/kappa)  #gaussian bell shaped curve normalized to unity

def SI_calc(symb,Lag,D):
    A=0.0
    for k in range(1,D):
        L=0.0
        for l in range(1+k,1+D):#one+k,one+D
            if(symb[-1+k]<symb[-1+l]):
                L += 1.0
        A += math.factorial(D-k)*L
    return A

#### comment this out: generates a test file of name dat1.dat
#debf=open("dat1.txt", "w")
#for i in range(1000):
    #debf.write(str(float(i)*0.1) + " " + str(math.sin((2.0*math.pi/10.0)*float(i)*0.1) + math.cos((2.0*math.pi/5.0)*float(i)*0.1)) + "\n")
#debf.close()
####################


################################################################################################
# INPUT PARAMETERS #
nameout= "SMOOTHED_abi1-1_ABA_kappa_0.1.txt" #sys.argv[1]      #name output file for gap statistics
namein= "Values_re" #"Log" #sys.argv[2]       #name inputfiles without iterator
start = 1 #int(sys.argv[3]) #start index ->1
end = 19 #int(sys.argv[4])+1 #end index ->13 !!!! 27 !!!!
kappa= 0.1 #float(sys.argv[5]) #smoothing parameter of Kernel function -> kappa large strong smoothing and vice versa (SPECTRAL SMOOTHING)
smoothFFT=1 #1=>FFT calculated for each file and smoothing of FFT data, 0=> FFT calculated for each file but smoothing of file data itself
delim = '\t'  # delimited used to separate colums
ending = ".txt" # file endings
normalizeINT=1  # normalizing the obtained intensity data 1: normalizing data; 0: not
KernelINT=1     # smoothing of data using a Gaussian smoothing kernel (scales as N^2)
SavitzkyINT=0   # smoothing of data using a Savitzky-Golay filter (alternative to Kernel smoothing) TODO...
Nh=500          # number of statistical bins
hmax=350.0      # range of peak statistics
D=4             # number of perumtable data points  D=2: ++ D=3: +++ D=4: ++++
Lagmax=20       # maximum lag parameter of patterns D=3, Lag=1: +++ Lag=2: + + +
kappa_p=10.0    # smoothing parameter of Kernel function -> kappa large strong smoothing and vice versa (PEAK STATISTICS SMOOTHING)
################################################################################################


end +=1 #needed to iterate through all files

# EXTRACT ALL DATA VALUES FROM RANGE OF PROBES #
stat=[]            # stores either raw data or data of the FT
peakstat=[]        # stores data of all peak distributions
entropy_peaks=[]   # stores the entropy of the peaks statistics
entropy_dat=[]     # stores the entropy of the whole data using symbols
entropy_dat_var=[] # stores the entropy of the whole data using symbols
fentropy = open("Entropy_"+nameout+ending,'w')#-> might be .dat instead of .txt
for i in range(start,end):
    probes=[]
    print ("extracting " + str(i))
    fin=open(namein+str(i)+ending,'r')#-> might be .dat instead of .txt
    for lines in fin:
        l=lines.split(delim)#-> might be space, , , ; , ., \t
        p=[]
        if len(l)>1: # actually >0 is sufficient. >1 means that really any symbols are excluded (like '\n')
            for j in range(len(l)):
                #print (l[j])
                p.append(float(l[j]))
            p.append(0.0)
            probes.append(p)
    fin.close()

############################
### STATISTICAL ANALYSIS ###
############################

    ### Peak statistics of Intensity ###
    print("calculate peak statistics")
    H=[]           # peak hights
    rho=[]         # denisty of peaks
    Hrho=[0.0,0.0] # dummy vector for statistics
    for j in range(Nh):
        H.append(float(j)*hmax/(float(Nh)))
        rho.append(0.0)
    peaks_count=0.0
    for j in range(2,len(probes)-2):
        Pat=copy.deepcopy(probes[j][1])
        if Pat>probes[j-1][1] and Pat>probes[j+1][1]:
            #print ("stat if 1")
            peaks_count +=1.0
            for k in range(len(H)):
                if probes[j][1]>H[k]-hmax/(float(Nh))*0.5 and probes[j][1]<=H[k]+hmax/(float(Nh))*0.5:
                    #rho[k] += 1.0/(float(Nh))
                    rho[k] += 1.0

    # normalize and check if integral is correct #
    check_rho=0.0
    for k in range(len(rho)):
        rho[k] /= peaks_count
        check_rho += rho[k]
    print("integral over rho= " + str(check_rho))

    ### calculate entropy of peaks ###
    print("calculate entropy of peaks")
    Se=0.0
    for k in range(len(rho)):
        if rho[k]!=0.0:
            Se -= rho[k]*math.log(rho[k]) # use previously calculated relative frequencies of peaks (rho) to obtain the entropy of the peaks
    entropy_peaks.append(Se)
    print(" entropy= " + str(Se))
    #fentropy.write("Sample entropy= " + str(Se))

    ### calculate entropy of the whole data ###
    print("calculate entropy of data")
    #fPent = open("Permutation_Entropy_dat_Lag"+nameout+ending,'w')#-> might be .dat instead of .txt
    entropy_dat_lag=[]
    for Lag in range(1,Lagmax):                    # scan different lag Parameters
        symb_dat=[]
        for k in range(0,len(probes)-(1+D)*Lag):       # go through data
            symb=[]
            for l in range(D):                     # fill symbol window
                symb.append(probes[k+l*Lag][1])
            #    print("k=" + str(k) + " l=" + str(l) + " actual lage= " + str(k+l*Lag))
            # calculate symbol index #
            symb_dat.append(SI_calc(symb,Lag,D))
            #print("found symbol is: " + str(SI_calc(symb,Lag,D)))

        # calculate the symbol entropy by counting the frequencies of numbers #
        Psymb=[]
        for k in range(math.factorial(D)):
            Psymb.append(0.0)
        print("Lag= " + str(Lag) + " number of symbols in statistics= " + str(len(Psymb)))

        # calculate the frequencies #
        print("calculate frequencies ")
        Nsymb_dat=0.0
        for k in range(len(symb_dat)):
            #print("k= " + str(k) + " len(symb_dat)= " + str(len(symb_dat)))
            for l in range(len(Psymb)):
                if(symb_dat[k]==l):#="ell" L count it
                    #print("if symb:" + str(symb_dat[k]) + " =?= " + str(l))
                    Psymb[l] += 1.0
                    Nsymb_dat += 1.0
            #print("Nsymb_dat= " + str(Nsymb_dat))

        # if Nsymb_dat still zero set to 1 #
        if Nsymb_dat==0.0:
            Nsymb_dat=1.0
        # normalize and check if integral is correct also output #
        check_rho=0.0
        for k in range(len(Psymb)):
            Psymb[k] /= Nsymb_dat
            check_rho += Psymb[k]
            fentropy.write(str(Lag) + " " + str(k) + " " + str(Psymb[k]) + "\n")
        print("integral over symbol statistics= " + str(check_rho))
        Se_p=0.0
        for k in range(len(Psymb)):
            if Psymb[k]!=0.0:
                Se_p -= Psymb[k]*math.log(Psymb[k]) # use previously calculated relative frequencies of symbols (Psymb) to obtain the entropy of the whole data
        entropy_dat_lag.append(Se_p)
        fentropy.write("Lag= " + str(Lag) + " Sample entropy= " + str(Se_p) + "\n")
        fentropy.write("\n")

    # calculate mean and variance of all lag entropies #
    Pent_mean=0.0
    Pent_var=0.0
    for k in range(len(entropy_dat_lag)):
        Pent_mean += entropy_dat_lag[k]
        Pent_var += entropy_dat_lag[k]**2.0
    Pent_mean /= float(len(entropy_dat_lag))
    Pent_var /= float(len(entropy_dat_lag))
    Pent_var -= Pent_mean**2.0
    entropy_dat.append(Pent_mean)
    entropy_dat_var.append(math.sqrt(Pent_var))


    rho2=[]
    fout3 = open("PEAK_STAT_"+str(i)+"_"+nameout,"w")
    for k in range(len(H)):
        fout3.write(str(H[k]) + " " + str(rho[k]) +"\n")
        Hrho[0]=H[k]
        Hrho[1]=rho[k]
        rho2.append(copy.deepcopy(Hrho))#copy x,y values together
    fout3.close()
    peakstat.append(rho2)#generate array for statistics of peaks


############################
### FOURIER     ANALYSIS ###
############################

    if normalizeINT==1:
        ##################### subtract baseline intensity #########
        minDat=+10000.0 # to find the minimum of data in the probe -> normalization
        for j in range(len(probes)):
            if probes[j][1]<minDat:
                minDat=probes[j][1]
                print ("minDat= " + str(minDat))
        for j in range(len(probes)):
            probes[j][1] -= minDat #subtract smallest value

        ##################### normalize data to 0,1 interval #########
        print ("normalizing intensity " + str(i))
        foutnorm = open("Norm_"+namein+str(i)+ending,"w")
        maxDat=-10000.0 # to find the maximum of data in the probe -> normalization
        for j in range(len(probes)):
            if probes[j][1]>maxDat:
                maxDat=probes[j][1]
                print ("maxDat= " + str(maxDat))
        for j in range(len(probes)):
            probes[j][1] /= maxDat #normalize

        print ("length of probes= " +str(len(probes)))

        #################### contrast adaption ###########################
        #for j in range(len(probes)):
        #    probes[j][1] = probes[j][1]**2.0

        ##################### subtract average ###########################
        ### Subtract the average of oscillation from the data to get rid of low-frequency peaks
        Mprobes=0.0
        for j in range(len(probes)):
            Mprobes += probes[j][1]
        Mprobes /= (float(len(probes)))
        for j in range(len(probes)):
            foutnorm.write(str(probes[j][0]) + " " + str(probes[j][1]) + " ")
            probes[j][1] -= Mprobes
            foutnorm.write(str(probes[j][1]) + "\n")
        foutnorm.close()

    ##################### Fourier transform ######################
    print ("start FT")
    even=[]#cosin modes
    odd=[]#sin modes
    x=[]
    y=[]
    #set data
    for j in range(len(probes)):
        x.append(probes[j][0])#domain (length of root)
        y.append(probes[j][1])#data (intensity)
    #determine length of integration (such that full periods of sin and cos are summed up only)
    #really???

    #integrate modes
    dx=x[1]-x[0]
    print("dx= " + str(dx))
    for j in range(len(probes)):
        s1=0.0#even summ
        s2=0.0#odd sum,
        #print ("integrate at frequency " + str(math.pi*(float(j)/(dx*float(len(probes))))) + "\n")
        for k in range(len(probes)):
            s1 += math.cos(math.pi*(float(j)/(float(len(probes))))*(float(k)))*y[k]
            s2 += math.sin(math.pi*(float(j)/(float(len(probes))))*(float(k)))*y[k]
        s1 /= (0.5*(float(len(x))))
        s2 /= (0.5*(float(len(x))))
        #print ("magnitude= " + str(math.sqrt(s1**2.0 + s2**2.0)))
        even.append(s1)
        odd.append(s2)
    fftout=open("fft"+namein+str(i)+ending,"w")
    for j in range(len(odd)):
        fftout.write(str(math.pi*(float(j)/(float(len(probes))*dx))) + " " + str(even[j]) + " " + str(odd[j]) + " " + str(math.sqrt(even[j]**2.0 + odd[j]**2.0)) + "\n")
    fftout.close()
    print("finished FT")
    ##################### end of Fourier transform ###############
    if(smoothFFT==1):
        print("reads FFT modes for smoothing")
        ##################### start extraction of Fourier modes for smoothing ######
        probes=[]
        print ("extracting" + str(i))
        fin=open("fft"+namein+str(i)+ending,'r')#-> might be .dat instead of .txt
        for lines in fin:
            l=lines.split(' ')#
            p=[]
            for j in range(len(l)):
                #print (l[j])
                if((j==0)or(j==3)):#index 3 is the magnitude of the FT (4th column of FT data file
                    p.append(float(l[j]))
            p.append(0.0)
            probes.append(p)
        fin.close()
    ##############################################################
    stat.append(probes)
    #off file iterator

print ("######## raw data=")
print (stat)

# FIND MINIMAL AND MAXIMAL VALUE OF GAP POSITION OVER ALL PROBES #
mi=10000000.0
ma=0.0
for i in range(len(stat)):
    print ("search for " + str(stat[i]) + "\n")
    #if stat[i][0][2]<mi:
    if stat[i][0][0]<mi:
        mi = copy.deepcopy(stat[i][0][0])
    #if stat[i][len(stat[i])-1][2]>ma:
    if stat[i][len(stat[i])-1][0]>ma:
        ma = copy.deepcopy(stat[i][len(stat[i])-1][0])

print ("minimal gap position= " + str(mi) + " maxima position= " + str(ma) + "\n")

# SET AUXILIARY DOMAIN #
NL=0
for i in range(len(stat)):
    print ("length of probe " + str(i) + " = " + str(len(stat[i])) + "\n")
    NL +=len(stat[i])
NL = int(float(NL)*2.0/(float(len(stat))))

print ("number of auxiliary points= " + str(NL) + "\n")

dL=(ma-mi)/float(NL)
print ("auxiliary discretiation= " + str(dL) + "\n")

X=[]
for i in range(NL+1):           #set domain with as many points as data values, equally spaced
    X.append(mi + float(i)*dL)

print ("######## auxiliary domain=")
print (X)

# SMOOTHING OF OBTAINED GAP WIDTH/FFT #
Y=[]   #np.zeros(len(X))
Var=[] #point wise variances of smoothed point ---> for statistical significance of the smoothed points
Aves=[] # pointwise averages of single samples

if KernelINT==1:
    print("KERNEL")
    for k in range(len(X)):
        print ("axilliary X= " + str(X[k]) + "\n")
        sy=0.0
        var=0.0
        N=0.0
        avep=[]
        for i in range(len(stat)):
           # print ("probe no " + str(i) + "\n")
            avepsamp = 0.0
            Navepsamp = 0.0
            for j in range(len(stat[i])):
                sy += stat[i][j][1]*Smoothing_Kernel(stat[i][j][0],X[k],kappa)   # calculate mean over all probes in a sliding window
                avepsamp += stat[i][j][1]*Smoothing_Kernel(stat[i][j][0],X[k],kappa) # calculate mean over all probes in a sliding window
                #print("kernel value= " +str(Smoothing_Kernel(stat[i][j][0],X[k],kappa))+"\n") # calculate mean over all probes in a sliding window
                var += stat[i][j][1]*stat[i][j][1]*Smoothing_Kernel(stat[i][j][0],X[k],kappa) # calculate second moment of smoothed points
                N += Smoothing_Kernel(stat[i][j][0],X[k],kappa)     # calculate mean over all probes in a sliding window
                Navepsamp += Smoothing_Kernel(stat[i][j][0],X[k],kappa) # calculate mean over all probes in a sliding window
            if Navepsamp==0.0:
                Navepsamp +=1.0
            avep.append(avepsamp/Navepsamp)# store separate averages of all probes at one point
        Aves.append(copy.deepcopy(avep))   # stores the list of all averages at one point
        #Y[k] = sy/N
        Y.append(sy/N)
        Var.append(math.sqrt(var/N-(sy/N)**2.))

print ("len X= " + str(len(X)) + " len Y= " + str(len(Y)) + "\n")

if SavitzkyINT==1:
    print("SAVITZKY-GOLAY")
    #TODO: include numpy and implement fitting


maxDat2=-10000.0 # to find the maximum of data in the probe -> normalization
if normalizeINT==1:
    ##################### normalize data to 0,1 interval #########
    print ("normalizing FFT")
    for j in range(len(Y)):
        if Y[j]>maxDat2 and X[j]>0.8:
            maxDat2=copy.deepcopy(Y[j])
            print ("maxDat FFT= " + str(maxDat2))

print ("######## calculate variance of single averages=> ")
Var_aves=[]
for k in range(len(Aves)):
    avesum=0.0
    avevar=0.0
    for m in range(len(Aves[0])):
        avesum += Aves[k][m]
        avevar += Aves[k][m]**2.
    Var_aves.append(copy.deepcopy(avevar/(float(len(Aves[0]))) - (avesum/(float(len(Aves[0]))))**2.))


print ("######## output smoothed=> ")
# OUTPUT VALUES SMOOTHED #
fout = open(nameout,"w")
for i in range(len(X)):
    fout.write(str(X[i]) + " " + str(Y[i]) + " " + str(Y[i]/maxDat2) + " " + str(math.sqrt(Var[i]/maxDat2)) + " " + str(math.sqrt(Var_aves[i]/maxDat2)) + "\n")
fout.close()

print ("######## output raw=> ")
# OUTPUT VALUES RAW #
fout2 = open("RAW"+nameout,"w")
for i in range(len(stat)):
    for j in range(len(stat[i])):
        fout2.write(str(stat[i][j][0]) + " " + str(stat[i][j][1]) + " " + str(stat[i][j][1]/maxDat2) +  "\n")
fout2.close()

# SET DOMAIN FOR PEAK SMOOTHING #

X=[]
for j in range(len(peakstat[0])):
    X.append(copy.deepcopy(peakstat[0][j][0]))

# KERNEL SMOOTHING OF OBTAINED PEAK STATISTICS #
print("KERNEL PEAKS")
Y=[]   #np.zeros(len(X))
Var=[] #point wise variances of smoothed point ---> for statistical significance of the smoothed points
kappa=10.0
for k in range(len(X)):
    print ("auxilliary X= " + str(X[k]) + "\n")
    sy=0.0
    var=0.0
    N=0.0
    for i in range(len(peakstat)):
       # print ("probe no " + str(i) + "\n")
        for j in range(len(peakstat[i])):
            sy += peakstat[i][j][1]*Smoothing_Kernel(peakstat[i][j][0],X[k],kappa_p) # calculate mean over all probes in a sliding window
            #print("kernel value= " +str(Smoothing_Kernel(stat[i][j][0],X[k],kappa))+"\n") # calculate mean over all probes in a sliding window
            var += peakstat[i][j][1]*peakstat[i][j][1]*Smoothing_Kernel(peakstat[i][j][0],X[k],kappa_p) # calculate second moment of smoothed points
            N += Smoothing_Kernel(peakstat[i][j][0],X[k],kappa_p) # calculate mean over all probes in a sliding window
    #Y[k] = sy/N
    Y.append(sy/N)
    Var.append(math.sqrt(var/N-(sy/N)**2.))

print ("PEAK SMOOTHING: len X= " + str(len(X)) + " len Y= " + str(len(Y)) + "\n")

print ("######## output smoothed=> ")
# OUTPUT VALUES SMOOTHED #
fout = open("PEAK_STAT_SMOOTH_"+nameout,"w")
for i in range(len(X)):
    fout.write(str(X[i]) + " " + str(Y[i]) + " " + str(Var[i]) + "\n")
fout.close()

### variance of averages to average of variances of averages ###
print ("######## calculate variance of single averages=> ")
Var_aves=[]
for k in range(len(Aves)):
    avesum=0.0
    avevar=0.0
    for m in range(len(Aves[0])):
        avesum += Aves[k][m]
        avevar += Aves[k][m]**2.
    Var_aves.append(math.sqrt(copy.deepcopy(avevar/(float(len(Aves[0]))) - (avesum/(float(len(Aves[0]))))**2.)))
print ("Var_aves = ")
print (Var_aves)
#average of standard deviations of all smoothed points for one kappa#
ave_var=0.0
for k in range(len(Var_aves)):
    ave_var += Var_aves[k]




### CALCULATE AVERAGE ENTROPY, VARIANCE, OUTPUT THEM ###
print("output entropies of data + standart deviations over different probes")
Mentr1=0.0   #peaks
Varentr1=0.0
Mentr2=0.0   #whole data (permutation entropy)
Varentr2=0.0

fentropy.write("single peak entropies \n")
for k in range(len(entropy_peaks)):
    Mentr1 += entropy_peaks[k]
    Varentr1 += entropy_peaks[k]**2.0
    Mentr2 += entropy_dat[k]
    Varentr2 += entropy_dat[k]**2.0
    fentropy.write(str(k) + " entropy peaks " + str(entropy_peaks[k]) + " permutation entropy " + str(entropy_dat[k])  + " Lag variance for permutation entropy " + str(entropy_dat_var[k]) + "\n")
Mentr1 /= (float(len(entropy_peaks)))
Varentr1 /= (float(len(entropy_peaks)))
Varentr1 -= Mentr1**2.0
Mentr2 /= (float(len(entropy_dat)))
Varentr2 /= (float(len(entropy_dat)))
Varentr2 -= Mentr2**2.0
fentropy.write("####################################")
fentropy.write("Peak entropy: Mean= " + str(Mentr1) + " standard deviations " + str(math.sqrt(Varentr1)) + "Data entropy: Mean= " + str(Mentr2) + " standard deviations " + str(math.sqrt(Varentr2)) + " Accuracy of averaging= " + str(ave_var/(float(len(Var_aves)))) + "\n")

fentropy.close()


