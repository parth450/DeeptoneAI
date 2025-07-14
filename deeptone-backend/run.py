from flask import Flask
from flask_cors import CORS
from app.routes import main  # should match: main = Blueprint(...)

app = Flask(__name__)

# Allow all origins – works fine for development and deployment (Render + Vercel)
CORS(app, resources={r"/*": {"origins": "*"}})

# Register your routes
app.register_blueprint(main)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # Render assigns a port via env variable
    app.run(host='0.0.0.0', port=port, debug=True)  # Make it publicly accessible on Render
