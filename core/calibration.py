# core/calibration.py
import numpy as np
import config

class Calibration:
    """
    Responsabilidad Única: Recopilar datos durante un período de tiempo
    y calcular la media de la posición del iris para la calibración.
    """
    def __init__(self):
        self.gaze_data_x = []
        self.gaze_data_y = []
        self.is_calibrated = False
        self.center_x = config.GAZE_CENTER_X
        self.center_y = config.GAZE_CENTER_Y

    def add_sample(self, gaze_x: float, gaze_y: float):
        """Añade un punto de datos de la mirada para la calibración."""
        if not self.is_calibrated:
            self.gaze_data_x.append(gaze_x)
            self.gaze_data_y.append(gaze_y)

            # Si tenemos suficientes muestras, calculamos la media
            if len(self.gaze_data_x) >= config.CALIBRATION_FRAMES:
                self.center_x = np.mean(self.gaze_data_x)
                self.center_y = np.mean(self.gaze_data_y)
                self.is_calibrated = True
                print(f"Calibración completada. Centro X: {self.center_x:.3f}, Centro Y: {self.center_y:.3f}")

    def reset(self):
        """Reinicia la calibración."""
        self.gaze_data_x = []
        self.gaze_data_y = []
        self.is_calibrated = False
        self.center_x = config.GAZE_CENTER_X
        self.center_y = config.GAZE_CENTER_Y