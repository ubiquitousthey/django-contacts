from django import forms
from django.contrib.admin import widgets
from django.utils.translation import ugettext_lazy as _
try:
    from django.contrib.contenttypes.generic import \
        generic_inlineformset_factory as inlineformset_factory
except ImportError:
    from django.contrib.contenttypes.forms import \
        generic_inlineformset_factory as inlineformset_factory

from contacts import models


class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = ('name', 'nickname', 'about')


class CompanyUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = '__all__'


class PersonCreateForm(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = ('first_name', 'last_name', 'title', 'company', 'about')


class PersonUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = ('first_name', 'last_name', 'title', 'company')


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = '__all__'
        widgets = {
            'people': widgets.FilteredSelectMultiple(
                _("People"), is_stacked=False),
            'companies': widgets.FilteredSelectMultiple(
                _("Companies"), is_stacked=False),
        }


class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = ('name', 'about')


class GroupUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Group
        exclude = ('slug',)


PhoneNumberFormSet = inlineformset_factory(models.PhoneNumber, extra=1)
EmailAddressFormSet = inlineformset_factory(models.EmailAddress, extra=1)
InstantMessengerFormSet = inlineformset_factory(models.InstantMessenger,
                                                extra=1)
WebSiteFormSet = inlineformset_factory(models.WebSite, extra=1)
StreetAddressFormSet = inlineformset_factory(models.StreetAddress, extra=1)
SpecialDateFormSet = inlineformset_factory(models.SpecialDate, extra=1)
