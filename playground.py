
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



source_path = "/home/justin/Desktop/GuantanamoFeatures"
    
for folder in os.listdir(source_path):
    for folderr in os.listdir(source_path +"/"+ folder + "/"):
        for folderrr in os.listdir(source_path +"/"+ folder +"/"+ folderr +"/"):
            for filename in os.listdir(source_path +"/"+ folder +"/"+ folderr +"/"+ folderrr +"/"):
                os.rename(source_path +"/"+ folder +"/"+ folderr +"/"+ folderrr +"/"+ filename , source_path +"/"+ folder +"/"+ folderr +"/"+ folderrr +"/"+ filename[:-4].replace(".","")+"-G.png")


"""
from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import pathlib
import warnings
from PIL import Image
from numpy import array

#region SSIM

source_path = "/home/justin/Desktop/GuantanamoFeatures/G_features_35/G_features/2/"
files = os.listdir(source_path)
for x in files:
    path = "/home/justin/Desktop/SimilarityTesting/"+x+"/"
    imageA = cv2.imread(source_path + x, 0)

    for a in imageA:
        a[a >= 255] = 100

    done = False
    for y in files:
        imageB = cv2.imread(source_path+y,0)
        sim = ssim(array(imageA), imageB)
        if(sim >= 0.40 and x!=y):
            pathlib.Path("/home/justin/Desktop/SimilarityTesting/"+x+"/").mkdir(parents=True, exist_ok=True)
            cv2.imwrite(path+y, imageB)
            if(not done):
                cv2.imwrite(path+"---", imageA)
                done = True
    
#endregion



imageA = cv2.imread("/home/justin/Desktop/raw3.png",0)
imageB = cv2.imread("/home/justin/Desktop/raw.png",0)
s = ssim(imageA, imageB)
print(s)
"""

        