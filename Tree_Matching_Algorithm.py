from hungarian import Hungarian
from multiprocessing import Queue
class Tree():
    def __init__(self,data,index,parent = None, preference = [[0,1],[0,2],[0,3],[0,4],[0,5]]):
        self.wt = 1
        self.parent = parent
        self.data = data
        self.index = index
        self.children = []
        self.preference = preference
        self.count = 1   
        
             
    def lookup(self,word):
        if(self == None):
            return None
        if(self.data == word):
            return self
        for i in self.children:
            temp = i.lookup(word)
            if(temp != None):
                return temp
        return None
            
    def levelorder(self):
        l = []
        q = Queue.Queue()
        q.put(self)
        
        while(not q.empty()):
            n = q.get()
            l.append(n.data)
            for i in n.children:
                q.put(i)
                
        return l
    
    def display(self,ts):
        for i in range(0,ts):
            print("\t"),
        print(self.data)
        for x in self.children:
            x.display(ts+1)
        if(len(self.children) == 0):
            return    
                

              
    
        




#T2.display()


import csv
sc = {}

cnt = 1

#dictionary
"""
sc = {("Wine","Wine"):1,("Mitchelton","Mitchelton"):1,
      ("Petaluma","Petaluma"):1, ("Rouge","Rouge"):1,("Beer","Beer"):1,
      ("Requests","Requests"):1,("Rouge","Mitchelton"):0.8,("Beer","Wine"):0.6,
      ("Wine","Beer"):0.6,("Mitchelton","Rouge"):0.8,("Mitchelton","Petaluma"):0.8,
      ("Petaluma","Mitchelton"):0.8,("Petaluma","Rouge"):0.1,("Rouge","Petaluma"):0.1,
      ("Rouge","Beer"):0, ("Beer","Rouge"):0,
      ("Requests","Wine"):0, ("Wine","Requests"):0,("Wine","Rouge"):0,("Wine","Petaluma"):0,("Petaluma","Wine"):0,
      ("Wine","Mitchelton"):0,("Mitchelton","Wine"):0,
      ("Beer","Petaluma"):0,("Petaluma","Beer"):0,("Beer","Mitchelton"):0,("Mitchelton","Beer"):0,
      ("Requests","Rouge"):0,("Rouge","Requests"):0,("Requests","Petaluma"):0,
      ("Petaluma","Requests"):0,("Requests","Mitchelton"):0,("Mitchelton","Requests"):0,
      ("Rouge","Wine"):0,
      ("Cider","Requests"):0,("Cider","Wine"):0,("Cider","Beer"):0.6,("Cider","Mitchelton"):0,("Cider","Petaluma"):0,
      ("Requests","Cider"):0,("Wine","Cider"):0,("Beer","Cider"):0.6,("Mitchelton","Cider"):0,("Petaluma","Cider"):0,
      ("Products","Requests"):0,("Products","Wine"):0,("Products","Beer"):0,("Products","Mitchelton"):0,("Products","Petaluma"):0,
      ("Requests","Products"):0,("Wine","Products"):0,("Beer","Products"):0,("Mitchelton","Products"):0,("Petaluma","Products"):0
      ,("Rtds","Requests"):0,("Rtds","Wine"):0,("Rtds","Beer"):0,("Rtds","Mitchelton"):0,("Rtds","Petaluma"):0,
      ("Requests","Rtds"):0,("Wine","Rtds"):0,("Beer","Rtds"):0,("Mitchelton","Rtds"):0,("Petaluma","Rtds"):0
      }"""

