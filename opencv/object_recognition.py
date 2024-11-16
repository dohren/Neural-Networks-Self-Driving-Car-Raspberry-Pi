import cv2
import numpy as np
import ESP32camModule as wM

# Laden der MobileNet SSD-Modell-Dateien
net = cv2.dnn.readNetFromCaffe("opencv/deploy.prototxt", "opencv/mobilenet_iter_73000.caffemodel")

# Klassenbezeichnungen des Modells
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor", "cup"]

while True:
    # Bild holen
    img = wM.getImg();

    # Bildgröße und Blob erstellen
    (h, w) = img.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 0.007843, (300, 300), 127.5)

    # Blob in das Netzwerk einspeisen
    net.setInput(blob)
    detections = net.forward()

    # Alle erkannten Objekte durchgehen
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # Nur Objekte mit einer Mindestwahrscheinlichkeit anzeigen
        if confidence > 0.2:
            idx = int(detections[0, 0, i, 1])
            label = CLASSES[idx]

            # Nur 'cup' anzeigen
            if True or label == "cup":
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # Rechteck um die erkannte Tasse zeichnen
                cv2.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0), 2)
                text = f"{label}: {confidence:.2f}"
                cv2.putText(img, text, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Das Bild anzeigen
    cv2.imshow("ESP32-CAM Object Detection", img)

    # Beenden mit der Taste 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
