# core/alert_manager_sound.py
import pygame
import os

class AlertManagerSound:
    """
    Responsabilidad Única: Gestionar la reproducción de la alerta sonora.
    """
    def __init__(self):
        pygame.mixer.init()
        sound_path = os.path.join("assets", "Pokémon-RB-Victory-Theme.wav")
        self.sound = pygame.mixer.Sound(sound_path)
        self.is_playing = False

    def start(self):
        """Reproduce la alerta en bucle."""
        if not self.is_playing:
            self.sound.play(-1)
            self.is_playing = True

    def stop(self):
        """Detiene la alerta."""
        if self.is_playing:
            self.sound.stop()
            self.is_playing = False

    def update(self, is_distracted: bool):
        """Actualiza el estado de la alerta basado en si hay distracción."""
        if is_distracted:
            self.start()
        else:
            self.stop()