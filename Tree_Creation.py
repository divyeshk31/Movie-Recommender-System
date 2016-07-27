#Getting the mapping from Tree_Matching_Algorithm

from Tree_Matching_Algorithm import Tree
rating = 5
def create_fuzzy_tree():
    T1 = Tree("Requests",1)
    T1.parent = T1
    
    T1.children.append(Tree("Wine",2,T1))
    T1.children.append(Tree("Beer",3,T1))
    T1.children[0].children.append(Tree("Mitchelton",4,T1.children[0]))
    T1.children[0].children.append(Tree("Petaluma",5,T1.children[0]))
    
    """
    T2 = Tree("Wine",1)
    T2.children.append(Tree("Rouge",2,T2))
    T2.children.append(Tree("Petaluma",3,T2))
    T2.children.append(Tree("Mitchelton",4,T2))
    """
    
    T3 = Tree("Products",1)
    T3.parent = T3
    T3.children.append(Tree("Wine",2,T3))
    T3.children.append(Tree("Cider",3,T3))
    T3.children[0].children.append(Tree("Rouge",4,T3.children[0]))
    T3.children[0].children.append(Tree("Petaluma",5,T3.children[0]))
    T3.children[1].children.append(Tree("Rtds",6,T3.children[1]))
    
    
    M = []        
    SCt(T1,T3,M)
    #print(M)
    #Import done. We have the matching in M
    
    rating = 5   #Max rating 1-5
    
    T1.levelorder()
    
def CopyTree(node):
    return node
    
def Insert(node,T):
    node.children.append(T)
   
def SetLeafValues(T,Pui):
    if(len(T.children) == 0):
        T.preference = Pui
        return 
    for x in T.children:
        SetLeafValues(x, Pui)

def GetMappedNode(Tu,Ni,Map):
    for i in Map:
        if(Ni.data == i[1]):
            return Tu.lookup(i[0])
    
  
def Parent(Ni):
    return Ni.parent



def SearchMappedDescendent(Ni,Mui):
    l = Ni.levelorder()
    
    for i in range(1,len(l)):
        for j in Mui:
            if(j[1] == l[i]):
                return Ni.lookup(j[1])
    

def Remove(Ni,Nt):
    l = Ni.levelorder()
    #print("Level Order list ",l)
    #print("Nt.data in Remove ",Nt.data)
    for i in range(1,len(l)):
        #print("Iterator in list ",l[i])
        if(l[i] == Nt.data):
            temp_node = Ni.lookup(l[i])
            #print("temp_node ",temp_node)
            if(len(temp_node.children) != 0):
                temp_node.children = []
            return
  

def Merge_Tree(Tu,Ni,Pui,Mui):
    if(len(Mui) == 0):
        r = Tree("Preference",0)
        
        Insert(r,Tu)
        
        
        Tni = CopyTree(Ni)
        
        SetLeafValues(Tni,Pui)
        
        Insert(r,Tni)
        
        Tu = r
        
    else:
        
        Np = GetMappedNode(Tu,Ni,Mui)
        #print("Merge 1st else ", Np)
        if(Np != None):
            if(Np.data != Ni.data):
                Tni = CopyTree(Ni)
                
                SetLeafValues(Tni, Pui)
                
                Insert(Parent(Np), Tni)
            else:
                if(len(Ni.children) == 0):
                    for i in range(0,rating):
                        #print(Np.preference[i][0])
                        Np.preference[i][0] =  (float)(Np.preference[i][0])*(float)(Np.count) + (float)(Pui[i][0])
                        Np.preference[i][0] /= (float)(Np.count+1)
                        Np.count += 1
                
                else:
                    for i in Ni.children:
                        Merge_Tree(Tu, i, Pui, Mui)
        else:
            Np = GetMappedNode(Tu,Parent(Ni), Mui)
            if(Np != None):
                Tni = CopyTree(Ni)
                SetLeafValues(Tni, Pui)
                Insert(Np, Tni)
            else:
                Nt = SearchMappedDescendent(Ni,Mui)
                #print("Nt.data ",Nt.data)
                Np = Parent(Nt)
                Remove(Ni,Nt)
                Tni = CopyTree(Ni)
                Insert(Np, Tu)
                Tu = Tni
                Merge_Tree(Tu, Nt, Pui, Mui)
"""          
for x in T3.children:
    Merge_Tree(T1, x, x.preference, M)

T1.data = "Preferences"
print("Mapping :", M)
print()
"""

             