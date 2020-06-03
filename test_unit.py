import string

full_forms = {'IBM' : 'International Business Machines',
				'ACM' : 'Association for Computing Machinery'}



def make_result(file_name):
	global full_forms
	for map in full_forms:
		print(map)
		print(str(map + '(' + full_forms[map] + ')'))
		data = data.replace(map, str(map + '(' + full_forms[map] + ')'))

	print(data)

	with open("final.txt", "w") as done_file:
	    done_file.write(data)

make_result('1.txt')