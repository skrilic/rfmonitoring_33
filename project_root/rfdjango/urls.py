"""RFdjango app"""
from .restapi import views as restapi_views
from django.conf.urls import url
from django.urls import path
from rest_framework import routers
from .views import *

app_name = 'rfdjango'

# REST-API

router = routers.SimpleRouter()
router.register(r'rest_transmitters', restapi_views.TransmitterViewSet)
router.register(r'rest_organizations', restapi_views.OrganizationViewSet)
router.register(r'rest_monitoringsystems', restapi_views.monitorstationViewSet)
urlpatterns = [
    url(r'^show_txmap/$', show_txmap),
    # url(r'^transmitters/(?P<name>[-\w]+)/(?P<lat>\d+\.\d{6})/(?P<lon>\d+\.\d{6})/$', show_detailmap),

    # # Class-based View (C.B.V.)
    url(r'^transmitters/(?P<service>[A-Z]{2,3})/$',
        TransmitterList.as_view(), name='transmitter_list'),
    url(r'^transmitters/$', TransmitterList.as_view(), name='transmitter_list_all'),
    path('transmitter/<int:pk>/', TransmitterDetail.as_view(), name='transmitter_detail'),
    path('transmitter/add/', TransmitterCreate.as_view(),
         name='create-transmitter'),
    path('transmitter/edit/<int:pk>', TransmitterUpdate.as_view(),
         name='update-transmitter'),

    # url(r'^transmitters/fm/$', MeasurementsList.as_view(), name='measurements_list'),
    # url(r'^transmitters/rds/$', RDSDecodedList.as_view(), name='rdsdecoded_list'),
    url(r'^licensees/$', LicenseeList.as_view(), name='licensee_list'),

    url(r'^rfdjango/fieldmeas/(?P<pk>\d+)/$',
        FieldMeasurementDetail.as_view(), name='fieldmeasurement_detail'),
    url(r'^rfdjango/fieldmeas/$', FieldMeasurementList.as_view(),
        name='fieldmeasurement_list'),
    url(r'^rfdjango/fieldmeas/new/$',
        FieldMeasurementCreate.as_view(), name='fieldmeasurement_new'),
    url(r'^rfdjango/fieldmeas/(?P<pk>\d+)/edit/$',
        FieldMeasurementUpdate.as_view(), name='fieldmeasurement_edit'),
    url(r'^rfdjango/fieldmeas/(?P<pk>\d+)/delete/$',
        FieldMeasurementDelete.as_view(), name='fieldmeasurement_delete'),

    # MEASUREMENT ADDITIONAL URLs
    # url(r'^transmitters/fm/plot/(?P<transmitter>.+)/(?P<monitorst>.+)/$', plotreport, name='plotreport'),

    #########
    # MY ADDITIONAL patterns
    #########
    # REST FRAMEWORK
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^docs/', include('rest_framework_docs.urls')),
]

urlpatterns += router.urls
