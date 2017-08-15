ratio=0.999#0.9
anno_file="annotations.json"
save_crop_nums=1
error_labeled="pn40"
true_label='pl40'


import os
from os import listdir, getcwd
wd=getcwd()
wd=os.path.join(wd,"data")

import json
datas=json.load(open(os.path.join(wd,anno_file),'r'))
#labels for tt100k-->220
#labels=datas["types"]
#labels for all china signs---->228
labels=['signs', 'po', 'io', 'wo', 'p_direction', 'ps', 'prx', 'pax', 'pd', 'pwx', 'p_object', 'p11', 'pg', 'plx', 'phx', 'pc', 'pmx', 'pne', 'pnl', 'p23', 'pn', 'p21', 'p19', 'pe', 'p28', 'p5', 'pb', 'p20', 'p14', 'p1', 'pr50', 'pr45', 'pr20', 'pr40', 'pr30', 'pr80', 'pr70', 'pr100', 'pr60', 'pr10', 'pa14', 'pa13', 'pa12', 'pa10', 'pa8', 'pw3.5', 'pw2', 'pw3.2', 'pw4.5', 'pw4', 'pw3', 'pw2.5', 'pw4.2', 'p25', 'p29', 'p6', 'p2', 'p24', 'p7', 'p12', 'p10', 'p8', 'p13', 'p18', 'p26', 'p27', 'p4', 'p9', 'p15', 'p16', 'p22', 'p17', 'p3', 'pl0', 'pl20', 'pl30', 'pl90', 'pl15', 'pl100', 'pl10', 'pl70', 'pl4', 'pl60', 'pl50', 'pl80', 'pl65', 'pl5', 'pl40', 'pl120', 'pl35', 'pl25', 'pl3', 'pl110', 'ph4.3', 'ph5.5', 'ph3.5', 'ph3.3', 'ph5.3', 'ph1.5', 'ph5', 'ph2.4', 'ph4.5', 'ph2', 'ph3', 'ph4.8', 'ph2.8', 'ph2.5', 'ph4', 'ph2.9', 'ph4.4', 'ph2.1', 'ph2.6', 'ph4.2', 'ph3.2', 'ph3.8', 'ph2.2', 'pm40', 'pm35', 'pm50', 'pm55', 'pm8', 'pm5', 'pm1.5', 'pm13', 'pm46', 'pm30', 'pm10', 'pm25', 'pm20', 'pm15', 'pm2', 'pm2.5', 'i9', 'ilx', 'i_object', 'i_direction', 'il70', 'il90', 'il100', 'il110', 'il50', 'il60', 'il80', 'i4', 'i2', 'i1', 'ip', 'i10', 'i11', 'i8', 'i3', 'i13', 'i12', 'i15', 'i6', 'i5', 'i14', 'i7', 'w_object', 'w_direction', 'w_danger', 'w55', 'w67', 'w36', 'w34', 'w50', 'w56', 'w64', 'w52', 'w40', 'w57', 'w6', 'w18', 'w22', 'w42', 'w33', 'w53', 'w16', 'w24', 'w48', 'w59', 'w19', 'w31', 'w20', 'w14', 'w43', 'w21', 'w35', 'w66', 'w17', 'w49', 'w10', 'w25', 'w47', 'w58', 'w15', 'w23', 'w41', 'w65', 'w11', 'w13', 'w8', 'w26', 'w27', 'w51', 'w44', 'w3', 'w12', 'w9', 'w62', 'w1', 'w2', 'w54', 'w39', 'w61', 'w46', 'w38', 'w28', 'w63', 'w37', 'w60', 'w4', 'w29', 'w45', 'w5', 'w30', 'w32', 'w7']
#labels=[]
if(error_labeled in labels):
        labels.remove(error_labeled)

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
			if category==error_labeled:
			    category=true_label
			    print _path," wrong labeled"
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
			if category not in labels:
			    print (category," not in labels!")
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

names=open(os.path.join(wd,"china_signs.names"), 'w')
for label in labels:
	names.write(label+'\n')
names.close()

names=open(os.path.join(wd,"all_labels.txt"), 'w')
for label in labels:
        names.write(','+label)
names.close()

#print count_dic
############################################################



######plot image
