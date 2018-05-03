from .audit import audit_bp

MODULES = (
    # (auth_bp, '/api'),
    (audit_bp, '/api'),
)
