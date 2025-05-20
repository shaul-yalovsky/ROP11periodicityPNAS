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

#FUNCTIONS

def Smoothing_Kernel(x,X,kappa):      #X is data position, x is auxiliary position, kappa is smoothing parameter
    return 1.0/(math.sqrt(math.pi)*kappa)*math.exp(-(X-x)*(X-x)/kappa)  #gaussian bell shaped curve normalized to unity

#### comment this out: generates a test file of name dat1.dat
#debf=open("dat1.txt", "w")
#for i in range(1000):
    #debf.write(str(float(i)*0.1) + " " + str(math.sin((2.0*math.pi/10.0)*float(i)*0.1) + math.cos((2.0*math.pi/5.0)*float(i)*0.1)) + "\n")
#debf.close()
####################


################################################################################################
# INPUT PARAMETERS #
nameout= "Error_genotype_treatment.txt" #sys.argv[1]      #name output file for gap statistics
namein= "SMOOTHED_genotype_treatment.txt" #"Log" #sys.argv[2]       #name inputfiles without iterator
delim = ' '  # delimited used to separate colums
skip_lines = 0
th=10.0 #averaging cutoff
#end of INPUT. No need to modify the script from here
################################################################################################

fin=open(namein,'r')#-> might be .dat instead of .txt
dat=[]
lines_count = 0
for lines in fin:
    l=lines.split(delim)#-> might be space, , , ; , ., \t
    p=[]
    if len(l)>0 and lines_count >= skip_lines:
        for j in range(len(l)):
            print (l[j])
            p.append(float(str(l[j])))
        dat.append(p)
    lines_count += 1
fin.close()
print(dat)

#NOTE: col=0: frequency, col=1: averaged spectra, col=2: normalized average spectrum, col=3: variance of data from averaged curve, col=4: variance of each single averaged curve from averaged curve (col=0)
#calculate mean square error of col3 with respect to col0
E0=0.0
for k in range(len(dat)):
    if dat[k][0]<th:
        E0 += dat[k][2]
E0 /= float(len(dat)-1)#(dat[len(dat)-1][0]-dat[0][0])
#E1 = math.sqrt(E1)
print ("Integral of normalized average spectrum"+str(E0))
       
E1=0.0
for k in range(len(dat)):
    if dat[k][0]<th:
        E1 += (dat[k][3])**2.
E1 /= float(len(dat)-1)
#E1 = math.sqrt(E1)
print ("Error of variance of data from averaged curve"+str(E1/E0))

E1=0.0
for k in range(len(dat)):
    if dat[k][0]<th:
        E1 += dat[k][4]
E1 /= float(len(dat)-1)
#E1 = math.sqrt(E1)
print ("Error of variance of each single averaged curve from averaged curve"+str(E1/E0))








