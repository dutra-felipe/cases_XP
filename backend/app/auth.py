from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User, db
from .config import Config


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/login', methods=['POST'])
def login():
    """Endpoint para login do admin com verificação de hash"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username e password são obrigatórios'}), 400

    # Tenta encontrar o usuário no banco de dados primeiro
    user = User.query.filter_by(username=username).first()

    if user:
        # Se o usuário existe, compara a senha enviada com a senha hasheada no banco
        if check_password_hash(user.password, password):
            login_user(user)
            return jsonify({'message': 'Login realizado com sucesso'})
        else:
            # Senha incorreta para usuário existente
            return jsonify({'error': 'Credenciais inválidas'}), 401
    else:
        # Se o usuário NÃO existe (primeiro login), verifica contra as variáveis de ambiente
        if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
            # Cria o usuário no banco
            new_user = User(
                username=username,
                password=generate_password_hash(password), # Armazena a senha hasheada
                is_admin=True
            )
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user)
            return jsonify({'message': 'Login realizado com sucesso e usuário admin criado'})
        else:
            # Usuário não existe e as credenciais do .env não batem
            return jsonify({'error': 'Credenciais inválidas'}), 401


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
                'is_admin': current_user.is_admin
            }
        })
    return jsonify({'authenticated': False})
