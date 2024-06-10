from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.urls import reverse
from .manager import UserManager
# Create your models here.
class User(AbstractBaseUser):
    
    email = models.EmailField(max_length=255,unique=True)
    is_active = models.BooleanField(default=True, )
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='static/media/avatar/', default='static/media/avatar/no_image.png', null=True, blank=True)
    objects = UserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


    def __str__(self):
        return self.email
    
    @property
    def is_staff(self):
        return self.is_admin
    
    # def get_absolute_url(self):
    #     return reverse('user_profile:profile')

    