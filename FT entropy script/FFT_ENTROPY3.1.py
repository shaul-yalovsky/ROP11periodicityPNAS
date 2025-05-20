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
nameout= "FT_Entropy_genotype_treatment.txt" # sys.argv[1]      #name output file for gap statistics
namein= "fftValues_re"                        # "Log" #sys.argv[2]       #name inputfiles without iterator
start = 1                               # int(sys.argv[3]) #start index ->1
end = 24                                # int(sys.argv[4])+1 #end index ->13 !!!! 27 !!!!
delim = ' '                            # delimited used to separate colums
ending = ".txt"                         # file endings
Nh=100                                  # number of statistical bins (peak entropy)
hmax=350.0                              # range of peak statistics
D=4                                    # number of perumtable data points  D=2: ++ D=3: +++ D=4: ++++
Lagmax=20                               # maximum lag parameter of patterns D=3, Lag=1: +++ Lag=2: + + +
colind=3                                # collumn index of file data: 1, fft data: 3
cutoff=5                                # cutoff value that is used to omit FT values at low frequencies
#END of INPUT. From now on, there is no need to change the code
################################################################################################

#kappa_p=10.0    # smoothing parameter of Kernel function -> kappa large strong smoothing and vice versa (PEAK STATISTICS SMOOTHING)
#kappa= 0.001 #float(sys.argv[5]) #smoothing parameter of Kernel function -> kappa large strong smoothing and vice versa (SPECTRAL SMOOTHING)
#smoothFFT=1 #1=>FFT calculated for each file and smoothing of FFT data, 0=> FFT calculated for each file but smoothing of file data itself
#normalizeINT=1  # normalizing the obtained intensity data 1: normalizing data; 0: not
#KernelINT=1     # smoothing of data using a Gaussian smoothing kernel (scales as N^2)
#SavitzkyINT=0   # smoothing of data using a Savitzky-Golay filter (alternative to Kernel smoothing) TODO...


end +=1 #needed to iterate through all files

# EXTRACT ALL DATA VALUES FROM RANGE OF PROBES #
stat=[]            # stores either raw data or data of the FT
peakstat=[]        # stores data of all peak distributions
entropy_peaks=[]   # stores the entropy of the peaks statistics
entropy_dat=[]     # stores the entropy of the whole data using symbols
entropy_dat_var=[] # stores the entropy variance according to lag L
entropy_ft=[]      # stores entropy of the FT spectrum
fentropy = open("Entropy_"+nameout+ending,'w')#-> might be .dat instead of .txt
for i in range(start,end):
    probes=[]
    print ("extracting " + str(i))
    fin=open(namein+str(i)+ending,'r')#-> might be .dat instead of .txt
    for lines in fin:
        l=lines.split(delim)#-> might be space, , , ; , ., \t
        p=[]
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
    for j in range(Nh): #set stat range
        H.append(float(j)*hmax/(float(Nh)))
        rho.append(0.0)
    peaks_count=0.0
    for j in range(2,len(probes)-2):
        Pat=copy.deepcopy(probes[j][colind])
        if Pat>probes[j-1][colind] and Pat>probes[j+1][colind]:
            #print ("stat if 1")
            peaks_count +=1.0
            for k in range(len(H)):#calculate peak statistical frequencies
                if probes[j][colind]>H[k]-hmax/(float(Nh))*0.5 and probes[j][colind]<=H[k]+hmax/(float(Nh))*0.5:
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
            print(Se)
    entropy_peaks.append(Se)
    print(" entropy= " + str(Se))
    #fentropy.write("Sample entropy= " + str(Se))

    ### calculate entropy of the whole data (permutation entropy) ###
    print("calculate entropy of data (permutation entropy)")
    #fPent = open("Permutation_Entropy_dat_Lag"+nameout+ending,'w')#-> might be .dat instead of .txt
    fentropy.write(namein+str(i)+ending+"\n") # list file name in entropy output file
    fentropy.write("Lag| Sample entropy \n")
    entropy_dat_lag=[]
    for Lag in range(1,Lagmax):                    # scan different lag Parameters
        symb_dat=[]
        for k in range(0,len(probes)-(1+D)*Lag):       # go through data
            symb=[]  
            for l in range(D):                     # fill symbol window
                symb.append(probes[k+l*Lag][colind])
            #    print("k=" + str(k) + " l=" + str(l) + " actual lage= " + str(k+l*Lag))
            # calculate symbol index #
            symb_dat.append(SI_calc(symb,Lag,D))#calculate symbol index
            #print("found symbol is: " + str(SI_calc(symb,Lag,D)))

        # calculate the symbol entropy by counting the frequencies of symbol index appearance #
        Psymb=[]
        for k in range(math.factorial(D)):
            Psymb.append(0.0)
        print("Lag= " + str(Lag) + " number of symbols in statistics= " + str(len(Psymb)))

        # calculate the statistical frequencies #
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
            #fentropy.write(str(Lag) + " " + str(k) + " " + str(Psymb[k]) + "\n") #write out all frequencies for one lag given one data file
        print("integral over symbol statistics= " + str(check_rho))
        Se_p=0.0
        for k in range(len(Psymb)):
            if Psymb[k]!=0.0:
                Se_p -= Psymb[k]*math.log(Psymb[k]) # use previously calculated relative frequencies of symbols (Psymb) to obtain the permutation entropy 
        entropy_dat_lag.append(Se_p) #append entropy of one lag based on all symbols for one data file
        fentropy.write(str(Lag) + " " + str(Se_p) + " " + str(Se_p/math.log(float(len(Psymb)))) + "\n")
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
    
    # ft entropy (used for fft data only)
    print("calculate FT entropy (DATA ENTROPY)")
    Nft=0.0
    for j in range(cutoff,len(probes)-2):# calculate normalization
        Nft += probes[j][colind]
    Se_p=0.0
    for j in range(cutoff,len(probes)-2):#calculate entropy
        if(probes[j][colind]>0.0):
            Se_p -= (probes[j][colind]/Nft)*math.log(probes[j][colind]/Nft)
    entropy_ft.append(Se_p/math.log(float(len(probes)-2-cutoff)))#append entropy of one ft spectrum to the vector of all ft entropies
    
