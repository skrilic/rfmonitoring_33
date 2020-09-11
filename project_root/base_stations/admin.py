from django.contrib import admin
from .models import MapDefinition, Basestations, Profile


class ProfileAdmin(admin.ModelAdmin):
    pass


class MapDefinitionAdmin(admin.ModelAdmin):
    pass


class BasestationsAdmin(admin.ModelAdmin):
    fieldsets = (
       (None, {
            'fields': (
                'call_sign',
                'address',
                'netid',
                'taclac',
                # 'latlon_decimal',
                # 'lat_decimal',
                # 'lon_decimal',
                # 'type_coord',
                'coord_y',
                'coord_x',
                #
                # 'downlinks',
                # 'uplinks',

                'nominal_power',
                'gain',
                'operator',
                'technology'
            )
        }),
       ('Latitude (DMS)', {
            'fields':  ('lat_deg', 'lat_min', 'lat_sec'),
       }),
       ('Longitude (DMS)', {
           'fields': ('lon_deg', 'lon_min', 'lon_sec'),
       }),
       ('Downlink channels', {
           'fields': ('downlink_cx',
                ('d_cx1', 'd_cx2', 'd_cx3', 'd_cx4', 'd_cx5', 'd_cx6', 'd_cx7', 'd_cx8',
                 'd_cx9', 'd_cx10', 'd_cx11', 'd_cx12', 'd_cx13', 'd_cx14', 'd_cx15', 'd_cx16'))
       }),
       ('Uplink channels', {
           'fields': ('uplink_cx',
                ('u_cx1', 'u_cx2', 'u_cx3', 'u_cx4', 'u_cx5', 'u_cx6', 'u_cx7', 'u_cx8',
                 'u_cx9', 'u_cx10', 'u_cx11', 'u_cx12', 'u_cx13', 'u_cx14', 'u_cx15', 'u_cx16'))
       })
    )

    list_display = (
        'call_sign',
        'address',
        'netid',
        'taclac',
        # 'latlon_decimal',
        # 'lat_decimal',
        # 'lon_decimal',
        # 'type_coord',
        'coord_x',
        # 'lon_deg',
        # 'lon_min',
        # 'lon_sec',
        #
        'coord_y',
        # 'lat_deg',
        # 'lat_min',
        # 'lat_sec',
        #
        'downlinks',
        'uplinks',
        # 'd_cx1',
        # 'u_cx1',
        'nominal_power',
        'gain',
        'operator',
        'technology'
    )
    ordering = ['-field_id']
    search_fields = [
        'address',
        'call_sign',
        'taclac',
        'd_cx1',
        'd_cx2',
        'd_cx3',
        'd_cx4',
        'd_cx5',
        'd_cx6',
        'd_cx7',
        'd_cx8',
        'd_cx9',
        'd_cx10',
        'd_cx11',
        'd_cx12',
        'd_cx13',
        'd_cx14',
        'd_cx15',
        'd_cx16',
        'u_cx1',
        'u_cx2',
        'u_cx3',
        'u_cx4',
        'u_cx5',
        'u_cx6',
        'u_cx7',
        'u_cx8',
        'u_cx9',
        'u_cx10',
        'u_cx11',
        'u_cx12',
        'u_cx13',
        'u_cx14',
        'u_cx15',
        'u_cx16'
    ]
    list_filter = ['operator', 'technology']
    list_per_page = 50


admin.site.register(Profile, ProfileAdmin)
admin.site.register(MapDefinition, MapDefinitionAdmin)
admin.site.register(Basestations, BasestationsAdmin)

base_stations_site = admin.AdminSite('Base\ Station')
base_stations_site.register(Basestations, BasestationsAdmin)
