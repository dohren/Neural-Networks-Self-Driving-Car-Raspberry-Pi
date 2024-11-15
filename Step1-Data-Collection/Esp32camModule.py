import cv2
from urllib.request import urlopen
import numpy as np

url = 'http://192.168.8.186:81/capture'

def getImg(display= False,size=[480,240]):
        img_resp = urlopen(url)
        imgnp = np.asarray(bytearray(img_resp.read()), dtype="uint8")
        img = cv2.imdecode(imgnp, -1)
        img = cv2.resize(img,(size[0],size[1]))
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        if display:
            cv2.imshow("Camera", img)
        
if __name__ == '__main__':
   while True:
    getImg(True)
    if cv2.waitKey(10) == 113:
            break
        