from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.utils.crypto import get_random_string

class CustomUserManager(BaseUserManager):
    def _create(self, email, password=None,name=None, **extra_fields):
        if not email:
            raise ValueError('Email объязателен для ввода')
        email = self.normalize_email(email)
        user = self.model(email=email,name=name, **extra_fields)
        # print('=----------------------------')
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password,name, **extra):
        extra.setdefault('is_staff', False)
        return self._create(email, password,name, **extra)
        



    def create_superuser(self, email,password,name, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_active', True)
        extra.setdefault('is_superuser', True)
        return self._create(email, password, name, **extra)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True, primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=15, blank=True)
    is_worker = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def create_activation_code(self):
        code = get_random_string(10)
        self.activation_code = code
        self.save()
        return code
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return self.is_superuser