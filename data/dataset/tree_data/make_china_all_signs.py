

import os
from os import listdir, getcwd

class tree:
	def __init__(self):
		self.wd=getcwd()
		self.out_tree_file=open(os.path.join(self.wd,"china_signs.tree"),'w')
		self.out_label_dic_file=open(os.path.join(self.wd,"china_signs.nodes"),'w')
		self.start_id=-1
		self.exclude="GTSDB"
		self.check_match=".png"
		self.visited={}	
	def dfs(self,path,parent):
		lists=os.listdir(path)
		go=[]#[dir,parent]
		for ll in lists:
			if os.path.isfile(os.path.join(path,ll)):
				#ll=ll.split('.')
				if ll[:len(self.exclude)]!=self.exclude  and ll[-len(self.check_match):]==self.check_match : #ph2.png ph2.5.png
					ll=ll[:-len(self.check_match)]
					if(ll not in self.visited.keys()):
					    self.visited[ll]=1
					    self.start_id+=1
					    self.out_label_dic_file.write(ll+' '+str(self.start_id)+'\n')
					    self.out_tree_file.write(ll+' '+str(parent)+"\n")
					else:
					   print("warning already visit node:",ll)
					
			elif os.path.isdir(os.path.join(path,ll)):
				if(ll not in self.visited.keys()):
				    self.visited[ll]=1
				    self.start_id+=1
				    self.out_label_dic_file.write(ll + ' ' + str(self.start_id) + '\n')
				    self.out_tree_file.write(ll + ' ' + str(parent) + "\n")
				    go.append([ll,self.start_id])
				else:
				    print("warning already visit node:",ll)
		for g in go:
			self.dfs(os.path.join(path,g[0]),g[1])
			
	def mk_tree(self,path):
		self.dfs(path,-1)
		self.out_tree_file.close()
		self.out_label_dic_file.close()
		
rst=tree()
rst.mk_tree(os.path.join(getcwd(),"all_signs"))


