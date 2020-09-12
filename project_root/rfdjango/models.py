# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django import forms
from datetime import date
from django.utils.html import format_html
from django.core.validators import RegexValidator

TXBAND = (
    ('FM-s', 'FM Radio broadcasting - stereo'),
    ('FM-m', 'FM Radio broadcasting - mono'),
    ('AM', 'AM Radio broadcasting'),
    ('VHF low', 'VHF low TV Broadcasting'),
    ('VHF high', 'VHF high TV Broadcasting'),
    ('UHF', 'UHF TV Broadcating'),
)

FREQ_UNIT = (
    ('Hz', 'Hz'),
    ('kHz', 'kHz'),
    ('MHz', 'MHz'),
    ('GHz', 'GHz')
)


LAT = (
    ('N', 'N - North'),
    ('S', 'S - South')
)

LONG = (
    ('W', 'W - West'),
    ('E', 'E - East')
)

YES_NO = (
    (False, 'NO'),
    (True, 'YES'),
)


MEAS_TYPE = (
    ('Drive', 'During drive'),
    ('Stationary', 'From fixed position'),
)


BWMET = (
    ('xdb', 'Method x-dB'),
    ('beta', 'Method beta %'),
    ('none', 'Not applicable'),
)

AREAS = (
    ('Rural', 'Rural'),
    ('Urban', 'Urban'),
    ('Large Cities', 'Large Cities'),
)

POL = (
    ('V', 'Vertical'),
    ('H', 'Horizontal'),
    ('S', 'Slant'),
)


EMISSIONS = (
    ('BC', 'Broadcast FM radio'),
    ('BT', 'Broadcast analog TV'),
    ('AT', 'Amateur radio')
)


# Monitoring stations
class monitorstanice(models.Model):
    naziv = models.CharField(max_length=64, unique=True)
    aktivna = models.BooleanField(choices=YES_NO, default=1,
                                  verbose_name="Operational state", help_text="Monitoring station is operational?")
    area = models.CharField(choices=AREAS, max_length=32,
                            default='Rural', help_text="ITU-R BS.412-... clasification")
    portalvisibility = models.BooleanField(choices=YES_NO, default=0,
                                           verbose_name="Portal visibility",
                                           help_text="Measurement results from this st. will be visibile on the portal?")
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    ip_address = models.GenericIPAddressField(
        null=True, blank=True, verbose_name="IP address")
    additional_info = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Monitoring station'

    def aktivnost(self, var):
        if var:
            return "Operational"
        return "Out of order"

    def __str__(self):
        # return '%s GPS: %s; %s' % (self.naziv, self.gps, self.aktivnost(self.aktivna))
        return '%s; long. %s  lat. %s [IP/FQDN: %s]' % (self.naziv, self.longitude, self.latitude, self.ip_address)


class Area(models.Model):
    name = models.CharField(max_length=64, verbose_name="Area name")
    zipcode = models.IntegerField(
        unique=True, verbose_name="Zipcode for the area")

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return "%s %s" % (self.name, self.zipcode)


# Sites
class kote(models.Model):
    naziv = models.CharField(max_length=64, verbose_name="Name")
    area = models.ForeignKey(
        Area, verbose_name="Area name", on_delete=models.PROTECT)
    extrainfo = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Site'
        # verbose_name_plural = 'Sites'
        ordering = ('naziv',)
        unique_together = (('naziv', 'area'),)

    def __str__(self):
        return '%s: %s %s' % (self.naziv, self.area.name, self.extrainfo)


