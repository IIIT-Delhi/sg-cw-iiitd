from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Student(models.Model):
	#building this will lead to instant access to self-projects
	pass

class NGO(models.Model):
	name 	= models.CharField(max_length=255)
	link 	= models.URLField()
	details = models.TextField()

class Document(models.Model):
	#FILE ACCESS URL
	date_added 	= models.DateTimeField(default=timezone.now)
	#category has the following options -> proposal, log, submission
	category	= models.CharField(max_length=16)

class Project(models.Model):
	credits 				= models.IntegerField(default=2)
	title 					= models.CharField(max_length=1024)
	date_created 			= models.DateTimeField(default=timezone.now)
	NGO_name 				= models.CharField(max_length=1024)
	NGO 					= models.ForeignKey(NGO, blank=True)
	NGO_details 			= models.CharField(max_length=2048)
	NGO_super 				= models.CharField(max_length=127)
	goals 					= models.TextField()
	expected_finish_date 	= models.DateTimeField()
	schedule_text 			= models.TextField()
	documents 				= models.ForeignKey(Document)
	#until I've not thrashed out the Student Model
	student 				= models.ForeignKey(User, 
								related_name='projects')

class Notification(models.Model):
	noti_type 	= models.CharField(max_length=16)
	#noti_type include -> new, edit, log, finish, suggest
	project 	= models.OneToOneField(Project, blank = True)
	NGO_name 	= models.CharField(max_length=255)
	NGO_link 	= models.URLField(max_length=200)
	NGO_details	= models.TextField()
	NGO_sugg_by = models.CharField(max_length=255)

class Example(models.Model):
	project 	 = models.OneToOneField(Project, primary_key = True)
	date_created = models.DateTimeField(timezone.now)