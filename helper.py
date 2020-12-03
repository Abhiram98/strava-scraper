import subprocess

f = with open('.gitignore')
txt = f.read().splitlines()
rem = txt[:14] + txt[1014:]

f.close()

f2 = open('.gitignore', 'w')

for i in rem[:-1]:
	f2.write(i)
	f2.write('\n')
f2.write(rem[-1])


process = subprocess.Popen(['git', 'add', '.'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
