# from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.utils import timezone

from studentportal.models import Project, NGO, Category


class notification_type(object):
    NEW_PROJECT, PROJECT_FINISHED, NGO_SUGGESTION = range(1, 4)


nt = notification_type()


class diff_type(object):
    PROJECT_ADDED, PROJECT_EDITED, PROJECT_SUBMITTED, PROJECT_VERIFIED, PROJECT_UNVERIFIED, \
    ADDED_AS_EXAMPLE, REMOVED_AS_EXAMPLE, PROJECT_COMPLETED, DOCUMENT_UPLOADED, EMAIL_SENT, \
    PROJECT_DELETED, FEEDBACK_GIVEN, ADD_TA, REMOVE_TA, PROJECT_PRESENTED = range(1, 16)


_ = diff_type()
diff_mapping = {
    _.PROJECT_ADDED: "Project added", _.PROJECT_EDITED: "Project edited",
    _.PROJECT_SUBMITTED: "Project submitted", _.PROJECT_VERIFIED: "Project verified",
    _.PROJECT_UNVERIFIED: "Project unverified", _.ADDED_AS_EXAMPLE: "Added as example",
    _.REMOVED_AS_EXAMPLE: "Removed as example", _.PROJECT_COMPLETED: "Project completed",
    _.DOCUMENT_UPLOADED: "Document uploaded", _.EMAIL_SENT: "Sent an email",
    _.PROJECT_DELETED: "Project deleted", _.FEEDBACK_GIVEN: "Feedback given",
    _.ADD_TA: "Added TA", _.REMOVE_TA: "Removed TA", _.PROJECT_PRESENTED: "Project presented"
}


def add_notification(noti_type, **kwargs):
    if noti_type in [nt.NEW_PROJECT, nt.PROJECT_FINISHED]:
        Notification.objects.create(noti_type=noti_type,
                                    project=kwargs['project'])
    elif noti_type == nt.NGO_SUGGESTION:
        Notification.objects.create(noti_type=noti_type,
                                    NGO_name=kwargs['NGO_name'],
                                    NGO_link=kwargs['NGO_link'],
                                    NGO_details=kwargs['NGO_details'],
                                    NGO_sugg_by=kwargs['NGO_sugg_by'])


def add_diff(diff_type, **kwargs):
    (person, project, details) = map(lambda x: kwargs.get(x, None),
                                     ['person', 'project', 'details'])
    Diff.objects.create(diff_type=diff_type, person=person,
                        project=project, details=details)


class Notification(models.Model):
    noti_type = models.IntegerField(null=True, blank=True)
    project = models.ForeignKey(Project, null=True, unique=False, on_delete=models.CASCADE)
    NGO_name = models.CharField(max_length=200, blank=True)
    NGO_link = models.URLField(max_length=200, blank=True)
    NGO_details = models.TextField(blank=True)
    NGO_sugg_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)


class Example(models.Model):
    project = models.OneToOneField(Project, primary_key=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)

    def delete(self, *args, **kwargs):
        for l in self.likes.all():
            l.delete()
        for c in self.comments.all():
            c.delete()
        super(Example, self).delete(*args, **kwargs)


class Like(models.Model):
    project = models.ForeignKey(Example, related_name='likes', on_delete=models.CASCADE)
    liked_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='liked_projects', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.project.likes_count += 1
        self.project.save()
        super(Like, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.project.likes_count -= 1
        self.project.save()
        super(Like, self).delete(*args, **kwargs)


class Comment(models.Model):
    text = models.CharField(max_length=200)
    project = models.ForeignKey(Example, related_name='comments', on_delete=models.CASCADE)
    commentor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.project.comments_count += 1
        self.project.save()
        super(Comment, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.project.comments_count -= 1
        self.project.save()
        super(Comment, self).delete(*args, **kwargs)


class News(models.Model):
    content = models.TextField(max_length=1000)
    date_created = models.DateTimeField(default=timezone.now)
    priority = models.BooleanField(default=False)

    def get_priority(self):
        return "High" if self.priority else "Low"


class TA(models.Model):
    email = models.CharField(max_length=100)
    instructor = models.BooleanField(default=False)
    sg_access = models.BooleanField(default=False)
    cw_access = models.BooleanField(default=False)


class Diff(models.Model):
    diff_type = models.IntegerField()
    person = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='diff', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, null=True, related_name='diff', on_delete=models.CASCADE)
    details = models.TextField(max_length=1000, null=True)
    when = models.DateTimeField(default=timezone.now)

    def get_clear_description(self):
        return diff_mapping[self.diff_type]


class Flag(models.Model):
    key = models.CharField(max_length=100)
    value = models.BooleanField(default=True)
