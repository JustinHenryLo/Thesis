from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import pathlib
import warnings
from PIL import Image
from numpy import array

source_path = "/home/justin/Desktop/FeatureClustering/"

feature_length = len(os.listdir(source_path))
vector_data = []
recorded_lines = []
labels =[]
for folder in os.listdir(source_path):
    for filename in os.listdir(source_path + folder +"/"):
        if(filename != "---.png"):
                linename = filename.split("-")
                linename = linename[0]+"-"+linename[1]
                
                if(linename not in recorded_lines):
                    vector = np.zeros(shape=(feature_length))
                    label = 0 if "G" in filename else 1 
                    vector_data.append(vector)
                    labels.append(label)
                    recorded_lines.append(linename)
                else:
                    index = recorded_lines.index(linename)
                    vector_data[index][int(folder)] += 1

#print(np.c_[recorded_lines,vector_data])
np.save("/home/justin/Desktop/vector_data.npy", vector_data)
np.save("/home/justin/Desktop/label_data.npy", labels)