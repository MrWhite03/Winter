import os
import shutil

try:
	os.mkdir('original_scripts')
except FileExistsError:
	print ('Directory already exists!  Please move or delete existing directory.\nExiting...')
	exit(0)

for filename in os.listdir(os.getcwd()):
	if os.path.isfile(filename) and not (filename.endswith('.py')):
		f_in = open(filename, 'r')
		
		shutil.copyfile(filename, 'original_scripts/' + filename)
		shutil.move(filename, filename + '~')

		f_out = open(filename, 'w+')

		for l in f_in:
			lal = l.split(' ')

			for i in lal:
				index = lal.index(i)

				if index == (len(lal)-1):
					lal[index] = lal[index].replace('(', '\(')
					lal[index] = lal[index].replace(')', '\)')

			for l in lal:
				f_out.write(l)
				if lal.index(l) != (len(lal)-1):
					f_out.write(' ')

		os.remove(filename + '~')
		f_out.close()
		f_in.close()