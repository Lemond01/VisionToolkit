# config.py
# Archivo de configuración central. Todos los parámetros ajustables están aquí.

# --- TIEMPOS ---
DISTRACTION_TIME = 5.0          # Tiempo (en segundos) para considerar una distracción
EYE_CLOSE_TIME = 2.0            # Tiempo (en segundos) con ojos cerrados para considerarlo distracción

# --- MIRADA ---
# Estos valores se sobreescribirán durante la calibración.
# Se usan como valores por defecto.
GAZE_HORIZONTAL_MARGIN = 0.18   # Tolerancia horizontal (±) para la mirada
GAZE_VERTICAL_MARGIN = 0.12     # Tolerancia vertical (±) para la mirada
GAZE_CENTER_X = 0.5             # Centro X de la mirada (se calibra)
GAZE_CENTER_Y = 0.5             # Centro Y de la mirada (se calibra)

# --- CALIBRACIÓN ---
CALIBRATION_FRAMES = 30         # Número de frames para la calibración (aprox. 1-2 segundos a 30 FPS)

# --- CÁMARA ---
CAMERA_INDEX = 0                # Índice de la cámara (por defecto, 0)

# --- ALERTAS ---
# URL del video de YouTube para la alerta
YOUTUBE_ALERT_URL = "https://www.youtube.com/watch?v=QkKNJr7ZMgc?autoplay=1"  # Cambia por tu video

# Tipo de alerta: 'sound' o 'video'
ALERT_TYPE = "video"  # 'sound' para usar el audio, 'video' para usar YouTube

# Tiempo de espera antes de cerrar la pestaña (segundos)
BROWSER_CLOSE_DELAY = 0.5

# --- VISUALIZACIÓN ---
MINIMAL_MODE = False           # Modo ultra minimalista (solo rectángulo y puntos clave)
DRAW_FACE_BOX = True           # Mostrar rectángulo alrededor del rostro
DRAW_EYE_CIRCLES = True        # Mostrar círculos alrededor de los ojos
DRAW_PUPIL = True              # Mostrar la pupila con resplandor
DRAW_GAZE_DIRECTION = False    # Mostrar línea de dirección de la mirada