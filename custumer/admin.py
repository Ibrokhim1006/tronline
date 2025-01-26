from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from custumer.models import (
    SportCategory, Custumer, CustumerDocs, CustumerRepresentatives, CustumerSubscription, TypeRepresentatives
)


admin.site.register(SportCategory)
admin.site.register(TypeRepresentatives)


class LimitCustumerSubscription(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # count all forms that have not been marked for deletion
        count = sum(1 for form in self.forms if not self._should_delete_form(form))
        max_num = 10  # specify your max number of images here
        if count > max_num:
            raise ValidationError(f'You can only associate up to {max_num} images with this product.')


class CustumerSubscriptionInline(admin.TabularInline):
    model = CustumerSubscription
    formset = LimitCustumerSubscription
    extra = 1
    min_num = 1
    max_num = 10


class LimitCustumerDocs(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # count all forms that have not been marked for deletion
        count = sum(1 for form in self.forms if not self._should_delete_form(form))
        max_num = 10  # specify your max number of images here
        if count > max_num:
            raise ValidationError(f'You can only associate up to {max_num} images with this product.')


class CustumerDocsInline(admin.TabularInline):
    model = CustumerDocs
    formset = LimitCustumerDocs
    extra = 1
    min_num = 1
    max_num = 10


class LimitCustumerRepresentatives(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # count all forms that have not been marked for deletion
        count = sum(1 for form in self.forms if not self._should_delete_form(form))
        max_num = 10  # specify your max number of images here
        if count > max_num:
            raise ValidationError(f'You can only associate up to {max_num} images with this product.')


class CustumerRepresentativesInline(admin.TabularInline):
    model = CustumerRepresentatives
    formset = LimitCustumerRepresentatives
    extra = 1
    min_num = 1
    max_num = 10




class AdminCustumer(admin.ModelAdmin):
    inlines = [
        CustumerSubscriptionInline,
        CustumerDocsInline,
        CustumerRepresentativesInline

    ]
    list_display = ['id', 'full_name', 'birth_date', 'phone']
    search_fields = ['id', 'full_name', 'birth_date', 'phone']

admin.site.register(Custumer, AdminCustumer)

