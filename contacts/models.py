from django.db import models
from django.db.models import permalink
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils.encoding import python_2_unicode_compatible
from django_comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import (GenericRelation,
                                                GenericForeignKey)

from contacts.managers import SpecialDateManager


@python_2_unicode_compatible
class Company(models.Model):
    """Company model."""
    name = models.CharField(_('name'), max_length=200)
    nickname = models.CharField(_('nickname'), max_length=50, blank=True,
                                null=True)
    slug = models.SlugField(_('slug'), max_length=50, unique=True)
    about = models.TextField(_('about'), blank=True, null=True)
    logo = models.ImageField(_('photo'), upload_to='contacts/companies/',
                             blank=True)

    phone_number = GenericRelation('PhoneNumber')
    email_address = GenericRelation('EmailAddress')
    instant_messenger = GenericRelation('InstantMessenger')
    web_site = GenericRelation('WebSite')
    street_address = GenericRelation('StreetAddress')
    special_date = GenericRelation('SpecialDate')
    note = GenericRelation(Comment, object_id_field='object_pk')

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    class Meta:
        db_table = 'contacts_companies'
        ordering = ('name',)
        verbose_name = _('company')
        verbose_name_plural = _('companies')

    def __str__(self):
        return "%s" % self.name

    @permalink
    def get_absolute_url(self):
        return ('contacts_company_detail', None, {
            'pk': self.pk,
            'slug': self.slug,
        })

    @permalink
    def get_update_url(self):
        return ('contacts_company_update', None, {
            'pk': self.pk,
            'slug': self.slug,
        })

    @permalink
    def get_delete_url(self):
        return ('contacts_company_delete', None, {
            'pk': self.pk,
            'slug': self.slug,
        })


@python_2_unicode_compatible
class Person(models.Model):
    """Person model."""
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=200)
    middle_name = models.CharField(_('middle name'), max_length=200, blank=True, null=True)
    suffix = models.CharField(_('suffix'), max_length=50, blank=True, null=True)
    nickname = models.CharField(_('nickname'), max_length=100, blank=True)
    slug = models.SlugField(_('slug'), max_length=50, unique=True)
    title = models.CharField(_('title'), max_length=200, blank=True)
    company = models.ForeignKey(Company, blank=True, null=True)
    about = models.TextField(_('about'), blank=True)
    photo = models.ImageField(_('photo'), upload_to='contacts/person/',
                              blank=True)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True,
                                null=True, verbose_name=_('user'))

    phone_number = GenericRelation('PhoneNumber')
    email_address = GenericRelation('EmailAddress')
    instant_messenger = GenericRelation('InstantMessenger')
    web_site = GenericRelation('WebSite')
    street_address = GenericRelation('StreetAddress')
    special_date = GenericRelation('SpecialDate')
    note = GenericRelation(Comment, object_id_field='object_pk')

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    class Meta:
        db_table = 'contacts_people'
        ordering = ('last_name', 'first_name')
        verbose_name = _('person')
        verbose_name_plural = _('people')

    def __str__(self):
        return self.fullname

    @property
    def fullname(self):
        return "%s %s" % (self.first_name, self.last_name)

    @permalink
    def get_absolute_url(self):
        return ('contacts_person_detail', None, {
            'pk': self.pk,
            'slug': self.slug,
        })

    @permalink
    def get_update_url(self):
        return ('contacts_person_update', None, {
            'pk': self.pk,
            'slug': self.slug,
        })

    @permalink
    def get_delete_url(self):
        return ('contacts_person_delete', None, {
            'pk': self.pk,
            'slug': self.slug,
        })


@python_2_unicode_compatible
class Group(models.Model):
    """Group model."""
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=50, unique=True)
    about = models.TextField(_('about'), blank=True)

    people = models.ManyToManyField(Person, verbose_name='people', blank=True)
    companies = models.ManyToManyField(Company, verbose_name='companies',
                                       blank=True)

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    class Meta:
        db_table = 'contacts_groups'
        ordering = ('name',)
        verbose_name = _('group')
        verbose_name_plural = _('groups')

    def __str__(self):
        return "%s" % self.name

    @permalink
    def get_absolute_url(self):
        return ('contacts_group_detail', None, {
            'pk': self.pk,
            'slug': self.slug,
        })

    @permalink
    def get_update_url(self):
        return ('contacts_group_update', None, {
            'pk': self.pk,
            'slug': self.slug,
        })

    @permalink
    def get_delete_url(self):
        return ('contacts_group_delete', None, {
            'pk': self.pk,
            'slug': self.slug,
        })


@python_2_unicode_compatible
class Location(models.Model):
    """Location model."""
    WEIGHT_CHOICES = [(i, i) for i in range(11)]

    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=50, unique=True)

    is_phone = models.BooleanField(_('is phone'), default=False,
        help_text=_("Only used for Phone"))
    is_street_address = models.BooleanField(_('is street address'),
        default=False, help_text=_("Only used for Street Address"))

    weight = models.IntegerField(choices=WEIGHT_CHOICES, default=0)

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        db_table = 'contacts_locations'
        ordering = ('weight',)
        verbose_name = _('location')
        verbose_name_plural = _('locations')


