# services/focus_service.py
import cv2
import time
import config

from core.camera import Camera
from core.calibration import Calibration
from core.attention_monitor import AttentionMonitor
from core.alert_manager import AlertManager
from core.focus_tracker import FocusTracker
from core.eye_state_tracker import EyeStateTracker

from detectors.face_mesh_detector import FaceMeshDetector
from detectors.eye_detector import EyeDetector
from detectors.gaze_detector import GazeDetector

from ui.overlay import Overlay

class FocusService:
    """
    Servicio principal que orquesta todos los componentes.
    """
    def __init__(self):
        self.camera = Camera()
        self.face_detector = FaceMeshDetector()
        self.eye_detector = EyeDetector()
        self.gaze_detector = GazeDetector()
        self.eye_state_tracker = EyeStateTracker()
        self.attention_monitor = AttentionMonitor()
        
        # Inicializar el gestor de alertas según la configuración
        if config.ALERT_TYPE == "video":
            self.alert_manager = AlertManager(youtube_url=config.YOUTUBE_ALERT_URL)
        else:
            # Versión con sonido (puedes mantener el código original o crear un archivo separado)
            from core.alert_manager_sound import AlertManagerSound
            self.alert_manager = AlertManagerSound()
        
        self.focus_tracker = FocusTracker()
        self.calibration = Calibration()
        self.overlay = Overlay()

        self.last_time = time.time()
        self.calibration_mode = True  # Iniciar en modo calibración
        print("Calibración iniciada. Mirá fijamente a la cámara...")

    def run(self):
        """Bucle principal de la aplicación."""
        while True:
            frame = self.camera.read()
            if frame is None:
                break

            self.process_frame(frame)

            if self.handle_keyboard():
                break

        self.camera.release()
        cv2.destroyAllWindows()

    def process_frame(self, frame):
        """Procesa un único frame: detección, análisis y visualización."""
        results = self.face_detector.detect(frame)
        h, w, _ = frame.shape

        # Variables por defecto
        face_detected = False
        gaze_x, gaze_y = 0.0, 0.0
        eyes_closed = False
        attention_status = {
            "state": "NO_FACE",
            "elapsed": 0.0,
            "progress": 0.0,
            "is_distracted": False
        }

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                face_detected = True

                # 1. Obtener puntos de los ojos y calcular EAR
                left_eye_points = self.eye_detector.get_eye_points(
                    face_landmarks, EyeDetector.LEFT_EYE_INDEXES
                )
                right_eye_points = self.eye_detector.get_eye_points(
                    face_landmarks, EyeDetector.RIGHT_EYE_INDEXES
                )
                left_ear = self.eye_detector.calculate_ear(left_eye_points)
                right_ear = self.eye_detector.calculate_ear(right_eye_points)

                # 2. Actualizar el estado de los ojos
                eyes_closed = self.eye_state_tracker.update(left_ear, right_ear)

                # 3. Obtener la mirada (iris)
                gaze_x, gaze_y = self.gaze_detector.get_ratio(face_landmarks)

                # 4. Calibración (si está activa)
                if self.calibration_mode:
                    self.calibration.add_sample(gaze_x, gaze_y)
                    if self.calibration.is_calibrated:
                        self.calibration_mode = False
                        print("Calibración completada. Iniciando monitoreo...")
                        # Actualizar configuración con los valores calibrados
                        config.GAZE_CENTER_X = self.calibration.center_x
                        config.GAZE_CENTER_Y = self.calibration.center_y
                    
                    # Durante la calibración, mostrar visualización ligera
                    # Dibujar rectángulo facial y ojos
                    frame = self.face_detector.draw_face_landmarks_light(frame, results)
                    # Dibujar pupila en color amarillo durante calibración
                    frame = self.gaze_detector.draw_pupil(frame, face_landmarks, color=(0, 255, 255))
                    
                    # Mostrar texto de calibración
                    cv2.putText(frame, "CALIBRANDO...", (frame.shape[1]//2 - 80, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                    
                    self._display_frame(frame, attention_status)
                    return

        # Si no estamos en calibración, procesamos la atención
        if not self.calibration_mode:
            # 5. Actualizar el monitor de atención
            attention_status = self.attention_monitor.update(
                face_detected, gaze_x, gaze_y, eyes_closed
            )

            # 6. Actualizar el gestor de alertas
            self.alert_manager.update(attention_status["is_distracted"])

            # 7. Actualizar el tracker de enfoque
            current_time = time.time()
            delta_time = current_time - self.last_time
            self.last_time = current_time
            self.focus_tracker.update(attention_status["is_distracted"], delta_time)

            # 8. Dibujar visualización limpia según el estado
            if face_detected and results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    # Elegir modo de visualización
                    if config.MINIMAL_MODE:
                        frame = self.face_detector.draw_minimal(frame, results)
                    else:
                        # Dibujar visualización limpia (rectángulo facial + ojos)
                        frame = self.face_detector.draw_face_landmarks_light(frame, results)
                    
                    # Dibujar la pupila con color según el estado
                    if attention_status["is_distracted"]:
                        # Rojo si está distraído
                        frame = self.gaze_detector.draw_pupil(frame, face_landmarks, color=(0, 0, 255))
                    else:
                        # Verde si está concentrado
                        frame = self.gaze_detector.draw_pupil(frame, face_landmarks, color=(0, 255, 0))
                    
                    # Opcional: Dibujar dirección de la mirada (desactivado por defecto)
                    frame = self.gaze_detector.draw_gaze_direction(frame, face_landmarks, gaze_x, gaze_y)
                    
                    # Si los ojos están cerrados, mostrar un mensaje
                    if eyes_closed:
                        cv2.putText(frame, "Ojos Cerrados", (20, frame.shape[1] - 30),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            else:
                # No se detecta rostro
                cv2.putText(frame, "No se detecta rostro", (frame.shape[1]//2 - 100, frame.shape[0]//2),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # 9. Mostrar la interfaz
        self._display_frame(frame, attention_status)

    def _display_frame(self, frame, attention_status):
        """Dibuja el overlay y muestra el frame."""
        # Obtener estadísticas del tracker
        report = self.focus_tracker.get_report()

        # Dibujar overlay
        frame = self.overlay.draw(
            frame,
            attention_status,
            report["distraction_events"],
            report["focused_minutes"],
            report["total_minutes"]
        )

        cv2.imshow("VisionToolkit - Focus Monitor", frame)

    def handle_keyboard(self):
        """Maneja la entrada del teclado."""
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("\n--- Reporte de la Sesión ---")
            report = self.focus_tracker.get_report()
            print(f"Total de la sesión: {report['total_minutes']} min")
            print(f"Tiempo enfocado: {report['focused_minutes']} min")
            print(f"Tiempo distraído: {report['distracted_minutes']} min")
            print(f"Número de distracciones: {report['distraction_events']}")
            return True
        elif key == ord('r'):  # Tecla 'r' para recalibrar
            print("Recalibrando... Mirá fijamente a la cámara.")
            self.calibration.reset()
            self.calibration_mode = True
            # Reiniciar tracker para empezar una nueva sesión
            self.focus_tracker.reset()
        elif key == ord('m'):  # Tecla 'm' para cambiar modo de visualización
            # Alternar entre modo minimalista y normal
            config.MINIMAL_MODE = not config.MINIMAL_MODE
            print(f"Modo minimalista: {config.MINIMAL_MODE}")
        return False