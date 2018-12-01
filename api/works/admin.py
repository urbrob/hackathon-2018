from django.contrib import admin
from works.models import Organization, Group, TasksList, Report


class GroupInline(admin.TabularInline):
    model = Group
    extra = 0


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ['name', 'address', 'email_contact', 'phone_contact']
    fields = ('name', 'address', 'email_contact', 'phone_contact')
    inlines = [
        GroupInline,
    ]

@admin.register(Group)
class Group(admin.ModelAdmin):
    search_fields = ['name', 'teacher', 'organization']
    fields = ('name', 'teacher', 'organization')
    list_display = ('name', 'teacher', 'organization_name')

@admin.register(TasksList)
class TasksList(admin.ModelAdmin):
    list_display = ('id', )

@admin.register(Report)
class Report(admin.ModelAdmin):
    search_fields = ['task']
    fields = ('task',)
    list_display = ('task',)