@python_2_unicode_compatible
class PhoneNumber(models.Model):
    """Phone Number model."""
    content_type = models.ForeignKey(ContentType, limit_choices_to={
        'app_label': 'contacts'})
    object_id = models.IntegerField(db_index=True)
    content_object = GenericForeignKey()

    phone_number = models.CharField(_('number'), max_length=50)
    location = models.ForeignKey(Location, limit_choices_to={
        'is_street_address': False})

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    def __str__(self):
        return "%s (%s)" % (self.phone_number, self.location)

    class Meta:
        db_table = 'contacts_phone_numbers'
        verbose_name = _('phone number')
        verbose_name_plural = _('phone numbers')


@python_2_unicode_compatible
class EmailAddress(models.Model):
    content_type = models.ForeignKey(ContentType, limit_choices_to={
        'app_label': 'contacts'})
    object_id = models.IntegerField(db_index=True)
    content_object = GenericForeignKey()

    email_address = models.EmailField(_('email address'))
    location = models.ForeignKey(Location, limit_choices_to={
        'is_street_address': False, 'is_phone': False})

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    def __str__(self):
        return "%s (%s)" % (self.email_address, self.location)

    class Meta:
        db_table = 'contacts_email_addresses'
        verbose_name = _('email address')
        verbose_name_plural = _('email addresses')


@python_2_unicode_compatible
class InstantMessenger(models.Model):
    OTHER = 'other'

    IM_SERVICE_CHOICES = (
        ('aim', _('AIM')),
        ('msn', _('MSN')),
        ('icq', _('ICQ')),
        ('jabber', _('Jabber')),
        ('yahoo', _('Yahoo')),
        ('skype', _('Skype')),
        ('qq', _('QQ')),
        ('sametime', _('Sametime')),
        ('gadu-gadu', _('Gadu-Gadu')),
        ('google-talk', _('Google Talk')),
        (OTHER, _('Other'))
    )

    content_type = models.ForeignKey(ContentType, limit_choices_to={
        'app_label': 'contacts'})
    object_id = models.IntegerField(db_index=True)
    content_object = GenericForeignKey()

    im_account = models.CharField(_('im account'), max_length=100)
    location = models.ForeignKey(Location, limit_choices_to={
        'is_street_address': False, 'is_phone': False})
    service = models.CharField(_('service'), max_length=11,
                               choices=IM_SERVICE_CHOICES, default=OTHER)

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    def __str__(self):
        return "%s (%s)" % (self.im_account, self.location)

    class Meta:
        db_table = 'contacts_instant_messengers'
        verbose_name = _('instant messenger')
        verbose_name_plural = _('instant messengers')


@python_2_unicode_compatible
class WebSite(models.Model):
    content_type = models.ForeignKey(ContentType, limit_choices_to={
        'app_label': 'contacts'})
    object_id = models.IntegerField(db_index=True)
    content_object = GenericForeignKey()

    url = models.URLField(_('URL'))
    location = models.ForeignKey(Location, limit_choices_to={
        'is_street_address': False, 'is_phone': False})

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    def __str__(self):
        return "%s (%s)" % (self.url, self.location)

    class Meta:
        db_table = 'contacts_web_sites'
        verbose_name = _('web site')
        verbose_name_plural = _('web sites')

    def get_absolute_url(self):
        return "%s?web_site=%s" % (self.content_object.get_absolute_url(),
                                    self.pk)


@python_2_unicode_compatible
class StreetAddress(models.Model):
    content_type = models.ForeignKey(ContentType, limit_choices_to={
        'app_label': 'contacts'})
    object_id = models.IntegerField(db_index=True)
    content_object = GenericForeignKey()

    street = models.TextField(_('street'), blank=True)
    city = models.CharField(_('city'), max_length=200, blank=True)
    province = models.CharField(_('province'), max_length=200, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=10, blank=True)
    country = models.CharField(_('country'), max_length=100)
    location = models.ForeignKey(Location, limit_choices_to={
        'is_phone': False})

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    def __str__(self):
        return "%s (%s)" % (self.city, self.location)

    class Meta:
        db_table = 'contacts_street_addresses'
        verbose_name = _('street address')
        verbose_name_plural = _('street addresses')


@python_2_unicode_compatible
class SpecialDate(models.Model):
    content_type = models.ForeignKey(ContentType, limit_choices_to={
        'app_label': 'contacts'})
    object_id = models.IntegerField(db_index=True)
    content_object = GenericForeignKey()

    occasion = models.TextField(_('occasion'), max_length=200)
    date = models.DateField(_('date'))
    every_year = models.BooleanField(_('every year'), default=True)

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    objects = SpecialDateManager()

    def __str__(self):
        return "%s: %s" % (self.occasion, self.date)

    class Meta:
        db_table = 'contacts_special_dates'
        verbose_name = _('special date')
        verbose_name_plural = _('special dates')
