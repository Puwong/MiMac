from .audit import audit_bp
from .auth import auth_bp, frontend
from .user import user_bp
from .base import test_bp
from .file import file_bp

MODULES = (
    (user_bp, '/api'),
    (audit_bp, '/api'),
    (test_bp, ''),
    (auth_bp, ''),
    (frontend, ''),
    (file_bp, '/api'),
)
