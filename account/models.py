from django.db import models
import random
from django.contrib.auth.models import AbstractUser
import datetime

# Create your models here.


class User(AbstractUser):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    REL_STATAS = [
        ('Single','Single'),
        ('Single with Kid(s)','Single with Kid(s)'),
        ('Divorced','Divorced'),
        ('Divorced with Kid(s)','Divorced with Kid(s)'),
        ('Widowed','Widowed'),
        ('Widowed with Kid(s)','Widowed with Kid(s)'),
        ('Separated','Separated'),
        ('Separated with Kid(s)','Separated with Kid(s)'),
    ]
    SMOKE = [
        ('No','No'),
        ('Yes','Yes'),
        ('Plan to Quit','Plan to Quit')
    ]

    DRINKING = [
        ('Regular','Regular'),
        ('Socialy','Socialy'),
        ('Occasionally','Occasionally'),
        ('Teetotaler','Teetotaler'),
        ('Plan to Quit','Plan to Quit')
    ]
    phone = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    bio=models.TextField(blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,default='Male')
    interest = models.CharField(max_length=100,null=True,blank=True)
    qualification=models.CharField(max_length=25,null=True, blank=True)
    location=models.CharField(max_length=100,blank=True,null=True)
    rel_status = models.CharField(max_length=25, choices=REL_STATAS,default='Single')
    smoke = models.CharField(max_length=15,choices=SMOKE,default='No')
    drinking = models.CharField(max_length=15,choices=DRINKING,default='Teetotaler')
    images = models.FileField(upload_to='upload/',null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)

    @property 
    def full_name(self):
        return f"{(self.first_name) (self.last_name)}"

    
    @property
    def age(self):
        if self.dob:
            return (datetime.date.today() - self.dob).days // 365
        return None     


class EmailOTP(models.Model):
    email = models.EmailField(unique=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()

    def __str__(self):
        return self.email
    


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.position}"

class Jobseeker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,null=True, blank=True)
    expertise_level = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.expertise_level}"
    
       
class Relationship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    relation = models.CharField(max_length=100,null=True, blank=True)
     
    @property
    def full_name(self):
        return f"{(User.first_name) (User.last_name)}"
    
    
    def __str__(self) -> str:
        return self.full_name

     
    
