# detectors/gaze_detector.py
import cv2
import config

class GazeDetector:
    """
    Responsabilidad Única: Calcular la dirección de la mirada basada en la posición del iris.
    """
    LEFT_IRIS_INDEX = 468  # Centro del iris izquierdo
    RIGHT_IRIS_INDEX = 473  # Centro del iris derecho (no se usa, pero está disponible)

    @staticmethod
    def get_ratio(face_landmarks):
        """
        Calcula la posición normalizada (x, y) del centro del iris izquierdo.
        Retorna un tuple (gaze_x, gaze_y) con valores entre 0 y 1.
        """
        iris = face_landmarks.landmark[GazeDetector.LEFT_IRIS_INDEX]
        return iris.x, iris.y

    @staticmethod
    def draw_pupil(frame, face_landmarks, color=(0, 255, 0), size=5):
        """
        Dibuja un círculo grande y brillante en la pupila para un mejor seguimiento.
        """
        if not config.DRAW_PUPIL:
            return frame
        
        h, w, _ = frame.shape
        iris = face_landmarks.landmark[GazeDetector.LEFT_IRIS_INDEX]
        cx, cy = int(iris.x * w), int(iris.y * h)
        
        # Dibujar un círculo con resplandor (glow effect)
        # Círculos exteriores (brillo)
        for radius in range(size + 4, size - 1, -2):
            cv2.circle(frame, (cx, cy), radius, color, 1)
        
        # Círculo interior (sólido)
        cv2.circle(frame, (cx, cy), size, color, -1)
        
        # Punto blanco en el centro (reflejo)
        cv2.circle(frame, (cx - 1, cy - 1), 2, (255, 255, 255), -1)
        
        return frame

    @staticmethod
    def draw_gaze_direction(frame, face_landmarks, gaze_x, gaze_y, color=(0, 255, 255)):
        """
        Dibuja una línea desde el ojo hasta la dirección de la mirada.
        Útil para depuración y para visualizar hacia dónde mira el usuario.
        """
        if not config.DRAW_GAZE_DIRECTION:
            return frame
        
        h, w, _ = frame.shape
        iris = face_landmarks.landmark[GazeDetector.LEFT_IRIS_INDEX]
        cx, cy = int(iris.x * w), int(iris.y * h)
        
        # Calcular el punto final de la línea (dirección de la mirada)
        # Multiplicamos por un factor para que la línea sea visible
        end_x = int(cx + (gaze_x - 0.5) * 200)
        end_y = int(cy + (gaze_y - 0.5) * 200)
        
        # Dibujar línea de dirección
        cv2.line(frame, (cx, cy), (end_x, end_y), color, 2, cv2.LINE_AA)
        
        # Dibujar un círculo en el punto final
        cv2.circle(frame, (end_x, end_y), 5, color, -1)
        
        return frame