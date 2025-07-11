from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime


db = SQLAlchemy()


class User(UserMixin, db.Model):
    """Modelo simples para autenticação do admin"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Case(db.Model):
    """Modelo para os cases práticos"""
    __tablename__ = 'cases'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    contextualizacao = db.Column(db.Text, nullable=False)
    diagnostico = db.Column(db.Text, nullable=False)
    dores_do_cliente = db.Column(db.Text, nullable=False)
    bullet_points = db.Column(db.Text, nullable=False)
    ferramentas = db.Column(db.Text, nullable=True)
    comentarios = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def to_dict(self):
        """Converte o case para dicionário para API"""
        import json
        
        return {
            'id': self.id,
            'titulo': self.titulo,
            'contextualizacao': self.contextualizacao,
            'diagnostico': self.diagnostico,
            'dores_do_cliente': json.loads(self.dores_do_cliente) if self.dores_do_cliente else [],
            'bullet_points': json.loads(self.bullet_points) if self.bullet_points else [],
            'ferramentas': json.loads(self.ferramentas) if self.ferramentas else [],
            'comentarios': self.comentarios,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
