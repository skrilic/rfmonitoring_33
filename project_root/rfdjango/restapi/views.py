from rest_framework import viewsets

from rfdjango.models import Organization
from rfdjango.models import Transmitter
from rfdjango.models import monitorstanice
from rfdjango.restapi.serializers import OrganizationSerializer
from rfdjango.restapi.serializers import TransmitterSerializer
from rfdjango.restapi.serializers import monitorstationSerializer


class TransmitterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transmitter.objects.all()
    serializer_class = TransmitterSerializer


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class monitorstationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = monitorstanice.objects.all()
    serializer_class = monitorstationSerializer
