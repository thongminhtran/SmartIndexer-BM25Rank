import nltk
from nltk.stem import PorterStemmer
from nltk import word_tokenize


nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
import re  # import regular expression
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
# intialize porter stemmer
ps = PorterStemmer()

def SegmentingDocuments(sgm_file):
    # Here, sgm files (string) is a content of sgm file
    doc_regex = r"<REUTERS.*?>.*?</REUTERS>"
    docRegexID = r'NEWID="(.*?)"'
    bodyRegex = r"<BODY>(.*?)</BODY>"
    documents = re.findall(doc_regex, sgm_file, flags=re.DOTALL)
    docNoContent = 0
    for doc in documents:
        doc_id = re.findall(docRegexID, doc, flags=re.DOTALL)[0]
        try:
            doc_text = re.findall(bodyRegex, doc, flags=re.DOTALL)[0]
            doc_text = ExtractSymbolsFromHTML(doc_text)
            doc_text = ExtractPunctuationThatHaveDigits(doc_text)
            yield doc_id, [token for token in doc_text.split(" ")]
            # here we yield docID as id of the latest doc from the file
            # docContent (string) will be the content of latest document
        except:
            docNoContent += 1
    
    print(str(docNoContent) + ' documents with no content')

def ExtractSymbolsFromHTML(document_str):
    html_symbol_regex = r'(&.+;)'
    document_str = re.sub(html_symbol_regex, " ", document_str)
    return document_str


def ExtractPunctuation(document_str):
    # Source: https://stackoverflow.com/questions/10805125/how-to-remove-all-line-breaks-from-a-string
    document_str = re.sub(r"\n", " ", document_str)  # replace linebreak with spacebar
    document_str = re.sub(r"/", " ", document_str)  # remove "/" character from those text
    document_str = re.sub(r'[^A-Za-z ]+', '', document_str)  # remove non-alphabet letters
    return document_str


def ExtractPunctuationThatHaveDigits(document_str):
    '''
           This eliminates non-alphanumeric letters, then replace all linebreak with the spacebar
           Replace '/' letter
           Replace non-alphanumeric letter
          :param document_str:
          :return:
          '''
    document_str = re.sub(r"\n", " ", document_str)  # replace linebreak with spacebar
    document_str = re.sub(r"/", " ", document_str)  # replace "/" letter
    document_str = re.sub(r'[^A-Za-z0-9 ]+', '', document_str)  # replace non-alphanumeric letters
    return document_str


def TokenizingDocsString(doc_id, document_str):
    '''
    Tokenizing document by using nltk, with its id token
    :param doc_id:
    :param document_str:
    :return:

    '''
    return [(doc_id, token) for token in word_tokenize(document_str)]

def CaseFoldTokens(token_tuples):
    '''

    :param token_tuples:
    :return:
    '''
    return [(doc_id, token.lower()) for doc_id, token in token_tuples]


def StemmingTokens(token_tuples):
    '''

       :param token_tuples:
       :return:
       '''
    return [(doc_id, ps.stem(token)) for doc_id, token in token_tuples]


def FilterTextByStopWords(token_tuples, stop_words):

    return [(doc_id, token) for doc_id, token in token_tuples if token not in stop_words]
# Explanation: This will keep the document id by the tuple token
# Take parameter as: list of typles, each of them will have id documents and token
# Return => a list of tuples, with id document and token for each of them

def ReadingSmg(file_paths):
    '''
        Using this function to read all sgm files.
        :param file_paths: list of file paths from Reuters files
        :yield:
        file_num (string): from 0 -21 number of files
        '''
    for file_path in file_paths:
        if not file_path.endswith(".sgm"):
            continue
        f = open(file_path, 'r')
        file_content = f.read()
        file_name = file_path.split('.')[0]
        file_num = file_name[-2:]
        yield file_num, file_content
        f.close()