
import os
from os import listdir, getcwd
wd=getcwd()
#wd="/Users/jt/Desktop/UISEE/data/data"
wd=os.path.join(wd,"data")

map_file=os.path.join("/home/jtao/jto/code/darknet/data/dataset/tree_data","tt100k.map")

names_file=os.path.join(wd,"tt100k.names")
names=open(names_file,'r').read().split('\n')

#map_file=os.path.join(wd,"tt100k.map")
maps=open(map_file,'r').read().split('\n')
maps_dic={}
for m in maps:
	_s=m.split(' ')
	if len(_s)==2:maps_dic[_s[0]]=_s[1]
	
out_file=os.path.join(wd,"tree.map")
out=open(out_file,'w')
for na in names:
	if na in maps_dic.keys():
		out.write(na+' '+maps_dic[na]+'\n')
	else:
		print na," not in map"
