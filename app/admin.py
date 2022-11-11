from django.contrib import admin
from .models import *

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("username", )

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("language", )

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("title", )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("username", "email")

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "course_brief")

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "enrolled_date")

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("rating_score", "feedback_text")