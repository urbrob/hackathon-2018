from django.contrib import admin
from works.models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ['name', 'address', 'email_contact', 'phone_contact']
    fields = ('name', 'address', 'email_contact', 'phone_contact')

"""@admin.register(Group)
class Group(admin.ModelAdmin):
    search_fields = ['name', 'teacher', 'organization']
    fields = ('name', 'teacher', 'organization')
    list_display = ('name', 'teacher', 'organization_name')

@admin.register()"""
