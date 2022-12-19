import os
import re
from math import log10
import json
import sys
from project2.helpers import ExtractSymbolsFromHTML, ExtractPunctuationThatHaveDigits, ReadingSmg
from project2.subproject2 import QueryProcessing

def AverageDocsLength(length_docs_index):
    return sum(length_docs_index.values()) / len(length_docs_index.values())


def BM25Searching(query):
    k1, b = 1.6, 0.75
    average_documents_length = AverageDocsLength(length_docs_index)
    N = len(length_docs_index.keys())
    def IDF(term):
        numerator = N - len(index[term]) + 0.5
        denominator = len(index[term]) + 0.5
        return log10((numerator / denominator) + 1)
    grades = []
    documents = ProcessingAND(query)
    for DOC_ID in documents:
        for term in query.split(" "):
            idf = IDF(term)
            term_frequency = term_indexing[(term, DOC_ID)]
            current_length = length_docs_index[DOC_ID]
            numerator = term_frequency * (k1 + 1)
            denominator = term_frequency + (k1 * ((1 - b) + (b * current_length / average_documents_length)))
            if denominator == 0:
                grades.append((DOC_ID, idf * numerator))
            else:
                grades.append((DOC_ID, idf * (numerator / denominator)))
    final_result = sorted(grades, key=lambda x: x[1], reverse=True)
    return final_result




def ProcessingFiles(index, doc_length_index):
    '''

    :param index:
    :param doc_length_index:
    :return:
    '''

    sgm_files = ['reuters21578/' + file_name for file_name in os.listdir('reuters21578')]
    fileStream = ReadingSmg(sgm_files)
    for FILE_NUM, file in fileStream:
        doc_stream = SegmentingDocuments(file, doc_length_index)
        for DOC_ID, TOKEN in DisplayingPairsWithDocsID(doc_stream):
            if TOKEN not in index:
                index[TOKEN] = []
            index[TOKEN].append(DOC_ID)

def IndexProbabilistic():
    '''
    Creating SPIMI index and still has duplicate term in docs
    Read indexes in the storage
    :return:
    '''
    index, doc_length_index = SinglePassInMemoryDuplicates()
    print('===============Docs Length Index has been created=================')
    term_index = CreatingTermIndex(index)
    print('Term Frequency Index has been created!!!')
    DeletingDuplicatedDocuments(index)
    print('Index created.')

    json.dump(index, open('indexes/index.json', "w", encoding="utf−8"), indent=3)
    json.dump(doc_length_index, open('indexes/doc_length_index.json', "w", encoding="utf−8"), indent=3)
    term_index = {k[0] + ' ' + k[1]: v for k, v in term_index.items()}
    json.dump(term_index, open('indexes/term_freq_index.json', "w", encoding="utf−8"), indent=3)


index = json.load(open('indexes/index.json', 'r'))
length_docs_index = json.load(open('indexes/doc_length_index.json', 'r'))
term_indexing = json.load(open('indexes/term_freq_index.json', 'r'))
term_indexing = {(k.split(' ')[0], k.split(' ')[1]): v for k, v in term_indexing.items()}


def DisplayingPairsWithDocsID(doc_stream):
    '''
    Displaying all token pairs along with docsID
    :param doc_stream:
    :return:
    '''
    docs = next(doc_stream, None)
    document_count = 0
    while docs is not None:
        doc_id, doc_token_list = docs
        for token in doc_token_list:
            if token != '':
                yield doc_id, token
        document_count += 1
        docs = next(doc_stream, None)
    print(str(document_count) + ' documents that have been processed')


def SinglePassInMemoryDuplicates():
    index = dict()
    length_docs_index = dict()
    ProcessingFiles(index, length_docs_index)
    return index, length_docs_index


def SegmentingDocuments(sgm_file, doc_length_index):
    '''
    Segmenting Documents by sgm files and length docs index
    :param sgm_file:
    :param doc_length_index:
    :return:
    '''
    BODY_REGEX = r"<BODY>(.*?)</BODY>"
    DocsID_REGEX = r'NEWID="(.*?)"'
    document_regex = r"<REUTERS.*?>.*?</REUTERS>"
    documents = re.findall(document_regex, sgm_file, flags=re.DOTALL)
    empty_docs = 0
    for doc in documents:
        doc_id = re.findall(DocsID_REGEX, doc, flags=re.DOTALL)[0]
        try:
            doc_text = re.findall(BODY_REGEX, doc, flags=re.DOTALL)[0]
            doc_text = ExtractSymbolsFromHTML(doc_text)
            doc_text = ExtractPunctuationThatHaveDigits(doc_text)
            tokens = doc_text.split(" ")
            doc_length_index[doc_id] = len(tokens)
            yield doc_id, [token for token in tokens]
        except:
            empty_docs += 1

    print(str(empty_docs) + ' documents that have no content body inside')

