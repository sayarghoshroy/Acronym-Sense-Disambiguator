# Removes everything else apart from lexical words from the file 'text.txt'
import __future__
import re
import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# print("Enter Path to File")
# file_name = str(raw_input())

def make_lexical(file_name):

	fp = open(str(file_name))
	data = fp.read()
	sentences=(tokenizer.tokenize(data))

	output_text = ""
	valid_POS = ['CD','FW','JJ','JJR','JJS','NN','NNS','NNP','NNPS','PDT','POS','PRP','PRP$','RB','RBR','RBS','VB','VBD','VBG','VBN','VBP','VBZ']
	be_verbs = ['be','is','was','were']

	lex_doc = []

	for sentence in sentences:
		tokenized_set = nltk.word_tokenize(sentence)
		tagged_map = nltk.pos_tag(tokenized_set)
		for elem in tagged_map:
			checker = elem[1]

			if checker in valid_POS and elem[0] not in be_verbs:
				if checker == 'POS':
					output_text = output_text + elem[0]
				else:
					output_text = output_text + " " + elem[0]
					lex_doc.append(elem[0].lower())

		output_text = output_text + tokenized_set[-1]

	output_text = output_text.strip()
	with open("result.txt", "w") as output_file:
	    output_file.write(output_text)

	return list(set(lex_doc))