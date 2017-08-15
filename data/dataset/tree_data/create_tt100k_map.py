
import os
from os import listdir, getcwd
wd=getcwd()
#wd="/Users/jt/Desktop/UISEE/data/data"
#wd=os.path.join(wd,"data")

map_file=os.path.join(wd,"china_signs.nodes")

names_file=os.path.join(wd,"tt100k.names")
names=open(names_file,'r').read().split('\n')

#map_file=os.path.join(wd,"tt100k.map")
maps=open(map_file,'r').read().split('\n')
maps_dic={}
for m in maps:
	_s=m.split(' ')
	if len(_s)==2:maps_dic[_s[0]]=_s[1]
	
out_map_file=os.path.join(wd,"tt100k.map")
out_map=open(out_map_file,'w')
out_nodes_file=os.path.join(wd,"tt100k.nodes")
out_node=open(out_nodes_file,'w')
for na in names:
	if na in maps_dic.keys():
		out_node.write(na+' '+maps_dic[na]+'\n')
		out_map.write(maps_dic[na]+'\n')
	else:
		print na," not in map"
