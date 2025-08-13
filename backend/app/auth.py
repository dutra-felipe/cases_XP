from flask import Blueprint, request, jsonify, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from .models import User, db
from .config import Config


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/login', methods=['POST'])
def login():
    """Endpoint para login do admin com verificação de hash e permissão."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username e password são obrigatórios'}), 400

    user = User.query.filter_by(username=username).first()

    if user:
        if check_password_hash(user.password, password):
            if user.is_admin:
                login_user(user)
                return jsonify({'message': 'Login realizado com sucesso'})
            else:
                return jsonify({'error': 'Acesso negado: este usuário não é um administrador'}), 403
        else:
            return jsonify({'error': 'Credenciais inválidas'}), 401
    else:
        if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
            new_user = User(
                username=username,
                password=generate_password_hash(password),
                is_admin=True
            )
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user)
            return jsonify({'message': 'Login realizado com sucesso e usuário admin criado'})
        else:
            return jsonify({'error': 'Credenciais inválidas'}), 401


@auth_bp.route('/api/user-login', methods=['POST'])
def user_login():
    """Login de usuários comuns, criando um usuário persistente se não existir"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username e password são obrigatórios'}), 400
    
    if username != Config.USER_USERNAME or password != Config.USER_PASSWORD:
        return jsonify({'error': 'Credenciais inválidas'}), 401

    user = User.query.filter_by(username=username).first()

    if user:
        if check_password_hash(user.password, password):
            login_user(user)
            return jsonify({'message': 'Login realizado com sucesso'})
        else:
            return jsonify({'error': 'Credenciais inválidas'}), 401
    else:
        new_user = User(
            username=username,
            password=generate_password_hash(password),
            is_admin=False
        )
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return jsonify({'message': 'Login realizado com sucesso e usuário comum criado'})


@auth_bp.route('/api/logout', methods=['POST'])
@login_required
def logout():
    """Endpoint para logout"""
    logout_user()
    return jsonify({'message': 'Logout realizado com sucesso'})


@auth_bp.route('/api/check-auth', methods=['GET'])
def check_auth():
    """Verifica se o usuário está autenticado"""
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': {
                'username': current_user.username,
                'is_admin': getattr(current_user, 'is_admin', False)
            }
        })
    return jsonify({'authenticated': False})


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Por favor, faça o login para acessar esta página.', 'warning')
            return redirect(url_for('views.login_page')) 
        
        if not getattr(current_user, 'is_admin', False):
            return jsonify({'error': 'Acesso negado: esta área é restrita a administradores'}), 403
        
        return f(*args, **kwargs)
    return decorated_function
