from django.db import models
from django.core.validators import RegexValidator

from authen.models import CustomUser, Gender
from groups_custumer.models import GroupsClass


class TypeRepresentatives(models.Model):
    name = models.CharField(max_length=250, verbose_name='Представители')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "type_representatives"
        verbose_name = "Тип родства"
        verbose_name_plural = "Тип родства"


class SportCategory(models.Model):
    name = models.CharField(max_length=250, verbose_name='Спортивный разряд')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "sport_category"
        verbose_name = "Спортивный разряд"
        verbose_name_plural = "Спортивный разряд"


class Custumer(models.Model):
    full_name = models.CharField(max_length=250, verbose_name='Ф.И.О')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+9989999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=250, null=True, blank=True, unique=True, verbose_name='Телефон')
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пол')
    birth_date = models.DateField(verbose_name='День рождения')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    email = models.EmailField(verbose_name='E-mail')
    contract_number = models.CharField(max_length=250, verbose_name='Номер договора')
    contract_type = models.CharField(max_length=250, verbose_name='Тип договора')
    strat_date = models.DateField(verbose_name='Дата начала обучения')
    groups = models.ManyToManyField(GroupsClass, blank=True, verbose_name='Группы')
    sport_category = models.ForeignKey(SportCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Спортивный разряд')
    photo = models.ImageField(upload_to='custumer/', null=True, blank=True, verbose_name='Фото')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Владелец')

    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = "custumer"
        verbose_name = "Клиент"
        verbose_name_plural = "Клиент"


class CustumerSubscription(models.Model):
    custumer = models.ForeignKey(Custumer, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Клиент')
    groups = models.ForeignKey(GroupsClass, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Группы')
    number_classes = models.BigIntegerField(verbose_name='Количество занятий', null=True, blank=True)
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    unlimited = models.BooleanField(default=False, verbose_name='Безлимитный')

    class Meta:
        db_table = "custumer_subscription"
        verbose_name = "Абонемент"
        verbose_name_plural = "Абонемент"


class CustumerDocs(models.Model):
    custumer = models.ForeignKey(Custumer, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Клиент')
    name = models.CharField(max_length=250, verbose_name='Название')
    files = models.FileField(upload_to='custumer_files/', verbose_name='Файл')
    
    class Meta:
        db_table = "custumer_docs"
        verbose_name = "Документы"
        verbose_name_plural = "Документы"


class CustumerRepresentatives(models.Model):
    custumer = models.ForeignKey(Custumer, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Клиент')
    type = models.ForeignKey(TypeRepresentatives, on_delete=models.CASCADE, verbose_name='Тип родства')
    full_name = models.CharField(max_length=250, verbose_name='Ф.И.О')
    phone = models.CharField(max_length=250, verbose_name='Телефон')
    work = models.CharField(max_length=250, null=True, blank=True, verbose_name='Место работы')

    class Meta:
        db_table = "custumer_representatives"
        verbose_name = "Представители"
        verbose_name_plural = "Представители"