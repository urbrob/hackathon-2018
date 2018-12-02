from django.contrib import admin
from works.models import User, Organization, GroupMembership, Group, TasksList, TaskAssign, Task, Test, TestResult, Report
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

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
    model = Test

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
    def get_queryset(self, request):
        if request.user.status == User.TEACHER:
            return super(GroupAdmin, self).get_queryset(request).filter(groupmembership__group=request.user.group)
        elif request.user.status == User.STUDENT:
            return [super(GroupAdmin, self).get_queryset(request).filter(user__id=request.user.id)]
        elif request.user.status == User.ADMIN:
            return super(GroupAdmin, self).get_queryset(request).filter(groupmembership__organization=request.user.organization)
        return super(GroupAdmin, self).get_queryset(request)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    search_fields = ['task', 'file', 'accepted_by', 'student']
    fields = ('task', 'file', 'accepted_by', 'student', 'passed')
    list_display = ('task', 'accepted_by', 'student', 'passed')
    inlines = [
        TestResultInline,
    ]
    def get_queryset(self, request):
        if request.user.status == User.TEACHER:
            return super(ReportAdmin, self).get_queryset(request).filter(user__id=request.user.id)
        elif request.user.status == User.STUDENT:
            return []
        elif request.user.status == User.ADMIN:
            return super(ReportAdmin, self).get_queryset(request).filter(task_list__organization=request.user.organization)
        return super(ReportAdmin, self).get_queryset(request)



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
        if request.user.status == User.TEACHER:
            return super(TaskAdmin, self).get_queryset(request).filter(task_list__organization=request.user.organization)
        elif request.user.status == User.STUDENT:
            return super(TaskAdmin, self).get_queryset(request).filter(user__group=request.user.group)
        return super(TaskAdmin, self).get_queryset(request)



@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    inlines = [
        TestResultInline,
    ]
    def get_queryset(self, request):
        if request.user.status == User.TEACHER:
            return super(TestAdmin, self).get_queryset(request).filter(task_list__organization=request.user.organization)
        elif request.user.status == User.STUDENT:
            return super(TestAdmin, self).get_queryset(request).filter(user__group=request.user.group)
        elif request.user.status == User.ADMIN:
            return super(TestAdmin, self).get_queryset(request).filter(task_list__organization=request.user.organization)
        return super(TestAdmin, self).get_queryset(request)


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    search_fields = ['error', 'passed', 'line']
    fields = ('error', 'passed', 'line')
    list_display = ('error', 'passed', 'line')
    def get_queryset(self, request):
        if request.user.status == User.TEACHER:
            return super(TestResultAdmin, self).get_queryset(request).filter(task_list__group=request.user.group)
        elif request.user.status == User.STUDENT:
            return super(TestResultAdmin, self).get_queryset(request).filter(user__id=request.user.id)
        elif request.user.status == User.ADMIN:
            return super(TestResultAdmin, self).get_queryset(request).filter(task_list__organization=request.user.organization)
        return super(TestResultAdmin, self).get_queryset(request)
