from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
      """
      Create and return a `User` with superuser powers.

      Superuser powers means that this use is an admin that can do anything
      they want.
      """
      if password is None:
          raise TypeError('Superusers must have a password.')

      user = self.create_user(username, email, password)
      user.is_superuser = True
      user.is_staff = True
      user.save()

      return user

class User(AbstractBaseUser, PermissionsMixin):
    # db_index means that the database will make an index for lookups
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    # is_staff is used to define superusers
    is_staff = models.BooleanField(default=False)
    # Each teacher or student must have an enroll number
    enroll_number = models.CharField(db_index=True, max_length=30, unique=True)
    is_teacher = models.BooleanField(default=False)
    birth_date = models.DateField(null=True)
    created_at = models.DateField(auto_now=True)
    course = models.CharField(max_length=255, null=True)
    # Define what field will be used to log in the system
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    # Necessary to user admin site
    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.email

    def get_full_name(self):
      """
      This method is required by Django for things like handling emails.
      Typically, this would be the user's first and last name. Since we do
      not store the user's real name, we return their username instead.
      """
      return self.username

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.username

    def authenticate(self, email=None, password=None):
        print("sdfsdf " +email+ ' ' + password)
        try:
            user = User.objects.get(email=email)
            print("cheguei " + user.password + ' ' + password)
            if password == user.password:
              print('ok')
              return user
            else:
              print('erro')
              return None
        except User.DoesNotExist:
            print('asdfghj')
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
