# python3
import re
import requests
import urllib
from xml.etree import ElementTree as ET

def get_all_expansions(acronym):
	acronym = acronym.replace('.','')
	acronym = acronym.replace(',','')
	request_URL = 'http://acronyms.silmaril.ie/cgi-bin/xaa?' + acronym
	r = requests.get(request_URL)
	root = ET.fromstring(r.content)

	possible_expansions = []

	for child in root.iter('acro'):
		possible_expansions.append(str(child[0].text))
		#print(child[0].text)

	return_list = []
	
	for elem in possible_expansions:
		remove_brackets = re.sub(r" ?\([^)]+\)", "", elem)
		remove_brackets = remove_brackets.strip()
		if remove_brackets == 'None':
			continue
		return_list.append(remove_brackets)

	return return_list

	# print(possible_expansions)

# got_list = get_all_expansions('nato')