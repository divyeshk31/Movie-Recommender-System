from Tree_Matching_Algorithm import Tree, SCT
from Tree_Creation import Merge_Tree
from Item_Tree import Item_Tree
from Rating_Prediction import pr
import Tree_Matching_Algorithm 
import csv
import sys

#Calling create_item_tree func here to get the item tree here also
item_obj = Item_Tree()

item_obj.make_dictionary()
print('Dictionary Generated')
Item_Tree = item_obj.create_item_tree()
print("Item Tree Created")

def get_fuzzy_rating(rating):
	pref = [[0,1],[0,1],[0,3],[0,4],[0,5]]
	for i in range(0,5):
		if(str(i+1) == rating):
			pref[i][0] = 1
	return pref

def create_user_tree(id):
	#Create user tree for a user with id = id. Accept id as string.
	T1 = Tree("Movies",1)
	T1.parent = T1
	#Append children (genres)
	for i,line in enumerate(open('ml-100k/u.genre', 'r')):
		fields = line.split('|')
		T1.children.append(Tree(fields[0],i+2,T1))

	for line in open('testing-data/user692-testing-set','r'):
		fields = line.split('\t')
		if(fields[0] == id):
			item_id = fields[1]
			rating = fields[2]
			for line2 in open('ml-100k/u.item','r'):
				fields2 = line2.split('|')
				if(fields2[0] == item_id):
					#Append the item item_id to the user tree under a genre.
					#To know what genre to put it in user_tree, see under what genre was
					#it in item_tree
					genre = Item_Tree.lookup(fields2[1]).parent.data
					genre_in_user_tree = T1.lookup(genre)
					pref = get_fuzzy_rating(rating)
					genre_in_user_tree.children.append(Tree(fields2[1],7,genre_in_user_tree,pref))

	#T1.display(0)
	return T1



User_Tree = create_user_tree("692")
print("User Tree Created")
User_Tree.display(0)

"""
reader = csv.reader(open('output.csv', 'r'))
obj = SCT()
for row in reader:
   k, v = row
   obj.sc[k] = v
"""


#Set prefenreces for genres in User_Tree

for n in range(0,19):
	i = User_Tree.children[n]
	pref = [[0,1],[0,2],[0,3],[0,4],[0,5]]
	val = 0.0
	for j in i.children:
		for k in range(0,5):
			val = val + (float)((k+1)*j.preference[k][0])
	if(len(i.children) != 0 and val > 0):
		val = val/(float)(len(i.children))
	val = int(val)-1
	pref[val][0] = 1
	Item_Tree.children[n].preference = pref
print('\n')

print("Preferences for genres set")

M=[]
obj = SCT()
obj.sc = item_obj.dictionary
genre_list = item_obj.genre_list
item_list = item_obj.item_list
for i in range(0,len(Item_Tree.children)):
	print("Genre scanned: "+genre_list[i])
	M_dash = []
	obj.SCt(User_Tree.children[i], Item_Tree.children[i], M_dash)
	M = M + M_dash
	#print(M_dash)

M = M + ['Movies','Movies']
print(M)
print()
for x in Item_Tree.children:
	Merge_Tree(User_Tree,x,x.preference,M)

print("Tree Merged\n")

#User_Tree.display(0)	

diff = 0.0
total = 0.0
intersection = 0
preferred = 0
recommended = 0
#Print Table:
print('Movie'),
for i in range(0,55):
	print(''),
print('Predicted Rating'),
for i in range(0,15):
	print(''),
print('Actual Rating')
for line in open('testing-data/user692-training-set','r'):
	fields = line.split('\t')
	print(item_list[int(fields[1])]),
	for i in range(len(item_list[int(fields[1])]),60):
		print(''),
	r = str(int(pr(User_Tree.lookup(item_list[int(fields[1])]),M)))
	print(r),
	for i in range(0,32):
		print(''),
	print(str(fields[2]))
	diff = diff + abs( int(r)-int(fields[2]) )
	total += 1
	if(int(r) >= 3):
		recommended += 1
	if(int(fields[2]) >= 3):
		preferred += 1
	if(int(r)>= 3 and int(fields[2])>=3):
		intersection += 1

recall = float(intersection)/float(preferred)
precision = float(intersection)/float(recommended)
f1 = float(2*recall*precision)/float(recall+precision)

print('\nMAE = '+str( float(diff)/float(total) ))
print('Recall = '+str( recall ))
print('Precision = '+str( precision ))
print('F1 = '+str( f1 ))