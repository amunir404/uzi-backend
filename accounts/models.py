from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(
            email=email,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email,
            password=password,
            **kwargs
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        INVESTOR = "INVESTOR", "Investor"
        PARTNER = "PARTNER", "Partner"
        MANAGER = "MANAGER", "Manager"

    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.INVESTOR)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserAccountManager()
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email
