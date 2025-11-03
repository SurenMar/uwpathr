from django.db import models
from django.contrib.auth.models import (
  BaseUserManager, 
  AbstractBaseUser,
  PermissionsMixin
)
from .utils import current_year


# Tells django how to create my custom users and superusers
class UserAccountManager(BaseUserManager):
  def create_user(self, email, first_name, password=None, **kwargs):
    if not email:
      raise ValueError("Users must have an email address")
    # This auto formats the email after @
    email = self.normalize_email(email)
    email = email.lower()

    if not first_name:
      first_name = email.split('@')[0]

    user = self.model(
      email=email,
      first_name=first_name
      **kwargs
    )

    user.set_password(password) # Hashes password
    user.save(using=self._db)
    return user

  def create_superuser(self, email, first_name, password=None, **kwargs):
    user = self.create_user(
      email,
      first_name,
      password=password,
      **kwargs
    )

    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)
    return user


# The actual user model
class UserAccount(AbstractBaseUser, PermissionsMixin):
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)
  first_name = models.CharField(max_length=255, blank=True)
  email = models.EmailField(unique=True, max_length=255)
  start_year = models.PositiveSmallIntegerField(
    default=current_year, 
    blank=True
  )
  active_specialization = models.ForeignKey(
    'Specialization', #TODO
    on_delete=models.PROTECT,
    related_name='users'
  )

  # Tells django to use our custom manger for creating users
  objects = UserAccountManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name'] # For creating superuser

  def __str__(self):
    return self.email