def CreatingTermIndex(index):
    term_indexing = dict()

    for TERM, doc_list in index.items():
        term_per_docs = dict()
        for DOC_ID in doc_list:
            if DOC_ID not in term_per_docs:
                term_per_docs[DOC_ID] = 0
            term_per_docs[DOC_ID] = term_per_docs[DOC_ID] + 1

        for DOC_ID in term_per_docs:
            term_indexing[(TERM, DOC_ID)] = term_per_docs[DOC_ID]

    return term_indexing


def DeletingDuplicatedDocuments(index):
    '''

    :param index:
    :return:
    '''
    for TERM in index:
        index[TERM] = sorted(list(set(index[TERM])), key=lambda x: int(x))






def ProcessingSingleTerm(TERM):
    if TERM not in index:
        print('term not found')
    else:
        return index[TERM]


def ProcessingOR(passed_query):
    passed_query = ExtractPunctuationThatHaveDigits(passed_query)
    current_terms = passed_query.split(" ")
    results = dict()
    for term in current_terms:
        for doc_id in index[term]:
            results[doc_id] = True
    return list(results.keys())


def IntersectionOfTwoElements(first_list, second_list):
    if first_list is None:
        return second_list
    return [elem for elem in first_list if elem in second_list]


def ProcessingAND(passed_query):
    passed_query = ExtractPunctuationThatHaveDigits(passed_query)
    current_terms = passed_query.split(" ")
    current_list = None
    for term in current_terms:
        post_list = index[term]
        current_list = IntersectionOfTwoElements(current_list, post_list)
    return current_list


def RunningAllTestQueries():
    '''

    :return:
    '''
    display_message = ""
    single_word = 'person'
    text = 'The single word comparison is running for ' + str(single_word)           #PART A
    print(text)
    display_message += text
    display_message += '\n'
    text = 'Single Pass In Memory Indexing Results'
    print(text)
    display_message += text
    display_message += '\n'
    final_result = ProcessingSingleTerm(single_word)
    print(final_result)
    display_message += str(final_result)
    display_message += '\n'
    text = 'original index Results'
    print(text)
    display_message += text
    display_message += '\n'
    final_result = QueryProcessing(single_word)
    print(final_result)
    display_message += str(final_result)
    display_message += '\n'
    text = 'Test Queries using BM25 formula is running: '              # PART B
    print(text)
    display_message += text
    display_message += '\n'
    given_queries = [
        "Democrats’ welfare and healthcare reform policies",
        "Drug company bankruptcies",
        "George Bush"
    ]
    text = 'Queries_List: '
    print(text)
    display_message += text
    display_message += '\n'

    for QUERY in given_queries:
        print(QUERY)
        display_message += QUERY
        display_message += '\n'
        final_result = BM25Searching(QUERY)
        print(final_result)
        display_message += str(final_result)
        display_message += '\n'

    text = 'Unranked Boolean retrieval AND test is running: '          # PART C
    print(text)
    display_message += text
    display_message += '\n'

    given_queries = [
        "Democrats’ welfare and healthcare reform policies",
        "Drug company bankruptcies",
        "George Bush"
    ]

    text = 'Queries_List: '
    print(text)
    display_message += text
    display_message += '\n'

    for QUERY in given_queries:
        print(QUERY)
        display_message += QUERY
        display_message += '\n'

        final_result = ProcessingAND(QUERY)
        print(final_result)
        display_message += str(final_result)
        display_message += '\n'

    text = 'Unranked boolean retrieval OR test is running: '           #PART D
    print(text)
    display_message += text
    display_message += '\n'

    given_queries = [
        "Democrats’ welfare and healthcare reform policies",
        "Drug company bankruptcies",
        "George Bush"
    ]

    text = 'Queries_List: '
    print(text)
    display_message += text
    display_message += '\n'

    for QUERY in given_queries:
        print(QUERY)
        display_message += QUERY
        display_message += '\n'

        final_result = ProcessingOR(QUERY)
        print(final_result)
        display_message += str(final_result)
        display_message += '\n'

    f = open('Results/subproject2.txt', 'w')
    f.write(display_message)
    f.close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        IndexProbabilistic()
        sys.exit(0)
    arg = sys.argv[1]
    if arg == '0':
        RunningAllTestQueries()
        sys.exit(0)
    processing_queries_names = {'1': 'single_term_processor',
                              '2': 'BM25_ranked_search',
                              '3': 'AND_processor',
                              '4': 'OR_processor'
                                }
    query_processing = {'1': ProcessingSingleTerm,
                        '2': BM25Searching,
                        '3': ProcessingAND,
                        '4': ProcessingOR
                        }
    print('Displaying processed queries: ' + query_processing[arg])
    query = input('Queries INPUT:\n')
    results = query_processing[arg](query)
    print('Queries for result: ' + query)
    print(results)
    sys.exit(0)
