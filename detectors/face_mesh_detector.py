# detectors/face_mesh_detector.py
import cv2
import mediapipe as mp
import config

class FaceMeshDetector:
    """
    Responsabilidad Única: Detectar los landmarks faciales usando MediaPipe.
    """
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.drawing_utils = mp.solutions.drawing_utils
        
        # Índices de landmarks para el contorno facial (para el rectángulo)
        self.FACE_OVAL = [
            10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
            397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
            172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109
        ]

    def detect(self, frame):
        """Procesa un frame BGR y retorna los resultados de MediaPipe."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        return results

    def draw_face_box(self, frame, face_landmarks, color=(0, 255, 0), thickness=2):
        """
        Dibuja un rectángulo alrededor del rostro basado en los landmarks.
        """
        if not config.DRAW_FACE_BOX:
            return frame
        
        h, w, _ = frame.shape
        
        # Obtener todos los puntos del contorno facial
        points = []
        for idx in self.FACE_OVAL:
            landmark = face_landmarks.landmark[idx]
            x, y = int(landmark.x * w), int(landmark.y * h)
            points.append((x, y))
        
        # Encontrar los límites del rostro
        if points:
            x_coords = [p[0] for p in points]
            y_coords = [p[1] for p in points]
            
            # Añadir un pequeño margen (10 píxeles)
            margin = 10
            x_min = max(0, min(x_coords) - margin)
            x_max = min(w, max(x_coords) + margin)
            y_min = max(0, min(y_coords) - margin)
            y_max = min(h, max(y_coords) + margin)
            
            # Dibujar el rectángulo
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, thickness)
            
            # Dibujar un borde más fino alrededor para efecto glow
            cv2.rectangle(frame, (x_min-2, y_min-2), (x_max+2, y_max+2), 
                         (0, 255, 0), 1, cv2.LINE_AA)
            
            return (x_min, y_min, x_max, y_max)  # Retornar las coordenadas del box
        
        return None

    def draw_eyes(self, frame, face_landmarks):
        """
        Dibuja círculos alrededor de los ojos con colores específicos.
        Ojo izquierdo: Azul, Ojo derecho: Cyan
        """
        if not config.DRAW_EYE_CIRCLES:
            return frame
        
        h, w, _ = frame.shape
        
        # Índices de los ojos (puntos clave para delimitar)
        LEFT_EYE_POINTS = [33, 133, 157, 158, 159, 160, 161, 173]
        RIGHT_EYE_POINTS = [362, 263, 387, 386, 385, 384, 398, 466]
        
        # Dibujar ojo izquierdo (azul)
        left_points = []
        for idx in LEFT_EYE_POINTS:
            landmark = face_landmarks.landmark[idx]
            x, y = int(landmark.x * w), int(landmark.y * h)
            left_points.append((x, y))
        
        if left_points:
            # Calcular el centro y radio aproximado del ojo
            center_x = sum(p[0] for p in left_points) // len(left_points)
            center_y = sum(p[1] for p in left_points) // len(left_points)
            radius = int(((max(p[0] for p in left_points) - min(p[0] for p in left_points)) / 2) * 1.2)
            
            # Dibujar círculo alrededor del ojo izquierdo (azul)
            cv2.circle(frame, (center_x, center_y), radius, (255, 100, 0), 2, cv2.LINE_AA)
            # Relleno semi-transparente
            overlay = frame.copy()
            cv2.circle(overlay, (center_x, center_y), radius, (255, 100, 0), -1)
            cv2.addWeighted(overlay, 0.15, frame, 0.85, 0, frame)
        
        # Dibujar ojo derecho (cyan)
        right_points = []
        for idx in RIGHT_EYE_POINTS:
            landmark = face_landmarks.landmark[idx]
            x, y = int(landmark.x * w), int(landmark.y * h)
            right_points.append((x, y))
        
        if right_points:
            center_x = sum(p[0] for p in right_points) // len(right_points)
            center_y = sum(p[1] for p in right_points) // len(right_points)
            radius = int(((max(p[0] for p in right_points) - min(p[0] for p in right_points)) / 2) * 1.2)
            
            # Dibujar círculo alrededor del ojo derecho (cyan)
            cv2.circle(frame, (center_x, center_y), radius, (255, 255, 0), 2, cv2.LINE_AA)
            # Relleno semi-transparente
            overlay = frame.copy()
            cv2.circle(overlay, (center_x, center_y), radius, (255, 255, 0), -1)
            cv2.addWeighted(overlay, 0.15, frame, 0.85, 0, frame)
        
        return frame

    def draw_face_landmarks_light(self, frame, results):
        """
        Dibuja una versión liviana de los landmarks (solo puntos clave).
        """
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # 1. Dibujar rectángulo verde alrededor del rostro
                self.draw_face_box(frame, face_landmarks)
                
                # 2. Dibujar círculos alrededor de los ojos
                self.draw_eyes(frame, face_landmarks)
                
                # 3. Dibujar puntos clave de la cara (nariz, boca) en color gris suave
                h, w, _ = frame.shape
                
                # Nariz (punto central)
                nose_tip = face_landmarks.landmark[1]
                nx, ny = int(nose_tip.x * w), int(nose_tip.y * h)
                cv2.circle(frame, (nx, ny), 3, (150, 150, 150), -1)
                
                # Boca (puntos de los labios)
                mouth_points = [61, 291, 78, 308, 0, 13, 14, 17]
                for idx in mouth_points:
                    landmark = face_landmarks.landmark[idx]
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(frame, (x, y), 2, (150, 150, 150), -1)
        
        return frame

    def draw_minimal(self, frame, results):
        """
        Versión minimalista: solo rectángulo facial y puntos clave muy pequeños.
        """
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                h, w, _ = frame.shape
                
                # Rectángulo facial (verde, más delgado)
                self.draw_face_box(frame, face_landmarks, color=(0, 255, 0), thickness=1)
                
                # Solo unos pocos puntos clave (nariz, ojos, boca)
                key_points = [1, 33, 133, 362, 263, 61, 291]  # Nariz, ojos, boca
                for idx in key_points:
                    landmark = face_landmarks.landmark[idx]
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(frame, (x, y), 2, (100, 255, 100), -1)
        
        return frame