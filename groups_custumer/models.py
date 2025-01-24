from django.db import models
from authen.models import CustomUser
from employe.models import Employe


class TypeSports(models.Model):
    name = models.CharField(max_length=250, verbose_name='Вид спорта')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "type_sport"
        verbose_name = "Вид спорта"
        verbose_name_plural = "Вид спорта"


class Week(models.Model):
    name = models.CharField(max_length=250, verbose_name='Неделя')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "week"
        verbose_name = "Неделя"
        verbose_name_plural = "Неделя"


class GroupsClass(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    type_sport = models.ForeignKey(TypeSports, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Вид спорта')
    employe_id = models.ManyToManyField(Employe, null=True, blank=True,  verbose_name='Тренеры')
    strat_training = models.DateField(null=True, blank=True, verbose_name='Начало обучения')
    position = models.BigIntegerField(null=True, blank=True, verbose_name='Позиция')
    owner_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='owner', verbose_name='Владелец')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "groups_class"
        verbose_name = "Группа класса"
        verbose_name_plural = "Группа класса"


class Schedule(models.Model):
    groups_id = models.ForeignKey(GroupsClass, on_delete=models.CASCADE, null=True, blank=True, related_name='groups', verbose_name='Группа класса')
    week = models.ForeignKey(Week, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='День недели')
    strat_time = models.TimeField(null=True, blank=True, verbose_name='Время начала')
    end_time = models.TimeField(null=True, blank=True, verbose_name='Время окончания')

    class Meta:
        db_table = "schedule"
        verbose_name = "Расписание"
        verbose_name_plural = "Расписание"
