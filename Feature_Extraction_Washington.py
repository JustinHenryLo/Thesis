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

def FindStartingPixel(img):
    startX=sys.maxsize
    startY=sys.maxsize
    outerloop=0
    innerloop=0
    for y in thresh:
        for x in y:
            if(x == 0):
                if(innerloop < startX):
                    startX = innerloop
                    startY = outerloop
                    break
            innerloop+=1
        outerloop+=1
        innerloop=0
    #startX and startY are X and Y axis of leftmost black pixel
    if((startX != sys.maxsize) and(startY != sys.maxsize)):
        return startX,startY
    else:
        return -1,-1

def ColorBox(img,Xcoordinate,Ycoordinate):
    for x in range(Xcoordinate,Xcoordinate+kernel_size):
        for y in range(Ycoordinate,Ycoordinate+kernel_size):
            try:
                img[y][x]=125     
            except:
                break

def SnipFeature(img,Xcoordinate,Ycoordinate):
    X=[]
    Y=[]
    for y in range(Ycoordinate,Ycoordinate+kernel_size):
        for x in range(Xcoordinate,Xcoordinate+kernel_size):
            try:
                X.append(img[y][x]) 
            except:
                X.append(np.uint8(255))
        Y.append(X)
        X=[]
    t=np.asarray(Y)
    
    return t

def UpOrDown(img,Xcoordinate,Ycoordinate):
    up=[]
    down=[]
    for y in range(Ycoordinate-kernel_size,Ycoordinate):
        try:
            up+=(img[y][Xcoordinate:Xcoordinate+kernel_size].tolist())
        except:
            break

    for y in range(Ycoordinate,Ycoordinate+kernel_size):
        try:
            down+=(img[y][Xcoordinate:Xcoordinate+kernel_size].tolist())
        except:
            break
    return up.count(0)>down.count(0) #returns true if there are more black pixels in up box than down box


kernel_size= int(sys.argv[1])
source_path = "/home/justin/Desktop/Jupyter/Test Data/Image/Washington/washingtondb-v1.0/data/line_images_normalized"
path="/home/justin/Desktop/WashingtonFeatures/Wtest_features_"+str(kernel_size)+"/"

