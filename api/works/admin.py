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

class TestForTaskInline(admin.TabularInline):
    model = Test.task.through

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
    fields =  ('name', 'address', 'email_contact', 'phone_contact')
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
    search_fields = ['task', 'accepted_by', 'student']
    fields = ('task', 'accepted_by', 'student')
    list_display = ('task', 'accepted_by', 'student' )
    inlines = [
        TestResultInline,
    ]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'organization', 'status']
    fields = ('first_name', 'last_name', 'organization', 'status', 'username')
    list_display = ('first_name', 'last_name', 'organization', 'status', 'username')
    list_display_links = ('first_name', 'last_name', 'organization', 'status', 'username')
    inlines = [
        GroupMembershipInline,
    ]
    def get_queryset(self, request):
        if request.user.status == User.TEACHER:
            return super(UserAdmin, self).get_queryset(request).filter(status=User.STUDENT,
                group__in=GroupMembership.objects.filter(is_teacher=True, user=request.user).values_list('group', flat=True))
        elif request.user.status == User.STUDENT:
            return []
        return super(UserAdmin, self).get_queryset(request)

@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    search_fields = ['is_teacher', 'group', 'user']
    fields = ('is_teacher', 'group', 'user')
    list_display = ('is_teacher', 'group', 'user')
    def get_queryset(self, request):
        return super(GroupMembershipAdmin, self).get_queryset(request).filter(user__id=request.user.id)


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

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    inlines = [
        TestResultInline,
    ]


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    search_fields = ['error', 'status', 'line']
    fields = ('error', 'status', 'line')
    list_display = ('error', 'status', 'line')
