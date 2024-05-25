import cv2
import numpy as np

# Liste zur Speicherung der Punkte
points = []

# Callback-Funktion für Mausklicks
def click_event(event, x, y, flags, params):
    # Überprüfen, ob die linke Maustaste geklickt wurde
    if event == cv2.EVENT_LBUTTONDOWN:
        # Punkt hinzufügen
        points.append((x, y))
        # Punkt auf dem Bild anzeigen
        cv2.circle(frame, (x,y), 50, (0,255,0), -1)
        cv2.imshow('Webcam', frame)


#Funktion zum transformieren der Punkte
def transform_image(image, pts1, pts2):
    # Erstellen der Transformationsmatrix.
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    
    # Wenden der perspektivische Transformation auf das Bild an.
    transformed_image = cv2.warpPerspective(image, matrix, (int(width), int(height)))
    
    return transformed_image

def sort_points(pts):
    # Sortieren der Punkte basierend auf ihrer x-Koordinate
    pts = sorted(pts, key=lambda x: x[0])

    # Teilen der Punkte in linke und rechte Punkte
    left_pts = pts[:2]
    right_pts = pts[2:]

    # Sortieren der linken Punkte basierend auf ihrer y-Koordinate
    left_pts = sorted(left_pts, key=lambda x: x[1])

    # Sortieren der rechten Punkte basierend auf ihrer y-Koordinate
    right_pts = sorted(right_pts, key=lambda x: x[1])

    # Die sortierte Liste der Punkte ist: oben links, oben rechts, unten links, unten rechts
    sorted_pts = [left_pts[0], right_pts[0], left_pts[1], right_pts[1]]

    return sorted_pts


# Öffnen der Webcam.
cap = cv2.VideoCapture(0)

# Lesen der Videodimensionen aus
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# Maus-Callback-Funktion zuweisen
cv2.namedWindow('Webcam')
cv2.setMouseCallback('Webcam', click_event)

while True:
    pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
    ptsreset = np.float32([[0,0],[width,0],[0,height],[width,height]])
    
    # Nehmen Sie ein Frame von der Webcam auf.
    ret, frame = cap.read()
    
    # Überprüfen Sie, ob das Frame erfolgreich aufgenommen wurde.
    if not ret:
        break

    # Wenn vier Punkte ausgewählt wurden, führen der Transformation durch
    if len(points) == 4:
        sorted_pts = sort_points(points)
        pts1 = np.float32(sorted_pts)
        frame = transform_image(frame, pts1, pts2)

    # Zeigen Sie das transformierte Bild in einem Fenster an.
    cv2.imshow('Webcam', frame)

    # [...], wenn die Taste 'q' gedrückt wird.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        frame = transform_image(frame, ptsreset, pts2)

# Schließen der Webcam und die Fenster, wenn die Schleife beendet ist.
cap.release()
cv2.destroyAllWindows()
