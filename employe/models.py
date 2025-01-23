from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from authen.models import CustomUser, Gender


class EmployeRoll(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название")
    permissons = models.ManyToManyField(Permission, null=True, verbose_name="Права")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Владелец")

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "employe_roll"
        verbose_name = "Сотрудники Ролл"
        verbose_name_plural = "Сотрудники Ролл"


class Employe(models.Model):
    full_name = models.CharField(max_length=250, verbose_name="Ф.И.О")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+9989999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=250, null=True, blank=True, unique=True, verbose_name="Телефон")
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, verbose_name="Пол")
    roll = models.ForeignKey(EmployeRoll, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Ролл")
    decription = models.TextField(null=True, blank=True, verbose_name="Комментарий")
    is_send = models.BooleanField(default=False, verbose_name="Отправить приглашение")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="user_id", verbose_name="Пользователь")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="owner_id", verbose_name="Владелец")

    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = "employe"
        verbose_name = "Сотрудники"
        verbose_name_plural = "Сотрудники"