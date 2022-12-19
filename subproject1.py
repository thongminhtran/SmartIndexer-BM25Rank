import json
import time
import os
import sys

from project2.helpers import SegmentingDocuments, ReadingSmg
from project2.subproject1 import NaiveIndexer
from output_helper import DisplayingPairsWithDocsID


def ProcessFiles(index, MAXIMUM_PAIRS):
    '''
    Changing some parts in Project 2 followed by the posting list
    processing files before displaying docsID and pairs
    :param index:
    :param MAXIMUM_PAIRS:
    :return:
    '''
    files_sgm = ['reuters21578/' + file_name for file_name in
                 os.listdir('reuters21578')]  # generate list of reuters path for processing
    fileStream = ReadingSmg(files_sgm)
    initialized_pairs = 0  # Using this to check the number of pairs that will be output

    for file_num, file in fileStream:  # Using this loop to track the docsID and token pairs
        docStream = SegmentingDocuments(file)
        for doc_id, token in DisplayingPairsWithDocsID(docStream):

            if token not in index:  # If it's not in the index => add docsID and token pairs into the index
                index[token] = []

            if doc_id not in index[token]:
                index[token].append(doc_id)
            initialized_pairs += 1

            if initialized_pairs == MAXIMUM_PAIRS:
                print(str(MAXIMUM_PAIRS) + ' that has been processed')
                return


def SinglePassInMemoryIndexing(max_pairs):
    index = dict()
    ProcessFiles(index, max_pairs)
    return index


if __name__ == '__main__':
    MAXIMUM_PAIRS = 10000
    spimi_time0 = time.time()
    SPIMI_index = SinglePassInMemoryIndexing(MAXIMUM_PAIRS)
    spimi_time1 = time.time()
    indexing_time0 = time.time()
    current_indexing = NaiveIndexer(MAXIMUM_PAIRS)
    indexing_time1 = time.time()
    results = ""
    message = 'There are totally ' + str(len(SPIMI_index.keys())) + ' tokens in the SPIMI indexing'
    print(message)
    results += message
    print('\n')
    results += '\n'
    message = 'SPIMI indexing takes totally ' + str(spimi_time1 - spimi_time0)
    print(message)
    results += message
    results += '\n'
    message = 'Naive indexing takes totally ' + str(indexing_time1 - indexing_time0)
    print(message)
    results += message
    results += '\n'
    message = 'SPIMI time process is ' + str(
        (indexing_time1 - indexing_time0) / (spimi_time1 - spimi_time0)) + ' times faster than the naive indexer'
    print(message)
    results += message
    f = open('Results/subproject1.txt', 'w')
    f.write(results)
    f.close()
    json.dump(SPIMI_index, open('indexes/index_10000.json', "w", encoding="utf−8"), indent=3)
    sys.exit(0)
