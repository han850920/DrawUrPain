from PIL import Image
from app.scripts.calculate_area_dfs import AreaProcesser
import cv2
import numpy as np
import time
im = Image.open('app/static/img/Lu.png')

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
                    f = open("app/static/txt/Lu.txt", "a")
                    f.write(text)
                    f.close()
                    ID+=1

mark_area = Image.fromarray(arr,"RGBA")

bg_im=Image.open("app/static/img/meta/input.png")
new_im2 = Image.new('RGBA', size=(375, 480), color=(0, 0, 0, 0))
new_im2.paste(bg_im,(0,0))
new_im2.paste(mark_area,(0,0),mark_area)
new_im2.save("app/static/img/Lu.png","PNG")