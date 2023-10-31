from django.contrib import admin
from .models import Book, Course, CourseBook

# Register your models here.
admin.site.register(Book)
admin.site.register(Course)
admin.site.register(CourseBook)