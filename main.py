__author__ = 'William Grant Lohsen'
__purpose__ = 'Some kinda science stuff for the wife'
__version__ = '1.0.0'
__license__ = 'Permission is hereby granted, free of charge, to any person obtaining a copy of this software and ' \
              'associated documentation files (the "Software"), thanking Sarah Lohsen PhD for asking her husband ' \
              'to automate this task, to deal in the Software without restriction, including without limitation ' \
              'the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the ' \
              'Software, and to permit persons to whom the Software is furnished to do so, subject to the following ' \
              'conditions: The above copyright notice and this permission notice shall be included in all copies or ' \
              'substantial portions of the Software.'

import subprocess
import os
from joblib import Parallel, delayed
import time

def parseFile(file):
    lines = file.split('\n')
    return lines


def load(filename):
    fp = open(filename)
    file = fp.read()
    return file

def writeResults(my_list):
    with open('results.txt', 'w') as f:
        for item in my_list:
            f.write("%s\n" % item)
    f.close()
    return

def searchSequence(target, input):
    #let the people know whats up
    print ('./sra-search ' + target + ' ' + input)
    #run search for target sequence
    try:
        test = subprocess.check_output(["./sra-search",target,input])
    except subprocess.CalledProcessError as e:
        if e.returncode ==3:
            #this happens if the target sequence is not found.
            input = ''
            pass
    #if target sequence is found, the source sequence name is returned, otherwise it is not
    return input

def main():
    #load list of sequences to search
    to_be_searched_file = load('SRR_Acc_List.txt')
    to_be_searched_file.strip()
    sequences_to_search = parseFile(to_be_searched_file)
    #load target sequence list
    target_sequences_file = load('SRR_Trgt_List.txt')
    target_sequences_file.strip()
    target_sequences = parseFile(target_sequences_file)

    count = 1
    start_time = time.time()
    #this is slow, so lets run 100 in parallel (to run more or less, change n_jobs). be aware the sra_search is a hdd space hog. running 100 normally uses about 6-10gb of disk space
    print('searching ' + str(len(target_sequences)) + ' target sequences')
    for target in target_sequences:
        results = Parallel(n_jobs=100,prefer='threads')(delayed(searchSequence)(target, i) for i in sequences_to_search)
        sequences_to_search = [x for x in results if x]
        print('target sequences ' + str(count) + ' of ' + str(len(target_sequences)) + ' complete, ' + str(len(sequences_to_search)) + ' sequences matched target and will be searched/returned in the next round')
        count = count + 1
    print("--- Search took %s seconds ---" % (time.time() - start_time))
    print('Search sequences that matched all target sequences are stored in results.txt')
    writeResults(sequences_to_search)



if __name__== "__main__":
  main()


