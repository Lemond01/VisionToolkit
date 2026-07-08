# core/eye_state_tracker.py
import time
import config

class EyeStateTracker:
    """
    Responsabilidad Única: Rastrear si los ojos están cerrados durante un período de tiempo.
    """
    def __init__(self):
        self.closed_start_time = None
        self.eyes_closed = False

    def update(self, left_ear: float, right_ear: float, ear_threshold: float = 0.20):
        """
        Actualiza el estado de los ojos basado en el EAR (Eye Aspect Ratio).
        Retorna True si los ojos han estado cerrados más de EYE_CLOSE_TIME segundos.
        """
        average_ear = (left_ear + right_ear) / 2.0

        if average_ear < ear_threshold:
            if not self.eyes_closed:
                self.eyes_closed = True
                self.closed_start_time = time.time()
        else:
            self.eyes_closed = False
            self.closed_start_time = None

        # Si los ojos han estado cerrados más del tiempo permitido, consideramos que es una distracción
        if self.closed_start_time is not None:
            elapsed = time.time() - self.closed_start_time
            if elapsed >= config.EYE_CLOSE_TIME:
                return True

        return False

    def get_closed_time(self):
        """Retorna el tiempo que los ojos llevan cerrados."""
        if self.closed_start_time is not None:
            return time.time() - self.closed_start_time
        return 0.0