import cv2
import numpy as np
import requests

capture_url = "http://192.168.253.254:81/capture"

def getImg(display= False,size=[480,240]):
    response = requests.get(capture_url)
    image_array = np.frombuffer(response.content, np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img = cv2.resize(img,(size[0],size[1]))
    return img

while True:
    frame = getImg()
    if frame is not None:
        cv2.imshow("ESP32-CAM", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
