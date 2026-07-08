# detectors/eye_detector.py
import math

class EyeDetector:
    """
    Responsabilidad Única: Calcular el EAR (Eye Aspect Ratio) a partir de los landmarks.
    """
    LEFT_EYE_INDEXES = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE_INDEXES = [362, 385, 387, 263, 373, 380]

    @staticmethod
    def get_eye_points(face_landmarks, eye_indexes):
        """Extrae los puntos (x, y) de un ojo dado."""
        points = []
        for index in eye_indexes:
            landmark = face_landmarks.landmark[index]
            points.append((landmark.x, landmark.y))
        return points

    @staticmethod
    def calculate_ear(eye_points):
        """Calcula el Eye Aspect Ratio para un ojo."""
        # Distancias verticales
        v1 = math.dist(eye_points[1], eye_points[5])
        v2 = math.dist(eye_points[2], eye_points[4])
        # Distancia horizontal
        h = math.dist(eye_points[0], eye_points[3])
        # EAR
        ear = (v1 + v2) / (2.0 * h)
        return ear