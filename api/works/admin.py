from django.contrib import admin
from works.models import Organization, Group, TasksList, Report


class GroupInline(admin.TabularInline):
    model = Group
    extra = 0

class TasksListInline(admin.TabularInline):
    model = TasksList
    extra = 0

class TaskInline(admin.TabularInline):
    model = Task
    extra = 0

class UserInline(admin.TabularInline):
    model = User
    extra = 0

class TestInline(admin.TabularInline):
    model = Test
    extra = 0

class TestResultInline(admin.TabularInline):
    model = TestResult
    extra = 0

class ReportInline(admin.TabularInline):
    model = Report
    extra = 0

class GroupMembershipInline(admin.TabularInline):
    model = Report
    extra = 0

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ['name', 'address', 'email_contact', 'phone_contact']
    fields = ('name', 'address', 'email_contact', 'phone_contact')
    inlines = [
        GroupInline,
        TasksListInline,
    ]

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    search_fields = ['name', 'organization']
    fields = ('name', 'organization')
    list_display = ('name', 'organization')

@admin.register(TasksList)
class TasksListAdmin(admin.ModelAdmin):
    list_display = ('id', )

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    search_fields = ['task']
    fields = ('task',)
    list_display = ('task',)

@admin.register(TaskAssign)
class TaskAssignAdmin(admin.ModelAdmin):
    search_fields = ['error', 'status', 'line']
    fields = ('error', 'status', 'line')
    list_display = ('error', 'status', 'line')
    inlines = [
        TaskInline,
        TasksListInline,
    ]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
