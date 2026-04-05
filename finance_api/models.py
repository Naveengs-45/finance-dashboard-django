from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICES = [

        ('viewer','Viewer'),
        ('analyst','Analyst'),
        ('admin','Admin')

    ]

    role = models.CharField(max_length=20,choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)


class Record(models.Model):

    TYPE_CHOICES = [

        ('income','Income'),
        ('expense','Expense')

    ]

    amount = models.DecimalField(max_digits=10,decimal_places=2)

    type = models.CharField(max_length=10,choices=TYPE_CHOICES)

    category = models.CharField(max_length=100)

    date = models.DateField()

    description = models.TextField(blank=True)

    created_by = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):

        return self.category