### Making A 'User Object' Available as a Request Attribute
# docs.pylonsproject.org/projects/pyramid_cookbook/dev/authentication.html
from pyramid.decorator import reify
from pyramid.request import Request
from pyramid.security import unauthenticated_userid


class RequestWithUserAttribute(Request):
    @reify
    def user(self):
        userid = unauthenticated_userid(self)
        #print "--- in RequestWithUserAttribute: userid = " + str(userid)
        if userid is not None:
            # this should return None if the user doesn't exist
            # in the database
            #return dbsession.query('users').filter(user.user_id == userid)
            pool = self.tryton_pool
            web_user_obj = pool.get('web.user')
            user = web_user_obj.search([('email', '=', userid)])
            if user:
                user = user[0]

            return user if user else None
        return userid  # pragma: no cover

# /end of ### Making A 'User Object' Available as a Request Attribute
