# main.py
from services.focus_service import FocusService

def main():
    """Punto de entrada de la aplicación."""
    print("="*50)
    print("VisionToolkit - Focus Monitor")
    print("="*50)
    print("Controles:")
    print("  'q' - Salir y mostrar reporte")
    print("  'r' - Recalibrar")
    print("  'm' - Cambiar modo de visualización (minimalista/normal)")
    print("="*50)
    print("Iniciando aplicación...")
    print()
    
    app = FocusService()
    app.run()

if __name__ == "__main__":
    main()