from Item_Tree import Item_Tree





pairs = {}#item_obj.dictionary
genre_num = []
for i,line1 in enumerate(open('ml-100k/u.genre', 'r')):
    fields = line1.split('|')
    genre_num.append(fields[0])
    for j,line2 in enumerate(open('ml-100k/u.genre', 'r')):
        fields2 = line2.split('|')
        pairs[(fields[0],fields2[0])] = float(0)
        pairs[(fields2[0],fields[0])] = float(0)


genre_array = [0] * 19
for i,line1 in enumerate(open('ml-100k/u.item2', 'r')):
    fields = line1.split('|')
    for k in range(5,24):
        if(fields[k] == "1"):
            #print("TRUE")
            genre_array[k-5] = 1
    for a in range (0,len(genre_array)):
        for b in range (0,len(genre_array)):                
            if(genre_array[a] == 1 and genre_array[b] == 1):
                pairs[(genre_num[a],genre_num[b])] += float(0.05)
                pairs[(genre_num[b],genre_num[a])] += float(0.05)
        
        
    for l in range (0,len(genre_array)):
        genre_array[l] = 0
                
for i,line1 in enumerate(open('ml-100k/u.genre', 'r')):
    fields = line1.split('|')
    pairs[(fields[0],fields[0])] = 1            


#print(genre_num)

genre_max = []

for i in genre_num:
	max1 = max2 = max3 = -1
	pos1 = pos2 = pos3 = 0

	for j in genre_num:
		if(pairs[(i,j)] > max1):
			pos1 = j
			max1 = pairs[(i,j)]
		elif(pairs[(i,j)] > max2):
			pos2 = j
			max2 = pairs[(i,j)]
		elif(pairs[(i,j)] > max3):
			pos3 = j
			max3 = pairs[(i,j)]
	genre_max.append([pos1,pos2,pos3])



print(genre_max)
