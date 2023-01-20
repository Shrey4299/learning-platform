from django.db import models


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    about = models.TextField()
    type = models.CharField(max_length=100, choices=(
        ('IT', 'IT'),
        ('NON IT', 'NON IT'),
        ('Mobiles phones', 'Mobiles phones')
    ))
    added_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default= True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    adress= models.CharField(max_length=50)
    phone=models.CharField(max_length=10)
    about=models.TextField()
    position= models.CharField(max_length=20, choices=(
        ('Manager', 'Manager'),
        ('Software Developer', 'SDE'),
        ('Hiring Mnager', 'HR')
    ))
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
