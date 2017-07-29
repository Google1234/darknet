import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

ratio=0.9 
classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]


def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id):
    in_file = open('Annotations/%s.xml'%(image_id))
    out_file = open('labels/%s.txt'%(image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

#part 1 :create train.txt test.txt
images=os.listdir(wd+"JPEGImages") 
train_file=open("train_set.txt",'w')
test_file= open("test_set.txt",'w')
all_images=[]
for name in os.listdir(anno_dir): 
    if name[:-3]+"jpg" in images:
	all_images.append(name[:-4])

import random
random.shuffle(all_images)
k=0
for image in all_images:
    if k<len(all_images)*ratio:
        train_file.write("%s\n" % image)
    else:
	test_file.write("%s\n" % image)
    k+=1
train_file.close()
test_file.close()


image_ids = open(train_file).read().strip().split()
list_file = open("train.txt", 'w')
for image_id in image_ids:
    list_file.write('%s/JPEGImages/%s.jpg\n'%(wd, image_id))
    convert_annotation( image_id)
    list_file.close()

image_ids = open(test_file).read().strip().split()
list_file = open("test.txt", 'w')
for image_id in image_ids:
    list_file.write('%s/JPEGImages/%s.jpg\n'%(wd, year, image_id))
    convert_annotation( image_id)
    list_file.close()

