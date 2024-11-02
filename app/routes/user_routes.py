from flask import Blueprint
from app.controllers.user_controllers import register, login, logout, current_user

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/register', methods=['POST'])(register)
auth_bp.route('/login', methods=['POST'])(login)
auth_bp.route('/logout', methods=['POST'])(logout)
auth_bp.route('/current_user', methods=['GET'])(current_user)