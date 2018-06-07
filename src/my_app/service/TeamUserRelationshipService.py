from .BaseService import BaseService
from my_app.models import TeamUserRelationship


class TeamUserRelationshipService(BaseService):
    model = TeamUserRelationship
