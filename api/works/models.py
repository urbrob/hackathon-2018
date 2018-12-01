from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    group = models.ManyToManyField('Group', through='GroupMembership')
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    STUDENT = 'ST'
    TEACHER = 'TE'
    ADMIN = 'SU'
    STATUS_CHOICES = (
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
        (ADMIN, 'Admin'),
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=STUDENT,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.username}'


class Organization(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    email_contact = models.CharField(max_length=30)
    phone_contact = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class GroupMembership(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.is_teacher}'


class Group(models.Model):
    name = models.CharField(max_length=50)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.organization.name}'


class TasksList(models.Model):
    group = models.ManyToManyField(Group)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.group.name} - {self.organization.name}'


class TaskAssign(models.Model):
    task_list = models.ForeignKey(TasksList, on_delete=models.CASCADE)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.task_list.group.name} - {self.task.list.organization}'


class Task(models.Model):
    tesk_list = models.ManyToManyField(TasksList, through='TaskAssign')
    title = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f'{self.title} - {self.tesk_list.group.name}'


class Test(models.Model):
    task = models.ManyToManyField(Task)



class TestResult(models.Model):
    IN_PROGRESS = 'in-progress'
    FAILED = 'failed'
    PASSED = 'passed'
    TASK_STATUSES = (
        (IN_PROGRESS, 'In progress'),
        (FAILED, 'Failed'),
        (PASSED, 'Passed')
    )
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    report = models.ForeignKey('Report', on_delete=models.CASCADE)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    error = models.CharField(null=True, max_length=150)
    status = models.CharField(max_length=30, choices=TASK_STATUSES)
    line = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.task.title} {self.report.id} - {self.status}'


class Report(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    accepted_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='reports', null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    teacher_comment = models.CharField(null=True, max_length=250)

    def __str__(self):
        return f'{self.taask.title} - {self.tests_result}'
