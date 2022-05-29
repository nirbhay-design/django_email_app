from django.db import models

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)

class Inbox(models.Model):
    from_name = models.CharField(max_length=100,default="nirbhay sharma")
    from_email = models.CharField(max_length=100)
    to_email = models.CharField(max_length=100)
    recv_time = models.DateTimeField()
    subj = models.CharField(max_length=100)
    content = models.TextField()

class Deleted(models.Model):
    from_name = models.CharField(max_length=100,default="nirbhay sharma")
    from_email = models.CharField(max_length=100)
    to_email = models.CharField(max_length=100)
    recv_time = models.DateTimeField()
    subj = models.CharField(max_length=100)
    content = models.TextField()

class Sent(models.Model):
    to_name = models.CharField(max_length=100,default="nirbhay sharma")
    from_email = models.CharField(max_length=100)
    to_email = models.CharField(max_length=100)
    recv_time = models.DateTimeField()
    subj = models.CharField(max_length=100)
    content = models.TextField()

