from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
      
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Email must be provided')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user