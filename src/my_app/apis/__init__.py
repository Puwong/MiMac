from .audit import audit_bp
from .auth import auth_bp, frontend
from .user import user_bp
from .base import test_bp, static_bp
from .image import image_bp
from .alg import alg_bp

MODULES = (
    (user_bp, '/api'),
    (audit_bp, '/api'),
    (test_bp, ''),
    (alg_bp, ''),
    (static_bp, ''),
    (auth_bp, ''),
    (frontend, ''),
    (image_bp, '/api'),
)
