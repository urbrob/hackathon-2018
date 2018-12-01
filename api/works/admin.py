from django.contrib import admin
from works.models import User, Organization, GroupMembership, Group, TasksList, TaskAssign, Task, Test, TestResult, Report

class OrganizationInline(admin.TabularInline):
    model = Organization
    extra = 0

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
    model = GroupMembership
    extra = 0

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ['name', 'address', 'email_contact', 'phone_contact']
    fields = ('id', 'name', 'address', 'email_contact', 'phone_contact')
    inlines = [
        GroupInline,
        TasksListInline,
    ]

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    search_fields = ['name']
    fields = ('id', 'name',)
    list_display = ('id', 'name',)
    inlines = [
        OrganizationInline,
    ]

@admin.register(TasksList)
class TasksListAdmin(admin.ModelAdmin):
    list_display = ('id', )
    inlines = [
        OrganizationInline,
        GroupInline,
    ]

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    search_fields = ['task', 'accepted_by', 'student']
    fields = ('id', 'task', 'accepted_by', 'student')
    list_display = ('id', 'task', 'accepted_by', 'student' )
    inlines = [
        TestResultInline,
    ]

@admin.register(TaskAssign)
class TaskAssignAdmin(admin.ModelAdmin):
    search_fields = ['error', 'status', 'line']
    fields = ('id', 'error', 'status', 'line')
    list_display = ('id', 'error', 'status', 'line')
    inlines = [
        TaskInline,
    ]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['organization', 'status']
    fields = ('id', 'organization', 'status')
    list_display = ('id', 'organization', 'status')
    inlines = [
        TestResultInline,
        GroupInline,
    ]

@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    search_fields = ['is_teacher']
    fields = ('id', 'is_teacher')
    list_display = ('id', 'is_teacher')
    inlines = [
        UserInline,
        GroupInline,
    ]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id',)
    inlines = [
        TaskAdminInline,
    ]

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id',)
    inlines = [
        TaskAdminInline,
    ]

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('id',)
    inlines = [
        TaskAdminInline,
        TestInline,
        ReportInline,
    ]
