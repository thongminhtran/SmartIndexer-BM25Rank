# The list of stop words json file can be found at: https://gist.github.com/sebleier/554280

import json
from nltk.stem import PorterStemmer
import sys
from tabulate import tabulate
ps = PorterStemmer()
initialized_index = json.load(open('indexes/index.json', 'r'))


def SizeOfDictionary(index):
    return len(index.keys())

def SizeOfToken(index):
    '''
       Return the size of token
       :param index:
       :return:
       '''
    return sum([len(lst) for freq, lst in index.values()])


def CaseFolding(index):
    for term in list(index):
        term_lower = term.lower()
        if term_lower == term:
            continue
        count, lst = index[term]
        if term_lower not in index:
            index[term_lower] = index[term]
        elif term_lower in index:
            lower_freq, lower_lst = index[term_lower]
            intersect_list = IntersectionOfTwoLists(lower_lst, lst)
            index[term_lower] = [len(intersect_list), intersect_list]
        del index[term]
    return index


def IntersectionOfTwoLists(lst1, lst2):
    '''
    Return the intersection of two list
    :param lst1:
    :param lst2:
    :return: the sorted intersection of two lists
    '''
    return sorted(list(set(lst1 + lst2)))

def ProcessingCompression(index, technique, init_dict_size, init_tokens_size):
    dictionary_size = SizeOfDictionary(index)
    token_size = SizeOfToken(index)
    index = technique(index)
    new_dictionary_size = SizeOfDictionary(index)
    new_tokens_size = SizeOfToken(index)
    delta_dict = (1 - (new_dictionary_size / dictionary_size)) * 100 * -1
    delta_tokens = (1 - (new_tokens_size / token_size)) * 100 * -1
    final_change_dict = (1 - (new_dictionary_size / init_dict_size)) * 100 * -1
    final_change_tokens = (1 - (new_tokens_size / init_tokens_size)) * 100 * -1

    results = [new_dictionary_size, delta_dict, final_change_dict,
                new_tokens_size, delta_tokens, final_change_tokens
                ]
    return index, results

def DeletingNumbers(index):
    return {k: v for k, v in index.items() if not k.isnumeric()}


def RemovingStopWords(stop_words):

    def remove_stop_words(index):
        return {k: v for k, v in index.items() if k not in stop_words}

    return remove_stop_words

stop_words_30 = json.load(open('Stop_Words/stop_words_30.json', 'r'))
remove_stop_words_30 = RemovingStopWords(stop_words_30)
stop_words_150 = json.load(open('Stop_Words/stop_words_150.json', 'r'))
remove_stop_words_150 = RemovingStopWords(stop_words_30)


def ComparingIndexes(index, compressed_index, queries, f):
    for query in queries:
        result_index = []
        compressed_result = []
        compressed_query = ps.stem(query.lower())
        if query not in index:
            print(f'query {query} not found in original index', file=f)
            print('\n', file=f)
        else:
            count, result_index = index[query]
            print('original index', file=f)
            print(f'query {query}', file=f)
            print(f'found in {count} docs: {result_index}', file=f)
            print('\n', file=f)

        if compressed_query not in compressed_index:
            print(f'query {query} not found in compressed index', file=f)
            print('\n', file=f)

        else:
            count, compressed_result = compressed_index[compressed_query]
            print('compressed index', file=f)
            print(f'query {query}', file=f)
            print(f'found in {count} docs: {compressed_result}', file=f)
            print('\n', file=f)

        if set(result_index) == set(compressed_result):
            print('Results are equal', file=f)
            print(result_index, file=f)
            print('\n', file=f)

        else:
            index_difference = set(result_index).difference(compressed_result)
            compressed_difference = set(compressed_result).difference(result_index)

            if len(index_difference) != 0:
                print(f'query {query}:', file=f)
                print('not found in compressed', file=f)
                print(f'docs: {index_difference}', file=f)
                print('\n', file=f)

            if len(compressed_difference) != 0:
                print(f'query {query}:', file=f)
                print('not found in original', file=f)
                print(f'docs: {compressed_difference}', file=f)
                print('\n', file=f)



def Stemming(index):
    for TERM in list(index):
        stemmed_term = ps.stem(TERM)
        count, lst = index[TERM]
        if stemmed_term == TERM:
            continue
        if stemmed_term not in index:
            index[stemmed_term] = index[TERM]
        elif stemmed_term in index:
            stem_freq, stem_lst = index[stemmed_term]
            intersected_list = IntersectionOfTwoLists(stem_lst, lst)
            index[stemmed_term] = [len(intersected_list), intersected_list]
        del index[TERM]

    return index



def RunningTheCompression():
    '''
      Generating the compression_table.txt file
      :return:
      '''
    technique_list = [
        ('remove_numbers', DeletingNumbers),
        ('case_fold', CaseFolding),
        ('remove_stop_words_30', remove_stop_words_30),
        ('remove_stop_words_150', remove_stop_words_150),
        ('stem', Stemming)
        ]
    initialized_size_dictionary = SizeOfDictionary(initialized_index)
    initialized_size_tokens = SizeOfToken(initialized_index)
    initialized_line = ['unfiltered',
                initialized_size_dictionary, '', '',
                initialized_size_tokens, '', '']

    final_output = [initialized_line]

    index = initialized_index

    for name, TECHNIQUE in technique_list:

        print('The compression will be processed with : ' + name)
        index, results = ProcessingCompression(index, TECHNIQUE, initialized_size_dictionary, initialized_size_tokens)
        final_output.append([name] + results)


    headers = ['number', 'Δ%', 'T%']
    table_headers = [' '] + headers + headers

    generated_table = tabulate(final_output, headers=headers, tablefmt='orgtbl')
    distance = '                         '
    header_term = '--------------------------------------------terms-------------------------------------------------------------'
    major_header = distance + header_term

    with open('Results/compression.txt', 'w', encoding="utf-8") as f:
        print(major_header, file=f)
        print(generated_table, file=f)

    with open('indexes/index_comparison.json', 'w',encoding="utf-8") as f:
        print(index, file=f)


    return index



    
def main():
    compressed_index = RunningTheCompression()
    index = initialized_index
    f = open('Results/comp_indexes.txt', 'w')
    queries = json.load(open('Queries_List/queries_to_validate.json', 'r'))
    ComparingIndexes(index, compressed_index, queries, f)
    queries = json.load(open('Queries_List/challenge_queries.json', 'r'))
    ComparingIndexes(index, compressed_index, queries, f)
    f.close()



if __name__ == '__main__':
    main()
    sys.exit(0)