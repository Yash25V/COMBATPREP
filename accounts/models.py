from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('OFFICER', 'Officer'),
        ('SOLDIER', 'Soldier'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='SOLDIER')
    is_email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    def is_admin(self):
        return self.role == 'ADMIN' or self.is_superuser

    def is_officer(self):
        return self.role == 'OFFICER'

    def is_soldier(self):
        return self.role == 'SOLDIER'
