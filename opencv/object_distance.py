import cv2
import numpy as np
from urllib.request import urlopen

# URL der ESP32-CAM
url = 'http://192.168.8.186:81/capture'

# Tatsächliche Breite der Tasse (in cm)
KNOWN_WIDTH = 8.0

# Kalibrierungsentfernung (in cm)
KNOWN_DISTANCE = 33.0

# Laden der MobileNet SSD-Modell-Dateien
net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "mobilenet_iter_73000.caffemodel")

# Klassenbezeichnungen des Modells
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor", "cup"]

# Kalibriere die Brennweite
def calculate_focal_length(known_distance, known_width, object_width_in_image):
    return (object_width_in_image * known_distance) / known_width

# Berechne die Entfernung zum Objekt
def calculate_distance(focal_length, known_width, object_width_in_image):
    return (known_width * focal_length) / object_width_in_image

# Initialisiere die Brennweite (wird bei der Kalibrierung gesetzt)
focal_length = None

while True:
    # Bild vom Stream abrufen
    img_resp = urlopen(url)
    imgnp = np.asarray(bytearray(img_resp.read()), dtype="uint8")
    img = cv2.imdecode(imgnp, -1)

    # Bild um 90 Grad gegen den Uhrzeigersinn drehen
    rotated_img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # Bildgröße und Blob erstellen
    (h, w) = rotated_img.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(rotated_img, (300, 300)), 0.007843, (300, 300), 127.5)

    # Blob in das Netzwerk einspeisen
    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # Nur Objekte mit einer Mindestwahrscheinlichkeit anzeigen
        if confidence > 0.2:
            idx = int(detections[0, 0, i, 1])
            label = CLASSES[idx]

            if True or label == "cup":
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # Breite des Objekts im Bild
                object_width_in_image = endX - startX

                # Kalibrierung der Brennweite, wenn sie noch nicht gesetzt ist
                if focal_length is None:
                    focal_length = calculate_focal_length(KNOWN_DISTANCE, KNOWN_WIDTH, object_width_in_image)
                    print(f"Kalibrierte Brennweite: {focal_length:.2f}")

                # Entfernung berechnen
                distance = calculate_distance(focal_length, KNOWN_WIDTH, object_width_in_image)
                print(f"Entfernung zur Tasse: {distance:.2f} cm")

                # Rechteck um die erkannte Tasse zeichnen
                cv2.rectangle(rotated_img, (startX, startY), (endX, endY), (0, 255, 0), 2)
                text = f"{label}: {confidence:.2f}, Dist: {distance:.2f} cm"
                cv2.putText(rotated_img, text, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Das gedrehte Bild anzeigen
    cv2.imshow("ESP32-CAM Object Detection (Rotated 90 Degrees)", rotated_img)

    # Beenden mit der Taste 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()