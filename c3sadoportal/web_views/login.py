import colander
import deform
from deform import ValidationFailure
from pkg_resources import resource_filename
from pyramid.httpexceptions import HTTPFound
from pyramid.i18n import get_localizer
from pyramid.view import view_config
from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
)
from pyramid.threadlocal import get_current_request
#from pyramid_mailer import get_mailer
#from pyramid_mailer.message import Message
from translationstring import TranslationStringFactory
#from types import NoneType

from c3sadoportal.models import (
    DBSession,
    Group,
    People,
)
deform_templates = resource_filename('deform', 'templates')
c3smembership_templates = resource_filename('c3sadoportal', 'templates')

my_search_path = (deform_templates, c3smembership_templates)

_ = TranslationStringFactory('c3sadoportal')


def translator(term):
    return get_localizer(get_current_request()).translate(term)

my_template_dir = resource_filename('c3sadoportal', 'templates/')
deform_template_dir = resource_filename('deform', 'templates/')

zpt_renderer = deform.ZPTRendererFactory(
    [
        my_template_dir,
        deform_template_dir,
    ],
    translator=translator,
)
# the zpt_renderer above is referred to within the demo.ini file by dotted name

DEBUG = False
LOGGING = True

if LOGGING:  # pragma: no cover
    import logging
    log = logging.getLogger(__name__)


@view_config(renderer='../templates/login.pt',
             route_name='login')
def login_view(request):
    """
    This view lets people log in.
    if a person is already logged in, she is forwarded to the dashboard
    """
    logged_in = authenticated_userid(request)
    #print("authenticated_userid: " + str(logged_in))

    log.info("login by %s" % logged_in)

    if logged_in is not None:  # if user is already authenticated
        return HTTPFound(  # redirect her to the dashboard
            request.route_url('logged_in'))

    class AccountantLogin(colander.MappingSchema):
        """
        colander schema for login form
        """
        login = colander.SchemaNode(
            colander.String(),
            title=_(u"login"),
            oid="login",
        )
        password = colander.SchemaNode(
            colander.String(),
            validator=colander.Length(min=5, max=100),
            widget=deform.widget.PasswordWidget(size=20),
            title=_(u"password"),
            oid="password",
        )

    schema = AccountantLogin()

    form = deform.Form(
        schema,
        buttons=[
            deform.Button('submit', _(u'Submit')),
        ],
        #use_ajax=True,
        #renderer=zpt_renderer
    )

    # if the form has been used and SUBMITTED, check contents
    if 'submit' in request.POST:
        #print("the form was submitted")
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except ValidationFailure, e:
            print(e)

            request.session.flash(
                _(u"Please note: There were errors, "
                  "please check the form below."),
                'message_above_form',
                allow_duplicate=False)
            return{'form': e.render()}

        # get user and check pw...
        login = appstruct['login']
        password = appstruct['password']

        try:
            checked = People.check_password(login, password)
        except AttributeError:  # pragma: no cover
            checked = False
        if checked:
            log.info("password check for %s: good!" % login)
            headers = remember(request, login)
            log.info("logging in %s" % login)
            return HTTPFound(  # redirect to logged_in-view
                location=request.route_url(  # after successful login
                    'logged_in',
                    request=request),
                headers=headers)
        else:
            log.info("password check: failed for %s." % login)
    else:
        request.session.pop('message_above_form')  # remove message fr. session

    html = form.render()
    return {'form': html, }


@view_config(permission='view',
             route_name='logout')
def logout_view(request):
    """
    can be used to log a user/staffer off. "forget"
    """
    request.session.invalidate()
    request.session.flash(u'Logged out successfully.')
    headers = forget(request)
    return HTTPFound(
        location=request.route_url('login'),
        headers=headers)


@view_config(permission='logged_in',
             renderer='../templates/logged_in.pt',
             route_name='logged_in')
def logged_in(request):
    """
    is shown when somebody has logged in
    """
    request.session.flash(
        'You are logged in, {}.'.format(authenticated_userid(request)),
        'message_loggedin'
    )
    return {'FOO': 'bar'}


@view_config(renderer='../templates/register.pt',
             route_name='register')
def register(request):
    """
    This view lets people register.
    if a person is already logged in, she is forwarded to the logged_in view
    """
    logged_in = authenticated_userid(request)

    if logged_in is not None:  # if user is already authenticated
        return HTTPFound(  # redirect her to the dashboard
            request.route_url('logout'))

    # roll your own captcha
    #_c1 = random.range(10)
    #_c2 = random.range(10)

    class AccountRegistration(colander.MappingSchema):
        """
        colander schema for registration form
        """
        login = colander.SchemaNode(
            colander.String(),
            title=_(u"login"),
            oid="login",
        )
        password = colander.SchemaNode(
            colander.String(),
            validator=colander.Length(min=5, max=100),
            widget=deform.widget.PasswordWidget(size=20),
            title=_(u"password"),
            oid="password",
        )
        email = colander.SchemaNode(
            colander.String(),
            validator=colander.Email(),
            title=_(u"email"),
            oid="email",
        )
        #captcha = colander.SchemaNode(
        #    colander.String(),
        #    title=_(u"captcha: what is foo + bar?"),
        #    oid="captcha",
        #)

    schema = AccountRegistration()

    form = deform.Form(
        schema,
        buttons=[
            deform.Button('submit', _(u'Submit')),
        ],
        #use_ajax=True,
        #renderer=zpt_renderer
    )

    # if the form has been used and SUBMITTED, check contents
    if 'submit' in request.POST:
        #print("the form was submitted")
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except ValidationFailure, e:
            print(e)

            request.session.flash(
                _(u"Please note: There were errors, "
                  "please check the form below."),
                'message_above_form',
                allow_duplicate=False)
            return{'form': e.render()}

        # get user and check pw...
        _login = appstruct['login']
        _password = appstruct['password']
        _email = appstruct['email']

        try:
            # check if data is valid
            # * no duplicate accounts...
            #print '*'*60
            login_unique = False if People.get_by_login(_login) else True
            #print "login_unique: {}".format(login_unique)
            email_unique = False if People.get_by_email(_email) else True
            #print "email_unique: {}".format(email_unique)
            #print '*'*60
        except:  # pragma: no cover
            pass
        if login_unique and email_unique:
            # persist user
            _new = People(
                login=_login,
                password=_password,
                email=_email
            )
            _new.groups = [Group.get_login_group()]
            DBSession.add(_new)
            headers = remember(request, _login)

            return HTTPFound(  # redirect to accountants dashboard
                location=request.route_url(  # after successful login
                    'logged_in',
                    request=request),
                headers=headers
            )
        else:
            log.info(
                "login or email already known: {}, {}".format(_login, _email))
            request.session.flash(
                'login or email already known',
                'message_sign_up',
            )
    else:
        request.session.pop('message_above_form')  # remove message fr. session

    html = form.render()
    return {
        'form': html, }
