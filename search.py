import sys
import re
import math
import time
from nltk import PorterStemmer

stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

ps = PorterStemmer()
TOTAL_DOC = 1

def scan_index(path, word):
    '''
    Returns the posting list for the word
    '''
    inputbuffer = ''
    with open(path,'r') as inputfile:
        mapping = {}
        for line in inputfile:
            i_word = line.split('.')[0]
            if word == i_word:
                doc_freq_map = line.split('.')[1:]
                for mapset in doc_freq_map:
                    if len(mapset) > 2:
                        terms = mapset.split('_')
                        mapping[terms[0]] = terms[1]
                return mapping
        return None

def rank(doclist, words, postings):
    collection = []
    scoring = {}
    for doc in doclist:
        score = 0
        for word in words:
            score += math.log(1 + int(postings[word][doc])) * math.log(TOTAL_DOC / len(postings[word]))
        scoring[doc] = score
    s = [k for k in sorted(scoring, key=scoring.get, reverse=True)]
    global doc_map
    keys = doc_map.keys()
    count = 0
    for i in range(len(s)):
        if s[i] not in keys:
            continue
        out = doc_map[s[i]]
        if re.search('Wikipedia', out) != None:
            continue
        if count > 1000:
            break
        collection.append(out)
        count += 1

    return collection


def process(postings):
    lst = {}
    words = postings.keys()
    for word in words:
        for doc in postings[word].keys():
            if doc not in lst.keys():
                lst[doc] = 1
            else:
                lst[doc] += 1
    req = len(words)
    lstfinal = []
    for elem in lst:
        if lst[elem] == req:
            lstfinal.append(elem)
    return rank(lstfinal, words, postings)

def query_func(index_path, search_string):
    global stopwords
    alphabet = range(0, 26)
    print("Ready")

    query = search_string
    
    querystart = time.time()
    query = query.lower()
    tokens = query.split(" ")
    plist = {} 
    for word in tokens:
        if word in stopwords:
            continue
        search_word = ps.stem(word)
        if len(search_word) < 2:
            continue
        t1 = ord(search_word[0]) - 97
        t2 = ord(search_word[1]) - 97
    
        if t1 not in alphabet:
            t1 = 26
        if t2 not in alphabet:
            t2 = 26
        search_path = str(t1) + '_' + str(t2)
        temp = scan_index(index_path + '/' + search_path, search_word)
        if temp:
            plist[search_word] = temp
    return process(plist)

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

doc_map = {}
        
def get_list(search_string, docmap):
    global doc_map
    doc_map = docmap
    global TOTAL_DOC
    index_path = 'index'
    
    if bool(doc_map) == False:
        load_doc_map()
        print("loaded")
    
    f = open('docnum', 'r')
    TOTAL_DOC = int(f.read())
    f.close()

    cleaned_list = format_list(query_func(index_path, search_string))
    unique_list = list(set(cleaned_list))
    #print(unique_list)
    return unique_list

def format_list(dirty):
    count = 0
    word_list = []

    for elem in dirty:
        token = elem[0 : len(elem) - 1]

        words = re.findall(r"[\w']+", elem)
        for word in words:
            word_list.append(word.lower())

    return word_list