from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_cors import CORS  

app = Flask(__name__)

CORS(app)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usersAssignment1.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)  # Added
    last_name = db.Column(db.String(80), nullable=False)  # Added


# User Loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/api/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        first_name=data['first_name'],  # Use the provided first_name
        last_name=data['last_name']     # Use the provided last_name
    )
    db.session.add(user)
    try:
        db.session.commit()
        return jsonify({"message": "User created successfully."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Could not create user.", "error": str(e)}), 400


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,  # Include first_name in the response
            "last_name": user.last_name,    # Include last_name in the response
            "message": "Logged in successfully."
        }), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


@app.route('/api/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully."}), 200

if __name__ == '__main__':
    app.run(debug=True)
