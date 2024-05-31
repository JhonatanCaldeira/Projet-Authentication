from flask import Flask, request
from flask_login import LoginManager
from config import API_URL
# from .models.user import User



def create_app():
    app = Flask(__name__, template_folder='templates')
    
    app.config['SECRET_KEY'] = 'secret_key'
    # app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"

    # db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from .models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        response = request.get(f"{API_URL}/users/{user_id}")    
        if response.status_code == 200:
            data = response.json()
            return User.from_dict(data)
        return None
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    return app