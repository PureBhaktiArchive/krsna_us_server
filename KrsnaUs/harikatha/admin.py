
from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from .models import User, HarikathaCollection

# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display_links = ('username', 'first_name')

admin.site.register(User, CustomUserAdmin)

requiredInputs = {
    'bhagavatpatrika': ['year', 'issue'],
    'song': ['directory'],
    'lecture': ['directory'],
    'book': ['language']
}

CHOICES = HarikathaCollection.CATEGORY_CHOICES


def has_perm(user, name):
    return user.has_perm('harikatha.write_{}'.format(name))


def get_choices(user):
    return (
        (choice[0], choice[1]) for choice in CHOICES if
        has_perm(user, choice[0])
    )


def can_write(user, obj=None):
    if user.is_superuser:
        return True
    if obj:
        return has_perm(user, obj.category)
    for choice in CHOICES:
        if has_perm(user, choice[0]):
            return True
    return False


def get_categories(user):
    """Return list of categories based on permissions like write_book, write_song"""
    return [
            permission.codename.split('_')[-1] for permission in user.user_permissions.filter(
                codename__startswith='write'
            )
        ]


class HariKathaCollectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # used if form is created separate from admin view i.e testing.
        current_user = kwargs.pop('current_user', None)
        if current_user:
            self.current_user = current_user
        super().__init__(*args, **kwargs)
        self.fields['category'] = forms.ChoiceField(
            choices=CHOICES if self.current_user.is_superuser else get_choices(self.current_user),
            required=False if self.instance and self.instance.pk else True
        )

    class Meta:
        model = HarikathaCollection
        fields = '__all__'
        exclude = ('indexed',)

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        if not category:
            category = self.instance and self.instance.category
            # this should not happen
            if not category:
                self.add_error('category', 'Category required')
        if category in requiredInputs:
            for field in requiredInputs[category]:
                data = cleaned_data.get(field)
                if not data:
                    self.add_error(field, 'This field is required when {} is selected'.format(category))
        else:
            extra_fields = ['language', 'directory', 'year', 'issue']
            for field in extra_fields:
                if cleaned_data.get(field):
                    self.add_error(field, 'This field is not allowed when {} is selected'.format(category))


class HariKathaCollectionAdmin(admin.ModelAdmin):
    exclude = ('indexed',)
    form = HariKathaCollectionForm

    def get_list_display(self, request):
        base_display = ('title', 'link', 'category')
        if request.user.is_superuser:
            base_display += ('directory', 'issue', 'year', 'language')
            return base_display
        for category in get_categories(request.user):
            if category in requiredInputs:
                for field in requiredInputs[category]:
                    base_display += (field,)
        return base_display

    def get_queryset(self, request):
        if request.user.is_superuser:
            return HarikathaCollection.objects.all()
        categories = get_categories(request.user)
        return HarikathaCollection.objects.filter(category__in=categories)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['category', 'item_id']
        else:
            return []

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form

    def has_add_permission(self, request):
        return can_write(request.user)

    def has_change_permission(self, request, obj=None):
        return can_write(request.user, obj)

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(HarikathaCollection, HariKathaCollectionAdmin)
