import os
import sys
import json

from .helpers import SegmentingDocuments, ReadingSmg

#         ============================= NAIVE INDEXER part ====================================
def NaiveIndexer(max_pairs=None):
    # initialize F list of (doc_id, term)
    F = []
    try:
        ProcessFiles(F, max_pairs)
    except:
        pass
    F = SortingWithoutDuplicates(F)
    index = GeneratingInvertedIndex(F)
    return index




def ProcessFiles(F, MAXIMUM_PAIRS):        # Processing list F
    sgm_files = ['reuters21578/' + file_name for file_name in os.listdir('reuters21578')]
    FileStream = ReadingSmg(sgm_files)        # Creating the file
    current_pairs = 0
    for file_num, file in FileStream:
        doc_stream = SegmentingDocuments(file)       # Creating doc stream
        for doc_id, token in CreatingTermDocIDPairs(doc_stream):
            F.append((doc_id, token))       # Adding DOC_ID to F list
            current_pairs += 1
            if current_pairs == MAXIMUM_PAIRS:
                print(str(MAXIMUM_PAIRS) + ' processed')
                return


def GeneratingInvertedIndex(F):
    print('===== Here is the generating step for inverted index of list F =====')
    index = dict()
    freq = 0
    for doc_id, term in F:
        if term not in index:
            freq = 0
            index[term] = [freq, []]
        freq += 1
        index[term] = [freq, index[term][1] + [doc_id]]
    print('===== The generating process of inverted index is DONE =====')
    print(f'There are totally {len(index.keys())} terms in the index!!!')
    return index


def CreatingTermDocIDPairs(DocStream):
    '''

       :param DocStream:
       :return:
       '''
    doc = next(DocStream, None)
    doc_count = 0
    while doc is not None:
        doc_id, doc_token_list = doc
        for token in doc_token_list:
            if token != '':
                yield doc_id, token
        doc_count += 1
        doc = next(DocStream, None)
    print(f'Total {doc_count} documents that have been processed')


def SortingWithoutDuplicates(F):
    '''
       This functions will remove any duplicates from F and sort F by term and docsID
       :param F:
       :return:
       '''
    print('===== Deleting any duplicates from the F list =====')
    F = list(set(F))
    print('===== Deleting duplicates in F is DONE =====')
    # Here is the sorting for F in term of term and docsID
    F = sorted(F, key=lambda t: (t[1], int(t[0])))
    print('===== Sorting F by term and DocsID DONE =====')
    return F




if __name__ == '__main__':
    index = NaiveIndexer()
    json.dump(index, open('indexes/index.json', "w", encoding="utf−8"), indent=3)
    sys.exit(0)