import csv
from Tree_Matching_Algorithm import Tree

class Item_Tree():
	item_list = []
	dictionary = {}
	count = []
	genres = []
	genre_max = []
	genre_list = []

	def __init__(self):
		self.dictionary = {}
		self.count = []
		self.genres = []
		genre_max = []
		genre_list = []
		item_list = []
		for i in range(0,20):
			self.count.append(0)

	def make_dictionary(self):
		self.dictionary[('Movies','Movies')] = 1
		for i,line1 in enumerate(open('ml-100k/u.item', 'r')):
			fields1 = line1.split('|')
			self.item_list.append(fields1[1])
			self.dictionary[('Movies',fields1[1])] = 0
			self.dictionary[(fields1[1],'Movies')] = 0
			for j,line2 in enumerate(open('ml-100k/u.item', 'r')):
				fields2 = line2.split('|')
				#print(str(i)+' '+str(j))
				if(j==i):
					self.dictionary[(fields1[1],fields1[1])] = 1
				elif(j>i):
					temp = 0.0
					for k in range(5,24):
						if(fields1[k] == "1" and fields2[k] == "1"):
							temp += (0.05263158)
					self.dictionary[(fields1[1],fields2[1])] = temp
					self.dictionary[(fields2[1],fields1[1])] = temp
					  


		for i,line1 in enumerate(open('ml-100k/u.item','r')):
			fields1 = line1.split('|')
			for j,line2 in enumerate(open('ml-100k/u.genre','r')):
				fields2 = line2.split('|')
				self.dictionary[(fields1[1],fields2[0])] = 0
				self.dictionary[(fields2[0],fields1[1])] = 0

		genre_num = []
		for i,line1 in enumerate(open('ml-100k/u.genre', 'r')):
			fields = line1.split('|')
			genre_num.append(fields[0])
			self.genre_list.append(fields[0])
			#print(genre_num[i])
			for j,line2 in enumerate(open('ml-100k/u.genre', 'r')):
				fields2 = line2.split('|')
				self.dictionary[(fields[0],fields2[0])] = float(0)
				self.dictionary[(fields2[0],fields[0])] = float(0)


		genre_array = [0] * 19
		for i,line1 in enumerate(open('ml-100k/u.item', 'r')):
			fields = line1.split('|')
			for k in range(5,24):
				if(fields[k] == "1"):
					genre_array[k-5] = 1
			for a in range (0,len(genre_array)):
				for b in range (0,len(genre_array)):                
					if(genre_array[a] == 1 and genre_array[b] == 1):
						#print(genre_num[a],genre_num[b])
						self.dictionary[(genre_num[a],genre_num[b])] += float(0.05)
						self.dictionary[(genre_num[b],genre_num[a])] += float(0.05)

			for l in range (0,len(genre_array)):
				genre_array[l] = 0

		for i,line1 in enumerate(open('ml-100k/u.genre', 'r')):
			fields = line1.split('|')
			self.dictionary[(fields[0],fields[0])] = 1
			#print(fields[0],":",self.dictionary[(fields[0],fields[0])]) 


		for i in range(0,len(genre_num)):
			max1 = 1
			pos1 = i
			max2 = max3 = -1
			pos2 = pos3 = 0
			for j in range(0,len(genre_num)):
				if(self.dictionary[(genre_num[i],genre_num[j])] > max2 and j!=pos1):
					pos2 = j
					max2 = self.dictionary[(genre_num[i],genre_num[j])]
		
			for j in range(0,len(genre_num)):
				if(self.dictionary[(genre_num[i],genre_num[j])] > max3 and j!=pos1 and j!=pos2):
					pos3 = j
					max3 = self.dictionary[(genre_num[i],genre_num[j])]
				

			

			self.genre_max.append([pos1,pos2,pos3])

			"""
			w = csv.writer(open("output.csv", "w"))
			for key, val in self.dictionary.items():
				w.writerow([key, val])
			"""


	def create_item_tree(self):
		T1 = Tree("Movies",1)
		T1.parent = T1
		
		#Append children (genres)
		for i,line in enumerate(open('ml-100k/u.genre', 'r')):
			fields = line.split('|')
			self.genres.append(fields[0])
			T1.children.append(Tree(fields[0],i+2,T1))
		
		#Append Movies to genres
		
		
		
		for i,line in enumerate(open('ml-100k/u.item', 'r')):
			fields = line.split('|')
			minimum = 1000000
			pos = -1
			flag = 0
			number = 0.5000004
			#decide where to put movie and make changes to dictionary?
			
			for k in range(5,24):
				if(fields[k] == "1"):
					number += 1.00
					if(minimum > self.count[k-5]):
						minimum = self.count[k-5]
						pos = k-5
						flag = 1
					
			if(flag == 1):
				self.count[pos] += 1
				#self.dictionary[( fields[1], self.genres[pos] )] = float(1.00)/float(number)
				#self.dictionary[( self.genres[pos], fields[1] )] = float(1.00)/float(number)
			
			T1.children[pos].children.append(Tree(fields[1],7,T1.children[pos]))

		#return the Item_Tree
		"""
		w = csv.writer(open("output.csv", "w"))
		for key, val in dictionary.items():
			w.writerow([key, val])
		"""
		
		
		for x in T1.children:
			x.wt = float(1.0)/float(len(T1.children))
			for y in x.children:
				y.wt = float(1.0)/float(len(x.children))
		
		#T1.display(0)
		return T1



