from django.contrib import admin
from .models import task, taskRecord
# Register your models here.

admin.site.register(task)
admin.site.register(taskRecord)

