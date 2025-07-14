from flask import Flask
from flask_cors import CORS
from app.routes import main  # Import your Blueprint

app = Flask(__name__)

#  Enable CORS for all origins — required for Vercel frontend to access Flask backend on Render
CORS(app, resources={r"/*": {"origins": "*"}})

# ✅Register all API routes
app.register_blueprint(main)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # Render provides PORT via env
    app.run(host='0.0.0.0', port=port, debug=True)  # Run on all interfaces
