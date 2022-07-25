from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    )
    password = models.CharField(max_length=128, blank=True)
    confirmation_code = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=ROLES, default='user')
    bio = models.TextField(blank=True)

    class Meta(AbstractUser.Meta):
        ordering = ('-date_joined',)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
