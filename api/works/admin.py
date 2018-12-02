from django.contrib import admin
from works.models import User, Organization, GroupMembership, Group, TasksList, TaskAssign, Task, Test, TestResult, Report
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class GroupInline(admin.TabularInline):
    model = Group
    extra = 0

class TasksListInline(admin.TabularInline):
    model = TasksList
    extra = 0

class TaskInline(admin.TabularInline):
    model = Task
    extra = 0

class TestForTaskInline(admin.TabularInline):
    model = Test
    extra = 0


class TestResultInline(admin.TabularInline):
    model = TestResult
    extra = 0
    readonly_fields = ('report', 'test', 'error', 'passed', 'line')
    max_num = 0

    def has_add_permission(self, obj):
        return False
        

class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra = 0

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ['name', 'address', 'email_contact', 'phone_contact']
    fields = ('name', 'address', 'email_contact', 'phone_contact')
    list_display = ('name', 'address', 'email_contact', 'phone_contact')
    inlines = [
        GroupInline,
        TasksListInline,
    ]

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    search_fields = ['name', 'organization']
    fields = ('name', 'organization')
    list_display = ('name', 'organization')
    inlines = [
        GroupMembershipInline,
    ]



@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    search_fields = ['task', 'file', 'accepted_by', 'student']
    fields = ('task', 'file', 'accepted_by', 'student')
    list_display = ('task', 'accepted_by', 'student', 'passed')
    inlines = [
        TestResultInline,
    ]


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    search_fields = ['first_name', 'last_name', 'organization', 'status', 'username', 'is_staff', 'password']
    fieldsets = (
        ('Personal info', {
            'fields': ('first_name', 'last_name')
            }
        ),
        ('The rest of important things', {
            'fields': ('organization', 'status', 'username', 'is_staff', 'password')
            }
        ),
    )
    list_display = ('first_name', 'last_name', 'organization', 'status', 'username', 'is_staff', 'password')
    inlines = [
        GroupMembershipInline,
    ]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ['title']
    fields = ('title', 'description')
    list_display =  ('title', 'description')
    inlines = [
        TestForTaskInline,
    ]
    exclude = ('test',)
    def get_queryset(self, request):
        return super(TaskAdmin, self).get_queryset(request).filter(task_list__organization=request.user.organization)
