from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


class Gender(models.Model):
    name = models.CharField(max_length=250, verbose_name="Пол")

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "gender"
        verbose_name = "Пол"
        verbose_name_plural = "Пол"


class CustomUser(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+9989999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=250, null=True, blank=True, unique=True, verbose_name="Телефон")
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, verbose_name="Аватар")