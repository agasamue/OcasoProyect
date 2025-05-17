from flask import Blueprint, render_template, redirect, url_for, request, session, flash, jsonify
from app.models import db, User
import os
from datetime import datetime
from functools import wraps
from middleware.require_jwt import require_jwt

auth_bp = Blueprint("auth", __name__)

RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")
@auth_bp.route("/dashboard")
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("autenticado"):
            flash("Necesitas iniciar sesión", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated
    @auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for("auth.login"))
@auth_bp.route("/dashboard")
def dashboard():
    if not session.get("autenticado"):
        return redirect(url_for("auth.verificar_pin"))

    user_id = session.get("user_id")
    user = User.query.get(user_id)

    notas = Reflexion.query.filter_by(usuario_id=user_id).order_by(Reflexion.fecha_creacion.desc()).all()

    # Para gráfica
    resumen = {}
    for nota in notas:
        fecha = nota.fecha_creacion.strftime("%Y-%m-%d")
        resumen[fecha] = resumen.get(fecha, 0) + 1

    fechas = list(resumen.keys())
    cantidades = list(resumen.values())

    return render_template(
        "index.html",
        notas_reflexion=notas,
        fechas=fechas,
        cantidades=cantidades,
        total_reflexiones=len(notas),
        ultima_fecha=notas[0].fecha_creacion.strftime("%d/%m/%Y") if notas else "N/A"
    )
@auth_bp.route('/api/protegido', methods=['GET'])
@require_jwt
def ruta_protegida():
    return jsonify({"message": "Acceso permitido. Token válido."}), 200

def solo_admin(f):
    @wraps(f)
    def decorado(*args, **kwargs):
        if not session.get("autenticado") or not session.get("es_admin"):
            flash("Acceso denegado. Solo administradores", "danger")
            return redirect(url_for("auth.verificar_pin"))
        return f(*args, **kwargs)
    return decorado
@auth_bp.route('/admin/solicitudes', methods=['GET', 'POST'])
@solo_admin
def ver_solicitudes():
    from manual_pin_change import listar_solicitudes
    solicitudes = listar_solicitudes()

    email_filtro = request.args.get('email')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    # Filtrar por email si se proporciona
    if email_filtro:
        solicitudes = [s for s in solicitudes if s['email'] == email_filtro]

    # Filtrar por fecha si se proporcionan ambas
    if fecha_inicio and fecha_fin:
        try:
            inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
            solicitudes = [s for s in solicitudes if inicio <= datetime.strptime(s['fecha'], "%Y-%m-%d") <= fin]
        except ValueError:
            flash("Formato de fecha incorrecto. Usa YYYY-MM-DD.", "danger")

    return render_template('admin_solicitudes.html', solicitudes=solicitudes)
@auth_bp.route("/admin/solicitud/<int:solicitud_id>/atender")
@solo_admin
def atender_solicitud(solicitud_id):
    from tools.manual_pin_change import marcar_como_atendida
    if marcar_como_atendida(solicitud_id):
        flash("Solicitud marcada como atendida", "success")
    else:
        flash(" No se pudo actualizar la solicitud", "danger")
    return redirect(url_for("auth.ver_solicitudes"))

@auth_bp.route("/convertirme-admin")
def convertirme_admin():
    if not session.get("autenticado"):
        flash("Debes iniciar sesión para hacerte admin", "warning")
        return redirect(url_for("auth.verificar_pin"))

    if os.getenv("ENABLE_ADMIN_CONVERSION", "false").lower() != "true":
        flash("Función desactivada por seguridad", "danger")
        return redirect(url_for("main.home"))

    email = session.get("email")
    user = User.query.filter_by(email=email).first()

    if user:
        user.es_admin = True
        db.session.commit()
        session["es_admin"] = True
        flash("¡Ahora eres administrador!", "success")
    else:
        flash("Usuario no encontrado", "danger")

    return redirect(url_for("main.home"))

@auth_bp.route("/verificar-pin", methods=["GET", "POST"])
def verificar_pin():
    if request.method == "POST":
        pin = request.form.get("pin")
        email = session.get("email")

        if not email:
            flash("Email no disponible en la sesión", "danger")
            return redirect(url_for("auth.verificar_pin"))

        user = User.query.filter_by(email=email).first()

        if user and user.check_pin(pin):
            session["autenticado"] = True
            session["es_admin"] = user.es_admin
            return redirect(url_for("main.home"))
        else:
            flash("PIN incorrecto", "danger")

    return render_template("verificar_pin.html", email=session.get("email"))

@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        username = request.form.get("username")
        pin = request.form.get("pin")
        empresa_nombre = request.form.get("empresa")

        if not username or not pin or not empresa_nombre:
            flash("Todos los campos son obligatorios (usuario, PIN, empresa)", "danger")
            return redirect(url_for("auth.registro"))

        # Verificar que el usuario no exista ya
        if User.query.filter_by(username=username).first():
            flash("Este nombre de usuario ya está registrado", "warning")
            return redirect(url_for("auth.registro"))

        # Buscar la empresa
        empresa = Empresa.query.filter_by(nombre=empresa_nombre).first()
        if not empresa:
            flash("Empresa no válida o no encontrada", "danger")
            return redirect(url_for("auth.registro"))

        # Crear y guardar usuario
        user = User(username=username, empresa_id=empresa.id)
        user.set_pin(pin)

        db.session.add(user)
        db.session.commit()

        # Guardar en sesión
        session["username"] = username
        session["empresa_id"] = empresa.id
        session["autenticado"] = False  # aún no ha pasado la verificación de PIN

        flash("Usuario registrado correctamente. Verifica tu PIN", "success")
        return redirect(url_for("auth.verificar_pin"))

    return render_template("registro.html")

def login():
    data = request.form
    username = data.get("username")
    pin = data.get("pin")
    empresa_nombre = data.get("empresa")  # campo nuevo en el formulario

    empresa = Empresa.query.filter_by(nombre=empresa_nombre).first()
    if not empresa:
        flash("Empresa no encontrada", "error")
        return redirect(url_for("auth.login"))

    user = User.query.filter_by(username=username, empresa_id=empresa.id).first()

    if not user or not user.check_pin(pin):
        flash("Credenciales incorrectas", "error")
        return redirect(url_for("auth.login"))

    session["user_id"] = user.id
    session["empresa_id"] = user.empresa_id
    session["rol"] = user.rol

    return redirect(url_for("main.home"))
