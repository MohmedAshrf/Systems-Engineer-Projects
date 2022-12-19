import os 			#to excute commands on OS
import re 			#using regular expressions to find numbers

def find_Instance(in_line):
	out= in_line.split(':') 		#i.e casi02-oss5:JBOD_5_6_SLOT_42 will be splitted at the ':'
	split = out[1].strip() 			#remove all unwanted spaces
	prefixes = ['JBOD','casi','raidz','mirror'] 
	if(any(split.startswith(x) for x in prefixes)):
		return str(out[1].strip())

def find_nums(in_line):
	return (re.findall('[0-9]+', in_line))

def convert_int(in_list):
	return map(int,in_list) 									 #convert all to integers

os.system('rm -f out.txt')
cmd = 'psh casi01-mds1-casi02-oss6 "zpool status" > out.txt'	 # find all errors from zpool
os.system(cmd)													 #excute the command

Result=[]
with open("out.txt") as f:
	for line in f:
		Instance_line = find_Instance(line)						 #find our targets to check
		if (Instance_line != None):
			numbers = convert_int(find_nums(Instance_line))
			if(sum(numbers[-3:])>0): 							 # if errors were found
				Result.append(line)								 # add to the whole results list

if (len(Result)>0):
	print("Found the following Errors:\n")
	print("find full output in out.txt:\n")
	print("\n".join(Result))
else:
	print("Every thing seems to run sucessfully")
	os.system('rm -f out.txt')
