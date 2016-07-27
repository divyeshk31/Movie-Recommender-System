

def isPresent(data,M):
	for i in M:
		if(i[0] == data):
			return True
	return False

def traverse(x,M,res):
	if(x == None):
		return None
	if(isPresent(x.data,M)):
		res.append(x.data)
		
	for y in x.children:
		traverse(y,M,res)

rating = 5

def MatchedChildren(tu,M):
	"""
	represent the child nodes of tu that are in the 
	maximum conceptual similarity tree mapping M
	"""
	res = []
	for x in tu.children:
		traverse(x,M,res)
	return res

def pr(tu,M):
	mc = MatchedChildren(tu,M)

	if(tu.preference == None and len(mc) == 0):
		return 0
	elif(len(mc) == 0):
		temp = 0
		for i in range(0,rating):
			temp += ( (i+1)*tu.preference[i][0] )
		return temp
	elif(tu.preference == None):
		temp = 0
		for i in mc:
			node = tu.lookup(i)
			temp += ( (node.wt * pr(node,M)) )
		return temp
	else:
		""" beta is influence factor of node tu """
		beta = tu.wt
		temp = 0
		for i in range(0,rating):
			temp += ( (i+1)*tu.preference[i][0] )
		for i in mc:
			node = tu.lookup(i)
			temp+= ( (1-beta)*(node.wt)*pr(node,M) )
		return temp
