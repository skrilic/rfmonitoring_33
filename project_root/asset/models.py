# -*- coding: utf-8 -*-
from django.urls import reverse
from django.utils import timezone
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

CHECKTYPE = (
    ('Calibration', 'Umjeravanje'),
    ('Registration', 'Tehnički pregled i registracija'),
    ('Renew', 'Obnova licence'),
)

CURRENCY = (
    ('EUR', '€'),
    ('BAM', 'KM'),
    ('USD', '$'),
)


class Office(models.Model):
    name = models.CharField(max_length=128, unique=True)
    address = models.CharField(
        max_length=128, default="NA", null=True, blank=True)
    postal = models.IntegerField(default=0, null=True, blank=True)
    city = models.CharField(max_length=24, default="NA", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = u'office'
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'


class UsedbyPerson(models.Model):
    # personid = models.CharField(max_length = 64, unique = True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    image = models.ImageField(upload_to='persons',
                              verbose_name='Picture',
                              default='persons/anonymous.jpg',
                              blank=True,
                              null=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    phone = models.CharField(max_length=16, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    class Meta:
        db_table = u'usedbyperson'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    # def show_image(self):
    #     if self.image != '':
    #         return '<img project_root="%s" height=70>' % self.image.url
    #     else:
    #         return 'N/A'

    # show_image.allow_tags = True

    def __str__(self):
        return '%s %s <email: %s>' % (self.first_name, self.last_name, self.email)


class Category(models.Model):
    name = models.CharField(max_length=16, unique=True)
    description = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        db_table = u'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return '%s' % self.name


class Procurer(models.Model):
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=128, blank=True, null=True)
    postal = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=24, blank=True, null=True)
    country = models.CharField(max_length=24, blank=True, null=True)

    class Meta:
        db_table = u'procurer'
        verbose_name = 'Procurer'
        verbose_name_plural = 'Procurers'

    def __str__(self):
        return '%s' % self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=64, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    web = models.URLField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = u'manufacturer'
        verbose_name = 'Manufacturer'
        verbose_name_plural = 'Manufacturers'

    def __str__(self):
        return '%s' % self.name


class Event(models.Model):
    type = models.CharField(max_length=20)
    description = models.TextField()

    class Meta:
        db_table = u'event'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return '%s' % self.type


class AssetEvent(models.Model):
    type = models.CharField(max_length=20, unique=True)
    description = models.TextField()

    class Meta:
        db_table = u'assetevent'
        verbose_name = 'Asset - Event type'
        verbose_name_plural = 'Assets - Event types'

    def __str__(self):
        return '%s' % (self.type)


class RFmonSiteEvent(models.Model):
    type = models.CharField(
        max_length=20,
        unique=True
    )
    description = models.TextField(max_length=65536)

    class Meta:
        db_table = u'rfmonsiteevent'
        verbose_name = 'Monitoring station - Event type'
        verbose_name_plural = 'Monitoring station - Event types'

    def __str__(self):
        return '%s' % (self.type)


class System(models.Model):
    dongle = models.CharField(
        max_length=64, verbose_name='Name (Licence/dongle...)')
    description = models.TextField(blank=True, null=True)
    location = models.ForeignKey(
        Office, verbose_name='Location', null=True, blank=True, on_delete=models.CASCADE)
    person = models.ForeignKey(
        UsedbyPerson, verbose_name='User', on_delete=models.CASCADE)
    microloc = models.CharField(
        max_length=64, null=True, blank=True, verbose_name='Room/vehicle')
    # location = models.ForeignKey(Office, verbose_name='Lokacija')
    inuse = models.BooleanField(verbose_name='In use', default=1)
    image = models.ImageField(upload_to='images',
                              verbose_name='Picture',
                              default='images/systemimage.jpg',
                              blank=True,
                              null=True)

    class Meta:
        db_table = u'system'
        verbose_name = 'System'
        verbose_name_plural = 'Systems'

    # def show_image(self):
    #     if self.image != '':
    #         return '<img project_root="%s" height=70>' % self.image.url
    #     else:
    #         return 'N/A'

    # show_image.allow_tags = True

    def __str__(self):
        return '%s: %s' % (self.dongle, self.location)


class Contract(models.Model):
    name = models.CharField(
        max_length=256, verbose_name='Contract name', unique=True)
    contractor = models.ForeignKey(
        Procurer, verbose_name='Contractor', on_delete=models.CASCADE)
    description = models.TextField(
        verbose_name='Description', blank=True, null=True)
    dateofcontract = models.DateField(verbose_name='Date')
    currency = models.CharField(max_length=12, choices=CURRENCY, default='BAM', null=True, blank=True,
                                verbose_name='Currency')
    costofcontract = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True,
                                         verbose_name='Price')
    bookvalue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True,
                                    verbose_name='Book value BAM')

    class Meta:
        db_table = u'contract'
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'

    def __str__(self):
        return '%s' % (self.name)


