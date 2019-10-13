from app import app
from PIL import Image
from app.scripts.calculate_area_dfs import AreaProcesser
from flask import Flask, render_template, request, redirect, url_for, send_file,send_from_directory
import requests
import os
import re
import io
import sys
import cv2
import json
import base64
import numpy as np
from zipfile import ZipFile
import time

@app.route('/', methods=['GET', 'POST'])
def paintapp():
    if request.method == 'GET':
        return render_template("paint.html") 
    elif request.method =='POST':
        filename = request.json['filename']
        canvas_image = request.json['save_image']
        print()
        imgstr = re.search(r'base64,(.*)', canvas_image).group(1)
        image_bytes = io.BytesIO(base64.b64decode(imgstr))

        im = Image.open(image_bytes)



        arr = np.array(im)
        start =time.time()
        Group_list = AreaProcesser(arr)
        print("execution time: ",str(time.time()-start))
        body_area = 36407.5 # sorry, but I have to hard code...
        ID=1
        for k,v in Group_list.items():
            for p in range(len(v)):
                if len(v[p])>0:
                    for a in v[p]:
                        if(len(a)>10):
                            cv2.putText(arr, str(ID) , (a[0][1],a[0][0]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,0,255), 2)
                            text = "ID: "+str(ID)+ " Color: "+str(k)+" "+"Degree: "+ str(p+1) +" Affect ratio: "+str((len(a)/body_area)*100) +" %\n"
                            f = open("app/static/txt/"+ filename + ".txt", "a")
                            f.write(text)
                            f.close()
                            ID+=1

        mark_area = Image.fromarray(arr,"RGBA")
        
        bg_im=Image.open("app/static/img/meta/input.jpg")
        new_im2 = Image.new('RGBA', size=(375, 480), color=(0, 0, 0, 0))
        new_im2.paste(bg_im,(0,0))
        new_im2.paste(mark_area,(0,0),mark_area)
        new_im2.save("app/static/img/" + filename + ".png","PNG")

        return render_template("paint.html") 

@app.route('/download/<path:filename>',methods=['GET','POST'])
def download(filename):
    
    with ZipFile('app/static/zip/'+filename+'.zip','w') as zip:
        path ='/home/nmsl/Paintapp-Flask-PostgreSQL/app/static/txt/'
        files = os.listdir(path)
        for f in files:
            dfile = os.path.join(path,f)
            if os.path.isfile(dfile):
                zip.write(dfile)
                os.remove(dfile)
        path = '/home/nmsl/Paintapp-Flask-PostgreSQL/app/static/img/'
        files = os.listdir(path)
        for f in files:
            dfile = os.path.join(path,f)
            if os.path.isfile(dfile):
                zip.write(dfile)
                print(dfile)
                os.remove(dfile)
    return send_file('static/zip/'+filename+'.zip',as_attachment=True)
    

@app.route('/download/img/<path:filename>',methods=['GET','POST'])
def downloadImage(filename):
    return send_file("static/img/"+filename,as_attachment=True)
    
@app.route('/download/txt/<path:filename>',methods=['GET','POST'])
def downloadTxt(filename):
    print("downloadtxt")
    return send_file("static/txt/"+filename,as_attachment=True)
    



