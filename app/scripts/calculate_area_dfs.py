import numpy as np
import sys
sys.setrecursionlimit(1000000000)
pixel_list = None
idx_array = []
width = None
height = None
img=None
Group_list=[]
class pixel():
    def __init__(self):
        self.color = None
        self.group = -1
    def setColor(self,color):
        self.color = color
    def setGroup(self,group,neighbor):
        self.group = group

def AreaProcesser(input_image):
    print("start process")
    global pixel_list,width,height,img,idx_array,Group_list
    Group_list ={
        'blue':[list() for i in range(10)],
        'green':[list() for i in range(10)],
        'orange':[list() for i in range(10)],
        'red':[list() for i in range(10)],
        'cyan':[list() for i in range(10)],
        'pink':[list() for i in range(10)]
    }
    
    img = input_image
    height = img.shape[0]
    width = img.shape[1]

    pixel_list=[ pixel() for k in range(width * height) ]
    

    # create neighbor mask
    mask = 3
    mask = int(mask/2)
    for j in range(-mask,mask+1):
        for i in range(-mask,mask+1):
            if (i,j)!= (0,0):
                idx_array.append((i,j))

    for j in range(0,width):
        for i in range(0,height):
            color, degree = checkProp(img[i][j][:])
            if color == 'empty':
                continue
            current_pixel = pixel_list[i*width+j]
            # It's new group, assign group by known group num
            if current_pixel.group == -1:
                current_pixel.group = len(Group_list[color][degree])
                Group_list[color][degree].append([(i,j)])
                dfs(color,i,j,pixel_list[i*width+j].group,degree)
                

    for k,v in Group_list.items():
        for p in range(len(v)):
            if len(v[p])>0:
                for a in v[p]:
                    print("Color: ",k,"degree", p ,"pixel num: ",len(a))
    return Group_list

    
def dfs(color,i,j,group,degree):
    global pixel_list,width,height,img,idx_array,Group_list
    try:
        # print('color: ',color,' ','group: ',group,'(',i,',',j,')')
        for k in range(len(idx_array)+1):
            if k == len(idx_array):
                return
            else:
                v = idx_array[k] # offset
                if i+v[0]<height and j+v[1]<width and i+v[0]>=0 and j+v[1]>=0:
                    if (color,degree) == checkProp(img[i+v[0]][j+v[1]][:]) and pixel_list[(i+v[0])*width+(j+v[1])].group == -1:
                        pixel_list[(i+v[0])*width+(j+v[1])].group = group
                        Group_list[color][degree][group].append((i+v[0],j+v[1]))
                        dfs(color,i+v[0],j+v[1],group,degree)
    except Exception as e:
        print(e)
       
def checkProp(pixel):

    # if pixel[0] in range(200,256) and pixel[1] in range(0, 30)and pixel[2] in range(0,30):
    #     print(pixel)            

    if pixel[0] in range(245,256) and pixel[1] in range(0,10) and pixel[2] in range(0,160):
        return ('red', checkDegree(pixel[2]))
    elif pixel[0] in range(0,160) and pixel[1] in range(245,256) and pixel[2] in range(245,256):
        return ('cyan', checkDegree(pixel[0]))
    elif pixel[0] in range(0,160) and pixel[1] in range(0,10) and pixel[2] in range(245,256):
        return ('blue', checkDegree(pixel[0]))
    elif pixel[0] in range(0,160) and pixel[1] in range(200,220) and pixel[2] in range(77,97):
        return ('green', checkDegree(pixel[0]))
    elif pixel[0] in range(245,256) and pixel[1] in range(143,163) and pixel[2] in range(0,160):
        return ('orange', checkDegree(pixel[2]))
    elif pixel[0] in range(245,256) and pixel[1] in range(0,160) and pixel[2] in range(245,256):
        return ('pink', checkDegree(pixel[1]))
    else:
        return ('empty', checkDegree(pixel[0]))

def checkDegree(degree_pixel):
    return int(round(degree_pixel/15)-1)
    