# Towers
class Towers(models.Model):
    oznaka = models.CharField(max_length=24, verbose_name="Name")
    towerid = models.SlugField(max_length=24, verbose_name="ID", unique=True)
    visina = models.FloatField(default=10.00, verbose_name="Height m")
    # position = GeopositionField(help_text="Helper for visualization and correction")
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    kota = models.ForeignKey(kote, verbose_name="Site",
                             on_delete=models.PROTECT)
    extrainfo = models.TextField(
        default='Comment...', blank=True, verbose_name='Description')

    class Meta:
        verbose_name = 'Tower'
        ordering = ('kota', 'latitude', 'longitude',)

    def __str__(self):
        return '%s %sm : (lat,lon) = %s, %s' % (self.oznaka, self.visina, self.latitude, self.longitude)

    def save(self, *args, **kwargs):
        twrid = self.oznaka
        # self.towerid = "%s" % twrid.replace(" ","_")
        # self.position = "%s,%s" % (self.latitude,self.longitude)
        super(Towers, self).save(*args, **kwargs)


class CountryCode(models.Model):
    name = models.CharField(max_length=128, unique=True)
    numcode = models.IntegerField()
    twoletters = models.CharField(max_length=2, unique=True)
    threeletters = models.CharField(max_length=3)

    def __str__(self):
        return '%s (%s)' % (self.threeletters, self.name)

    # Maps definition


class MapDefinition(models.Model):
    name = models.CharField(max_length=32, unique=True,
                            help_text='Name of the page where the map resists (without extension .htm*)')
    description = models.CharField(max_length=256, blank=True, null=True)
    # script = models.TextField(blank=True, null=True)
    map_lat = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Lattitude of the central map point',
                                  blank=True, null=True)
    map_lon = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Longitude of the central map point',
                                  blank=True, null=True)
    map_zoom = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Map Definition'
        ordering = ('name',)


class Organization(models.Model):
    name = models.CharField(max_length=256, unique=True)
    index = models.CharField(max_length=4, unique=True)
    person = models.CharField(default='N.N.', max_length=64)
    phone = models.CharField(default='111-222', max_length=16)
    fax = models.CharField(default='111-222', max_length=16)
    email = models.EmailField(default='unknown@email.com')
    street = models.CharField(default='---', max_length=128)
    # zipcode = models.IntegerField(max_length=6, default=00000)
    # city = models.CharField(max_length=128)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    countryCode = models.ForeignKey(CountryCode, on_delete=models.PROTECT)
    rds_pi = models.IntegerField(
        blank=True, null=True, help_text="For FM Radio only")
    rds_pihex = models.CharField(
        max_length=4, blank=True, null=True, help_text="For FM Radio only")

    def zipcode(self):
        return "%s" % self.area.zipcode

    def city(self):
        return "%s" % self.area.name

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
        ordering = ('name', 'area', 'countryCode')

    def __str__(self):
        return self.name


class TechnicalContact(models.Model):
    name = models.CharField(
        max_length=200, help_text='Company or person(s) to contact')
    phone = models.CharField(default='111-222', max_length=16)
    fax = models.CharField(default='111-222', max_length=16)
    email = models.EmailField(default='unknown@email.com')
    additional_info = models.TextField(blank=True, null=True,
                                       help_text="Additional data i.e. contacts, phones, persons, notes, remarks etc.")

    def __str__(self):
        return "%s %s" % (self.name, self.phone)


class LicenceType(models.Model):
    type = models.CharField(max_length=200)
    licence_class = models.CharField(max_length=100, choices=EMISSIONS)
    description = models.TextField(default="License")

    def __str__(self):
        return "%s" % self.type


