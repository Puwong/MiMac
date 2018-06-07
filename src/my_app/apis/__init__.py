from .audit import audit_bp
from .auth import auth_bp, frontend
from .user import user_bp
from .base import test_bp, static_bp
from .image import image_bp
from .alg import alg_bp
from .article import article_bp
from .team import team_bp

MODULES = (
    (user_bp, ''),
    (audit_bp, ''),
    (test_bp, ''),
    (alg_bp, ''),
    (static_bp, ''),
    (auth_bp, ''),
    (frontend, ''),
    (image_bp, ''),
    (article_bp, ''),
    (team_bp, ''),
)
