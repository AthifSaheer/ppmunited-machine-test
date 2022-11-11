from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

class Instructor(models.Model):
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    qualification = models.CharField(max_length=200, null=True, blank=True)
    introduction_brief = models.CharField(max_length=250, null=True, blank=True)
    image = models.FileField(upload_to="Images", null=True, blank=True)

    num_of_published_course = models.IntegerField(default=0)
    num_of_enrolled_students = models.IntegerField(default=0)
    average_review_rating = models.IntegerField(default=0)
    num_of_reviews = models.IntegerField(default=0)
    registration_date = models.DateField(auto_now_add=True)

class Language(models.Model):
    language = models.CharField(max_length=100)

class Chapter(models.Model):
    title = models.CharField(max_length=200)
    
class Course(models.Model):
    title = models.CharField(max_length=200)
    course_brief = models.CharField(max_length=200)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    course_fee = models.IntegerField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

class Student(models.Model):
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    num_of_course_enrolled = models.IntegerField(default=0)
    num_of_course_completed = models.IntegerField(default=0)
    registration_date = models.DateField(auto_now_add=True)

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_date = models.DateField(auto_now_add=True)
    is_paid_subscription = models.BooleanField(default=False)

class Feedback(models.Model):
    enroll = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    rating_score = models.IntegerField()
    feedback_text = models.CharField(max_length=200)
    submition_date = models.DateField(auto_now_add=True)
