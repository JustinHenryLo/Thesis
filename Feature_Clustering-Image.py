from PIL import Image
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import medfilt
import collections
import sys
import os
import itertools
import pathlib
import sys
from  skimage.measure import compare_ssim
import linecache
from ast import literal_eval

pathlib.Path().mkdir(parents=True, exist_ok=True)
source_path = "/home/justin/Desktop/testa/"
#source_path = "/home/justin/Desktop/GuantanamoFeatures/G_features_45/G_features/"
save_path = "/home/justin/Desktop/FeatureClustering/"
pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)

model=[]
"""
with open(save_path + "model.txt", "w+") as save:
    model = save.read().rstrip().split("\n")
    if(len(model)!=1):
        model = [np.array(literal_eval(line),dtype=np.uint8) for line in model]
model=[]
"""
for folder in os.listdir(source_path):
    for filename in os.listdir(source_path + folder +"/"):
        instance = cv.imread(source_path + folder +"/"+ filename,0)
        saved= False
        index=0
        for x in model:
            if(compare_ssim(x, instance) >= 0.40):
                Image.fromarray(instance).save(save_path + str(index) + "/" + filename)
                saved=True
            index+=1
        
        if(not saved):
            pathlib.Path(save_path+str(len(model))+"/").mkdir(parents=True, exist_ok=True)
            Image.fromarray(instance).save(save_path + str(len(model)) + "/" + filename)
            instance[instance >= 255] = 100
            Image.fromarray(instance).save(save_path+str(len(model))+"/"+ "---" +".png")
            model.append(instance)
            """cv.imwrite(save_path+str(len(model)-1)+"/"+ "---" +".png", instance)
            saveline= "["
            for a in instance:
                saveline += "["
                for b in a:
                    saveline+= (str(b)+",")
                saveline = saveline[:-1]
                saveline += "],"
            saveline = saveline[:-1]
            saveline+= "]\n"
            saveline = saveline.rstrip()
            with open(save_path + "model.txt", "a") as save:
                save.write(saveline)
            """

"""
arr =np.array([1,2,3,4,5,6])
ts = arr.tostring()
print np.fromstring(ts,dtype=int)
"""