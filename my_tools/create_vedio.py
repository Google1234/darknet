import matplotlib
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob
import numpy as np
import os
import pdb
#import builtins as __builtin__
import sys
import os
import glob
import shutil
from os import listdir, getcwd
wd=getcwd()
wd=os.path.join(wd,"data")


def makedirs(dir):
    if not os.path.isdir(dir): os.makedirs(dir)


def remove(file):
    if os.path.exists(file): os.remove(file)


def empty(dir):
    if os.path.isdir(dir):
        shutil.rmtree(dir, ignore_errors=True)
    else:
        os.makedirs(dir)



save_root = wd+'/Video/'
#data_root = 'result_sequence/'
data_root = wd+'/results/'

makedirs(save_root)
files_list=glob.glob(data_root+'*')
files=[]
for file in files_list:
    base=os.path.basename(file)
    files.append(int(os.path.splitext(base)[0]))

base=os.path.basename(files_list[0])
suffix=os.path.splitext(base)[1]
dir_name=os.path.dirname(files_list[0])

files.sort()
# pdb.set_trace()
num_frames=len(files)
	
video_path=save_root+'rst.avi'
fps =25
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
print os.path.join(dir_name,str(files[0])+suffix)
img=cv2.imread(os.path.join(dir_name,str(files[0])+suffix))
videoWriter = cv2.VideoWriter(video_path, fourcc,fps,(img.shape[1], img.shape[0]))
	# fig, axes = plt.subplots(2, 1, figsize=(16, 12))
	# ax0, ax1 = axes.ravel()
	
for i in range(1,len(files)):
    print os.path.join(dir_name,str(files[i])+suffix)
    image=cv2.imread(os.path.join(dir_name,str(files[i])+suffix))
    image = cv2.resize(image, (img.shape[1], img.shape[0]))
    videoWriter.write(image)# cv2.waitKey(1)	
videoWriter.release()




