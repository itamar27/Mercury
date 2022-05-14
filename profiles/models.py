from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, first_name, last_name, password=None):
        """Create a new user """
        if not email:
            raise ValueError("Email has to be provided")
        #insert email and full name to profile
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        #set password as a hash
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, password):
        """Create and save superuser"""
        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Researcher(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    
    #Mercury related fields
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    
    #General user fields
    is_active= models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    #Define a class to interact with django cli/ admin system
    objects=UserProfileManager()

    #Configure email to be the main key for users authentication  
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['first_name','last_name']

    def get_full_name(self):
        """Return the full name of user"""
        return self.first_name + ' ' + self.last_name
    
    def get_short_name(self):
        """Return the first name of user"""
        return self.first_name

    def __str__(self):
        """Return string representation of user (email only)"""
        return self.email


