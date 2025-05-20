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
nameout= "Values_re"        #name output file for gap statistics
namein= "Values"                        # "Log" #sys.argv[2]       #name inputfiles without iterator
start = 1                               # int(sys.argv[3]) #start index ->1
end = 10                                # int(sys.argv[4])+1 #end index ->13 !!!! 27 !!!!
delim = '\t'                            # delimited used to separate colums
ending = ".txt"                         # file endings
dx= 0.1                                # constant sampling size (microns)
wind=1.2                                # width of sampling window (microns) NOTE: largest step so far is 0.4 thus, at least 4 points are used for averaging here
################################################################################################
end +=1 #needed to iterate through all files

# find sampling width kappa for which the kernel has decreased within half the window size to 0.01
kappa= (wind**2.)/(8.0*math.log(10.0))
#set sampling width for new data
Wx=int(wind/dx) 
    
# EXTRACT ALL DATA VALUES FROM RANGE OF PROBES #
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

    Nx=int((probes[len(probes)-1][0]-probes[0][0])/dx)
    X=[]
    Y=[]
    for k in range(Nx):
        X.append(float(k)*dx)
    for k in range(Nx):
        S1=0.0
        S2=0.0
        for m in range(len(probes)):
            S1 += probes[m][1]*Smoothing_Kernel(X[k],probes[m][0],kappa)
            S2 += Smoothing_Kernel(X[k],probes[m][0],kappa)
        S1 /= S2
        Y.append(S1)

    # output new data
    fout=open(nameout+str(i)+ending,'w')
    for k in range(Nx):
        fout.write(str(X[k]) + "\t" + str(Y[k]) + "\n")
    fout.close()
    

        
    


