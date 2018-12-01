from django.db import models
from django.contrib.auth.models import AbstractUser


class Organization(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    email_contact = models.CharField(max_length=30)
    phone_contact = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="teacher")
    tasks = models.ManyToManyField(TasksList)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

class TasksList(models.Model):
    group = models.ManyToManyField(Group)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

class Task(models.Model):
    list = models.ManyToManyField(TasksList, through='task_assign')

class Test(models.Model):
    task = models.ManyToManyField(Task)

class Report(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

class User(AbstractUser):
