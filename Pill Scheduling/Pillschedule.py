from google.colab import drive
drive.mount('/content/gdrive')
!pip install tesseract
! apt install tesseract-ocr
! apt install libtesseract-dev
! pip install Pillow
! pip install pytesseract
import imageio
from IPython.display import Image

path = '/content/gdrive/My Drive/input4.jpeg'
display(Image(path))
# Image preprocessing for OCR (enhancing tech recognition)
# 1
import tempfile

import cv2
import numpy as np
from PIL import Image

IMAGE_SIZE = 1800
BINARY_THREHOLD = 180

def process_image_for_ocr(file_path):
    # TODO : Implement using opencv
    temp_filename = set_image_dpi(file_path)
    im_new = remove_noise_and_smooth(temp_filename)
    return im_new

def set_image_dpi(file_path):
    im = Image.open(file_path)
    length_x, width_y = im.size
    factor = max(1, int(IMAGE_SIZE / length_x))
    size = factor * length_x, factor * width_y
    # size = (1800, 1800)
    im_resized = im.resize(size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(300, 300))
    return temp_filename

def image_smoothening(img):
    ret1, th1 = cv2.threshold(img, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3

def remove_noise_and_smooth(file_name):
    img = cv2.imread(file_name, 0)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41,
                                     3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothening(img)
    or_image = cv2.bitwise_or(img, closing)
    return or_image

img = process_image_for_ocr(path) #this is ndArray

# ndArray to image
from matplotlib import cm
img2 = Image.fromarray(np.uint8(cm.gist_earth(img)*255))
display(img2)
# OCR
import pytesseract
print('Result without any preprocessing..')
img = Image.open(path)
print(type(img))
result = pytesseract.image_to_string(img)
print(result)

print('Result with #1 preprocessing...')
print(type(img2))
result = pytesseract.image_to_string(img2,lang='eng')
print(result)

import time
def convert24(str1): #converting 12 to 24 hour format
    if str1[-2:] == "AM" and str1[:2] == "12": 
        return "00" + str1[2:-2] 
    elif str1[-2:] == "AM": 
        return str1[:-2]   
    elif str1[-2:] == "PM" and str1[:2] == "12": 
        return str1[:-2] 
    else: 
        return str(int(str1[:2]) + 12) + str1[2:8] 
def processing_the_data(result):
  file= open("pills.txt","w+")
  sentences = list(map(str,result.split('\n')))
  medarr=[]
  timearr=[]
  for med in sentences:
    med=list(map(str,med.split()))
    for ti in range(1,len(med)):
      tm=med[t1]
      tm=tm[0:-2]+":00"+tm[-2:]
      medarr.append(med[0])
      timearr.append(convert24(tm))
  #sort based on time and writing into a txt file
  both = [[timearr[i], medarr[i]] for i in range(len(medarr))]
  both.sort()
  for i in range(len(medarr)):
    f.write("%s %s\n" % both[i][0],both[i][1])

  

import os, datatime
# lookup file from home directory
file_path = os.getenv('HOME') + '/pills.txt'
def check_schedule():
   lookup_file = open(file_path, 'r') #open the lookup file as read mode
   s=str(datetime.datetime.now()).split()
   s=str(s[1])
   hh,mm,ss=map(float,s.split(':'))
   bday_flag = 0
   for entry in lookup_file:
     tablet_name,time = map(str,entry.split())
     time=time[0:-3]
     t1 = datetime.datetime.strptime(str(hh)+":"+str(mm), '%H:%M')
     t2 = datetime.datetime.strptime(time, '%H:%M')
     wait=t2-t1
     wait_seonds=wait.total_seconds()
     time.sleep(wait_seconds)
     os.system('notify-send "Should put "+tablet_name')
     hh,mm=map(float,time.split(":"))
