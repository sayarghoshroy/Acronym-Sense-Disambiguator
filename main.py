import string
import find_acr
import get_expansion
import only_lex
import search
import get_score

full_forms = {}

docmap = {}

def load_doc_map():
    global docmap
    index_path = 'index'
    with open(index_path+'/'+'doc_id_map', 'r') as inputfile:
        for line in inputfile:
            if len(line) > 2:
                docid = line.split(':')[0]
                reststart = len(docid)
                content = line[reststart+1:]
                docmap[docid] = content


def disambiguate(acronym):
	global full_forms
	possible = get_expansion.get_all_expansions(acronym)
	print(possible)

	max_score = -1
	most_likely = ':('

	for case in possible:
		lex_case = search.get_list(case.lower(), docmap)
		#print(lex_case)
		score = get_score.calc_score(lex_doc, lex_case)
		if score > max_score:
			max_score = score
			most_likely = case

		print(case)
		print(score)

	print('The chosen one')
	print(most_likely)
	print(max_score)
	if max_score != -1:
		full_forms[acronym.upper()] = most_likely


def make_result(file_name):
	global full_forms
	fp = open((file_name))
	data = str(fp.read())
	for map in full_forms:
		data = data.replace(map, str(map + '(' + full_forms[map] + ')'))

	#print(data)
	with open("final.txt", "w") as done_file:
	    done_file.write(data)


print("Enter File Name")
file_name = str(input())

load_doc_map()

lex_doc = only_lex.make_lexical(file_name)

acro_list = find_acr.get_all_acronyms()

print(acro_list)

for acronym in acro_list:
	disambiguate(acronym)

make_result(file_name)