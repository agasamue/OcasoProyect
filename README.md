# 🌅 Ocaso – Seguridad emocional y digital para entornos modernos

**Ocaso** es una plataforma modular y segura que combina gestión de usuarios por PIN, protección de infraestructura cloud y un enfoque emocional basado en zonas de reflexión. Pensada para empresas, comunidades o entornos educativos que necesiten una herramienta de introspección y control ético digital.

---

## 🧠 Características clave

- Autenticación por PIN y control por IP
- Suspensiones con guía reflexiva en lugar de castigos directos
- Visualización de gastos en tiempo real desde AWS
- Scripts automatizados de control (detener EC2, Lambda, apagar logs…)
- Panel privado para admins con logs de seguridad y gráficas
- Conexión con Telegram para alertas y comandos
- Multitenant por empresa (SaaS-ready)
- Seguridad avanzada: JWT, validación de IP, segmentación de acceso
- Despliegue en AWS con EC2, RDS (PostgreSQL), S3, Lambda, etc.
- Separación de módulos: `bot/`, `lambda/`, `tools/`, `scripts/`, `app/`

---

## 🚀 Instalación rápida

1. Clona este repositorio:

```bash
git clone https://github.com/tu_usuario/ocaso.git
cd ocaso
```

2. Crea tu entorno virtual y activa:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Configura tus variables en `.env`

```env
DB_HOST=...
SECRET_KEY=...
TELEGRAM_TOKEN=...
```

4. Ejecuta la app:

```bash
python run.py
```

---

## ⚙️ Estructura del proyecto

```
AWSVersion1.5/
│
├── app/
│   ├── models/
│   ├── routes/
│   ├── api/
│   ├── templates/
│   ├── static/
│   ├── middleware/
│   └── __init__.py
│
├── bot/
├── lambda/
├── scripts/        ← Producción AWS
├── tools/          ← Herramientas locales
├── migrations/
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── run.py
```

---

## 👁️ Licencia

Este proyecto está licenciado bajo **Creative Commons BY-NC 4.0**.  
Puedes estudiar y adaptar el código, pero no usarlo comercialmente sin autorización del autor.

---

## 🤝 Autor y contacto

Desarrollado por **Samuel Enrique García Díaz**  
📫 [sam.dgarcia02@gmail.com](mailto:sam.dgarcia02@gmail.com)

---

Este repositorio puede usarse para presentar en convocatorias oficiales como el **SEPE** o para futuros despliegues SaaS reales.
