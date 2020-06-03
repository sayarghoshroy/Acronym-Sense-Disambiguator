def format_list(dirty):
	count = 0
	word_list = []

	for elem in dirty:
		token = elem[0 : len(elem) - 2]

		words = token.split()
		for word in words:
			word_list.append(word)

	return word_list

		
