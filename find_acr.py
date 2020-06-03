import string

def get_all_acronyms():
	fp = open("result.txt")
	data = fp.read()

	words = data.split()

	count = 0

	for word in words:
		if word[-1] == '.' or word[-1] == ',':
			new_word = word[0:len(word)-1]
			words[count] = new_word
		count = count + 1

	words = list(set(words))
	#List of content words for Evaluation

	acronym_list = []

	for word in words:
		if word.isupper():
			acronym_list.append(word)

	return acronym_list