#off loop through all data files


### CALCULATE AVERAGE ENTROPY, VARIANCE, OUTPUT THEM ###
print("output entropies of data + standart  deviations over different probes")
Mentr1=0.0   #peaks
Varentr1=0.0
Mentr2=0.0   #whole data (permutation entropy)
Varentr2=0.0
Mentr3=0.0   #ft data 
Varentr3=0.0

fentropy.write("Entropy statistics of experiment cohort \n")
fentropy.write("Sample| entropy peaks| permutation entropy| Lag variance for permutation entropy| normalized entropy of FT spectrum \n")
for k in range(len(entropy_peaks)):
    Mentr1 += entropy_peaks[k]
    Varentr1 += entropy_peaks[k]**2.0
    Mentr2 += entropy_dat[k]
    Varentr2 += entropy_dat[k]**2.0
    Mentr3 += entropy_ft[k]
    Varentr3 += entropy_ft[k]**2.0 
    fentropy.write(str(k) + " " + str(entropy_peaks[k]) + " " + str(entropy_dat[k])  + " " + str(entropy_dat_var[k]) + " " + str(entropy_ft[k]) + "\n")
Mentr1 /= (float(len(entropy_peaks)))
Varentr1 /= (float(len(entropy_peaks)))
Varentr1 -= Mentr1**2.0
Mentr2 /= (float(len(entropy_dat)))
Varentr2 /= (float(len(entropy_dat)))
Varentr2 -= Mentr2**2.0
Mentr3 /= (float(len(entropy_ft)))
Varentr3 /= (float(len(entropy_ft)))
Varentr3 -= Mentr3**2.0
fentropy.write("################################## \n")
fentropy.write("Peak entropy: Mean= " + str(Mentr1) + ", standard deviation= " + str(math.sqrt(Varentr1)) + "Permutation entropy: Mean= " + str(Mentr2) + ", standard deviations " + str(math.sqrt(Varentr2)) + "Fourier entropy: Mean= " + str(Mentr3) + ", standard deviation= " + str(math.sqrt(Varentr3)) + "\n")

fentropy.close()


