from flask import Flask
from flask_cors import CORS
from app.routes import main  # should match: main = Blueprint

app = Flask(__name__)
CORS(app)

app.register_blueprint(main)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # Render provides the PORT 
    app.run(host='0.0.0.0', port=port, debug=True)  # Expose publicly on Render
