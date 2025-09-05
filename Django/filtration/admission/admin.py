from django.contrib import admin
from .models import Student, Branch, Admission

# Register your models here.
admin.site.register(Student)
admin.site.register(Branch)
admin.site.register(Admission)
