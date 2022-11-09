from django.db import models

# Create your models here.


class Student(models.Model):
    pin = models.CharField(max_length=7, primary_key=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    time_created = models.DateTimeField(auto_now_add=True)


class Instructor(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    time_created = models.DateTimeField(auto_now_add=True)


class Course(models.Model):
    name = models.CharField(max_length=100)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    total_time = models.SmallIntegerField()
    credit = models.SmallIntegerField()
    time_created = models.DateTimeField(auto_now_add=True)


class student_courses_xref(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completion_date = models.DateTimeField(blank=True, null=True)
