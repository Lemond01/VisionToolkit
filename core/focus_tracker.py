# core/focus_tracker.py
import time

class FocusTracker:
    """
    Responsabilidad Única: Rastrear estadísticas de enfoque y distracción a lo largo del tiempo.
    Es un componente genérico que podría reutilizarse para otros proyectos.
    """
    def __init__(self):
        self.start_time = time.time()
        self.focus_time = 0.0
        self.distraction_time = 0.0
        self.distraction_events = 0
        self.was_distracted = False

    def update(self, is_distracted: bool, delta_time: float):
        """Actualiza las estadísticas con el estado actual y el tiempo transcurrido."""
        if is_distracted:
            self.distraction_time += delta_time
            if not self.was_distracted:
                self.distraction_events += 1
        else:
            self.focus_time += delta_time

        self.was_distracted = is_distracted

    def get_report(self) -> dict:
        """Retorna un reporte de las estadísticas de la sesión."""
        total_time = self.focus_time + self.distraction_time
        return {
            "total_minutes": round(total_time / 60.0, 2),
            "focused_minutes": round(self.focus_time / 60.0, 2),
            "distracted_minutes": round(self.distraction_time / 60.0, 2),
            "distraction_events": self.distraction_events,
        }

    def reset(self):
        """Reinicia todas las estadísticas."""
        self.start_time = time.time()
        self.focus_time = 0.0
        self.distraction_time = 0.0
        self.distraction_events = 0
        self.was_distracted = False