class Asset(models.Model):
    barcode = models.CharField(
        max_length=24, verbose_name='Bar code', unique=True)
    prodcode = models.CharField(
        max_length=64, null=True, blank=True, verbose_name='Prod. code')
    description = models.CharField(max_length=128, verbose_name='Description')
    manufacturer = models.ForeignKey(
        Manufacturer, verbose_name='Manufacturer', on_delete=models.CASCADE)
    serialno = models.CharField(
        max_length=128, null=True, blank=True, verbose_name='Serial no.')
    license = models.CharField(
        max_length=128, null=True, blank=True, verbose_name='Licence')
    usedby = models.ForeignKey(UsedbyPerson, verbose_name='Assigned to',
                               blank=True, null=True, on_delete=models.CASCADE)
    contract = models.ForeignKey(
        Contract, verbose_name='Contract', blank=True, null=True, on_delete=models.CASCADE)
    partof = models.ForeignKey(
        System, verbose_name='Part of', blank=True, null=True, on_delete=models.CASCADE)
    location = models.ForeignKey(
        Office, null=True, blank=True, verbose_name='Location', on_delete=models.CASCADE)
    annotation = models.CharField(
        max_length=128, null=True, blank=True, verbose_name='Note')
    procurementdate = models.DateField(
        null=True, blank=True, verbose_name='Procurement date')
    depreciationdate = models.DateField(
        null=True, blank=True, verbose_name='Depreciation date')
    currency = models.CharField(max_length=12, choices=CURRENCY, default='BAM', null=True, blank=True,
                                verbose_name='Currency')
    purchaseprice = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True,
                                        verbose_name='Purchase price')
    bookprice = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True,
                                    verbose_name='Book value BAM')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    orderno = models.CharField(
        max_length=30, null=True, blank=True, verbose_name='Order no.')
    procurer = models.ForeignKey(
        Procurer, verbose_name='Procurer', null=True, blank=True, on_delete=models.CASCADE)
    microloc = models.CharField(
        max_length=64, null=True, blank=True, verbose_name='Room/vehicle/place')
    checked = models.BooleanField(default=False, verbose_name='Checked up')
    calibrated = models.BooleanField(default=True, verbose_name='Calibrated')
    proper = models.BooleanField(default=True, verbose_name='Operational')

    class Meta:
        db_table = u'asset'
        verbose_name = 'Asset'
        verbose_name_plural = 'Assets'

    def __str__(self):
        return '%s %s: %s %s; %s' % (self.description, self.prodcode, self.barcode, self.location, self.usedby)


class AssetLog(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    logevent = models.ForeignKey(
        AssetEvent, verbose_name='Event', on_delete=models.CASCADE)
    details = models.TextField(null=True, blank=True)
    datetime = models.DateTimeField(verbose_name='Event start')
    enddatetime = models.DateTimeField(
        null=True, blank=True, verbose_name='Event end')
    expiration = models.DateField(
        null=True, blank=True, verbose_name='Expiration', help_text='Due date')
    document = models.URLField(null=True, blank=True, max_length=200,
                               help_text='https://... (Link on a document on the cloud)')

    class Meta:
        db_table = u'assetlog'
        verbose_name = 'Log - Asset event'
        verbose_name_plural = 'Logs - Asset events'
        unique_together = (('asset', 'logevent', 'datetime'),)


class Periodically(models.Model):
    asset = models.ForeignKey(
        Asset, verbose_name='Equipment', on_delete=models.CASCADE)
    type = models.CharField(max_length=24, choices=CHECKTYPE, default='Calibration', null=True, blank=True,
                            verbose_name='Periodical checkup')
    description = models.TextField(
        verbose_name='Checkup description', null=True, blank=True)
    lastcheck = models.DateField(verbose_name='Last checkup')
    duedate = models.DateField(verbose_name='Next checkup')

    alarm = models.IntegerField(verbose_name='Alarm', blank=True, null=True,
                                help_text='How many days before expiration Warnings should be risen?')

    class Meta:
        db_table = u'periodically'
        verbose_name = 'Checkup'
        verbose_name_plural = 'Checkups'

    def warningdate(self):
        return self.duedate - datetime.timdelta(days=self.alarm)


class RFmonSite(models.Model):
    MONSITE_CHOICES = (
        ('FMS', 'Fixed'),
        ('RMS', 'Remote'),
        ('MMS', 'Mobile'),
        ('TMS', 'Transportable'),
    )
    office = models.OneToOneField(
        Office, verbose_name="Office/Station", on_delete=models.CASCADE)
    description = models.TextField(
        verbose_name="Additional Info/Description", default="No data...", null=True, blank=True)
    type = models.CharField(
        max_length=24,
        choices=MONSITE_CHOICES,
        null=True,
        blank=True,
        verbose_name='Station type'
    )
    document = models.URLField(null=True, blank=True, max_length=200,
                               help_text='https://... (Link on a document on the cloud)')

    def __str__(self):
        return "%s" % self.office.name

    def office_name(self):
        return self.office.name

    class Meta:
        db_table = u'site'
        verbose_name = 'Monitoring station'
        verbose_name_plural = 'Monitoring stations'

    # def warningdate(self):
    #     return (self.duedate - datetime.timdelta(days=self.alarm))


class RFmonSiteLog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rfmonsite = models.ForeignKey(
        RFmonSite, verbose_name='RF monitoring site', on_delete=models.CASCADE)
    logevent = models.ForeignKey(
        RFmonSiteEvent, verbose_name='Event', on_delete=models.CASCADE)
    details = models.TextField(max_length=65536)
    datetime = models.DateTimeField(
        verbose_name='Event start', default=timezone.now)
    enddatetime = models.DateTimeField(
        null=True, blank=True, verbose_name='Event end')
    expiration = models.DateField(
        null=True, blank=True, verbose_name='Expiration', help_text='Due date for the next action.')
    report = models.URLField(null=True, blank=True, max_length=200,
                             help_text='https://... (Link on a document on the cloud)')

    def get_absolute_url(self):
        return reverse('inventories:rfmonsitelog_detail', kwargs={'pk': self.pk})

    class Meta:
        db_table = u'rfmonsitelog'
        verbose_name = 'Log - RF mon. sites event'
        verbose_name_plural = 'Logs - RF mon. sites events'
