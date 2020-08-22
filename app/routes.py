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
import sqlite3
import multiprocessing 
import threading
import shutil
from datetime import datetime
@app.route('/', methods=['GET', 'POST'])
def paintapp():
    if request.method == 'GET':
        return render_template("paint.html") 
    elif request.method =='POST':
        multiprocessing.Process(target=process_request, args=(request,)).start()
        return render_template("paint.html") 


@app.route('/saved',methods=['GET'])
def saved():
    # check those unzip file
    path = 'app/static/img'
    files = os.listdir(path)
    complete_file_list= []
    for f in files:
        img_dir = os.path.join(path,f)
        img_file = os.listdir(img_dir)
        if len(img_file) == 2:
            date_time = datetime.fromtimestamp(os.path.getmtime(img_dir)).strftime('%Y-%m-%d %H:%M:%S')
            complete_file_list.append((f, date_time))
    complete_file_list.sort(key=lambda x: x[1],reverse=True)

    #check those ziped file
    path = 'app/static/zip'
    files = os.listdir(path)
    files_list =[]
    for f in files:
        zipfile = os.path.join(path,f)
        date_time = datetime.fromtimestamp(os.path.getmtime(zipfile)).strftime('%Y-%m-%d %H:%M:%S')
        files_list.append((f, date_time))
    files_list.sort(key=lambda x: x[1],reverse=True)
    return render_template("save.html",complete_file_list = complete_file_list, saved_files=files_list) 
    

@app.route('/download/<path:filename>',methods=['GET','POST'])
def download(filename):
    with ZipFile('app/static/zip/'+filename+'.zip','w') as zip:
        path = os.path.join('app/static/txt/')
        files = os.listdir(path)
        for d in files:
            dfile = os.path.join(path,d)
            files = os.listdir(dfile)

            for f in files:
                ffile = os.path.join(dfile,f)

                zip.write(ffile)
            shutil.rmtree(dfile)

        path = os.path.join('app/static/img/')
        files = os.listdir(path)
        for d in files:
            dfile=os.path.join(path,d)
            files = os.listdir(dfile)
            for f in files: 
                ffile = os.path.join(dfile,f)

                zip.write(ffile)
            shutil.rmtree(dfile)
    return send_file('static/zip/'+filename+'.zip',as_attachment=True)
    

# @app.route('/download/img/<path:filename>',methods=['GET','POST'])
# def downloadImage(filename):
#     return send_file("static/img/"+filename,as_attachment=True)
    
# @app.route('/download/txt/<path:filename>',methods=['GET','POST'])
# def downloadTxt(filename):
#     print("downloadtxt")
#     return send_file("static/txt/"+filename,as_attachment=True)

@app.route('/download/zip/<path:filename>',methods=['GET'])
def downloadZip(filename):
    print("downloadzip")
    return send_file("static/zip/"+filename,as_attachment=True)

def body_proc(filename):
    print("start body process of " + filename)
    body_start =time.time()
    img=Image.open(os.path.join('./app/static/meta/',filename,"0.png"))
    arr = np.array(img)
    
    total_Group_list = AreaProcesser(arr)
    body_area = 36407.5 # sorry, but I have to hard code...
    ID=1
    for k,v in total_Group_list.items():
        for p in range(len(v)):
            if len(v[p])>0:
                for a in v[p]:
                    if(len(a)>10):
                        cv2.putText(arr, str(ID) , (a[0][1],a[0][0]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,0,255), 2)
                        text = "ID: "+str(ID)+ " Color: "+str(k)+" "+"Degree: "+ str(p+1) +"\nTotal affect ratio: "+str((len(a)/body_area)*100) +"%\n"
                        f = open(os.path.join("app/static/txt/", filename, filename + ".txt"), "a")
                        f.write(text)
                        f.close()
                        ID+=1

    total_mark_area = Image.fromarray(arr,"RGBA")
    total_mark_area.save(os.path.join("app/static/img/", filename, filename+"_total.png"),"PNG")
    print(filename + " body execution time: ",str(time.time()-body_start))

def spine_proc(filename):
    # Calculate spine
    print("start spine process of " + filename)
    spine_start =time.time()
    spine_area = 15425 + 17480
    left_spine_im=Image.open(os.path.join('./app/static/meta/',filename,"1.png"))
    spine_arr = np.array(left_spine_im)
    spine_Group_list = AreaProcesser(spine_arr)

    ID_=1
    
    for k_,v_ in spine_Group_list.items():
        for p_ in range(len(v_)):
            if len(v_[p_])>0:
                for a_ in v_[p_]:
                    if(len(a_)>10):
                        cv2.putText(spine_arr, str(ID_) , (a_[0][1],a_[0][0]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,0,255), 2)
                        text_ = "ID: "+str(ID_)+ " Color: "+str(k_)+" "+"Degree: "+ str(p_+1) +"\nSpine affect ratio: "+str((len(a_)/spine_area)*100) +"%\n"
                        f_ = open(os.path.join("app/static/txt", filename, filename + "_spine.txt"), "a")
                        f_.write(text_)
                        f_.close()
                        ID_+=1

    spine_mark_area = Image.fromarray(spine_arr,"RGBA")
    spine_mark_area.save(os.path.join("app/static/img/", filename, filename+"_spine.png"),"PNG")
    print(filename + " spine execution time: ",str(time.time()-spine_start))

def process_request(request):
    filename = request.json['filename']
    canvas_image = request.json['save_image']
    
    imgstr = re.search(r'base64,(.*)', canvas_image).group(1)
    image_bytes = io.BytesIO(base64.b64decode(imgstr))

    im = Image.open(image_bytes)
    pre_process(filename, im)


    body_proc_instance = multiprocessing.Process(target = body_proc, args =(filename,))
    body_proc_instance.start()

    # spine_proc_instance = multiprocessing.Process(target = spine_proc, args =(filename,))
    # spine_proc_instance.start()

    
    body_proc_instance.join()
    # spine_proc_instance.join()

    print(filename + " has completed!")


def pre_process(filename,im):

    raw_img_dir = os.path.join('./app/static/meta/',filename)
    os.mkdir(raw_img_dir)
    file_img_dir = os.path.join('./app/static/img/',filename)
    os.mkdir(file_img_dir)
    file_txt_dir = os.path.join('./app/static/txt/',filename)
    os.mkdir(file_txt_dir)

    # save the original img
    bg_im=Image.open("app/static/meta/input.png")
    mask = Image.open('app/static/meta/edge.png')
    color_img = Image.new('RGBA', size=(375, 480), color=(0, 0, 0, 0))
    color_img.paste(bg_im,(0,0))
    color_img.paste(im,(0,0),mask=im)
    color_img.paste(mask, (0,0), mask=mask)
    color_img.save(os.path.join(raw_img_dir, "0.png"),"PNG")
    
    # image for spine
    # mask = Image.open('app/static/meta/spine_.png')

    # spine_img = Image.new('RGBA', (375,480), (0, 0, 0, 0))
    # spine_img.paste(color_img, (0,0))
    # spine_img.paste(mask, (0,0), mask=mask)

    
    # spine_img.save(os.path.join(raw_img_dir,'1.png'))