#dictionary end
class SCT():
    sc = {}
    alpha = 0.5
    globe = []
    cnt = 1
    def __init__(self):
        sc = {}
        alpha = 0.5
        globe = []
        cnt = 1

    def copy_list(self,M,Mi):
        for i in Mi:
            M.append(i)

    def make_sc(self):
        i = 0
        for key, val in csv.reader(open('output.csv','r')):
            self.sc[key] = val
            if(i<2):
                print(str(i)+' '+key+' '+str(val))
                print(self.sc[key])
                i += 1

    def check_sc(self):
        print("Checking:")
        for k,v in self.sc.items():
            print(k,' -> ',str(v))
            print("checked")
            break
        print(self.sc[('Tokyo Fist (1995)', 'Apt Pupil (1998)')])
        print(self.sc[('unknown','unknown')])



    def SCt(self,tj, tk, M):
        M1 = []
        M1.append([tj.data,tk.data])
        sct1 = 0
        #if(tj.data == tk.data):
            #print(tj.data)
        if(len(tj.children)==0 and len(tk.children)==0):
            sct1 = self.sc[(tj.data, tk.data)]
        elif(len(tj.children)==0):
            sct1 = self.alpha *  self.sc[(tj.data,tk.data)]
            for i in tk.children:
                sct1 += ( (1-self.alpha) * i.wt * self.SCt(tj, i, []) )
        elif(len(tk.children)==0):
            sct1 = self.alpha *  self.sc[(tj.data,tk.data)]
            for i in tj.children:
                sct1 += ( (1-self.alpha) * i.wt * self.SCt(i,tk,[]) )
        else:
            Vj = []
            for i in tj.children:
                Vj.append(i)
            Vk = []
            for i in tk.children:
                Vk.append(i)
            
            
            ew= [[0 for x in range(0,len(Vk))] for x in range(0,len(Vj))] 
            temp= [[0 for x in range(0,len(Vk))] for x in range(0,len(Vj))] 

            M2st = [[[] for x in range(0,len(Vk))] for x in range(0,len(Vj))]
            for s in range(0,len(Vj)):
                for t in range(0,len(Vk)):
                    ew[s][t]= (-1) * self.SCt(tj.children[s],tk.children[t],M2st[s][t])
                    temp[s][t] = [tj.children[s].data, tk.children[t].data]
            
            hungarian = Hungarian(ew)
            hungarian.calculate()
            
            m = hungarian.get_results()
            #print(hungarian.get_total_potential())
         
            
            for x in m:
                self.copy_list(M1,M2st[x[0]][x[1]])
            #print(M1)
            sct1 = self.alpha * self.sc[(tj.data,tk.data)]
            for x in m:
                sct1 += ( (1-self.alpha) * abs(ew[x[0]][x[1]] * (0.5)))
        
        sct2 = 0
        M2 = []
            
        for t in range(0,len(tk.children)):
            M2jt = []
            sct = tk.children[t].wt * self.SCt(tj,tk.children[t],M2jt)
            if(sct2 < sct):
                sct2 = sct
                M2 = M2jt
                
                
        sct3 = 0
        M3 = []
            
        for t in range(0,len(tj.children)):
            M2tk = []
            sct = tj.children[t].wt * self.SCt(tj.children[t],tk,M2tk)
            if(sct3 < sct):
                sct3 = sct
                M3 = M2tk
        
        maximum = -1
        if(maximum < sct1):
            maximum = sct1
            
        if(maximum < sct2):
            maximum = sct2
        
        if(maximum < sct3):
            maximum = sct3
        
        if(sct1 == maximum):
            self.copy_list(M, M1)
            return sct1
        elif(sct2 == maximum):
            self.copy_list(M, M2)
            return sct2
        
        self.copy_list(M, M3)
        return sct3    
        

T1 = Tree("Requests",1)
T1.parent = T1

T1.children.append(Tree("Wine",2,T1))
T1.children.append(Tree("Beer",3,T1))
T1.children[0].children.append(Tree("Mitchelton",4,T1.children[0]))
T1.children[0].children.append(Tree("Petaluma",5,T1.children[0]))


T2 = Tree("Wine",1)
T2.children.append(Tree("Rouge",2,T2))
T2.children.append(Tree("Petaluma",3,T2))
T2.children.append(Tree("Mitchelton",4,T2))

T3 = Tree("Products",1)
T3.parent = T3
T3.children.append(Tree("Wine",2,T3))
T3.children.append(Tree("Cider",3,T3))
T3.children[0].children.append(Tree("Rouge",4,T3.children[0]))
T3.children[0].children.append(Tree("Petaluma",5,T3.children[0]))
T3.children[1].children.append(Tree("Rtds",6,T3.children[1]))
#T1.display(0)

T4 = Tree("Wine",1)
T4.children.append(Tree("Rouge",2,T4))
T4.children.append(Tree("Petaluma",3,T4))




#T1.display(0)
#T3.display(0)

#M = []        
#SCt(T1,T3,M)
#print(M) 

    