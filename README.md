# SRA_Search_Automation

Requirements:
Requires python 3.9 or higher
Targeted at ubuntu 18.04 (though the ubuntu version doesn't really matter).
only special toolkit to install requires pip3 to install (google install pip3)
sudo pip3 install joblib


Operation:
Place files in your sra-toolkit/bin folder
place list of sequences to search in "SRR_ACC_list.txt" (next line \n character is the only allowed nextline character. so file should be SEQUENCE\nSEQUENCE\n....SEQUENCE' - no \n after the last entry)
place list of target sequences to search for in "SRR_TRGT_list.txt" (next line \n character is the only allowed nextline character. so file should be SEQUENCE\nSEQUENCE\n....SEQUENCE' - no \n after the last entry)
Currently this runs 100 sequence searchs in parallel. scale to meet your needs but be aware it is more hdd space intensive than processor intensive

Results:
results are stored in - "results.txt" 


Troubleshooting: 
if something goes wrong, and it has joblib anywhere in its title, or your computer crashes, reduce n_jobs, it is the likely culprit. 
