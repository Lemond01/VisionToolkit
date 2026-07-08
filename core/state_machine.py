# core/state_machine.py
from enum import Enum

class AttentionState(Enum):
    """Estados posibles de atención del usuario."""
    FOCUSED = "FOCUSED"
    LOOKING_AWAY = "LOOKING_AWAY"
    NO_FACE = "NO_FACE"
    EYES_CLOSED = "EYES_CLOSED"