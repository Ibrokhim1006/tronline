from django.contrib import admin
from employe.models import Employe, EmployeRoll


class AdminEmployeRoll(admin.ModelAdmin):
    list_display = ['id', 'name']

admin.site.register(EmployeRoll, AdminEmployeRoll)

class AdminEpmloye(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone']

admin.site.register(Employe, AdminEpmloye)
