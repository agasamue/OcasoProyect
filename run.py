import os
from app import create_app
from tools.manual_pin_change import crear_tabla_si_no_existe
crear_tabla_si_no_existe()

# Usa "development" por defecto si no se especifica APP_ENV
env = os.getenv("APP_ENV", "development")

# Crea la app con la configuración correspondiente
app = create_app(env)

if __name__ == "__main__":
    # Ejecuta en modo debug solo si no es producción
    debug_mode = env != "production"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)

@app.route('/saltarme')
def saltarme():
    session['autenticado'] = True
    session['user_id'] = 1  # ID real del usuario en la DB
    return redirect(url_for('main.dashboard'))