class Licensee(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    licence_type = models.ForeignKey(
        LicenceType, default=0, on_delete=models.PROTECT)
    licence_issued = models.DateField(blank=True, null=True)
    licence_valid_to = models.DateField(blank=True, null=True)
    technician = models.ForeignKey(TechnicalContact, on_delete=models.PROTECT)
    stream = models.URLField(blank=True, null=True,
                             max_length=200, help_text="Live stream URL")
    web_site = models.URLField(
        blank=True, null=True, max_length=200, help_text="Web page URL")
    additional_info = models.TextField(blank=True, null=True,
                                       help_text="Additional data i.e. contacts, phones, persons, notes and remarks "
                                                 "etc.")

    def stream_url(self):
        return format_html(f'<a href={self.stream}>Live</a>') if self.stream else 'No'

    def licensee_url(self):
        return format_html(f'<a href={self.web_site}>WEB</a>') if self.web_site else 'No'

    def name(self):
        return "%s" % self.organization.name

    def city(self):
        return "%s" % self.organization.area.name

    def address(self):
        return "%s %s" % (
            self.organization.area.zipcode,
            self.organization.street
        )

    def contact(self):
        return "%s %s %s" % (
            self.organization.person,
            self.organization.phone,
            self.organization.email
        )

    def country(self):
        return "%s" % self.organization.countryCode.twoletters

    def technical_contact(self):
        return "(%s %s %s %s)" % (
            self.technician.name,
            self.technician.phone,
            self.technician.fax,
            self.technician.additional_info
        )

    class Meta:
        verbose_name = 'Licensee'
        verbose_name_plural = 'Licensees'
        ordering = ('organization__name', 'organization__area__name')
        unique_together = ('organization', 'licence_type')

    def __str__(self):
        return self.organization.name


class portalUser(models.Model):
    username = models.ForeignKey(User, on_delete=models.PROTECT)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    description = models.TextField(verbose_name="Description", help_text="Additional info about portla user, if any.",
                                   blank=True)

    def e_mail(self):
        return '%s' % self.username.email

    class Meta:
        verbose_name = 'Portal user'
        # verbose_name_plural = 'Korisnici portala'
        permissions = (
            # Opis dozvola i njihovi nazivi
            ("can_view_results", "View measurement results"),
            # ("view_measurement_results",   "View measurement results"),
        )

    def __str__(self):
        return '%s, %s, %s' % (self.username, self.organization, self.description)


class LicenceState(models.Model):
    short_code = models.CharField(max_length=2, unique=True)
    description = models.CharField(max_length=64)

    def __str__(self):
        return '%s (%s)' % (self.short_code, self.description)


class Antenna(models.Model):
    name = models.CharField(max_length=128,
                            help_text="Antenna model, type ...",
                            unique=False)
    ERP_00 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='0°')
    ERP_10 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='10°')
    ERP_20 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='20°')
    ERP_30 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='30°')
    ERP_40 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='40°')
    ERP_50 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='50°')
    ERP_60 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='60°')
    ERP_70 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='70°')
    ERP_80 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='80°')
    ERP_90 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='90°')
    ERP_100 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='100°')
    ERP_110 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='110°')
    ERP_120 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='120°')
    ERP_130 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='130°')
    ERP_140 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='140°')
    ERP_150 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='150°')
    ERP_160 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='160°')
    ERP_170 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='170°')
    ERP_180 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='180°')
    ERP_190 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='190°')
    ERP_200 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='200°')
    ERP_210 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='210°')
    ERP_220 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='220°')
    ERP_230 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='230°')
    ERP_240 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='240°')
    ERP_250 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='250°')
    ERP_260 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='260°')
    ERP_270 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='270°')
    ERP_280 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='280°')
    ERP_290 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='290°')
    ERP_300 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='300°')
    ERP_310 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='310°')
    ERP_320 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='320°')
    ERP_330 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='330°')
    ERP_340 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='340°')
    ERP_350 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name='350°')
    vertical_pattern = models.TextField(help_text='Comma separated pair of values in form DEG:DB', blank=True,
                                        null=True)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ['name', ]


