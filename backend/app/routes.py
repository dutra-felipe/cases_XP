from flask import Blueprint, request, jsonify
from flask_login import login_required
from sqlalchemy import func
from .models import Case, db
from .auth import admin_required
import json


api_bp = Blueprint('api', __name__)


@api_bp.route('/api/cases', methods=['GET'])
def get_cases():
    """Retorna todos os cases"""
    cases = Case.query.order_by(func.lower(Case.titulo)).all()
    return jsonify([case.to_dict() for case in cases])


@api_bp.route('/api/cases/<int:case_id>', methods=['GET'])
def get_case(case_id):
    """Retorna um case específico"""
    case = Case.query.get_or_404(case_id)
    return jsonify(case.to_dict())


@api_bp.route('/api/cases', methods=['POST'])
@admin_required
def create_case():
    """Cria um novo case"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    required_fields = ['titulo', 'contextualizacao', 'diagnostico', 'dores_do_cliente', 'bullet_points']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Campo {field} é obrigatório'}), 400
    
    try:
        case = Case(
            titulo=data['titulo'],
            contextualizacao=data['contextualizacao'],
            diagnostico=data['diagnostico'],
            dores_do_cliente=json.dumps(data['dores_do_cliente'], ensure_ascii=False),
            bullet_points=json.dumps(data['bullet_points'], ensure_ascii=False),
            ferramentas=json.dumps(data.get('ferramentas', []), ensure_ascii=False) if data.get('ferramentas') else None,
            comentarios=data.get('comentarios')
        )
        
        db.session.add(case)
        db.session.commit()
        
        return jsonify(case.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao criar case: {str(e)}'}), 500


@api_bp.route('/api/cases/<int:case_id>', methods=['PUT'])
@admin_required
def update_case(case_id):
    """Atualiza um case existente"""
    case = Case.query.get_or_404(case_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    try:
        case.titulo = data.get('titulo', case.titulo)
        case.contextualizacao = data.get('contextualizacao', case.contextualizacao)
        case.diagnostico = data.get('diagnostico', case.diagnostico)
        
        if 'dores_do_cliente' in data:
            case.dores_do_cliente = json.dumps(data['dores_do_cliente'], ensure_ascii=False)
        
        if 'bullet_points' in data:
            case.bullet_points = json.dumps(data['bullet_points'], ensure_ascii=False)
        
        if 'ferramentas' in data:
            case.ferramentas = json.dumps(data['ferramentas'], ensure_ascii=False) if data['ferramentas'] else None
        
        case.comentarios = data.get('comentarios', case.comentarios)
        
        db.session.commit()
        return jsonify(case.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao atualizar case: {str(e)}'}), 500


@api_bp.route('/api/cases/<int:case_id>', methods=['DELETE'])
@admin_required
def delete_case(case_id):
    """Deleta um case"""
    case = Case.query.get_or_404(case_id)
    
    try:
        db.session.delete(case)
        db.session.commit()
        return jsonify({'message': 'Case deletado com sucesso'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao deletar case: {str(e)}'}), 500
