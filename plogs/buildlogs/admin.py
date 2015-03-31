from django.contrib import admin
from .models import Partner, Category, BuildLog, Project

admin.site.register(Partner)
admin.site.register(Category)
admin.site.register(BuildLog)
admin.site.register(Project)