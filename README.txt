GENERAL COMMENTS

The core script used in the APACHE analysis is "FOURIER_TRANSFORM6.1", which was adjusted for running the Permutation and FT Entropy scripts. A previous version of this script (5.3) has been uploaded as well for maintaining the continuity of development of this script through time, since sometimes we had to implement small changes in the script to solve some technical coding issues.  

Ulterior scripts were created to provide statistical analyses of the results and are contained in "Errors and Statistics script" folder.

The "Random test" and "test on white entropy" folders contain fabricated data used to test the accuracy of the APACHE analysis at the case limit of total noisy signal. They were run with the earliest version of the FOURIER_TRANSFORM script, but the results are equivalent with any versions.

The folder "FT output to be run in MATLAB for visualization" contains the ultimate files that are necessary to have a visual representation of the Power Spectral curves, which we ran in MATLAB. A MATLAB script file was uploaded as an example (plot_FFT6_Col_rop11.m). Importantly, the output files can be run on other platforms (i.e. Python) provided that they possess appropriate libraries and visualization commands.

The folder "resampling script" contains a script that must be used wherever the X, Y scaling of a confocal picture do not correspond to the one of the chosen standard/control picture. In this case, the rop11 mutants were pictured with a X,Y scaling of 0.415 um, while the Col-0 WT had a scaling of 0.104 um. Therefore, all of the genotypes compared to Col-0 and rop11 mutants have been resampled to have a homogeneous population of X,Y scaling 0.104 um.

The folder "raw data from the images" contains the *.txt files saved from ImageJ after having performed the measurements on the images (see the methods appendix to the paper). These files are the ones used as input in various scripts.

The results we obtained when we performed the permutation and the FT entropy analyses are reported in the folder "Output of entropy calculations" and saved as *.xlsx files readable and modifiable with Microsoft Excel or similar software. At the end of each output file there is a table named "Entropy Statistics of experiment cohort",  with 4 columns of numbers that represent the final output to be used in a statistics software to make the comparisons (sample,entropy peaks, permutation entropy, lag variance for permutationn entropy,normalized entropy of FT spectrum). 

Importantly, when we plotted this data for the statistical analysis, we normalized the permutation to make sure that the ultimate entropy value is in a range 0-100.

COMMENTS FOR RUNNING THE SCRIPTS

Ech script is provided with a series of lines where INPUT parameters need to be adjusted according to the data one is using.
There are comments in the script code where it is indicated what needs to be modified to properly run the script with your own data.
 
Typically one needs to decide what is the name of the new file (nameout), how many samples (files) should be run (start, end) in which kappa (we set it at 0.1) to obtain the best degree of smoothing of the spectrum. The input files should be a .txt files with the same name, and different index in order to be correctly processed by the script. For example, we had the ImageJ output file "Values" when we saved the intensity profile measurements. Per each protoxylem file we analyzed, we saved the file as "Values1", "Values2", "Values 3" etc. In the script, we wrote the code:  namein= "Values" start=1 end=24 because we analyzed 24 samples in this case. Pay attention on the note: the namein= attribute is without the file extension and the number!

Importantly, the raw data (for example "Values1.txt")needs to be formatted with only 2 columns tab separated, without any letter, only numbers. Typically ImageJ provides the files already in this format, but sometimes it saves the columns name in the first line of the .txt document, and it must be removed.

When the rsampling script is used before any other script, the input name needs to be readjusted (for example, namein= "Values_re" means that we are reading the "Values1.txt" file that has been resampled by the script, and now it is "Values_re1.txt". Eventually, everything needs to be renamed accordingly.

In the case of the FFT_Entropy3.1 script, the input is NOT the raw data but rather the fourier transform elaborated version, typically called "fftValues", therefore in the script (namein="fftValues").

