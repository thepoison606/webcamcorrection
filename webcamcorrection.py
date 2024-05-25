import cv2
import numpy as np

#BLABLABLABLA

# Liste zur Speicherung der Punkte
points = []
transformation_applied = False

# Callback-Funktion für Mausklicks
def click_event(event, x, y, flags, params):
    global points, transformation_applied
    # Überprüfen, ob die linke Maustaste geklickt wurde
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            # Punkt hinzufügen
            points.append((x, y))
            # Punkt auf dem Bild anzeigen
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow('Webcam', frame)
            # Überprüfen, ob vier Punkte ausgewählt wurden
            if len(points) == 4:
                transformation_applied = True
        else:
            # Zurücksetzen der Punkte und Transformation deaktivieren
            points = []
            transformation_applied = False

# Funktion zum Transformieren der Punkte
def transform_image(image, pts1, pts2):
    # Erstellen der Transformationsmatrix
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    
    # Anwenden der perspektivische Transformation auf das Bild.
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

# Öffnen der Webcam
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
    
    # Aufnahme eines Frames
    ret, frame = cap.read()
    
    # Überprüfen , ob das Frame erfolgreich aufgenommen wurde.
    if not ret:
        break

    # Markiere die geklickten Punkte
    for point in points:
        cv2.circle(frame, point, 5, (0, 255, 0), -1)

    # Wenn vier Punkte ausgewählt wurden, Transformation anwenden
    if transformation_applied:
        sorted_pts = sort_points(points)
        pts1 = np.float32(sorted_pts)
        frame = transform_image(frame, pts1, pts2)

    # Anzeigen des transformierte Bildes in einem Fenster .
    cv2.imshow('Webcam', frame)

    # Beenden der Schleife, wenn die Taste 'q' gedrückt wird
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Schließen der Webcam und der Fenster, wenn die Schleife beendet ist.
cap.release()
cv2.destroyAllWindows()
