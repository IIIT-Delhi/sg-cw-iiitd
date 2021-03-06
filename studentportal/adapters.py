from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib import messages
from django.contrib.auth import logout

import studentportal.format_resources as fmt
import supervisor.communication
from CW_Portal import settings, access_cache
from studentportal import views


# prevent login from accounts other than allowed providers.
class DomainLoginAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        # allow TAs be outside ALLOWED DOMAINS
        email = user.email
        if all([email.split('@')[1] not in \
                getattr(settings, "ALLOWED_DOMAINS", []),
                email not in access_cache.get_TA()]):
            print("Rejecting login to", user, "with email", email,
                  "because of invalid domain as well as not in list of TAs", access_cache.get_TA())
            logout(request)
            messages.warning(request, fmt.MESSAGE_LOGIN_INVALID_DOMAIN)
            raise ImmediateHttpResponse(views.home(request))


# I subclassed the DefaultAccountAdapter and made the allauth
# app use this Adapter instead of this default adapter.
# This allowed me to override the add_message function,
# which used to add `you've logged in successfully <username>`
# on its own accord.
class NoMessagesLoginAdapter(DefaultAccountAdapter):
    def add_message(self, request, level, message_template,
                    message_context={}, extra_tags=''):
        pass


def send_report_to_admins():
    proposals = access_cache.get_noti_count('proposal')
    submissions = access_cache.get_noti_count('submissions')
    ngos = access_cache.get_noti_count('NGO')

    if any([proposals, submissions, ngos]):
        info = {'proposals': proposals, 'submissions': submissions, 'ngos': ngos}
        body = fmt.MAIL_BODY_ADMIN_DAILY_REPORT % info

        supervisor.communication.send_email(fmt.MAIL_TITLE_ADMIN_DAILY_REPORT, body, access_cache.get_TA())

        print("Sent report to admins: ", body)
    else:
        print("No report sending required.")
