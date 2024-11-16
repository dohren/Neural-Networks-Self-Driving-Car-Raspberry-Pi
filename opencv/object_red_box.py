import cv2
import numpy as np
import ESP32camModule as wM

while True:
    # Bild holen
    img = wM.getImg()

    # Bild in HSV-Farbraum umwandeln
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Grenzen für die Farbe Rot festlegen
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Maske für rote Farbe erstellen
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.add(mask1, mask2)

    # Rauschunterdrückung und Maske verbessern
    kernel = np.ones((7, 7), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # Konturen der roten Objekte finden
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Konturen durchgehen und konvexe Hülle verwenden
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # Mindestgröße der Konturen
            hull = cv2.convexHull(contour)
            x, y, w, h = cv2.boundingRect(hull)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, "Red Object", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Das Bild anzeigen
    cv2.imshow("Red Object Detection", img)

    # Beenden mit der Taste 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()