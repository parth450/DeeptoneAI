from flask import Flask
from flask_cors import CORS
from app.routes import main  # should match: main = Blueprint(...)

app = Flask(__name__)
CORS(app)

app.register_blueprint(main)  # ✅ attaches all routes like /predict

if __name__ == '__main__':
    app.run(debug=True)
