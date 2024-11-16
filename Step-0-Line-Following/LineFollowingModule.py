import cv2
import numpy as np
import ESP32camModule as wM
import time

threshold_value = 25

def follow(img, display= False):
    # 1. Bild in Graustufen konvertieren
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Gaußscher Weichzeichner, um Rauschen zu reduzieren
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 3. Schwellenwert anwenden, um das dunkle Paketband zu erkennen
    _, threshold = cv2.threshold(blurred, threshold_value, 255, cv2.THRESH_BINARY_INV)

    # 4. Morphologische Operationen, um kleine Fehler zu beseitigen
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)

    # 5. Konturen finden
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 6. Konturen zeichnen (optional zur Visualisierung)
    result = img.copy()
    cv2.drawContours(result, contours, -1, (0, 255, 0), 2)

    # 7. Ausgabe des bearbeiteten Bildes
    if display:
        cv2.imshow('IMG',img)
        cv2.imshow("Mask", mask)
        cv2.imshow("Result", result)

    if len(contours) == 0:
        print("Kein Weg erkannt")
        return {"axis2": 0, "axis1": 0} 

    # Größte Kontur finden (das Paketband)
    largest_contour = max(contours, key=cv2.contourArea)

    # Schwerpunkt (Centroid) der größten Kontur berechnen
    M = cv2.moments(largest_contour)
    if M["m00"] == 0:  # Vermeidet Division durch Null
        return "stop"

    cx = int(M["m10"] / M["m00"])  # x-Koordinate des Schwerpunkts
    cy = int(M["m01"] / M["m00"])  # y-Koordinate des Schwerpunkts

    # Mittellinie des Bildes berechnen
    height, width = img.shape[:2]
    mid_x = width // 2

    # Entscheidungslogik basierend auf der Position des Schwerpunkts
    if cx < mid_x - 40:
        # Linksdrehung
        command = {"axis2": 0, "axis1": -1}
    elif cx > mid_x + 40:
        # Rechtsdrehung
        command = {"axis2": 0, "axis1": 1}
    else:
        # Geradeaus fahren
        command = {"axis2": -1, "axis1": 0}

    # Ergebnis visualisieren (optional)
    if display:
        result = img.copy()
        cv2.drawContours(result, [largest_contour], -1, (0, 255, 0), 2)
        cv2.circle(result, (cx, cy), 5, (255, 0, 0), -1)
        cv2.line(result, (mid_x, 0), (mid_x, height), (0, 0, 255), 2)
        cv2.imshow("Result", result)
    return command


def find_threshold():
    global threshold_value
    time.sleep(0.5)
    threshold_value = threshold_value + 1
    print(threshold_value)


if __name__ == '__main__':
    while True:
        img = wM.getImg(True, size=[240,120])
        find_threshold()
        print(follow(img, True))
        
        cv2.waitKey(1)

