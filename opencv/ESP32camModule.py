import cv2
import numpy as np
import requests

capture_url = "http://192.168.8.186:81/capture"

def getImg():
    response = requests.get(capture_url)
    image_array = np.frombuffer(response.content, np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return img


if __name__ == '__main__':
    while True:
        img = getImg()
        cv2.imshow('IMG',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
