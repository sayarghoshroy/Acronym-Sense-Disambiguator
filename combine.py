import sys
import gc
from os import listdir
from os.path import isfile, join
mypath = sys.argv[1]
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
onlyfiles.remove('doc_id_map')
num = 0
for subindex in onlyfiles:
    print("Starting" + str(subindex))
    f = open(mypath+'/'+str(subindex), 'r')
    worddict = {}
    while True:
        line = f.readline()
        if not line: 
            break
        else:
            wordlimit = 0
            while line[wordlimit] != '.':
                wordlimit += 1
            word = line[:wordlimit]
            rest = line[wordlimit+1:-1]
            if word not in worddict.keys():
                worddict[word] = rest
            else:
                worddict[word] += rest
    f.close()
    f = open(mypath+'/'+str(subindex), 'w')
    strfinal = ''
    for word in worddict:
        strfinal += word + '.' + worddict[word] + '\n'
    half = int(len(strfinal) / 2)
    f.write(strfinal[:half])
    f.write(strfinal[half:])
    f.close()
    print("Done with" + str(subindex))
    worddict = None
    gc.collect()
    num += 1
    print(num)
