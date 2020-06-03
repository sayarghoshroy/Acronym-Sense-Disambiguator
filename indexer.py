import gc
import string
import sys
from nltk import PorterStemmer
import time
import xml.etree.cElementTree as ET
import re

stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

ps = PorterStemmer()
stem_cache = {}
def stem_word(word):
    global stem_cache
    if word not in stem_cache:
        if len(word) > 50:
            return 'zyx'
        else:
            stem_cache[word] = ps.stem(word)
    return stem_cache[word]

def stopword(x):
    global stopwords
    if x in stopwords:
        return True
    else:
        return False

def parse_body(body):
    words = re.findall("[A-Z]{2,}(?![a-z])|[\w]+", str(body.text))
    wordlist = {}
    for word in words:
        word = word.lower()
        if not stopword(word):
            wordfinal = stem_word(word)
            if wordfinal not in wordlist.keys():
                wordlist[wordfinal] = 1
            else:
                wordlist[wordfinal] += 1
    return wordlist



def cleaner():
    global store_dict
    global doc_id_map
    for alphabet in store_dict:
        for alpha in store_dict[alphabet]:
            wo = open(outputfile+'/'+str(alphabet)+'_'+str(alpha), 'a')
            tostore = store_dict[alphabet][alpha]
            strfinal = ''
            for word in tostore:
                strfinal += word + '.'
                for term in tostore[word]:
                    strfinal += term + '.'
                strfinal += '\n'
            wo.write(strfinal)
            wo.close()
    wo = open(outputfile+'/doc_id_map', 'a')
    strf = ''
    for docidtemp in doc_id_map.keys():
        strf += str(docidtemp) + ':' + str(doc_id_map[docidtemp]) + '\n'
    wo.write(strf)
    store_dict = None
    doc_id_map = None
    gc.collect()
    store_dict = {}
    for i in range(27):
        store_dict[i] = {}
        for j in range(27):
            store_dict[i][j] = {}
    doc_id_map = {}

store_count = 0
store_dict = {}
def store(words, doc_id):
    global store_dict
    global store_count
    alphabet = range(0,26)
    store_count += 1
    for word in words:
        if len(word) < 2:
            continue
        diff = ord(word[0]) - 97 
        if diff not in alphabet:
            diff = 26
        diff2 = ord(word[1]) - 97
        if diff2 not in alphabet:
            diff2 = 26
        storval = str(doc_id) + '_' + str(words[word])
        if word not in store_dict[diff][diff2].keys():
            store_dict[diff][diff2][word] = [storval]
        else:
            store_dict[diff][diff2][word].append(storval)

    if store_count > 6000:
        cleaner()
        store_count = 0


            

numt = 0
doc_id_map = {}
def extract_elem_buffer(buf):
    global doc_id_map
    global doc_id_count
    page = ET.fromstring(buf)
    redirect = page.find('redirect')
    if redirect != None:  
        if redirect.attrib['title'] != None:
            return 
    doc_title = (page.find('title')).text
    doc_id_map[doc_id_count] = doc_title 
    revision = page.find('revision')
    body = revision.find('text')
    words = parse_body(body)
    store(words, doc_id_count)
    doc_id_count += 1
    return



num = 0
def read_file(path):
    def readchunk():
        while True:
            data = f.read(100000)
            if data:
                yield data
            else:
                break
    inputbuffer = ''
    carry = ''
    f = open(path, 'r', 1 << 15, encoding='utf-8')
    for piece in readchunk():
        assert piece
        global num
        piece = carry + piece
        carry = ''
        num += 1
        if num % 1000 == 0:
            print(num)
        if num < startpoint:
            started = True
            continue
        if num > endpoint:
            return 
        while piece != '': 
            start = re.search("<page>", piece)
            end = re.search("</page>", piece)
            if start != None and end != None:
                if end.start() < start.start():
                        print("whoops")
                        piece = piece[start.start():]
                else:
                    inputbuffer = piece[start.start():end.end()]
                    extract_elem_buffer(inputbuffer)
                    piece = piece[end.end():]
            elif start != None and end == None:
                carry = piece[start.start():]
                piece = ''
            elif start == None and end == None:
                carry = piece
                piece = ''
            else:
                piece = ''


if __name__ == "__main__":
    t1 = time.time()
    # USEFUL WITH BASH SCRIPTING
    f = open('docnum', 'r')
    k = f.read()
    if k[len(k) - 1] == '\n':
        k = k[:len(k) - 1]
    doc_id_count = int(k)
    f.close()
    # END
    path_to_dump = sys.argv[1]
    outputfile = sys.argv[2]
    startpoint = int(sys.argv[3])
    endpoint = int(sys.argv[4])
    cleaner()
    read_file(path_to_dump)
    cleaner()

    f = open('docnum', 'w')
    f.write(str(doc_id_count))
    f.close()

    print(time.time() - t1)
