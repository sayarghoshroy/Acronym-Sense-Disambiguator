import __future__
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.porter import *

def calc_score(A, B):
	# stemmer = SnowballStemmer("english")
	stemmer = PorterStemmer()
	stemmed_A = []
	stemmed_B = []

	for word in A:
		stemmed = stemmer.stem(word)
		stemmed_A.append(stemmed)

	for word in B:
		stemmed = stemmer.stem(word)
		stemmed_B.append(stemmed)

	A_set = set(stemmed_A)
	B_set = set(stemmed_B)

	return len(A_set.intersection(B_set))