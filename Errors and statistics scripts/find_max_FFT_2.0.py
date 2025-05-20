import math
import copy
import sys

def Smoothing_Kernel(x,X,kappa):      #X is data position, x is auxiliary position, kappa is smoothing parameter
    return 1.0/(math.sqrt(math.pi)*kappa)*math.exp(-(X-x)*(X-x)/kappa)  #gaussian bell shaped curve normalized to unity

#INPUT PARAMETERS 
k_i = 1 #here the first FT file index #int(sys.argv[1])
k_f = 18 #here the last FT file index #int(sys.argv[max_file_index]) 
name = "fftValues" #str(sys.argv[fftValues])#name of FT file without extension (for example .txt .dat)
kappa=10.0 #degree of the smoothing parameter #this parameter should be set for all of the measurements #use much larger value to smooth spectra significantly
#END of input. No more modifications needed to run the script

#determine all frequencies where the spectra are maximal
x_max=[]
for k in range(k_i,k_f+1):
    f= open(name+str(k)+".txt")
    print ("extracting " + name+str(k)+".txt")
    FFT_max= -10000.0
    k_max = 0.0
    X=[]
    Y=[]
    for lines in f:
        l=lines.split()
#        print(lines)
        X.append(float(l[0]))
        Y.append(float(l[3]))
#        if((float(l[0])>0.5) and (float(l[3])>FFT_max)): # put here column index that corresonds to |F|(omega) index from FT file
#            print (str(float(l[3])) + " " + str(FFT_max))
#            FFT_max=copy.deepcopy(float(l[3]))
#            k_max = copy.deepcopy(float(l[0]))
#    x_max.append(k_max)

    # SMOOTHING OF OBTAINED GAP WIDTH/FFT #
    Y2=[]   
    print("KERNEL")
    for l in range(len(X)):
        #print ("axilliary X= " + str(X[l]) + "\n")
        sy=0.0
        N=0.0
        for j in range(len(X)):
            sy += Y[j]*Smoothing_Kernel(X[j],X[l],kappa)    
            N += Smoothing_Kernel(X[j],X[l],kappa)          
        Y2.append(sy/N)

    # searching for maximum of smoothed data #    
    FFT_max= -10000.0
    k_max = 0.0
    for l in range(len(X)):
        if((X[l]>0.5) and (Y[l]>FFT_max)): # put here column index that corresonds to |F|(omega) index from FT file
            print (str(X[l]) + " " + str(FFT_max))
            FFT_max=copy.deepcopy(Y[l])
            k_max = copy.deepcopy(X[l])
    x_max.append(k_max)     
            
#calculate the mean, and variance

print ("extracted k_max are: ")
for k in range(len(x_max)):
    print (str(x_max[k]))

m1=0.0
m2=0.0
for k in range(len(x_max)):#mean
    m1 += x_max[k]
m1 /= float(len(x_max))

for k in range(len(x_max)):#variance  
    m2 += (x_max[k] - m1)**2. 
m2 /= float(len(x_max))
    
print("FT maximum is on average at k_max= " + str(m1) + " and the standard deviation is " + str(math.sqrt(m2)) + "\n")       
