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
from  skimage.measure import compare_ssim,compare_mse
import linecache
from ast import literal_eval
import sqlite3
import math 

def run_query_return(query,conn):
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def run_query_void(query,conn):
    cur = conn.cursor()
    cur.execute(query)

def create_tables(instance,conn):
    kernel = len(instance[0])
    run_query_void("CREATE TABLE IF NOT EXISTS _"+str(kernel)+" (feature INTEGER ,name VARCHAR(20));",conn)#ROWID implicit
    run_query_void("CREATE TABLE IF NOT EXISTS _"+str(kernel)+"count (feature INTEGER PRIMARY KEY, count INTEGER);",conn)
    return "_"+str(kernel)


DBname = "FeaturesDB.db"
save_path = "/home/justin/Desktop/Thesis/"
source_path = "/home/justin/Desktop/45/"

pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)
pathlib.Path(save_path+"Features/").mkdir(parents=True, exist_ok=True)
#dbfile= open(save_path + DBname,"w+")

try:
    dbfile = open(save_path + DBname, 'r')
except FileNotFoundError:
    dbfile = open(save_path + DBname, 'w')

conn = sqlite3.connect(save_path+DBname)

model=[]

run_once = True
table =""

for folder in os.listdir(source_path):
    for filename in os.listdir(source_path + folder +"/"):
        instance = cv.imread(source_path + folder +"/"+ filename,0)
        saved= False
        if(run_once):
            table = create_tables(instance,conn)
            if not os.path.exists(save_path+"Features/"+table[1:]+"/"):
                pathlib.Path(save_path+"Features/"+table[1:]+"/").mkdir(parents=True, exist_ok=True)
            try:
                m = run_query_return("SELECT COUNT(*) FROM "+table+"count",conn)[0][0]
                for x in range(1,m+1):
                    model.append(save_path+"Features/"+table[1:]+"/"+str(x)+'/---.png')
                model =[cv.imread(i,0) for i in model] #list of <class 'numpy.ndarray'> features/1/---.png
            except:
                model=[]
            run_once=False
        
        index=1
        for x in model:
            if(compare_ssim(x, instance) >= 0.35):#and compare_mse(x,instance)>=16000): #<class 'numpy.ndarray'>
                run_query_void("INSERT INTO "+table+" VALUES ('"+str(index)+"','"+filename+"');",conn)
                count = run_query_return("SELECT count FROM "+table+"count WHERE ROWID ="+str(index)+";",conn)[0][0] + 1
                run_query_void("UPDATE "+table+"count SET count='"+str(count)+"' WHERE ROWID ="+str(index)+";",conn)
                Image.fromarray(instance).save(save_path +"Features/"+table[1:]+"/"+str(index)+"/"+ filename)
                saved=True
                conn.commit()
            
            index+=1
        
        if(not saved):
            pathlib.Path(save_path+"Features/"+table[1:]+"/"+str(index)+"/").mkdir(parents=True, exist_ok=True)
            Image.fromarray(instance).save(save_path + "Features/"+table[1:]+"/"+str(index) + "/" + filename)

            run_query_void("INSERT INTO "+str(table)+" VALUES ('"+str(index)+"','"+filename+"');",conn)
            instance[instance >= 255] = 100
            Image.fromarray(instance).save(save_path + "Features/"+table[1:]+"/"+str(index) + "/" + "---.png")
            run_query_void("INSERT INTO "+table+"count VALUES ('"+str(index)+"','1');",conn)
            model.append(instance)
            conn.commit()

