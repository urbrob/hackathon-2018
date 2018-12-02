from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class User(AbstractUser):
    group = models.ManyToManyField('Group', through='GroupMembership')
    organization = models.ForeignKey('Organization', null=True, on_delete=models.CASCADE)
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

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

        if self.status == self.STUDENT:
            self.user_permissions.clear()
            self.user_permissions.add(Permission.objects.get(codename='view_report'),
            Permission.objects.get(codename='add_report'),
            Permission.objects.get(codename='view_testresult'),
            Permission.objects.get(codename='view_taskslist'),
            Permission.objects.get(codename='view_task'),
            Permission.objects.get(codename='view_test'))

        if self.status == self.TEACHER:
            self.user_permissions.clear()
            self.user_permissions.add(Permission.objects.get(codename='view_report'),
            Permission.objects.get(codename='change_report'),
            Permission.objects.get(codename='view_testresult'),
            Permission.objects.get(codename='view_taskslist'),
            Permission.objects.get(codename='add_taskslist'),
            Permission.objects.get(codename='change_taskslist'),
            Permission.objects.get(codename='delete_taskslist'),
            Permission.objects.get(codename='view_task'),
            Permission.objects.get(codename='add_task'),
            Permission.objects.get(codename='change_task'),
            Permission.objects.get(codename='delete_task'),
            Permission.objects.get(codename='view_test'),
            Permission.objects.get(codename='change_test'),
            Permission.objects.get(codename='add_test'),
            Permission.objects.get(codename='delete_test'),
            Permission.objects.get(codename='view_groupmembership'),
            Permission.objects.get(codename='add_groupmembership'),
            Permission.objects.get(codename='delete_groupmembership'),
            Permission.objects.get(codename='change_groupmembership'),
            Permission.objects.get(codename='view_group', content_type__app_label='works'),
            Permission.objects.get(codename='add_groupmembership'),
            Permission.objects.get(codename='delete_groupmembership'),
            Permission.objects.get(codename='change_groupmembership'))

        if self.status == self.ADMIN:
            self.user_permissions.clear()
            self.user_permissions.set(Permission.objects.all())




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
    deadline_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.task_list.group.name} - {self.task.list.organization}'


class Task(models.Model):
    task_list = models.ManyToManyField(TasksList, through='TaskAssign')
    title = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f'{self.title}'


class Test(models.Model):
    VALUE_TYPE = 'value_type'
    VALUE_EQUALS = 'value_equals'
    TEST_TYPES = (
        (VALUE_TYPE, 'Value type check'),
        (VALUE_EQUALS, 'Value equals'),
    )
    test_type = models.CharField(choices=TEST_TYPES, max_length=50)
    value = models.CharField(max_length=100, null=True, blank=True)
    function_name = models.CharField(max_length=100, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='tests')



class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    report = models.ForeignKey('Report', on_delete=models.CASCADE, related_name='tests_result')
    error = models.CharField(null=True, max_length=150)
    passed = models.NullBooleanField()
    line = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.test.task.title} {self.report.id} - {self.passed}'


class Report(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    accepted_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='reports', null=True, blank=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    teacher_comment = models.CharField(null=True, max_length=250)
    passed = models.NullBooleanField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    file = models.FileField(upload_to='reports/')

    def __str__(self):
        return f'{self.task.title} - {self.tests_result} by {self.student.first_name} {self.student.last_name}'
