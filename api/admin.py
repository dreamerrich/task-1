from django.contrib import admin
from .models import * 

# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('UUID','project_name','description','project_color_identify','created_at','created_by')
admin.site.register(Project, ProjectAdmin)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','project', 'task_name', 'description', 'user')
admin.site.register(Task, TaskAdmin)

admin.site.register(Permission)