from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password = None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email= email, name=name,)  # will create new model for the admin

        user.set_password(password) #so the set password function is encrypted and showed as a hash
        user.save(using = self._db) #standard procedure to save objects in django

        return user

    def create_superuser(self, email, name, password): #password not none bec superuser needs a password
        """Create and save a new super user with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True     ## is staff and is user automatically created by PermisssionsMixin
        user.save(using = self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system."""
    email = models.EmailField(max_length=255, unique = True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager() #havent created this yet

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['name',]


    def get_full_name(self):
        """Retrieve full name of the user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of the user"""
        return self.name   #dont have short name field right now so same
    def __str__(self): #recommended for all django mdels to return string represetnation of our user
        """Return string representation of our user"""
        return self.email  #will show users by email addresses
