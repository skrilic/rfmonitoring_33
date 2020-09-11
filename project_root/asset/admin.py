# -*- coding: utf-8 -*-
__author__ = "skrilic"
__date__ = "$11.02.2011. 23:32:20$"

from django.contrib import admin

from asset.models import Office
# from asset.models import Person
from asset.models import UsedbyPerson
from asset.models import Category
from asset.models import Procurer
from asset.models import Manufacturer
# from asset.models import Event
from asset.models import AssetEvent
from asset.models import RFmonSiteEvent
from asset.models import Contract
from asset.models import Asset
from asset.models import AssetLog
from asset.models import Periodically
from asset.models import System
from asset.models import RFmonSite
from asset.models import RFmonSiteLog


#
# -------------Inlines----------------
# ForeignKey
class AssetInline(admin.TabularInline):
    model = Asset


class SystemInline(admin.TabularInline):
    model = System


# Many to Many
# class AssetincludedInline(admin.TabularInline):
#    model = System.asset.through
# -------------------------------------


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'postal', 'city')
    list_display = ('name',)
    search_field = ('name', 'city')
    # actions = [csv_export_selected]


class UsedbyPersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'show_image', 'office', 'phone', 'email')
    inlines = [
        AssetInline,
    ]
    ordering = ('last_name', 'first_name')
    list_filter = ('office',)
    search_fields = ('last_name', 'first_name')
    # actions = [export_as_csv_action("Export selected Persons as CSV file",\
    #     fields=['first_name','last_name','office','phone','email'],header=False),]
    list_per_page = 12


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    ordering = ('name',)
    search_fields = ('name', 'description')
    list_per_page = 12


class ProcurerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'postal', 'city', 'country')
    # readonly_fields = ()
    list_filter = ('city', 'country')
    ordering = ('name', '-country')
    list_per_page = 12

    class Media:
        js = ('admin/js/collapse.js',)


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'web')
    ordering = ('name',)
    list_per_page = 12


class AssetLogAdmin(admin.ModelAdmin):
    list_display = (
        'asset_barcode',
        'asset_description',
        'logevent',
        'asset_location',
        'details',
        'document',
        'datetime',
        'enddatetime',
        'expiration'
    )
    list_filter = ('logevent',)
    search_fields = ('asset__barcode', 'asset__prodcode', 'asset__description', 'details')
    ordering = ('-datetime', '-asset__barcode')
    list_per_page = 12

    def asset_location(self, obj):
        return obj.asset.location.name

    def asset_barcode(self, obj):
        return obj.asset.barcode

    def asset_description(self, obj):
        return obj.asset.description


class ContractAdmin(admin.ModelAdmin):
    list_display = ('name', 'contractor', 'description', 'dateofcontract', 'costofcontract', 'currency', 'bookvalue')
    list_filter = ('contractor__name',)
    search_fields = ('name', 'contractor__name', 'description',)
    ordering = ('-dateofcontract', 'name', 'contractor__name',)
    # actions = [export_as_csv_action("Export selected Contracts as CSV file",\
    #     fields=['name','contractor','description','dateofcontract','costofcontract','bookvalue'], header=False),]
    list_per_page = 12

    class Media:
        js = ('admin/js/collapse.js',)


class AssetAdmin(admin.ModelAdmin):
    list_display = ('barcode',
                    'prodcode',
                    'description',
                    'serialno',
                    'license',
                    'manufacturer',
                    'partof',
                    'location',
                    'microloc',
                    'usedby',
                    'contract',
                    'annotation',
                    'checked',
                    'calibrated',
                    'proper',
                    'procurementdate',
                    'depreciationdate',
                    'purchaseprice',
                    'currency',
                    'bookprice',
                    'category',
                    'procurer',
                    )

    class Media:
        js = ('admin/js/collapse.js',)

    list_filter = ('category', 'contract__name', 'partof__dongle', 'location', 'checked', 'calibrated', 'proper')
    search_fields = ('barcode', 'prodcode', 'description',
                     'serialno', 'location__name', 'location__city',
                     'annotation', 'license', 'microloc',
                     'usedby__first_name', 'usedby__last_name', 'usedby__office__name',
                     'contract__description', 'manufacturer__name', 'procurer__name')
    ordering = ('barcode', 'serialno', '-checked')
    list_per_page = 12


class PeriodicallyAdmin(admin.ModelAdmin):
    list_display = ('asset', 'type', 'lastcheck', 'duedate')
    list_filter = ('type',)
    search_fields = ('asset__barcode', 'asset__prodcode', 'asset__description')
    # readonly_fields = ('logevent',)
    ordering = ('-lastcheck', 'asset__barcode')
    list_per_page = 12


class SystemAdmin(admin.ModelAdmin):
    list_display = ('dongle', 'description', 'show_image', 'inuse', 'person', 'location', 'microloc')
    inlines = [
        AssetInline,
    ]
    list_filter = ('location', 'inuse')
    search_fields = ('dongle', 'description', 'microloc', \
                     'person__first_name', 'person__last_name')
    # readonly_fields = ('logevent',)
    ordering = ('-dongle',)
    list_per_page = 12

    class Media:
        js = ('admin/js/collapse.js',)


class RFmonSiteAdmin(admin.ModelAdmin):
    list_display = ('office_name', 'type', 'document')
    list_filter = ('type',)
    search_fields = ('office__name', 'office__city',)
    # readonly_fields = ('logevent',)
    ordering = ('office__city', 'office__name')
    list_per_page = 12


class RFmonSiteLogAdmin(admin.ModelAdmin):
    # exclude = ('author',)
    list_display = (
        'author',
        'rfmonsite',
        'logevent',
        'details',
        # 'show_attachment',
        'report',
        'datetime',
        'enddatetime',
        'expiration'
    )
    list_filter = ('rfmonsite', 'logevent')
    search_fields = ('rfmonsite__office__name', 'rfmonsite__office__city', 'details')
    ordering = ('-datetime', '-rfmonsite__office__name')
    list_per_page = 12

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(RFmonSiteLogAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.author.id:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        has_class_permission = super(RFmonSiteLogAdmin, self).has_delete_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.author.id:
            return False
        else:
            return True


class AssetEventAdmin(admin.ModelAdmin):
    list_display = ('type', 'description')


class RFmonSiteEventAdmin(admin.ModelAdmin):
    list_display = ('type', 'description')


admin.site.register(Office, OfficeAdmin)
# admin.site.register(Person, PersonAdmin)
admin.site.register(UsedbyPerson, UsedbyPersonAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Procurer, ProcurerAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
# admin.site.register(Event, EventAdmin)
# admin.site.register(Contract, ContractAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetLog, AssetLogAdmin)
admin.site.register(AssetEvent, AssetEventAdmin)
admin.site.register(Periodically, PeriodicallyAdmin)
# admin.site.register(System, SystemAdmin)
admin.site.register(RFmonSite, RFmonSiteAdmin)
admin.site.register(RFmonSiteLog, RFmonSiteLogAdmin)
admin.site.register(RFmonSiteEvent, RFmonSiteEventAdmin)
