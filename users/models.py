from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# def user_directory_path(instance, filename):
#     return 'user_{0}/{1}'.format(instance.user.id, filename)

# class User(AbstractUser):			
#     profile_picture = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
#     phone_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{10}', message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
#     phone = models.DecimalField(validators=[phone_regex], max_digits=10, decimal_places=0)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username', 'phone',]

#     def __str__(self):
#         return u'Profile of user: %s' % self.user