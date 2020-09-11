# -*- coding: utf-8 -*-
__author__ = "skrilic"
__date__ = "$28.07.2011. 14:00:00$"

from django.contrib import admin

admin.site.disable_action('delete_selected')

from .models import Organization
from .models import TechnicalContact
from .models import LicenceType
from .models import Licensee
from .models import portalUser
from .models import Antenna
from .models import FieldMeasurement
from .models import Transmitter
from .models import MapDefinition
from .models import Towers
from .models import kote
from .models import monitorstanice
from .models import Area


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'person',
                    'phone',
                    'email',
                    'street',
                    'zipcode',
                    'city',
                    'countryCode',
                    'rds_pi',
                    'rds_pihex')

    # list_filter = ['city',]
    class Media:
        js = ('admin/js/collapse.js',)

    search_fields = ['name',
                     'area__name',
                     ]
    # class Media:
    #    js = ('admin/js/collapse.js',)
    ordering = ['name', 'countryCode', 'area__name']


admin.site.register(Organization, OrganizationAdmin)


class TechnicalContactAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'phone',
        'fax',
        'email',
        'additional_info'
    )
    list_filter = ['name', 'phone']
    search_fields = ['name', ]
    ordering = ['name', 'phone']


admin.site.register(TechnicalContact, TechnicalContactAdmin)


class LicenceTypeAdmin(admin.ModelAdmin):
    list_display = (
        'type',
        'licence_class',
        'description'
    )

    list_filter = ['type', ]
    search_fields = ['type', ]
    ordering = ['type', ]


admin.site.register(LicenceType, LicenceTypeAdmin)


class LicenseeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'country',
        'address',
        'city',
        'contact',
        'licence_type',
        # 'licence_issued',
        'licence_valid_to',
        'technician',
        'stream_url',
        'licensee_url',
        'additional_info'
    )

    class Media:
        js = ('admin/js/collapse.js',)

    search_fields = ['organization__name',
                     'organization__area__name',
                     ]

    class Media:
        js = ('admin/js/collapse.js',)

    ordering = ['organization__name', 'organization__countryCode', 'organization__area__name']
    unique_together = ['organization__name', 'licence_type']


admin.site.register(Licensee, LicenseeAdmin)


class portalUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'e_mail', 'phone_number', 'organization', 'description')
    list_filter = ('organization',)
    ordering = ['username', ]
    search_fields = ['username__username', 'organization__naziv', ]


admin.site.register(portalUser, portalUserAdmin)


class AntennaAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'ERP_00', 'ERP_10', 'ERP_20', 'ERP_30', 'ERP_40', 'ERP_50', 'ERP_60', 'ERP_70', 'ERP_80', 'ERP_90',
                    'ERP_100', 'ERP_110', 'ERP_120', 'ERP_130', 'ERP_140', 'ERP_150', 'ERP_160', 'ERP_170', 'ERP_180',
                    'ERP_190',
                    'ERP_200', 'ERP_210', 'ERP_220', 'ERP_230', 'ERP_240', 'ERP_250', 'ERP_260', 'ERP_270', 'ERP_280',
                    'ERP_290',
                    'ERP_300', 'ERP_310', 'ERP_320', 'ERP_330', 'ERP_340', 'ERP_350',
                    # 'vertical_pattern',
                    )
    search_fields = ['name', ]
    fieldsets = (
        ('Name',
         {'fields': ('name',)}),
        ('Horizontal Antenna Pattern',
         {'fields': ('ERP_00', 'ERP_10', 'ERP_20', 'ERP_30', 'ERP_40', 'ERP_50', 'ERP_60', 'ERP_70', 'ERP_80', 'ERP_90',
                     'ERP_100', 'ERP_110', 'ERP_120', 'ERP_130', 'ERP_140', 'ERP_150', 'ERP_160', 'ERP_170', 'ERP_180',
                     'ERP_190',
                     'ERP_200', 'ERP_210', 'ERP_220', 'ERP_230', 'ERP_240', 'ERP_250', 'ERP_260', 'ERP_270', 'ERP_280',
                     'ERP_290',
                     'ERP_300', 'ERP_310', 'ERP_320', 'ERP_330', 'ERP_340', 'ERP_350')}),
        # ('Vertical Antenna Pattern',
        #       {'fields':('vertical_pattern',)})
    )


admin.site.register(Antenna, AntennaAdmin)


class FieldMeasurementAdmin(admin.ModelAdmin):
    exclude = ('author',)
    list_display = ('title', 'date', 'operator', 'type', 'location', 'description', 'status', 'report')
    list_filter = [
        'type',
        'status'
    ]
    search_fields = [
        'description',
        'location',
        'title'
    ]

    # class Media:
    #    js = ('admin/js/collapse.js',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(FieldMeasurementAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.author.id:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        has_class_permission = super(FieldMeasurementAdmin, self).has_delete_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.author.id:
            return False
        else:
            return True


admin.site.register(FieldMeasurement, FieldMeasurementAdmin)


class TransmitterAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'licence_type',
        'callsign',
        'frequency',
        'organization',
        'antenna_height',
        'antenna',
        'antenna_direction',
        'antenna_tilt',
        'tower',
        'enabled',
        'license_issuing_date',
        'license_expiration_date',
        'licence_state'
    )
    list_filter = [
        'licence_type',
        #    'organization__name',
    ]

    class Media:
        js = ('admin/js/collapse.js',)

    search_fields = ['name',
                     'organization__name',
                     'frequency',
                     'callsign',
                     'licence_type',
                     ]
    fieldsets = (
        ('Name',
         {'fields': ('organization',
                     'licence_type',
                     'callsign',
                     'signature',
                     'name',
                     'licence_state',
                     'enabled',
                     'frequency',
                     # 'erp',
                     'transmitter_power',
                     'antenna_height',
                     'antenna',
                     'antenna_direction',
                     'antenna_tilt',
                     'tower')}),
    )


admin.site.register(Transmitter, TransmitterAdmin)


class MapDefinitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'map_lat', 'map_lon', 'map_zoom', 'description')
    list_filter = ('name',)
    search_fields = ['name', ]


admin.site.register(MapDefinition, MapDefinitionAdmin)


class TowersAdmin(admin.ModelAdmin):
    list_display = ('oznaka', 'visina', 'latitude', 'longitude', 'extrainfo')
    prepopulated_fields = {'towerid': ('oznaka',)}
    unique_together = (('latitude', 'longitude'),)
    search_fields = ['oznaka', 'kota__naziv', 'extrainfo']
    raw_id_fields = ('kota',)


admin.site.register(Towers, TowersAdmin)


class koteAdmin(admin.ModelAdmin):
    list_display = ('naziv', 'area_name', 'area_zipcode', 'extrainfo')
    search_fields = ['naziv', 'extrainfo']

    def area_name(self, obj):
        return "%s" % obj.area.name

    area_name.short_description = 'Area name'

    def area_zipcode(self, obj):
        return "%s" % obj.area.zipcode

    area_zipcode.short_description = 'Area zipcode'


admin.site.register(kote, koteAdmin)


class monitorstaniceAdmin(admin.ModelAdmin):
    list_display = (
        'naziv', 'longitude', 'latitude', 'ip_address', 'area', 'aktivna', 'portalvisibility', 'additional_info')
    list_filter = ('naziv', 'aktivna', 'additional_info')


admin.site.register(monitorstanice, monitorstaniceAdmin)


class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'zipcode',)


admin.site.register(Area, AreaAdmin)

