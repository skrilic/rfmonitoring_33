from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator

from .constants import (
    SPACING,
    BITRATE_NETWORK,
    CATEGORY_NETWORK,
    COMPANIES,
    TECHNOLOGY
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    organization = models.CharField(
        choices=COMPANIES, max_length=64, default="NA")

    def __str__(self):
        return f"{self.user} :: {self.organization}"

    class Meta:
        verbose_name = "User profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# Maps definition
class MapDefinition(models.Model):
    name = models.CharField(max_length=32, unique=True,
                            help_text='Name of the page where the map resists (without extension .htm*)')
    description = models.CharField(max_length=256, blank=True, null=True)
    map_lat = models.DecimalField(max_digits=5, decimal_places=2,
                                  verbose_name='Latitude of the central point of the map', blank=True, null=True)
    map_lon = models.DecimalField(max_digits=5, decimal_places=2,
                                  verbose_name='Longitude of the central point of the map', blank=True, null=True)
    map_zoom = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Map Definition'
        ordering = ('name',)


class Basestations(models.Model):
    call_sign = models.CharField(db_column='CALL_SIGN', max_length=255,
                                 help_text='CID identification number of a Tx (BTS) or the BTS sector in the LAC')
    address = models.CharField(db_column='ADDRESS', db_index=True, max_length=255,
                               help_text="Operator's identification of the cell")
    netid = models.IntegerField(db_column='NETID', default=0, help_text='MNC')
    type_coord = models.CharField(db_column='TYPE_COORD', max_length=5, default='4DMS',
                                  help_text='i.e. DMS, 4DMS, WGS84')
    coord_x = models.CharField(
        db_column='COORD_X', max_length=11, default=0, help_text='Longitude (4DMS)')
    lon_deg = models.IntegerField(validators=[MinValueValidator(-179), MaxValueValidator(179)], blank=True, null=True,
                                  help_text="° degrees")
    lon_min = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(59)], blank=True, null=True,
                                  help_text="' minutes")
    lon_sec = models.DecimalField(max_digits=4, decimal_places=2,
                                  validators=[MinValueValidator(00.00), MaxValueValidator(59.99)], blank=True,
                                  null=True, help_text="'' seconds")

    coord_y = models.CharField(
        db_column='COORD_Y', max_length=10, default=0, help_text='Latitude (4DMS)')
    lat_deg = models.IntegerField(validators=[MinValueValidator(-179), MaxValueValidator(179)], blank=True, null=True,
                                  help_text="° degrees")
    lat_min = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(59)], blank=True, null=True,
                                  help_text="' minutes")
    lat_sec = models.DecimalField(max_digits=4, decimal_places=2,
                                  validators=[MinValueValidator(00.00), MaxValueValidator(59.99)], blank=True,
                                  null=True, help_text="'' seconds")

    # altitude = models.DecimalField(db_column='ALTITUDE', max_digits=6, decimal_places=2, blank=True, null=True, help_text="Altitude of the site from the sea level (m)")
    nominal_power = models.DecimalField(db_column='NOMINAL_POWER', max_digits=7, decimal_places=2, default=0,
                                        help_text='Transmitter output power in Watts')
    gain = models.DecimalField(db_column='GAIN', max_digits=8, decimal_places=2, default=0,
                               help_text="Tx antenna's gain in dB")
    # gainrx = models.DecimalField(db_column='GAINRX', max_digits=8, decimal_places=2, blank=True, null=True)
    # losses = models.DecimalField(db_column='LOSSES', max_digits=8, decimal_places=2, blank=True, null=True)
    # lossesrx = models.DecimalField(db_column='LOSSESRX', max_digits=8, decimal_places=2, blank=True, null=True)
    # frequency = models.DecimalField(db_column='FREQUENCY', max_digits=8, decimal_places=3, blank=True, null=True)
    h_antenna = models.DecimalField(db_column='H_ANTENNA', max_digits=6, decimal_places=2, default=10,
                                    help_text='Antenna height from the ground in meters')
    # polar = models.CharField(db_column='POLAR', max_length=255, blank=True, null=True)
    # polarrx = models.CharField(db_column='POLARRX', max_length=255, blank=True, null=True)
    threshold = models.DecimalField(db_column='THRESHOLD', max_digits=5, decimal_places=2, default=0,
                                    help_text='Target receive level in dBuV/m')
    # thresholdrx = models.CharField(db_column='THRESHOLDRX', max_length=255, blank=True, null=True)
    bandwidth = models.IntegerField(
        db_column='BANDWIDTH', default=0, help_text='Bandwidth in kHz')
    bandwidthrx = models.IntegerField(
        db_column='BANDWIDTHRX', default=0, help_text='Bandwidth in kHz')
    # channel = models.CharField(db_column='CHANNEL', max_length=255, blank=True, null=True)
    # nb_lines = models.CharField(db_column='NB_LINES', max_length=255, blank=True, null=True)
    # title = models.CharField(db_column='TITLE', max_length=255, blank=True, null=True)
    # info1 = models.TextField(db_column='INFO1', max_length=255, blank=True, null=True)
    # info2 = models.TextField(db_column='INFO2', max_length=255, blank=True, null=True)
    azimuth = models.IntegerField(
        db_column='AZIMUTH', default=0, help_text='Antenna azimuth in degrees')
    tilt = models.IntegerField(
        db_column='TILT', default=0, help_text='Mechanical antenna tilt in degrees')
    tilte = models.IntegerField(
        db_column='TILTE', default=0, help_text='Electrical antenna tilt in degrees')
    # type_element = models.CharField(db_column='TYPE_ELEMENT', max_length=255, blank=True, null=True)
    # info3 = models.CharField(db_column='INFO3', max_length=255, blank=True, null=True)
    # type_station = models.CharField(db_column='TYPE_STATION', max_length=255, blank=True, null=True)
    # type_link = models.CharField(db_column='TYPE_LINK', max_length=255, blank=True, null=True)
    # group = models.CharField(db_column='GROUP', max_length=255, blank=True, null=True)
    antenna_nameh = models.CharField(db_column='Antenna_nameH', max_length=255, blank=True, null=True,
                                     default='generic')
    antenna_namev = models.IntegerField(
        db_column='Antenna_nameV', blank=True, null=True, default=0)
    diagh_0 = models.IntegerField(db_column='DIAGH_0', blank=True, null=True, default=0,
                                  help_text='Antenna correction in dB for the correspondig direction')
    diagh_5 = models.IntegerField(db_column='DIAGH_5', blank=True, null=True, default=0,
                                  help_text='Antenna correction in dB for the correspondig direction')
    diagh_15 = models.IntegerField(db_column='DIAGH_15', blank=True, null=True, default=0,
                                   help_text='Antenna correction in dB for the correspondig direction')
    diagh_10 = models.IntegerField(db_column='DIAGH_10', blank=True, null=True, default=0,
                                   help_text='Antenna correction in dB for the correspondig direction')
    diagh_20 = models.IntegerField(db_column='DIAGH_20', blank=True, null=True, default=0,
                                   help_text='Antenna correction in dB for the correspondig direction')
    diagh_25 = models.IntegerField(db_column='DIAGH_25', blank=True, null=True, default=0,
                                   help_text='Antenna correction in dB for the correspondig direction')
    diagh_30 = models.IntegerField(db_column='DIAGH_30', blank=True, null=True, default=0,
                                   help_text='Antenna correction in dB for the correspondig direction')
    diagh_35 = models.IntegerField(db_column='DIAGH_35', blank=True, null=True, default=0,
                                   help_text='Antenna correction in dB for the correspondig direction')
    diagh_40 = models.IntegerField(db_column='DIAGH_40', blank=True, null=True, default=0,
                                   help_text='Antenna correction in dB for the correspondig direction')
    diagh_45 = models.IntegerField(db_column='DIAGH_45', blank=True, null=True, default=0,
                                   help_text='Antenna correction in dB for the correspondig direction')
    diagh_50 = models.IntegerField(db_column='DIAGH_50', blank=True, null=True, default=0,
                                   help_text='Antenna correction in dB for the correspondig direction')
    diagh_55 = models.IntegerField(db_column='DIAGH_55', blank=True, null=True, default=0,
                                   help_text='Antenna correction in dB for the correspondig direction')
    diagh_60 = models.IntegerField(db_column='DIAGH_60', blank=True, null=True, default=0,
                                   help_text='Antenna correction in dB for the correspondig direction')
    diagh_65 = models.IntegerField(db_column='DIAGH_65', blank=True, null=True, default=0,
                                   help_text='Antenna correction in dB for the correspondig direction')
    diagh_70 = models.IntegerField(db_column='DIAGH_70', blank=True, null=True, default=0,
                                   help_text='Antenna correction in dB for the correspondig direction')
    diagh_75 = models.IntegerField(db_column='DIAGH_75', blank=True, null=True, default=0,
                                   help_text='Antenna correction in dB for the correspondig direction')
    diagh_80 = models.IntegerField(db_column='DIAGH_80', blank=True, null=True, default=0,
                                   help_text='Antenna correction in dB for the correspondig direction')
    diagh_85 = models.IntegerField(db_column='DIAGH_85', blank=True, null=True, default=0,
                                   help_text='Antenna correction in dB for the correspondig direction')
    diagh_90 = models.IntegerField(db_column='DIAGH_90', blank=True, null=True, default=0,
                                   help_text='Antenna correction in dB for the correspondig direction')
    diagh_95 = models.IntegerField(db_column='DIAGH_95', blank=True, null=True, default=0,
                                   help_text='Antenna correction in dB for the correspondig direction')
    diagh_100 = models.IntegerField(db_column='DIAGH_100', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_105 = models.IntegerField(db_column='DIAGH_105', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_110 = models.IntegerField(db_column='DIAGH_110', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_115 = models.IntegerField(db_column='DIAGH_115', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_120 = models.IntegerField(db_column='DIAGH_120', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_125 = models.IntegerField(db_column='DIAGH_125', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_130 = models.IntegerField(db_column='DIAGH_130', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_135 = models.IntegerField(db_column='DIAGH_135', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_140 = models.IntegerField(db_column='DIAGH_140', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_145 = models.IntegerField(db_column='DIAGH_145', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_150 = models.IntegerField(db_column='DIAGH_150', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_155 = models.IntegerField(db_column='DIAGH_155', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_160 = models.IntegerField(db_column='DIAGH_160', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_165 = models.IntegerField(db_column='DIAGH_165', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_170 = models.IntegerField(db_column='DIAGH_170', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_175 = models.IntegerField(db_column='DIAGH_175', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_180 = models.IntegerField(db_column='DIAGH_180', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_185 = models.IntegerField(db_column='DIAGH_185', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_190 = models.IntegerField(db_column='DIAGH_190', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_195 = models.IntegerField(db_column='DIAGH_195', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_200 = models.IntegerField(db_column='DIAGH_200', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_205 = models.IntegerField(db_column='DIAGH_205', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_210 = models.IntegerField(db_column='DIAGH_210', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_215 = models.IntegerField(db_column='DIAGH_215', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_220 = models.IntegerField(db_column='DIAGH_220', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_225 = models.IntegerField(db_column='DIAGH_225', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_230 = models.IntegerField(db_column='DIAGH_230', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_235 = models.IntegerField(db_column='DIAGH_235', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_240 = models.IntegerField(db_column='DIAGH_240', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_245 = models.IntegerField(db_column='DIAGH_245', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_250 = models.IntegerField(db_column='DIAGH_250', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_255 = models.IntegerField(db_column='DIAGH_255', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_260 = models.IntegerField(db_column='DIAGH_260', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_265 = models.IntegerField(db_column='DIAGH_265', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_270 = models.IntegerField(db_column='DIAGH_270', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_275 = models.IntegerField(db_column='DIAGH_275', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_280 = models.IntegerField(db_column='DIAGH_280', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_285 = models.IntegerField(db_column='DIAGH_285', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_290 = models.IntegerField(db_column='DIAGH_290', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_295 = models.IntegerField(db_column='DIAGH_295', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_300 = models.IntegerField(db_column='DIAGH_300', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_305 = models.IntegerField(db_column='DIAGH_305', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_310 = models.IntegerField(db_column='DIAGH_310', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_315 = models.IntegerField(db_column='DIAGH_315', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_320 = models.IntegerField(db_column='DIAGH_320', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_325 = models.IntegerField(db_column='DIAGH_325', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_330 = models.IntegerField(db_column='DIAGH_330', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_335 = models.IntegerField(db_column='DIAGH_335', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_340 = models.IntegerField(db_column='DIAGH_340', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_345 = models.IntegerField(db_column='DIAGH_345', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_350 = models.IntegerField(db_column='DIAGH_350', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    diagh_355 = models.IntegerField(db_column='DIAGH_355', blank=True, null=True, default=0,
                                    help_text='Antenna correction in dB for the correspondig direction')
    # project_owner = models.CharField(db_colu'mn='PROJECT_OWNER', max_length=255, blank=True, null=True)
    # project_name = models.CharField(db_column='PROJECT_NAME', max_digits=5, decimal_places=2, blank=True, null=True)
    # time_stamp = models.CharField(db_column='TIME_STAMP', max_length=255, blank=True, null=True)
    # status = models.CharField(db_column='STATUS', max_length=255, blank=True, null=True)
    # service = models.CharField(db_column='SERVICE', max_length=255, blank=True, null=True)
    # codesitea = models.CharField(db_column='CodeSiteA', max_length=255, blank=True, null=True)
    downlink_cx = models.IntegerField(db_column='Downlink_cx', validators=[MinValueValidator(0), MaxValueValidator(16)],
                                      default=0, help_text='Number of ARFCNs per sector')
    d_cx1 = models.DecimalField(db_column='D_cx1', max_digits=8, decimal_places=3, blank=True, null=True, default=0.000,
                                help_text="MHz")
    d_cx2 = models.DecimalField(db_column='D_cx2', max_digits=8, decimal_places=3, blank=True, null=True, default=0.000,
                                help_text="MHz")
    d_cx3 = models.DecimalField(db_column='D_cx3', max_digits=8, decimal_places=3, blank=True, null=True, default=0.000,
                                help_text="MHz")
    d_cx4 = models.DecimalField(db_column='D_cx4', max_digits=8, decimal_places=3, blank=True, null=True, default=0.000,
                                help_text="MHz")
    d_cx5 = models.DecimalField(db_column='D_cx5', max_digits=8, decimal_places=3, blank=True, null=True, default=0.000,
                                help_text="MHz")
    d_cx6 = models.DecimalField(db_column='D_cx6', max_digits=8, decimal_places=3, blank=True, null=True, default=0.000,
                                help_text="MHz")
    d_cx7 = models.DecimalField(db_column='D_cx7', max_digits=8, decimal_places=3, blank=True, null=True, default=0.000,
                                help_text="MHz")
    d_cx8 = models.DecimalField(db_column='D_cx8', max_digits=8, decimal_places=3, blank=True, null=True, default=0.000,
                                help_text="MHz")
    d_cx9 = models.DecimalField(db_column='D_cx9', max_digits=8, decimal_places=3, blank=True, null=True, default=0.000,
                                help_text="MHz")
    d_cx10 = models.DecimalField(db_column='D_cx10', max_digits=8, decimal_places=3, blank=True, null=True,
                                 default=0.000, help_text="MHz")
    d_cx11 = models.DecimalField(db_column='D_cx11', max_digits=8, decimal_places=3, blank=True, null=True,
                                 default=0.000, help_text="MHz")
    d_cx12 = models.DecimalField(db_column='D_cx12', max_digits=8, decimal_places=3, blank=True, null=True,
                                 default=0.000, help_text="MHz")
    d_cx13 = models.DecimalField(db_column='D_cx13', max_digits=8, decimal_places=3, blank=True, null=True,
                                 default=0.000, help_text="MHz")
    d_cx14 = models.DecimalField(db_column='D_cx14', max_digits=8, decimal_places=3, blank=True, null=True,
                                 default=0.000, help_text="MHz")
    d_cx15 = models.DecimalField(db_column='D_cx15', max_digits=8, decimal_places=3, blank=True, null=True,
                                 default=0.000, help_text="MHz")
    d_cx16 = models.DecimalField(db_column='D_cx16', max_digits=8, decimal_places=3, blank=True, null=True,
                                 default=0.000, help_text="MHz")
    uplink_cx = models.IntegerField(db_column='Uplink_cx', validators=[MinValueValidator(0), MaxValueValidator(16)],
                                    default=0, help_text='Number of ARFCNs per sector')
    u_cx1 = models.DecimalField(db_column='U_cx1', max_digits=8, decimal_places=3, blank=True, null=True, default=0.000,
                                help_text="MHz")
    u_cx2 = models.DecimalField(db_column='U_cx2', max_digits=8, decimal_places=3, blank=True, null=True, default=0.000,
                                help_text="MHz")
    u_cx3 = models.DecimalField(db_column='U_cx3', max_digits=8, decimal_places=3, blank=True, null=True, default=0.000,
                                help_text="MHz")
    u_cx4 = models.DecimalField(db_column='U_cx4', max_digits=8, decimal_places=3, blank=True, null=True, default=0.000,
                                help_text="MHz")
    u_cx5 = models.DecimalField(db_column='U_cx5', max_digits=8, decimal_places=3, blank=True, null=True, default=0.000,
                                help_text="MHz")
    u_cx6 = models.DecimalField(db_column='U_cx6', max_digits=8, decimal_places=3, blank=True, null=True, default=0.000,
                                help_text="MHz")
    u_cx7 = models.DecimalField(db_column='U_cx7', max_digits=8, decimal_places=3, blank=True, null=True, default=0.000,
                                help_text="MHz")
    u_cx8 = models.DecimalField(db_column='U_cx8', max_digits=8, decimal_places=3, blank=True, null=True, default=0.000,
                                help_text="MHz")
    u_cx9 = models.DecimalField(db_column='U_cx9', max_digits=8, decimal_places=3, blank=True, null=True, default=0.000,
                                help_text="MHz")
    u_cx10 = models.DecimalField(db_column='U_cx10', max_digits=8, decimal_places=3, blank=True, null=True,
                                 default=0.000, help_text="MHz")
    u_cx11 = models.DecimalField(db_column='U_cx11', max_digits=8, decimal_places=3, blank=True, null=True,
                                 default=0.000, help_text="MHz")
    u_cx12 = models.DecimalField(db_column='U_cx12', max_digits=8, decimal_places=3, blank=True, null=True,
                                 default=0.000, help_text="MHz")
    u_cx13 = models.DecimalField(db_column='U_cx13', max_digits=8, decimal_places=3, blank=True, null=True,
                                 default=0.000, help_text="MHz")
    u_cx14 = models.DecimalField(db_column='U_cx14', max_digits=8, decimal_places=3, blank=True, null=True,
                                 default=0.000, help_text="MHz")
    u_cx15 = models.DecimalField(db_column='U_cx15', max_digits=8, decimal_places=3, blank=True, null=True,
                                 default=0.000, help_text="MHz")
    u_cx16 = models.DecimalField(db_column='U_cx16', max_digits=8, decimal_places=3, blank=True, null=True,
                                 default=0.000, help_text="MHz")
    spacing = models.IntegerField(
        db_column='Spacing', choices=SPACING, default=45, help_text='45, 95 or 190 in kHz')
    category = models.IntegerField(db_column='Category', choices=CATEGORY_NETWORK, default=19,
                                   help_text='Category UMTS: 35, GSM: 19')
    # wiencodeh = models.CharField(db_column='WiencodeH', max_length=255, blank=True, null=True)
    # wiencodev = models.CharField(db_column='WiencodeV', max_length=255, blank=True, null=True)

    # erlang = models.DecimalField(db_column='Erlang', max_digits=8, decimal_places=3, help_text='Traffic in Erlangs', default=0.000)
    # call_no = models.IntegerField(db_column='Call_no', help_text='Number of calls')
    # delay = models.IntegerField(db_column='Delay', default=0)

    # user = models.CharField(db_column='User', max_length=255, blank=True, null=True)
    # til = models.CharField(db_column='TIL', max_length=255, blank=True, null=True)
    # lineoffset = models.CharField(db_column='LineOffset', max_length=255, blank=True, null=True)
    # precision = models.CharField(db_column='Precision', max_length=255, blank=True, null=True)
    # dateserv = models.CharField(db_column='DateServ', max_length=255, blank=True, null=True)
    # datebegin = models.CharField(db_column='DateBegin', max_length=255, blank=True, null=True)
    # dateend = models.CharField(db_column='DateEnd', max_length=255, blank=True, null=True)
    work_status = models.CharField(
        db_column='Work_status', max_length=255, blank=True, null=True)
    # rpe = models.CharField(db_column='RPE', max_length=255, blank=True, null=True)
    # nfdname = models.CharField(max_length=255, blank=True, null=True)  # This field type is a guess.
    # type_coord_adm = models.CharField(db_column='Type_coord_adm', max_length=255, blank=True, null=True)
    # coord_xadm = models.CharField(db_column='COORD_Xadm', max_length=255, blank=True, null=True)
    # coord_yadm = models.CharField(db_column='COORD_Yadm', max_length=255, blank=True, null=True)
    # coord_zadm = models.CharField(db_column='COORD_Zadm', max_length=255, blank=True, null=True)

    # sectorbegin = models.IntegerField(db_column='SectorBegin', default=0)
    # sectorend = models.IntegerField(db_column='SectorEnd', default=0)
    # distsimul = models.IntegerField(db_column='DistSimul', default=0)
    # modulation = models.IntegerField(db_column='Modulation', default=0)
    # fktb = models.IntegerField(db_column='FKTB', default=0)
    # aperture = models.IntegerField(db_column='Aperture', default=0)
    # radius = models.IntegerField(db_column='Radius', default=0)
    # dynamic = models.IntegerField(db_column='Dynamic', default=0)
    # diameter = models.IntegerField(db_column='Diameter', default=0)
    # xpd = models.IntegerField(db_column='XPD', default=0)
    # rad_step = models.IntegerField(db_column='Rad_Step', default=0)
    # carrier = models.IntegerField(db_column='Carrier', default=0)
    # thr10_3 = models.IntegerField(db_column='THR10_3', default=0)
    # thr10_6 = models.IntegerField(db_column='THR10_6', default=0)
    # noisefloor = models.IntegerField(db_column='NoiseFloor', default=0)
    # activity = models.IntegerField(db_column='Activity', default=0)
    # pilot = models.IntegerField(db_column='Pilot', default=0)
    # paging = models.IntegerField(db_column='Paging', default=0)
    # sync = models.IntegerField(db_column='Sync', default=0)
    bit_rate = models.IntegerField(db_column='Bit_rate', choices=BITRATE_NETWORK, default=232,
                                   help_text='Bitrate in kb/s (UMTS: 42000, GSM: 232)')
    # mchips_s = models.IntegerField(db_column='Mchips_s', default=0)
    # discrep = models.IntegerField(db_column='Discrep', default=0)
    # peak_pow = models.IntegerField(db_column='Peak_Pow', default=0)
    # pulse = models.IntegerField(db_column='Pulse', default=0)
    # rd_noise = models.IntegerField(db_column='Rd_Noise', default=0)
    # det_pd = models.IntegerField(db_column='Det_PD', default=0)

    # channel_d = models.CharField(db_column='Channel_d', max_length=255, blank=True, null=True)
    # plan = models.CharField(db_column='Plan', max_length=255, blank=True, null=True)
    # ics_value = models.CharField(db_column='ICS_VALUE', max_length=255, blank=True, null=True)
    # heff_vi = models.CharField(db_column='HEFF_VI', max_length=255, blank=True, null=True)
    # heff_ge = models.CharField(db_column='HEFF_GE', max_length=255, blank=True, null=True)
    # diag_v = models.CharField(db_column='DIAG_V', max_length=255, blank=True, null=True)
    # icst_status = models.CharField(db_column='ICST_STATUS', max_length=255, blank=True, null=True)
    # polygon = models.CharField(db_column='POLYGON', max_length=255, blank=True, null=True)
    # ant_file = models.CharField(db_column='ANT_FILE', max_length=255, blank=True, null=True)
    # options = models.CharField(db_column='OPTIONS', max_length=255, blank=True, null=True)
    availability = models.IntegerField(db_column='Availability', default=0)
    # stringc = models.CharField(db_column='STRINGC', max_length=255, blank=True, null=True)
    # addloss = models.CharField(db_column='addloss', max_length=255, blank=True, null=True)
    station_id = models.IntegerField(db_column='STATION_ID', default=0, blank=True, null=True,
                                     help_text="Operator's specific BTS or Sector identification")
    # color = models.CharField(db_column='Color', max_length=255, blank=True, null=True)
    # neighbours = models.CharField(db_column='Neighbours', max_length=255, blank=True, null=True)
    taclac = models.IntegerField(
        db_column='TACLAC', default=0, help_text='LAC')
    # rsi = models.CharField(db_column='RSI', max_length=255, blank=True, null=True)
    # mme = models.CharField(db_column='MME', max_length=255, blank=True, null=True)
    # saegw = models.CharField(db_column='SAEGW', max_length=255, blank=True, null=True)
    # pathcfd = models.CharField(db_column='PATHCFD', max_length=255, blank=True, null=True)
    # ci_n0 = models.CharField(db_column='CI_N0', max_length=255, blank=True, null=True)
    # ci_n1 = models.CharField(db_column='CI_N1', max_length=255, blank=True, null=True)
    # rdspi_sid = models.CharField(db_column='RDSPI_SID', max_length=255, blank=True, null=True)
    # lsn_swtpi = models.CharField(db_column='LSN_SWTPI', max_length=255, blank=True, null=True)
    # tiimain = models.CharField(db_column='TIImain', max_length=255, blank=True, null=True)
    # tiisub = models.CharField(db_column='TIIsub', max_length=255, blank=True, null=True)
    fffh_trx = models.IntegerField(db_column='FFFH_TRX', default=0)
    # etsi_class = models.CharField(db_column='ETSI_CLASS', max_length=255, blank=True, null=True)
    # smart = models.CharField(db_column='SMART', max_length=255, blank=True, null=True)
    # arraytx = models.CharField(db_column='ARRAYTX', max_length=255, blank=True, null=True)
    # arrayrx = models.CharField(db_column='ARRAYRX', max_length=255, blank=True, null=True)
    # mu = models.CharField(db_column='MU', max_length=255, blank=True, null=True)
    pdcch = models.IntegerField(db_column='PDCCH', default=0)
    pbch = models.IntegerField(db_column='PBCH', default=0)
    pss = models.IntegerField(db_column='PSS', default=0)
    sss = models.IntegerField(db_column='SSS', default=0)
    powermaxw = models.DecimalField(
        db_column='PowerMaxW', max_digits=7, decimal_places=2, default=0.00)
    # change_date = models.CharField(db_column='CHANGE_DATE', max_length=255, blank=True, null=True)
    # diag_h = models.CharField(db_column='DIAG_H', max_length=255, blank=True, null=True)
    # thr10_8 = models.CharField(db_column='THR10_8', max_length=255, blank=True, null=True)
    # thr10_10 = models.CharField(db_column='THR10_10', max_length=255, blank=True, null=True)
    # string = models.CharField(db_column='STRING', max_length=255, blank=True, null=True)
    # chg_date = models.CharField(db_column='CHG_DATE', max_length=255, blank=True, null=True)
    pncode = models.IntegerField(db_column='PNCODE', blank=True, null=True)
    operator = models.CharField(
        db_column='OPERATOR', db_index=True, max_length=128, default='NA', choices=COMPANIES)
    technology = models.CharField(db_column='TECHNOLOGY', db_index=True, max_length=128, choices=TECHNOLOGY,
                                  default='2G Network')
    field_id = models.AutoField(db_column='_ID', primary_key=True, unique=True)

    class Meta:
        # managed = False
        db_table = 'BaseStations2'
        verbose_name_plural = 'Base Stations'

    @staticmethod
    def coord_to_latlon_decimal(coord):
        """
        :param coord: Coordinate in 4DMS format
        :return latitude in decimal format
        """
        degree, the_rest = str.split(coord, '.')
        while len(the_rest) < 6:
            the_rest = the_rest + "0"
        minutes = float(the_rest[:2])
        seconds = float(the_rest[2:4])
        seconds_decimal = float(the_rest[4:6])
        decimals = (minutes + (seconds + seconds_decimal / 100) / 60) / 60
        return round(float(degree) + decimals, 5)

    @staticmethod
    def frequencies_string(freq_list):
        freqs = ""
        for freq in freq_list:
            if freq is not None:
                freqs = freqs + str(freq) + " "
        return str.rstrip(freqs)

    def latlon_decimal(self):
        return f"{str(self.coord_to_latlon_decimal(self.coord_y))},{str(self.coord_to_latlon_decimal(self.coord_x))}"
        # return f"{self.coord_y},{self.coord_x}"

    def lat_decimal(self):
        return f"{str(self.coord_to_latlon_decimal(self.coord_y))}"

    def lon_decimal(self):
        return f"{str(self.coord_to_latlon_decimal(self.coord_x))}"

    def downlinks(self):
        dcx = [
            self.d_cx1,
            self.d_cx2,
            self.d_cx3,
            self.d_cx4,
            self.d_cx5,
            self.d_cx6,
            self.d_cx7,
            self.d_cx8,
            self.d_cx9,
            self.d_cx10,
            self.d_cx11,
            self.d_cx12,
            self.d_cx13,
            self.d_cx14,
            self.d_cx15,
            self.d_cx16
        ]
        return self.frequencies_string(dcx)

    def uplinks(self):
        ucx = [
            self.u_cx1,
            self.u_cx2,
            self.u_cx3,
            self.u_cx4,
            self.u_cx5,
            self.u_cx6,
            self.u_cx7,
            self.u_cx8,
            self.u_cx9,
            self.u_cx10,
            self.u_cx11,
            self.u_cx12,
            self.u_cx13,
            self.u_cx14,
            self.u_cx15,
            self.u_cx16
        ]
        return self.frequencies_string(ucx)

    @staticmethod
    def adjust(x):
        if len(str(x)) < 1 or x is None:
            return "00"
        elif len(str(x)) == 1:
            return f"0{x}"
        else:
            return str(x)

    def save(self, *args, **kwargs):
        if self.lat_sec is None:
            self.lat_sec = f"00.00"
        if self.lon_sec is None:
            self.lon_sec = f"00.00"
        lat_seconds = str.split(str(self.lat_sec), '.')
        lon_seconds = str.split(str(self.lon_sec), '.')
        if len(lat_seconds) < 2:
            lat_seconds = [str(self.lat_sec), "00"]
        if len(lon_seconds) < 2:
            lon_seconds = [str(self.lon_sec), "00"]
        self.coord_y = f"{self.adjust(self.lat_deg)}.{self.adjust(self.lat_min)}{self.adjust(lat_seconds[0])}{self.adjust(lat_seconds[1])}"
        self.coord_x = f"{self.adjust(self.lon_deg)}.{self.adjust(self.lon_min)}{self.adjust(lon_seconds[0])}{self.adjust(lon_seconds[1])}"
        super(Basestations, self).save(*args, **kwargs)
