import os
from app import create_app

# Usa "development" por defecto si no se especifica APP_ENV
env = os.getenv("APP_ENV", "development")

# Crea la app con la configuración correspondiente
app = create_app(env)

if __name__ == "__main__":
    # Ejecuta en modo debug solo si no es producción
    debug_mode = env != "production"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)

