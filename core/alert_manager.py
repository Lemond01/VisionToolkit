# core/alert_manager.py
import webbrowser
import time
import threading
import platform
import config

class AlertManager:
    """
    Responsabilidad Única: Gestionar la alerta visual (video de YouTube) cuando hay distracción.
    """
    def __init__(self, youtube_url=None):
        """
        Inicializa el gestor de alertas.
        :param youtube_url: URL del video de YouTube a reproducir
        """
        self.youtube_url = youtube_url or config.YOUTUBE_ALERT_URL
        self.is_playing = False
        self.browser_tab_opened = False
        self.alert_thread = None
        self.stop_alert_flag = False
        
        # Detectar el sistema operativo
        self.os_name = platform.system()
        print(f"Sistema operativo detectado: {self.os_name}")
        print(f"Video de alerta: {self.youtube_url}")

    def start(self):
        """Abre el video de YouTube en el navegador."""
        if not self.is_playing:
            print("🔴 ALERTA: Abriendo video de YouTube...")
            
            # Abrir el video en el navegador predeterminado
            webbrowser.open(self.youtube_url)
            self.is_playing = True
            self.browser_tab_opened = True
            
            # Iniciar un hilo para monitorear y cerrar la pestaña si es necesario
            if self.alert_thread is None or not self.alert_thread.is_alive():
                self.stop_alert_flag = False
                self.alert_thread = threading.Thread(target=self._monitor_alert)
                self.alert_thread.daemon = True
                self.alert_thread.start()

    def stop(self):
        """Detiene la alerta y cierra la pestaña del navegador."""
        if self.is_playing and self.browser_tab_opened:
            print("🟢 Enfoque recuperado. Cerrando video...")
            self.stop_alert_flag = True
            self._close_browser_tab()
            self.is_playing = False
            self.browser_tab_opened = False
            
            # Esperar a que el hilo termine
            if self.alert_thread and self.alert_thread.is_alive():
                self.alert_thread.join(timeout=0.5)

    def update(self, is_distracted: bool):
        """Actualiza el estado de la alerta basado en si hay distracción."""
        if is_distracted:
            self.start()
        else:
            self.stop()

    def _monitor_alert(self):
        """Monitorea si la alerta debe detenerse."""
        while not self.stop_alert_flag:
            time.sleep(0.1)
        
        # Si se detiene, asegurar que se cierre la pestaña
        if self.browser_tab_opened:
            self._close_browser_tab()

    def _close_browser_tab(self):
        """Cierra la pestaña activa del navegador usando atajos de teclado."""
        try:
            # Intentar importar pyautogui
            try:
                import pyautogui
                # Dar tiempo para que el navegador esté enfocado
                time.sleep(config.BROWSER_CLOSE_DELAY)
                
                # Cerrar pestaña según el sistema operativo
                if self.os_name == "Windows":
                    pyautogui.hotkey('ctrl', 'w')
                elif self.os_name == "Darwin":  # macOS
                    pyautogui.hotkey('command', 'w')
                elif self.os_name == "Linux":
                    pyautogui.hotkey('ctrl', 'w')
                else:
                    pyautogui.hotkey('ctrl', 'w')
                
                print("✅ Pestaña del navegador cerrada")
                self.browser_tab_opened = False
                return
                
            except ImportError:
                print("⚠️ pyautogui no instalado. Instálalo con: pip install pyautogui")
                print("💡 Cierra la pestaña manualmente con Ctrl+W o Cmd+W")
                
        except Exception as e:
            print(f"⚠️ Error al cerrar la pestaña del navegador: {e}")
            print("💡 Puedes cerrar la pestaña manualmente con Ctrl+W (Windows/Linux) o Cmd+W (macOS)")

    def set_youtube_url(self, url):
        """Cambia la URL del video de YouTube."""
        self.youtube_url = url
        print(f"URL del video actualizada: {url}")