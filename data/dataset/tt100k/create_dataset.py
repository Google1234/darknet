ratio=1.0#0.9
anno_file="annotations.json"
save_crop_nums=1



import os
from os import listdir, getcwd
wd=getcwd()
wd=os.path.join(wd,"data")

import json
datas=json.load(open(os.path.join(wd,anno_file),'r'))
labels=datas["types"]
imgs=datas["imgs"]
count_dic={}
examples_nums={}
for label in labels:
	count_dic[label]=0
	examples_nums[label]=0
############################################################
	# part 1 :create train.txt test.txt
import random
from PIL import Image
indexs=list(imgs.keys())
random.shuffle(indexs)
train_nums=len(imgs)*ratio
train_file=open(os.path.join(wd,"train.txt"), 'w')
test_file=open(os.path.join(wd,"test.txt"), 'w')
k=0

if os.path.exists(os.path.join(wd,"labels"))==False:
	os.mkdir(os.path.join(wd,"labels"))
if os.path.exists(os.path.join(wd,"examples"))==False:
	os.mkdir(os.path.join(wd,"examples"))
else:
	os.removedirs(os.path.join(wd,"examples"))
	os.mkdir(os.path.join(wd, "examples"))
for index  in indexs:
	img=imgs[index]
	_path=os.path.join(wd, img['path'])
	if os.path.exists(_path):
		if k<train_nums:
			train_file.write("%s\n" % _path)
		else:
			test_file.write("%s\n" % _path)
		objs=img["objects"]
		out_file = open(os.path.join(wd,'labels/%s.txt' % (img['id'])), 'w')
		
		im=Image.open(_path)
		size_w,size_h=im.size
		for obj in objs:
			category= obj["category"]
			xmax	= float(obj['bbox']["xmax"])
			ymax    = float(obj['bbox']["ymax"])
			xmin 	= float(obj['bbox']["xmin"])
			ymin 	= float(obj['bbox']["ymin"])
			###########convert ############
			dw = 1. / size_w
			dh = 1. / size_h
			x = (xmin + xmax) / 2.0
			y = (ymin + ymax) / 2.0
			w = xmax - xmin
			h = ymax - ymin
			x = x * dw
			w = w * dw
			y = y * dh
			h = h * dh
			out_file.write(str(labels.index(category)) + " " + str(x)+ " " + str(y)+" " + str(w)+" " + str(h)+'\n')
			
			count_dic[category]+=1
			
			if examples_nums[category]<save_crop_nums:
				temp=im.copy()
				temp.crop((int(xmin), int(ymin), int(xmax), int(ymax))).save(os.path.join(wd,"examples",category+".jpg"))
				examples_nums[category]+=1
				
		out_file.close()
	k+=1
train_file.close()
test_file.close()

names=open(os.path.join(wd,"tt100k.names"), 'w')
for label in labels:
	names.write(label+'\n')
names.close()


print count_dic
############################################################



######plot image
