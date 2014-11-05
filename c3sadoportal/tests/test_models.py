# -*- coding: utf-8  -*-
import os
import unittest
import transaction
#from pyramid.config import Configurator
from pyramid import testing
from datetime import date
from sqlalchemy import create_engine
#from sqlalchemy.exc import IntegrityError
from c3sadoportal.models import (
    DBSession,
    Base,
    Group,
    People
)
DEBUG = False


class ModelTestBase(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_mailer.testing')
        try:
            DBSession.remove()
            #print("removing old DBSession ==============================")
        except:
            #print("no DBSession to remove ==============================")
            pass
        #engine = create_engine('sqlite:///test_models.db')
        engine = create_engine('sqlite:///:memory:')
        self.session = DBSession
        DBSession.configure(bind=engine)  # XXX does influence self.session!?!
        Base.metadata.create_all(engine)

    def tearDown(self):
        self.session.close()
        self.session.remove()
        #os.remove('test_models.db')

    def _getTargetClass(self):
        return People

    def _makeOne(self,
                 login='alogin',
                 password=u'arandompassword',
                 email=u'dev@office.c3s.cc'):
        #print "type(self.session): " + str(type(self.session))
        return self._getTargetClass()(  # order of params DOES matter
            login,
            password,
            email,
        )

    def _makeAnotherOne(self,
                        login='anotherlogin',
                        password=u'arandompassword2',
                        email=u'dev@office.c3s.cc'):
        return self._getTargetClass()(  # order of params DOES matter
            login,
            password,
            email
        )


# class ModelTests(ModelTestBase):

#     def setUp(self):
#         super(ModelTests, self).setUp()
#         with transaction.manager:
#             l1 = People(  # german
#                 login=u'onelogin',
#                 email=u'some@shri.de',
#                 password=u'onerandompassword',
#             )
#             DBSession.add(l1)
#             DBSession.flush()

#     def test_constructor(self):
#         instance = self._makeOne()
#         #print(instance.address1)
#         self.assertEqual(instance.login, u'alogin', "No match!")
#         self.assertEqual(instance.email, u'dev@office.c3s.cc', "No match!")

    # def test_get_number(self):
    #     instance = self._makeOne()
    #     #session = DBSession()
    #     self.session.add(instance)
    #     myClass = self._getTargetClass()
    #     number_from_DB = myClass.get_number()
    #     #print number_from_DB
    #     self.assertEqual(number_from_DB, 2)


    # def test_get_by_id(self):
    #     instance = self._makeOne()
    #     #session = DBSession()
    #     self.session.add(instance)
    #     self.session.flush()
    #     _id = instance.id
    #     _date_of_birth = instance.date_of_birth
    #     _date_of_submission = instance.date_of_submission
    #     myClass = self._getTargetClass()
    #     instance_from_DB = myClass.get_by_id(_id)
    #     #self.session.commit()
    #     #self.session.remove()
    #     #print instance_from_DB.email
    #     if DEBUG:
    #         print "myClass: " + str(myClass)
    #         #        print "str(myUserClass.get_by_username('SomeUsername')): "
    #         # + str(myUserClass.get_by_username('SomeUsername'))
    #         #        foo = myUserClass.get_by_username(instance.username)
    #         #        print "test_get_by_username: type(foo): " + str(type(foo))
    #     self.assertEqual(instance_from_DB.firstname, u'SomeFirstnäme')
    #     self.assertEqual(instance_from_DB.lastname, u'SomeLastnäme')
    #     self.assertEqual(instance_from_DB.email, u'some@shri.de')
    #     self.assertEqual(instance_from_DB.address1, u'addr one')
    #     self.assertEqual(instance_from_DB.address2, u'addr two')
    #     self.assertEqual(instance_from_DB.postcode, u'12345')
    #     self.assertEqual(instance_from_DB.city, u'Footown Mäh')
    #     self.assertEqual(instance_from_DB.country, u'Foocountry')
    #     self.assertEqual(instance_from_DB.locale, u'DE')
    #     self.assertEqual(instance_from_DB.date_of_birth, _date_of_birth)
    #     self.assertEqual(instance_from_DB.email_is_confirmed, False)
    #     self.assertEqual(instance_from_DB.email_confirm_code, u'ABCDEFGHIK')
    #     self.assertEqual(instance_from_DB.date_of_submission,
    #                      _date_of_submission)
    #     self.assertEqual(instance_from_DB.membership_type, u'normal')
    #     self.assertEqual(instance_from_DB.member_of_colsoc, True)
    #     self.assertEqual(instance_from_DB.name_of_colsoc, u'GEMA')
    #     self.assertEqual(instance_from_DB.num_shares, u'23')

    # def test_delete_by_id(self):
    #     instance = self._makeOne()
    #     #session = DBSession()
    #     self.session.add(instance)
    #     myClass = self._getTargetClass()
    #     instance_from_DB = myClass.get_by_id('1')
    #     del_instance_from_DB = myClass.delete_by_id('1')
    #     #print
    #     del_instance_from_DB
    #     instance_from_DB = myClass.get_by_id('1')
    #     self.assertEqual(None, instance_from_DB)

    # def test_check_user_or_None(self):
    #     instance = self._makeOne()
    #     #session = DBSession()
    #     self.session.add(instance)
    #     myClass = self._getTargetClass()
    #     # get first dataset (id = 1)
    #     result1 = myClass.check_user_or_None('1')
    #     #print check_user_or_None
    #     self.assertEqual(1, result1.id)
    #     # get invalid dataset
    #     result2 = myClass.check_user_or_None('1234567')
    #     #print check_user_or_None
    #     self.assertEqual(None, result2)

    # def test_check_for_existing_confirm_code(self):
    #     instance = self._makeOne()
    #     self.session.add(instance)
    #     myClass = self._getTargetClass()

    #     result1 = myClass.check_for_existing_confirm_code(
    #         u'ABCDEFGHIK')
    #     #print result1  # True
    #     self.assertEqual(result1, True)
    #     result2 = myClass.check_for_existing_confirm_code(
    #         u'ABCDEFGHIK0000000000')
    #     #print result2  # False
    #     self.assertEqual(result2, False)

    # def test_member_listing(self):
    #     instance = self._makeOne()
    #     self.session.add(instance)
    #     instance2 = self._makeAnotherOne()
    #     self.session.add(instance2)
    #     myClass = self._getTargetClass()

    #     result1 = myClass.member_listing("id")
    #     self.failUnless(result1[0].firstname == u"SomeFirstnäme")
    #     self.failUnless(result1[1].firstname == u"SomeFirstnäme")
    #     self.failUnless(result1[2].firstname == u"SomeFirstname")

    # def test_member_listing_exception(self):
    #     instance = self._makeOne()
    #     self.session.add(instance)
    #     instance2 = self._makeAnotherOne()
    #     self.session.add(instance2)
    #     myClass = self._getTargetClass()

    #     #self.assertRaises(myClass, member_listing, "foo")
    #     with self.assertRaises(Exception):
    #         result1 = myClass.member_listing("foo")
        #self.failUnless(result1[0].firstname == u"SomeFirstnäme")
        #self.failUnless(result1[1].firstname == u"SomeFirstnäme")
        #self.failUnless(result1[2].firstname == u"SomeFirstname")


# class TestMemberListing(ModelTestBase):
#     def setUp(self):
#         super(TestMemberListing, self).setUp()
#         instance = self._makeOne(
#             login=u"ABC",
#             email=u'xyz@office.c3s.cc',
#             password=u'0987654321')
#         self.session.add(instance)
#         instance = self._makeAnotherOne(
#             login=u"DEF",
#             email=u'abc@office.c3s.cc',
#             password=u'19876543210')
#         self.session.add(instance)
#         instance = self._makeAnotherOne(
#             login=u"GHI",
#             email=u'def@office.c3s.cc',
#             password=u'098765432101')
#         self.session.add(instance)
#         self.session.flush()
#         self.class_under_test = self._getTargetClass()

#     def test_orderByLastname_sortedByLastname(self):
#         #print "now test " * 45
#         result = self.class_under_test.member_listing(order_by='lastname')
#         self.assertIsNotNone(result)
#         self.assertIsNotNone(result[0])
#         self.assertEqual("ABC", result[0].lastname)
#         self.assertEqual("GHI", result[-1].lastname)

#     def test_orderByLastnameOrderAsc_sortedByLastname(self):
#         result = self.class_under_test.member_listing(
#             order_by='lastname', order="asc")
#         self.assertIsNotNone(result)
#         self.assertIsNotNone(result[0])
#         self.assertEqual("ABC", result[0].lastname)
#         self.assertEqual("GHI", result[-1].lastname)

#     def test_orderByLastnameOrderDesc_sortedByLastname(self):
#         result = self.class_under_test.member_listing(
#             order_by='lastname', order="desc")
#         self.assertIsNotNone(result)
#         self.assertIsNotNone(result[0])
#         self.assertEqual("GHI", result[0].lastname)
#         self.assertEqual("ABC", result[-1].lastname)

#     def test_orderByInvalidName_raisesException(self):
#         self.assertRaises(self.class_under_test.member_listing,
#                           order_by='unknown', order="desc")
#         self.assertRaises(self.class_under_test.member_listing,
#                           order_by=None, order="desc")
#         self.assertRaises(self.class_under_test.member_listing,
#                           order_by="", order="desc")

#     def test_orderInvalid_raisesException(self):
#         self.assertRaises(self.class_under_test.member_listing,
#                           order_by='lastname', order="unknown")
#         self.assertRaises(self.class_under_test.member_listing,
#                           order_by='lastname', order="")
#         self.assertRaises(self.class_under_test.member_listing,
#                           order_by='lastname', order=None)


class GroupTests(unittest.TestCase):
    """
    test the groups
    """
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_mailer.testing')
        try:
            DBSession.remove()
        except:
            pass
        #engine = create_engine('sqlite:///test_model_groups.db')
        engine = create_engine('sqlite://')
        self.session = DBSession
        self.session.configure(bind=engine)
        Base.metadata.create_all(engine)

        with transaction.manager:
            group1 = Group(name=u'staff')
            DBSession.add(group1)
            DBSession.flush()
            self.assertEquals(group1.__str__(), 'group:staff')

    def tearDown(self):
        self.session.close()
        self.session.remove()
        #os.remove('test_model_groups.db')

    def test_group(self):
        #test_group = Group(name=u'testgroup')
        #self.session.add(test_group)

        result = Group.get_staffers_group()
        self.assertEquals(result.__str__(), 'group:staff')


class StaffTests(unittest.TestCase):
    """
    test the staff and cashiers accounts
    """
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_mailer.testing')
        try:
            DBSession.remove()
        except:
            pass
        #engine = create_engine('sqlite:///test_model_staff.db')
        engine = create_engine('sqlite://')
        self.session = DBSession
        self.session.configure(bind=engine)
        Base.metadata.create_all(engine)

        with transaction.manager:
            group1 = Group(name=u'staff')
            group2 = Group(name=u'staff2')
            DBSession.add(group1, group2)
            DBSession.flush()

    def tearDown(self):
        self.session.close()
        self.session.remove()
        #os.remove('test_model_staff.db')

    def test_staff(self):
        staffer1 = People(
            email=u'staffer1@c3s.cc',
            password=u'stafferspassword'
        )
        staffer1.group = ['staff']
        staffer2 = People(
            email=u'staffer2@c3s.cc',
            password=u'staffer2spassword',
        )
        staffer2.group = ['staff2']

        self.session.add(staffer1)
        self.session.add(staffer2)
        self.session.flush()

        _staffer2_id = staffer2.id
        _staffer1_id = staffer1.id

        self.assertTrue(staffer2.password is not '')

        #print('by id: %s' % People.get_by_id(_staffer1_id))
        #print('by id: %s' % People.get_by_id(_cashier1_id))
        #print('by login: %s' % People.get_by_login(u'staffer1'))
        #print('by login: %s' % People.get_by_login(u'cashier1'))
        self.assertEqual(
            People.get_by_id(_staffer1_id),
            People.get_by_email(u'staffer1@c3s.cc')
        )
        self.assertEqual(
            People.get_by_id(_staffer2_id),
            People.get_by_email(u'staffer2@c3s.cc')
        )

        '''test get_all'''
        res = People.get_all()
        self.assertEqual(len(res), 2)

        '''test delete_by_id'''
        People.delete_by_id(1)
        res = People.get_all()
        self.assertEqual(len(res), 1)

        '''test check_user_or_None'''
        res1 = People.check_user_or_None(u'staffer2@c3s.cc')
        res2 = People.check_user_or_None(u'staffer1@c3s.cc')
        #print res1
        #print res2
        self.assertTrue(res1 is not None)
        self.assertTrue(res2 is None)

        '''test check_password'''
        #print(People.check_password(cashier1, 'cashierspassword'))
        People.check_password(u'staffer2@c3s.cc', u'staffer2spassword')
        #self.assert
