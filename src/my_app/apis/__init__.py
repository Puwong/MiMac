from .audit import audit_bp
from .user import user_bp

MODULES = (
    (user_bp, '/api'),
    (audit_bp, '/api'),

)
