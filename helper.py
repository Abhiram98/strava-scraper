import subprocess

done = False
while(done == False):

	f = open('.gitignore')
	txt = f.read().splitlines()

	# try:
	if len(txt) > 1015:
		rem = txt[:15] + txt[1015:]
	else:
		done = True
		rem = txt[:15]
	# except:
	# 	done = True
	# 	rem = txt[:15]

	f.close()

	f2 = open('.gitignore', 'w')
	print("Writing to .gitignore", 1000, len(txt))
	for i in rem[:-1]:
		f2.write(i)
		f2.write('\n')
	f2.write(rem[-1])
	f2.close()

	process = subprocess.run(['git', 'add', '.'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	print("Git add done")
	process = subprocess.run(['git', 'commit', '-m', "Adding raw files to repo"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	print("Git commit done")
