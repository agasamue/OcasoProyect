# 🌅 Ocaso – Notes

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
git clone https://github.com/wkeysam/OcasoNotes.git
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
├── app/
├── bot/
├── lambda/
├── middleware/
├── migrations/
├── scripts/
├── tools/
├── tests/
├── .env
├── .gitignore
├── .dockerignore
├── requirements.txt
├── run.py
├── Dockerfile
├── docker-compose.yml
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

---

## 👁️ Licencia

Este proyecto está licenciado bajo la **Apache License 2.0**.  
Puedes usar, modificar y distribuir este software libremente, incluso con fines comerciales, siempre que mantengas el aviso de copyright.

Consulta el archivo [`LICENSE`](LICENSE) para más detalles.
Contacto: sam.dgarcia02@gmail.com
---

## 💼 Uso Comercial

Este software puede ser utilizado libremente bajo la Licencia Apache 2.0.  
Sin embargo, si deseas integrar esta herramienta en un producto comercial con soporte, personalización o marca propia, ponte en contacto para una **licencia empresarial personalizada**:

📩 Contacto: [sam.dgarcia02@gmail.com](mailto:sam.dgarcia02@gmail.com)

---

## 🤝 Autor y contacto

Desarrollado por **Samuel Enrique García Díaz**  
📫 [sam.dgarcia02@gmail.com](mailto:sam.dgarcia02@gmail.com)

---

## ❤️ Apoya al creador

¿Te gusta el proyecto? Puedes ayudarme a mantenerlo y mejorarlo desde:

👉 [patreon.com/wkeysam](https://patreon.com/wkeysam)

Como mecenas puedes recibir:
- Acceso anticipado a nuevas funciones
- Soporte prioritario
- Participación en decisiones del roadmap
- Menciones en futuras publicaciones

---

## 🏷️ Etiquetas

#Python #Flask #AWS #Docker #PostgreSQL #Lambda #SQLAlchemy #API  
#RedSocial #BienestarDigital #Reflexión #Autenticación #SaaS #Seguridad  
#Apache2 #OpenSource #TechForGood #SelfImprovement #MentalHealth

> No dejes que nadie destruya lo que llevas tiempo construyendo con esfuerzo. 💪🏽

