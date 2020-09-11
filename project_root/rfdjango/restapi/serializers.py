#!/usr/bin/env python
from rfdjango.models import Transmitter
from rfdjango.models import Organization
from rfdjango.models import monitorstanice

from rest_framework import serializers


class TransmitterSerializer(serializers.ModelSerializer):
    #organization = serializers.StringRelatedField(read_only=True)
    service_type = serializers.ReadOnlyField(source='service_type.name.abbreviation')
    service_subtype = serializers.ReadOnlyField(source='service_type.subtype.name')
    organization = serializers.ReadOnlyField(source='organization.name')
    lat = serializers.FloatField(source='tower.latitude')
    lng = serializers.FloatField(source='tower.longitude')
    class Meta:
        model = Transmitter
        fields = (
            'id',
            'name',
            'organization',
            'service_type',
            'service_subtype',
            'transmitter_power',
            'erp',
            'frequency',
            'lat',
            'lng'
        )


class OrganizationSerializer(serializers.ModelSerializer):
    area = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Organization
        fields = (
            'id',
            'name',
            'area',
            'rds_pihex'
        )


class monitorstationSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.StringRelatedField(source='naziv')
    lat = serializers.FloatField(source='latitude')
    lng = serializers.FloatField(source='longitude')
    class Meta:
        #model = monitorstation
        model = monitorstanice
        fields = (
            'id',
            'name',
            'lat',
            'lng'
        )
