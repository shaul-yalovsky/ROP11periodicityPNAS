The core script used in the APACHE analysis is "FOURIER_TRANSFORM6.1", which was adjusted for running the Permutation and FT Entropy scripts. A previous version of this script (5.3) has been uploaded as well to maintaining the continuity of development through time, since we had to implement small changes in the script to solve some technical coding issues.  

Ulterior scripts were created to provide statistical analyses of the results and are contained in "Errors and Statistics script" folder.

The "Random test" and "test on white entropy" folders contain fabricated data used to test the accuracy of the APACHE analysis at the case limit of total noisy signal.

The folder "FT output to be run in MATLAB for visualization" contains the ultimate files that are necessary to have a visual representation of the Power Spectral curves, which we ran in MATLAB. A MATLAB script file was uploaded as an example. Importantly, the output files can be run on other platforms (i.e. Python) provided that they possess appropriate libraries and visualization commands.

The folder "resampling script" contains a script that must be used wherever the X, Y scaling of a confocal picture do not correspond to the one of the chosen standard/control picture. In this case, the rop11 mutants were pictured with a X,Y scaling of 0.415 um, while the Col-0 WT had a scaling of 0.104 um. Therefore, all of the genotypes compared to Col-0 and rop11 mutants have been resampled to have a homogeneous population of X,Y scaling 0.104 um.

The folder "raw data from the images" contains the *.txt files saved from ImageJ after having performed the measurements on the images. These files are the ones used as input in various scripts.

The results we obtained when we performed the permutation and the FT entropy analyses are reported in the folder "Output of entropy calculations" and saved as *.xlsx files readable and modifiable with Microsoft Excel or similar software. 


   

