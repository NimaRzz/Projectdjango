from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, phone, email, fullname, password):
        if not email:
          raise ValueError('You do not have an email')
        
        if not phone:
          raise ValueError('You do not have an phone')
        
        if not fullname:
          raise ValueError('You do not have an fullname')
        user = self.model(phone=phone, email=self.normalize_email(email), fullname=fullname)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, phone, email, fullname, password):
       user = self.create_user(phone=phone, email=email, fullname=fullname, password=password)
       user.is_admin = True
       user.is_superuser = True
       user.save()
       return user

class User(PermissionsMixin, AbstractBaseUser):
    phone = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=30)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
        
    
    objects = UserManager()

    USERNAME_FIELD =    'phone'
    REQUIRED_FIELDS = ['email', 'fullname']
     
    def __str__(self):
        return self.phone
    
    def is_staff(self):
        return self.is_admin

class OtpCode(models.Model):
   code = models.PositiveSmallIntegerField()
   phone = models.CharField(max_length=11)
   created = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return f'{self.phone} - {self.code} - {self.created}'
  