from flask import Flask, session

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret_key'  
    
    from .routes import main
    app.register_blueprint(main)

    return app
