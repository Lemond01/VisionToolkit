# core/camera.py
import cv2
import config

class Camera:
    """
    Responsabilidad Única: Abrir la cámara, capturar frames y liberar el recurso.
    """

    def __init__(self, camera_index: int = config.CAMERA_INDEX):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise RuntimeError(f"No se pudo abrir la cámara con índice {camera_index}.")

    def read(self):
        """Captura y devuelve un frame de la cámara."""
        success, frame = self.cap.read()
        if not success:
            return None
        return frame

    def release(self):
        """Libera la cámara."""
        self.cap.release()