# Field Measurement - Stationary or during drive
class FieldMeasurement(models.Model):
    author = models.ForeignKey(
        User,
        default=1000000,
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=256,
        verbose_name='Measurement Title'
    )
    date = models.DateField(
        default=date.today
    )
    location = models.CharField(
        max_length=512,
        help_text='Measurements location or area'
    )
    equipment = models.CharField(
        max_length=256,
        verbose_name='Measurement Equipment'
    )
    antenna = models.CharField(
        max_length=256,
        verbose_name='Measurement antenna'
    )
    operator = models.CharField(
        max_length=512,
        help_text='Measurement Operator(s)',
        default='---'
    )
    type = models.CharField(
        max_length=128,
        choices=MEAS_TYPE, default='Stationary',
        verbose_name='Type of measurement',
        help_text='Select the type of measurement?',
        blank='False'
    )
    description = models.TextField(
        verbose_name='Meas description'
    )
    status = models.CharField(max_length=100, choices=(
        # ('ACCEPTED', 'Accepted'),
        ('ONHOLD', 'On hold'),
        ('OPENED', 'Opened'),
        ('INPROGRESS', 'In progress'),
        # ('FINISHED', 'Finished'),
        # ('APPROVED', 'Approved'),
        ('DONE', 'Done')
    ), default="ONHOLD"
    )
    scope = models.CharField(max_length=64, choices=(
        ('PRIVATE', 'Private'),
        ('PUBLIC', 'Public'),
        ('STAFF', 'Staff only')
    ), default="STAFF"
    )
    report = models.URLField(null=True, blank=True, max_length=200,
                             help_text='https://... (Link to the document on the cloud)')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Measurement'
        verbose_name_plural = 'Measurements'


# Transmitters
class Transmitter(models.Model):
    name = models.CharField(
        max_length=64,
        help_text="Please provide Transmitter name",
        verbose_name="Transmitter name"
    )
    licence_type = models.CharField(max_length=100, choices=EMISSIONS)
    callsign = models.CharField(
        max_length=12,
        blank=True,
        null=True
    )
    signature = models.CharField(
        max_length=24,
        blank=True,
        null=True
    )
    description = models.CharField(
        max_length=64,
        verbose_name="Description",
        blank=True,
        null=True
    )
    enabled = models.BooleanField(
        choices=YES_NO, default=True,
        verbose_name="Operational?",
        help_text="Is Transmitter in operation?",
        blank="False"
    )
    licence_state = models.BooleanField(
        choices=YES_NO, default=True,
        verbose_name="Licence Validity",
        help_text="Does Transmitter have valid licence?",
        blank="False"
    )
    frequency = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Tx Freq. MHz"
    )
    frequency_rx = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        blank=True,
        null=True,
        help_text="Only relevant for services like PMR or Radio Ameteurs",
        verbose_name="Rx Freq. MHz"
    )
    erp = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        help_text="ERP power of the transmitter in Watts",
        verbose_name="ERP",
        blank=True,
        null=True
    )
    transmitter_power = models.DecimalField(
        max_digits=11, decimal_places=2,
        help_text="Output power of the transmitter in Watts",
        verbose_name="Output power",
        blank=True,
        null=True
    )
    antenna_height = models.DecimalField(
        max_digits=4, decimal_places=2,
        verbose_name="Antenna height",
        help_text="Antenna height from the ground.",
        blank=True,
        null=True
    )
    tower = models.ForeignKey(
        Towers,
        verbose_name="Tower",
        on_delete=models.PROTECT
    )
    organization = models.ForeignKey(
        Organization,
        verbose_name="Organization",
        on_delete=models.PROTECT
    )
    license_issuing_date = models.DateField(
        blank=True,
        null=True
    )
    license_expiration_date = models.DateField(
        blank=True,
        null=True
    )
    antenna = models.ForeignKey(
        Antenna,
        on_delete=models.PROTECT
    )
    antenna_direction = models.CharField(
        max_length=64,
        default='30/60/90',
        help_text='Direction(s) in °'
    )
    antenna_tilt = models.DecimalField(
        max_digits=5, decimal_places=2, help_text='Tilt in °')

    def __str__(self):
        # return '%s; %sMHz; %s' % (self.name, self.frequency, self.tower)
        return '%s' % self.name

    class Meta:
        ordering = ['organization__name',
                    'tower__kota__naziv', 'name', 'frequency']


