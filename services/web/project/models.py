"""Database models."""
from . import db
from flask_login import UserMixin, _compat
from flask_login._compat import text_type
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


"""User Object"""
class User(db.Model):
    """User account model."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        unique=False,
        nullable=False
    )
    user_type = db.Column(
        db.String(40),
        unique=False,
        nullable=False
    )    
    email = db.Column(
        db.String(40),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
    )
    organization = db.Column(
        db.String(60),
        index=False,
        unique=False,
        nullable=True
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    """backreferences User class on retentions table"""    
    documents = relationship(
        'Retention',
        back_populates='user'
        )

    """UserMixin requirements from flask-login"""
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return text_type(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    """Password Check Functions"""
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

"""Document Object"""
class Document(db.Model):
    """Document model."""
    """Describes table which includes documents."""

    __tablename__ = 'documents'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    document_name = db.Column(
        db.String(100),
        unique=False,
        nullable=True
    )
    document_body = db.Column(
        db.String(1000),
        unique=False,
        nullable=True
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    """backreferences User class on retentions table"""
    users = relationship(
        'Retention',
        back_populates='document'
        )


"""Association Object - User Retentions of Documents"""
class Retention(db.Model):
    """Model for who retains which document"""
    """Associate database."""
    __tablename__ = 'retentions'

    id = db.Column(
        db.Integer, 
        primary_key=True,
        autoincrement=True
    )

    sponsor_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id'),
        primary_key=True,
        unique=False,
        nullable=True
    )

    editor_id = db.Column(
        db.Integer, 
        unique=False,
        nullable=True
    )

    document_id = db.Column(
        db.Integer, 
        db.ForeignKey('documents.id'),
        primary_key=True,
        unique=False,
        nullable=True
    )

    """backreferences to user and document tables"""
    user = db.relationship(
        'User', 
        back_populates='documents'
        )

    document = db.relationship(
        'Document', 
        back_populates='users'
        )