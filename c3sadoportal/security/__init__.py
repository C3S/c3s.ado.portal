from pyramid.security import (
    Allow,
    #Deny,
)
from pyramid.security import ALL_PERMISSIONS


def groupfinder(userid, request):
    user = request.user
    if user:
        return [g.name for g in user.groups]


### MAP GROUPS TO PERMISSIONS
class Root(object):
    __acl__ = [
        (Allow, 'system.Everyone', 'view'),
        (Allow, 'system.Authenticated', 'logged_in'),
        (Allow, 'group:staff', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request
