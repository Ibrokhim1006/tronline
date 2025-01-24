from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from groups_custumer.models import TypeSports, Week, GroupsClass, Schedule


admin.site.register(TypeSports)
admin.site.register(Week)


class LimitSchedule(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # count all forms that have not been marked for deletion
        count = sum(1 for form in self.forms if not self._should_delete_form(form))
        max_num = 7  # specify your max number of images here
        if count > max_num:
            raise ValidationError(f'You can only associate up to {max_num} images with this product.')


class ScheduleInline(admin.TabularInline):
    model = Schedule
    formset = LimitSchedule
    extra = 1
    min_num = 1
    max_num = 7


class AdminGroupsClass(admin.ModelAdmin):
    inlines = [
        ScheduleInline
    ]
    list_display = ['id', 'name', 'type_sport', 'strat_training']
    search_fields = ['name', 'type_sport', 'strat_training']
    list_filter = ['name']

admin.site.register(GroupsClass, AdminGroupsClass)