__author__  = 'William Grant Lohsen'
__App_Name__    = 'SRA Search Automator'
__purpose__ = 'Some kinda science shit for the wifey'
__version__ = '1.0.1'
__license__ = 'Permission is hereby granted, free of charge, to any person obtaining a copy of this software and ' \
              'associated documentation files (the "Software"), thanking Sarah Lohsen PhD for asking her husband ' \
              'to automate this task, to deal in the Software without restriction, including without limitation ' \
              'the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the ' \
              'Software, and to permit persons to whom the Software is furnished to do so, subject to the following ' \
              'conditions: The above copyright notice and this permission notice shall be included in all copies or ' \
              'substantial portions of the Software.'

#HISTORY
# VERSION | DATE         | AUTHOR | Notes
#___________________________________________________________________________________________________________________
# 1.0.1   | 10/08/2021   | WGL    | Put better error handeling from sra-search results.
#___________________________________________________________________________________________________________________




import subprocess
import os
from joblib import Parallel, delayed
import time
from tqdm import tqdm

def parseFile(file):
    #split by newline
    lines = file.split('\n')
    #remove empty lines
    lines = list(filter(('').__ne__, lines))
    return lines


def load(filename):
    fp = open(filename)
    file = fp.read()
    return file

def writeResultsSimple(my_list, target):
    with open('results_'+target+'.txt', 'w') as f:
        for item in my_list:
            f.write("%s\n" % item)
    f.close()
    return

#def writeResultsComplex(dataTuple):
#    with open('results.txt', 'w') as f:
#    for item in my_list:
#        f.write("%s\n" % item)
#    f.close()
#    return

def searchSequence(target, input):
    #let the people know whats up

    #run search for target sequence
    try:
        #print ('./sra-search ' + target + ' ' + input)
        test = subprocess.check_output(["./sra-search",target,input])

    except subprocess.CalledProcessError as e:
        if e.returncode ==3:
            #this happens if the target sequence is not found.
            input = ''

        else:
            print('error---->')
            print ('./sra-search ' + target + ' ' + input)
            print('<--------error')
            if e.returncode ==6:
                input = ''
                print('caught error code 6---->')
                print ('./sra-search ' + target + ' ' + input)
                print('<--------caught error code 6')


    #if //target sequence is found, the source sequence name is returned, otherwise it is not
    return input

def main():
    #load list of sequences to search
    print (__App_Name__)
    print ('Version: ' + __version__)
    to_be_searched_file = load('SRR_Acc_List.txt')
    to_be_searched_file.strip()
    sequences_to_search = parseFile(to_be_searched_file)
    #load target sequence list
    target_sequences_file = load('SRR_Trgt_List.txt')
    target_sequences_file.strip()
    target_sequences = parseFile(target_sequences_file)

    count = 1
    start_time = time.time()
    #this shit is slow, so lets run 100 in parallel (to run more or less, change n_jobs). be aware the sra_search is a hdd space hog. running 100 normally uses about 6-10gb of disk space
    print('searching ' + str(len(target_sequences)) + ' target sequences')
    #searchSequence('TTATTTCCACATACAGGACATGTT', 'SRR2072219')
    for target in target_sequences:
        results = Parallel(n_jobs=10,prefer='threads')(delayed(searchSequence)(target, i) for i in tqdm(sequences_to_search))
        sequences_to_search = [x for x in results if x]
        print('target sequences ' + str(count) + ' of ' + str(len(target_sequences)) + ' complete, ' + str(len(sequences_to_search)) + ' sequences matched target and will be searched/returned in the next round')
        count = count + 1
    print("--- Search took %s seconds ---" % (time.time() - start_time))
    print('Search sequences that matched all target sequences are stored in results.txt')
    writeResultsSimple(sequences_to_search, target)



if __name__== "__main__":
  main()


