# ui/overlay.py
import cv2

class Overlay:
    """
    Responsabilidad Única: Dibujar la información en el frame (UI).
    """
    def draw(self, frame, attention_status, distraction_events, focused_minutes, total_minutes):
        """Dibuja el overlay con el estado de atención, estadísticas y barra de progreso."""
        # Copiar el frame para no modificar el original
        display = frame.copy()

        # Obtener datos del estado
        state = attention_status["state"]
        progress = attention_status["progress"]
        elapsed = attention_status["elapsed"]

        # Colores y textos
        is_distracted = attention_status["is_distracted"]
        color = (0, 0, 255) if is_distracted else (0, 255, 0)  # Rojo si distraído, Verde si concentrado
        status_text = state

        # 1. Estado principal (arriba a la izquierda)
        cv2.putText(display, f"Estado: {status_text}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        # 2. Estadísticas
        cv2.putText(display, f"Distracciones: {distraction_events}", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(display, f"Enfoque: {focused_minutes:.1f} min", (20, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(display, f"Sesión: {total_minutes:.1f} min", (20, 140),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        # 3. Barra de progreso de distracción
        bar_x, bar_y = 20, 170
        bar_width, bar_height = 300, 20
        cv2.rectangle(display, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height),
                      (80, 80, 80), 2)
        # Llenar la barra según el progreso
        fill_width = int(progress * bar_width)
        cv2.rectangle(display, (bar_x, bar_y), (bar_x + fill_width, bar_y + bar_height),
                      (0, 255, 0), -1)

        # 4. Texto del tiempo de distracción
        cv2.putText(display, f"Tiempo: {elapsed:.1f}s / 5.0s", (bar_x, bar_y + bar_height + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        return display