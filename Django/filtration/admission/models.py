from django.db import models

# Create your models here.
class Branch(models.Model):
    BRANCH_CHOICES = [
        ('ECE', 'Electronics & Communication'),
        ('CSE', 'Computer Science'),
        ('CVE', 'Civil Engineering'),
        ('ME', 'Mechanical Engineering'),
    ]
    name = models.CharField(max_length=30, choices=BRANCH_CHOICES)
    short_form = models.CharField(max_length=3)

    def __str__(self):
        return self.name
    
class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    ]
    name = models.CharField(max_length=40)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    age = models.IntegerField()
    sem = models.IntegerField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=10, unique=True)
    registration_date = models.DateField()

    def __str__(self):
        return self.name

class Admission(models.Model):
    students = models.OneToOneField(Student, on_delete=models.CASCADE)
    sem = models.IntegerField(max_length=1)
    fees = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.student.name} - {self.fees}"