for filename in os.listdir(source_path):
    img = cv.imread(source_path+"/"+filename,0)
    ret,thresh = cv.threshold(img,127,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    thresh_copy=thresh.copy()
    folder_name=filename.split("-")[0]
    #pathlib.Path(path+"/W_features_raw/"+folder_name+"/").mkdir(parents=True, exist_ok=True)
    pathlib.Path(path+"/W_features/"+folder_name+"/").mkdir(parents=True, exist_ok=True)
    #pathlib.Path(path+"/W_feature_steps/"+folder_name+"/").mkdir(parents=True, exist_ok=True)
    
    name=0
    name_steps=0
    while True:
        X,Y=FindStartingPixel(thresh)
        if(X==-1 and Y==-1):
            break
        else:
            Y=(Y-kernel_size if UpOrDown(thresh,X,Y) else Y)
            features = SnipFeature(thresh,X,Y)
            ColorBox(thresh,X,Y)
            flat_list = list(itertools.chain.from_iterable(features))
            flat_list_len=len(flat_list)
            if(flat_list.count(125) < flat_list_len*(1/2) and flat_list.count(0) > flat_list_len*(1/10) and flat_list.count(0) < flat_list_len*(9/10)):
                #Image.fromarray(features).save(path+"/W_features_raw/"+folder_name+"/"+filename[:-4]+"-"+str(name)+"-W.png")
                features = SnipFeature(thresh_copy,X,Y)
                Image.fromarray(features).save(path+"/W_features/"+folder_name+"/"+filename[:-4]+"-"+str(name)+"-W.png")
                name+=1

            #img = Image.fromarray(thresh)
            #img.save(path+"/W_feature_steps/"+folder_name+"/"+filename[:-4]+"-"+str(name_steps)+"-W.png")
            #name_steps+=1
    #break
"""

img = cv.imread('/home/justin/Desktop/testing2.png',0)
ret,thresh = cv.threshold(img,127,255,cv.THRESH_BINARY+cv.THRESH_OTSU)






      



#img = Image.fromarray(thresh)
#img.show()
"""

#region comments
"""

#median filtering is ineffective
#medianfiltering= medfilt(thresh,3)
#img = Image.fromarray(medianfiltering)
#img.show()

#extract black pixels per row

black=[]
for x in thresh:
    black.append(list(x).count(0))

for x in range(black.__len__()):
    if(black[x-2]>black[x-1] and black[x-1]>black[x] and black[x+1]>black[x] and black[x+2]>black[x+1]):
        print(black[x],">>>",str(x))
    if(is_depression(x) and is_ascension(x)):
        print(black[x],">>>",str(x))
#find points where black pixels are at its lowest
"""
"""
depression_points=[]
index=0
for x in black:
    if(is_depression(x)):
        if(is_ascension(x)):
            depression_points.append(index)
    index+=1

print(depression_points)
"""

"""
for x in range(1,470):
    number=str(x).zfill(3) 
    img = cv.imread('/home/justin/Desktop/DiaryJPG/Mohamedou_Ould_Slahi_Diary-'+number+'.jpg',0)
    ret,thresh = cv.threshold(img,127,255,cv.THRESH_BINARY)
    #The function used is cv.threshold. 
    #First argument is the source image, which should be a grayscale image. 
    #Second argument is the threshold value which is used to classify the pixel values. 
    #Third argument is the maxVal which represents the value to be given if pixel value is more than (sometimes less than) the threshold value
    
    
    #img = Image.fromarray(thresh)
    #img.save('/home/justin/Desktop/DiaryThreshold/'+number+'.png')
"""

"""
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
img = cv.imread('/home/justin/Desktop/DiaryJPG/Mohamedou_Ould_Slahi_Diary-002.jpg',0)

#The function used is cv.threshold. 
#First argument is the source image, which should be a grayscale image. 
#Second argument is the threshold value which is used to classify the pixel values. 
#Third argument is the maxVal which represents the value to be given if pixel value is more than (sometimes less than) the threshold value

ret,thresh1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
ret,thresh2 = cv.threshold(img,127,255,cv.THRESH_BINARY_INV)
ret,thresh3 = cv.threshold(img,127,255,cv.THRESH_TRUNC)
ret,thresh4 = cv.threshold(img,127,255,cv.THRESH_TOZERO)
ret,thresh5 = cv.threshold(img,127,255,cv.THRESH_TOZERO_INV)
titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
for i in range(6):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()
"""
"""
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
img = cv.imread('/home/justin/Desktop/DiaryJPG/Mohamedou_Ould_Slahi_Diary-002.jpg',0)
img = cv.medianBlur(img,5)
ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
            cv.THRESH_BINARY,11,2)
th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,11,2)
titles = ['Original Image', 'Global Thresholding (v = 127)',
            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
images = [img, th1, th2, th3]
for i in range(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()
"""
"""
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
img = cv.imread('/home/justin/Desktop/DiaryJPG/Mohamedou_Ould_Slahi_Diary-002.jpg',0)
# global thresholding
ret1,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
# Otsu's thresholding
ret2,th2 = cv.threshold(img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
# Otsu's thresholding after Gaussian filtering
blur = cv.GaussianBlur(img,(5,5),0)
ret3,th3 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
# plot all the images and their histograms
images = [img, 0, th1,
          img, 0, th2,
          blur, 0, th3]
titles = ['Original Noisy Image','Histogram','Global Thresholding (v=127)',
          'Original Noisy Image','Histogram',"Otsu's Thresholding",
          'Gaussian filtered Image','Histogram',"Otsu's Thresholding"]
for i in range(3):
    plt.subplot(3,3,i*3+1),plt.imshow(images[i*3],'gray')
    plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])
    plt.subplot(3,3,i*3+2),plt.hist(images[i*3].ravel(),256)
    plt.title(titles[i*3+1]), plt.xticks([]), plt.yticks([])
    plt.subplot(3,3,i*3+3),plt.imshow(images[i*3+2],'gray')
    plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])
plt.show()
"""
"""
from PIL import Image
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
img = cv.imread('/home/justin/Desktop/DiaryJPG/Mohamedou_Ould_Slahi_Diary-002.jpg',0)
ret,thresh1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
img = Image.fromarray(thresh1)
img.save('/home/justin/Desktop/my.png')
img.show()
#print(thresh1)
"""

#endregion 
