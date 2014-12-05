#########
# Shift to multiprocessing
#########
#########
# Create a notes system in the self growth portal.
# add actions that were dont to the project.
# don't delete projects and comments so soon.
#########
from multiprocessing import Process
from django.core.mail import EmailMultiAlternatives
from CW_Portal import settings
from studentportal.models import Project, project_stage

def _send_mail(subject, text_content, recipient_list):
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, recipient_list)
    # msg.send()
    pass

def send_email(subject, text_content, to=[]):
    # _send_mail(subject, text_content, to).start()
    pass

def chunks(full, size):
    for i in xrange(0, len(full), size):
        yield full[i:i+size]

def send_email_to_all(text_content,subject="New Announcement"):
    projects = Project.objects.filter(stage=project_stage.ONGOING)
    projects = list(chunks(projects, 30))
    for p in projects:
        send_email(subject, text_content, to=[str(x.student.email) for x in p])