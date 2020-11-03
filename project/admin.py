from django.contrib import admin

from project.models import Project, Deliverable


@admin.register(Deliverable)
class DeliverableAdmin(admin.ModelAdmin):
    list_display = ('name', 'addingDate', 'status', 'progression', 'project')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'creationDate', 'status', 'advancement')

