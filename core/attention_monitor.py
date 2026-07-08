# core/attention_monitor.py
import time
import config
from core.state_machine import AttentionState

class AttentionMonitor:
    """
    Responsabilidad Única: Evaluar el estado de atención del usuario basado en
    datos de la cámara (mirada, detección de rostro, estado de los ojos).
    """
    def __init__(self):
        self.distraction_start_time = None
        self.current_state = AttentionState.FOCUSED

    def update(self, face_detected: bool, gaze_x: float, gaze_y: float, eyes_closed: bool) -> dict:
        """
        Actualiza el estado de atención y retorna un diccionario con el estado,
        el tiempo de distracción y el progreso.
        """
        # Determinar el estado actual basado en los inputs
        if not face_detected:
            new_state = AttentionState.NO_FACE
        elif eyes_closed:
            new_state = AttentionState.EYES_CLOSED
        elif self._is_looking_away(gaze_x, gaze_y):
            new_state = AttentionState.LOOKING_AWAY
        else:
            new_state = AttentionState.FOCUSED

        # Lógica de temporizador
        if new_state != AttentionState.FOCUSED:
            if self.distraction_start_time is None:
                self.distraction_start_time = time.time()
            elapsed = time.time() - self.distraction_start_time
            is_distracted = elapsed >= config.DISTRACTION_TIME
            progress = min(elapsed / config.DISTRACTION_TIME, 1.0)
        else:
            self.distraction_start_time = None
            elapsed = 0.0
            is_distracted = False
            progress = 0.0

        self.current_state = new_state

        return {
            "state": new_state.value,
            "elapsed": elapsed,
            "progress": progress,
            "is_distracted": is_distracted
        }

    def _is_looking_away(self, gaze_x: float, gaze_y: float) -> bool:
        """Verifica si la mirada está fuera de los márgenes establecidos."""
        center_x = config.GAZE_CENTER_X
        center_y = config.GAZE_CENTER_Y
        margin_x = config.GAZE_HORIZONTAL_MARGIN
        margin_y = config.GAZE_VERTICAL_MARGIN

        if (gaze_x < center_x - margin_x or gaze_x > center_x + margin_x or
            gaze_y < center_y - margin_y or gaze_y > center_y + margin_y):
            return True
        return False