# # Measurement Results
# class rezmjerenja(models.Model):
#     odasiljac = models.ForeignKey(Transmitter, editable=False, on_delete=models.PROTECT)
#     datum = models.DateField(editable=False)
#     vrijeme = models.TimeField(editable=False)
#     razina = models.DecimalField(max_digits=7, decimal_places=3, verbose_name="field strength dB(uV/m)", editable=False)
#     offset = models.DecimalField(max_digits=7, decimal_places=3, editable=False, verbose_name="offset kHz")
#     bw = models.DecimalField(max_digits=7, decimal_places=3, verbose_name="bandwidth kHz", editable=False)
#     modul = models.DecimalField(max_digits=7, decimal_places=3, verbose_name="deviation kHz", help_text="Deviation",
#                                 editable=False)
#     monitorst = models.ForeignKey(monitorstanice, editable=False, on_delete=models.PROTECT)
#     mjernaoprema = models.CharField(max_length=256, editable=False)
#     reliability = models.BooleanField(choices=YES_NO, default=0, verbose_name="Meas. OK?")
#     los = models.BooleanField(choices=YES_NO, default=0, verbose_name="LOS")
#
#     class Meta:
#         verbose_name = 'Meas. result'
#
#     class Admin:
#         pass
#
#
#     def plot_link(self):
#         return "?transmitter=%s&monitorst=%s" % (self.odasiljac.name, self.monitorst.naziv)
#
#     def diagnosis(self):
#         if (float(self.razina) > 54.0 and self.reliability and float(self.offset) < 2.2):
#             if float(self.modul) > 75.0:
#                 exceed = (float(self.modul) / 75.0 - 1.0) * 100.0
#                 return 'Modulation exceeded: ' + '{0:.0f}%'.format(exceed)
#             else:
#                 return 'OK'
#         elif (float(self.razina) < 54.0 and self.reliability and float(self.offset) > 2.2):
#             return "Transmitting probably stopped"
#         else:
#             return ''
#
#     def __str__(self):
#         return '%i, %s, %s %s %s %s %s' % \
#                (self.id, self.odasiljac, self.datum, self.vrijeme, self.razina, self.offset, self.bw)
#

# # RDS decoding results
# class rdsmjerenja(models.Model):
#     transmitter = models.ForeignKey(Transmitter, editable=False, on_delete=models.PROTECT)
#     monitst = models.ForeignKey(monitorstanice, editable=False, on_delete=models.PROTECT)
#     datum = models.DateField(editable=False)
#     vrijeme = models.TimeField(editable=False)
#     rds_pi = models.CharField(max_length=10, editable=False)
#     rds_tp = models.CharField(max_length=10, editable=False)
#     rds_ta = models.CharField(max_length=10, editable=False)
#     rds_info = models.CharField(max_length=128, editable=False)
#     rds_progname = models.CharField(max_length=64, editable=False)
#     rds_text = models.CharField(max_length=128, editable=False)
#
#     class Meta:
#         verbose_name = 'RDS checkout'
#         # verbose_name_plural = 'RDS'
#
#     class Admin:
#         pass
#         # list_display = ('odasiljac','monitst','rds_pi','rds_tp','rds_ta',\
#         # 'datum','vrijeme','rds_progname','rds_text','rds_info')
#         # list_filter = ['odasiljac','monitst', 'rds_pi', 'rds_progname','datum','vrijeme']
#         # search_fields = ('rds_pi', 'odasiljac','rds_progname','datum','vrijeme')
#
#     def wrongPiHex(self):
#         if self.rds_pi != '':
#             if self.rds_pi != self.transmitter.organization.rds_pihex:
#                 return 'Wrong PI'
#             else:
#                 return 'OK'
#         return ''
#
#     def __str__(self):
#         return '%s, %s %s %s' % \
#                (self.transmitter, self.monitst, self.rds_progname, self.rds_pi)
#
#     # "progname":rds_progname,"info":rds_info,"text":rds_text,"pi":rds_pi,"tp":rds_tp,"ta":rds_ta,"datum":datum,"vrijeme":vrijeme
#
#
# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField()
#
#
# class PasswordForm(forms.Form):
#     new_password = forms.CharField()
#     new_password1 = forms.CharField()
