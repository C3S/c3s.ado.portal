#!/bin/env/python
# -*- coding: utf-8 -*-
# http://docs.pylonsproject.org/projects/pyramid/dev/narr/testing.html
#                                            #creating-functional-tests
import unittest
from pyramid import testing
from c3sadoportal.models import (
    DBSession,
    Base,
    Group,
    People,
)
from sqlalchemy import engine_from_config
import transaction


class LoginFunctionalTests(unittest.TestCase):
    """
    these tests are functional tests to check functionality of the whole app
    (i.e. integration tests)
    they also serve to get coverage for 'main'
    """
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_mailer.testing')
        my_settings = {
            #'sqlalchemy.url': 'sqlite:///test_webtest_accountants.db',
            'sqlalchemy.url': 'sqlite:///:memory:',
            'available_languages': 'de en',
        }
        engine = engine_from_config(my_settings)
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)

        self._insert_groups()
        self._insert_members()

        from c3sadoportal import main
        app = main({}, **my_settings)
        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        DBSession.close()
        DBSession.remove()
        testing.tearDown()

    def _insert_groups(self):
        with transaction.manager:
            login_group = Group(
                name=u'login',
            )
            DBSession.add(login_group)
            staff_group = Group(
                name=u'staff',
            )
            DBSession.add(staff_group)
            DBSession.flush()

    def _insert_members(self):
        with transaction.manager:
            member1 = People(  # german
                email=u'l1@c3s.cc',
                password=u'arandompassword',
            )
            member2 = People(  # german
                email=u'l2@c3s.cc',
                password=u'arandompassword2',
            )
            member3 = People(  # german
                email=u'l3@c3s.cc',
                password=u'arandompassword3',
            )
            DBSession.add(member1)
            DBSession.add(member2)
            DBSession.add(member3)
            DBSession.flush()

    def test_login(self):
        """
        load the login form, log in
        """
        #
        # login
        #
        res = self.testapp.get('/login', status=200)
        self.failUnless('login' in res.body)
        # try invalid user
        form = res.form
        form['login'] = 'foo'
        form['password'] = 'bar'
        res2 = form.submit('submit')
        self.failUnless(
            'Please note: There were errors' in res2.body)
        # try valid user & invalid password
        form = res2.form
        form['login'] = 'rut'
        form['password'] = 'berry'
        res3 = form.submit('submit', status=200)
        # try valid user, valid password
        form = res2.form
        form['login'] = 'l1@c3s.cc'
        form['password'] = 'arandompassword'
        res3 = form.submit('submit', status=302)
        #
        # being logged in ...
        res4 = res3.follow()
        #print(res4.body)
        self.failUnless(
            'You are logged in' in res4.body)
        # now that we are logged in,
        # the login view should redirect us to the same page
        res5 = self.testapp.get('/login', status=302)
        # so yes: that was a redirect
        res6 = res5.follow()

        #print(res4.body)
        self.failUnless(
            'You are logged in' in res6.body)

    def test_login_logout(self):
        """
        load the login form, log in
        """
        #
        # login
        #
        res = self.testapp.get('/login', status=200)
        self.failUnless('login' in res.body)
        # try invalid user
        form = res.form
        form['login'] = u'l1@c3s.cc'
        form['password'] = u'arandompassword'
        res = form.submit('submit', status=302)
        #
        # being logged in ...
        res2 = res.follow()
        #print(res4.body)
        self.failUnless(
            'You are logged in' in res2.body)
        # now that we are logged in, log out again
        res5 = self.testapp.get('/logout', status=302)
        # so yes: that was a redirect
        res6 = res5.follow()

        self.failUnless(
            "If you don't have an account yet, make sure to" in res6.body)

    def test_register(self):
        """
        load the registration form, register
        """
        #
        # login
        #
        res = self.testapp.get('/register', status=200)
        self.failUnless('sign up!' in res.body)
        # try invalid user
        form = res.form
        form['login'] = 'login1'
        form['password'] = 'arandompassword'
        res = form.submit('submit', status=200)
        #
        #print(res.body)
        self.failUnless(
            'There was a problem with your submission' in res.body)

        # start over with the form
        form['login'] = 'l1@c3s.cc'
        form['password'] = u'arandompassword'
        res = form.submit('submit', status=200)
        #
        #print(res.body)
        self.failUnless(
            'login or email already known' in res.body)

        # start over with the form
        form['login'] = u'dev4@c3s.cc'
        form['password'] = u'arandompassword4'
        res2 = form.submit('submit', status=302)
        #
        res3 = res2.follow()
        #print(res3.body)
        self.failUnless(
            'You are logged in, dev4@c3s.cc' in res3.body)

        # those who are logged in, may not register
        res5 = self.testapp.get('/register', status=302)
        # so yes: that was a redirect
        res6 = res5.follow()
        self.failUnless(
            "The resource was found at http://localhost/login; you should "
            "be redirected automatically." in res6.body)

        res7 = res6.follow()
        #print res7.body
        self.failUnless("login" in res7.body)
        self.failUnless("register" in res7.body)

        # now that we are logged in, log out again
        res5 = self.testapp.get('/logout', status=302)
        # so yes: that was a redirect
        res6 = res5.follow()

        self.failUnless(
            "If you don't have an account yet, make sure to" in res6.body)
