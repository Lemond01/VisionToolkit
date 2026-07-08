# detectors/head_pose_detector.py
import cv2
import numpy as np

class HeadPoseDetector:
    """
    Responsabilidad Única: Calcular la pose de la cabeza.
    (Actualmente no se usa en el flujo principal, pero se mantiene para futuros proyectos)
    """
    def __init__(self):
        self.model_points = np.array([
            (0.0, 0.0, 0.0),          # Nariz
            (0.0, -330.0, -65.0),     # Barbilla
            (-225.0, 170.0, -135.0),  # Ojo izquierdo
            (225.0, 170.0, -135.0),   # Ojo derecho
            (-150.0, -150.0, -125.0), # Boca izquierda
            (150.0, -150.0, -125.0)   # Boca derecha
        ])

    def get_rotation(self, face_landmarks, width, height):
        """Calcula la rotación de la cabeza basada en los landmarks."""
        image_points = np.array([
            (face_landmarks.landmark[1].x * width, face_landmarks.landmark[1].y * height),      # Nariz
            (face_landmarks.landmark[152].x * width, face_landmarks.landmark[152].y * height),  # Barbilla
            (face_landmarks.landmark[33].x * width, face_landmarks.landmark[33].y * height),    # Ojo izquierdo
            (face_landmarks.landmark[263].x * width, face_landmarks.landmark[263].y * height),  # Ojo derecho
            (face_landmarks.landmark[61].x * width, face_landmarks.landmark[61].y * height),    # Boca izquierda
            (face_landmarks.landmark[291].x * width, face_landmarks.landmark[291].y * height)   # Boca derecha
        ], dtype="double")

        focal_length = width
        center = (width / 2, height / 2)
        
        camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype="double")

        dist_coeffs = np.zeros((4, 1))
        
        success, rotation_vector, translation_vector = cv2.solvePnP(
            self.model_points,
            image_points,
            camera_matrix,
            dist_coeffs
        )
        
        rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
        angles, _, _, _, _, _ = cv2.RQDecomp3x3(rotation_matrix)
        
        return angles