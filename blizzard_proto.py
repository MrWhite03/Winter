import os
import math

SRC = 'Z:'
DEST = 's3://container/unimatrix03'
SRC_STRIP_VAL = 18
DEST_STRIP_VAL = 18
JOBS_PER_SNOWBALL = 15
MAX_COPY_SIZE_PER_SNOWBALL = 1073741824 #* 1024 * 75 #1GB for testing ##Size is in bytes 
MAX_COPY_SIZE_PER_JOB = MAX_COPY_SIZE_PER_SNOWBALL/JOBS_PER_SNOWBALL

copy_size_job = 0
copy_size_snowball = 0
script_num = 1

f = open('snowball_' + str(math.ceil(script_num/JOBS_PER_SNOWBALL)) + '_job_' + str((script_num%JOBS_PER_SNOWBALL) + 1) + '.sh','w+')
f.write('#/bin/bash\n\n')

def get_all_filenames(path):
	global SRC, DEST, SRC_STRIP_VAL, DEST_STRIP_VAL, JOBS_PER_SNOWBALL, MAX_COPY_SIZE_PER_SNOWBALL, f, copy_size_job, copy_size_snowball, script_num

	#Recursively go through all files in current directory and all subdirectories
	for rel_filename in os.listdir(path):
		if rel_filename.startswith('.'):
			continue
		file_path = path + '/' + rel_filename


		#Check if 'file_path' is a file, and if so add it to the list
		if os.path.isfile(file_path):
			try:			
				file_size = os.path.getsize(file_path)
			except OSError:
				#If os.path.getsize returns OSError due to corrupt or file not found or dir
				#  Do not add file to script and continue with next file
				print('Error getting filesize for: ' + file_path)
				continue;

			#Check to see if 'copy_size_job' has reached 'MAX_COPY_SIZE_PER_SNOWBALL'
			#If so, close current POWERSHELL SCRIPT and create the next one
			if copy_size_job + file_size >= MAX_COPY_SIZE_PER_JOB:
				print('\'' + os.path.basename(f.name) + '\' successfully generated with a total copy size of: ' + str(copy_size_job))
				script_num += 1
				f.close()
				f = open('snowball_' + str(math.ceil(script_num/JOBS_PER_SNOWBALL)) + '_job_' + str((script_num%JOBS_PER_SNOWBALL) + 1) + '.sh','w+')
				f.write('#/bin/bash\n\n')
				copy_size_job = 0

				if script_num%JOBS_PER_SNOWBALL == 1:
					print("===========================================================")
					if copy_size_snowball > MAX_COPY_SIZE_PER_SNOWBALL:
						print('WARNING: Copy size greater than snowball capacity!!!')
					print('Total size for snowball_' + str(math.floor(script_num/JOBS_PER_SNOWBALL)) + ': ' + str(copy_size_snowball) + '\n')
					copy_size_snowball = 0

			# Add the filename to the script and add 'file_size' to 'copy_size_job'
			f.write('snowball cp \'' + SRC + file_path[SRC_STRIP_VAL:] + '\' \'' + DEST + file_path[DEST_STRIP_VAL:] + '\'\n')
			copy_size_job += file_size
			copy_size_snowball += file_size

		#Check if 'file_path' is a directory and if so, get all the filenames from that directory
		elif os.path.isdir(file_path):
			get_all_filenames(file_path)  #go go recursion

get_all_filenames(os.getcwd())

#Print info for last file and close open file handle
print('\'' + os.path.basename(f.name) + '\' successfully generated with a total copy size of: ' + str(copy_size_job))
print("===========================================================")
if copy_size_snowball > MAX_COPY_SIZE_PER_SNOWBALL:
	print('WARNING: Copy size greater than snowball capacity!!!')
print('Total size for snowball_' + str(math.floor(script_num/JOBS_PER_SNOWBALL)) + ': ' + str(copy_size_snowball) + '\n')
	
f.close()