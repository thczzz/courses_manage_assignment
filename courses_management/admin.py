from django.contrib import admin
from .models import Student, Instructor, Course, student_courses_xref
# Register your models here.

admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(student_courses_xref)
