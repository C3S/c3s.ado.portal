import cryptacular.bcrypt
from datetime import datetime
from sqlalchemy import (
    #Boolean,
    Column,
    #Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Text,
    Table,
    Unicode,
    #or_,
    #and_,
    #desc,
    #asc
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    relationship,
    scoped_session,
    sessionmaker,
    synonym,
)
from sqlalchemy.sql import func
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()
crypt = cryptacular.bcrypt.BCRYPTPasswordManager()


def hash_password(password):
    return unicode(crypt.encode(password))


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)


class Group(Base):
    """
    groups aka roles for people
    """
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Unicode(30), unique=True, nullable=False)

    def __str__(self):
        return 'group:%s' % self.name

    def __init__(self, name):
        self.name = name

    @classmethod
    def get_staffers_group(cls, groupname=u'staff'):
        dbsession = DBSession()
        staff_group = dbsession.query(
            cls).filter(cls.name == groupname).first()
        #print('=== get_staffers_group:' + str(staff_group))
        return staff_group

    @classmethod
    def get_login_group(cls, groupname=u'login'):
        login_group = DBSession().query(
            cls).filter(cls.name == groupname).first()
        #print('=== get_staffers_group:' + str(staff_group))
        return login_group

#    @classmethod
#    def get_Users_group(cls, groupname="User"):
#        """Choose the right group for users"""
#        dbsession = DBSession()
#        users_group = dbsession.query(
#            cls).filter(cls.name == groupname).first()
#        print('=== get_Users_group:' + str(users_group))
#        return users_group


# table for relation between staffers and groups
people_groups = Table(
    'people_groups', Base.metadata,
    Column(
        'people_id', Integer, ForeignKey('people.id'),
        primary_key=True, nullable=False),
    Column(
        'group_id', Integer, ForeignKey('groups.id'),
        primary_key=True, nullable=False)
)


class People(Base):
    """
    people may log in and do things
    """
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    email = Column(Unicode(255), unique=True)
    _password = Column('password', Unicode(60))
    last_password_change = Column(
        DateTime,
        default=func.current_timestamp())
    groups = relationship(
        Group,
        secondary=people_groups,
        backref="people")

    def _init_(self, email, password):  # pragma: no cover
        self.email = email
        self.password = password
        self.last_password_change = datetime.now()

    #@property
    #def __acl__(self):
    #    return [
    #        (Allow,                           # user may edit herself
    #         self.username, 'editUser'),
    #        #'user:%s' % self.username, 'editUser'),
    #        (Allow,                           # accountant group may edit
    #         'group:accountants', ('view', 'editUser')),
    #        (Allow,                           # admin group may edit
    #         'group:admins', ('view', 'editUser')),
    #    ]

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = hash_password(password)

    password = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password)

    @classmethod
    def get_by_id(cls, id):
        return DBSession.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_by_email(cls, email):
        #dbSession = DBSession()
        return DBSession.query(cls).filter(cls.email == email).first()

    @classmethod
    def check_password(cls, email, password):
        #dbSession = DBSession()
        staffer = cls.get_by_email(email)
        #if staffer is None:  # ?
        #    return False
        #if not staffer:  # ?
        #    return False
        return crypt.check(staffer.password, password)

    # this one is used by RequestWithUserAttribute
    @classmethod
    def check_user_or_None(cls, email):
        """
        check whether a user by that username exists in the database.
        if yes, return that object, else None.
        returns None if username doesn't exist
        """
        email = cls.get_by_email(email)  # is None if user not exists
        return email

    @classmethod
    def delete_by_id(cls, id):
        _del = DBSession.query(cls).filter(cls.id == id).first()
        _del.groups = []
        DBSession.query(cls).filter(cls.id == id).delete()
        return

    @classmethod
    def get_all(cls):
        return DBSession.query(cls).all()
