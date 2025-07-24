from flask import Flask
from app.routes import url_routes

# Initialize Flask app
app = Flask(__name__)

# Register URL shortener routes
app.register_blueprint(url_routes)

# Health check endpoint
@app.route('/')
def health_check():
    return {"status": "healthy", "service": "URL Shortener API"}

# API health check endpoint
@app.route('/api/health')
def api_health():
    return {"status": "ok", "message": "URL Shortener API is running"}

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
