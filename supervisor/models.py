from django.db import models

from studentportal.models import Project, NGO
from django import forms
from django.utils import timezone

class Notification(models.Model):
	noti_id = models.IntegerField(primary_key= True)
	noti_type 	= models.CharField(max_length=16, null=True, blank=True)
	#noti_type include -> new, edit, log, finish, suggest
	project 	= models.ForeignKey(Project, blank = True, unique= False)
	NGO_name 	= models.CharField(max_length=255)
	NGO_link 	= models.URLField(max_length=200)
	NGO_details	= models.TextField()
	NGO_sugg_by = models.CharField(max_length=255)
	#i should create a seen field too

class Example(models.Model):
	project 	 = models.OneToOneField(Project, primary_key = True)
	date_created = models.DateTimeField(default = timezone.now)

class AdvanceSearchForm(forms.Form):
    stage = forms.ChoiceField(choices=(
    	('all', 'all'),('ongoing', 'ongoing'),('to_be_verified', 'unverified'), ('completed', 'completed')
    	),
    label="Stage of project"
    )
    name = forms.CharField(label="Name of student", required = False) 
    email = forms.EmailField(label="Email", required = False)
    roll_no = forms.IntegerField(required = False, label="Roll number")
    project_title = forms.CharField(required = False, label = "Words in project title")
    NGO_name = forms.CharField(required = False, label = "Name of the NGO")
    year_choices = ((x,str(x)) for x in range(2014, timezone.now().year + 1))
    proposal_year = forms.ChoiceField(choices = year_choices, label="Year of proposal of CW project")
    # category
    # time_completed_before
    # time_completed_after