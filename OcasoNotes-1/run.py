from app import create_app
from mangum import Mangum

app = create_app()

handler = Mangum(app)
db.init_app(app)
#Flask en local
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)