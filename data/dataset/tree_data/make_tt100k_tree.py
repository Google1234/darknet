

import os
from os import listdir, getcwd

class tree:
	def __init__(self):
		self.wd=getcwd()
		self.out_tree_file=open(os.path.join(self.wd,"tt100k.tree"),'w')
		self.out_label_dic_file=open(os.path.join(self.wd,"tt100k.map"),'w')
		self.start_id=-1
		self.exclude="GTSDB"
		self.check_match=".png"
		
	def dfs(self,path,parent):
		lists=os.listdir(path)
		go=[]#[dir,parent]
		for ll in lists:
			if os.path.isfile(os.path.join(path,ll)):
				#ll=ll.split('.')
				if ll[:len(self.exclude)]!=self.exclude  and ll[-len(self.check_match):]==self.check_match : #ph2.png ph2.5.png
					ll=ll[:-len(self.check_match)]
					self.start_id+=1
					self.out_label_dic_file.write(ll+' '+str(self.start_id)+'\n')
					self.out_tree_file.write(ll+' '+str(parent)+"\n")
					
			elif os.path.isdir(os.path.join(path,ll)):
				self.start_id+=1
				self.out_label_dic_file.write(ll + ' ' + str(self.start_id) + '\n')
				self.out_tree_file.write(ll + ' ' + str(parent) + "\n")
				go.append([ll,self.start_id])
		for g in go:
			self.dfs(os.path.join(path,g[0]),g[1])
			
	def mk_tree(self,path):
		self.dfs(path,-1)
		self.out_tree_file.close()
		self.out_label_dic_file.close()
		
rst=tree()
rst.mk_tree(os.path.join(getcwd(),"labels"))


