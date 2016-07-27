
w2 = open('user226','w')
array = [0] * 945
for line in open('../ml-100k/u.data','r'):
	fields = line.split('\t')
	array[int(fields[0])] += 1
	if(fields[0] == "226"):
		w2.write(line)


		
