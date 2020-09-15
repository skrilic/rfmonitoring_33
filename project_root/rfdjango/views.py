# -*- coding: utf-8 -*-
"""RFdjango views"""
import datetime
import math

from django.http import HttpRequest
from django.shortcuts import render

from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core import serializers
from django.urls import reverse_lazy

from .models import (
    Transmitter,
    Towers,
    monitorstanice,
    MapDefinition,
    FieldMeasurement,
    Licensee
)

from .forms import TransmitterForm
from .forms import FieldMeasurementForm


def transmitters2json(service):
    """Prepare data about transmitters to be sawn on the geographic map"""
    tower_list = Towers.objects.values(
        'towerid', 'latitude', 'longitude').all()
    transmitter_list = Transmitter.objects.values(
        'name',
        'frequency',
        'callsign',
        'antenna_height',
        'transmitter_power',
        'licence_type',
        'organization__name',
        'tower__towerid',
        'tower__longitude',
        'tower__latitude'
    ).filter(
        licence_type=service,
        enabled=True,
        organization__countryCode__twoletters='BA'
    )

    towers = []
    for tower in tower_list:
        tower_dict = {}
        tower_dict['popup'] = ""
        for tx in transmitter_list:
            if tx['tower__towerid'] == tower['towerid']:
                tower_dict['popup'] += "* <b>{}</b> [{}] {}MHz<br />".format(str(tx['name']), str(tx['callsign']),
                                                                             float(tx['frequency']))
        tower_dict['latitude'] = float(tower['latitude'])
        tower_dict['longitude'] = float(tower['longitude'])
        if tower_dict['popup'] != "":
            towers.append(tower_dict)
    return towers


def show_txmap(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'rfdjango/txmap.html',
        context={
            'user': request.user,
            'title': 'Home Page',
            'monitoringStations': serializers.serialize(
                'json',
                monitorstanice.objects.only(
                    'naziv', 'latitude', 'longitude').filter(aktivna=True),
                fields=(
                    'naziv',
                    'latitude',
                    'longitude'
                )
            ),
            # FM Radio: name, frequency, longitude, latitude
            'bcfmTxs': transmitters2json('BC'),
            # Analog. TV: name, frequency, longitude, latitude
            'atvTxs': transmitters2json('BT'),
            # Amateur Repetitor: name, frequency, longitude, latitude
            'amateurTxs': transmitters2json('AT'),
            'mapDefinition': serializers.serialize(
                'json',
                MapDefinition.objects.only(
                    'map_lat', 'map_lon', 'map_zoom').filter(name='home_page'),
                fields=('map_lat', 'map_lon', 'map_zoom')
            ),
            'year': datetime.datetime.now().year,
        }
    )


def show_detailmap(request, name, lat, lon):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'rfdjango/detailmap.html',
        context={
            'user': request.user,
            'title': name,
            'name': name,
            'latitude': lat,
            'longitude': lon
        }
    )


def distance(gps1, gps2):
    """Calculate distance between two gps points."""
    # I've got this code from http://www.androidsnippets.com/calculate-distance-between-two-gps-coordinates
    # Distance=ACOS(SIN(lat1/180*PI)*SIN(lat2/180*PI)+ COS(lat1/180*PI)*COS(lat2/180*PI)*COS(lon1/180*PI-lon2/180*PI))*180*60/PI)
    lat1, lon1 = float(gps1['latitude']) * math.pi / \
        180, float(gps1['longitude']) * math.pi / 180
    lat2, lon2 = float(gps2['latitude']) * math.pi / \
        180, float(gps2['longitude']) * math.pi / 180
    t1 = math.cos(lat1) * math.cos(lon1) * math.cos(lat2) * math.cos(lon2)
    t2 = math.cos(lat1) * math.sin(lon1) * math.cos(lat2) * math.sin(lon2)
    t3 = math.sin(lat1) * math.sin(lat2)
    return "%.3g" % (6366000 * math.acos(t1 + t2 + t3) / 1000)


def bearing(gps1, gps2):
    """Calculate bearing between two gps points"""
    # This code has derived from here http://mathforum.org/library/drmath/view/55417.html
    lat1, lon1 = float(gps1['latitude']) * math.pi / \
        180, float(gps1['longitude']) * math.pi / 180
    lat2, lon2 = float(gps2['latitude']) * math.pi / \
        180, float(gps2['longitude']) * math.pi / 180
    y = math.sin(lon2 - lon1) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * \
        math.cos(lat2) * math.cos(lon2 - lon1)
    if y > 0:
        if x > 0:
            bearing_tmp = math.atan(y / x)
        elif x < 0:
            bearing_tmp = math.pi - math.atan(-y / x)
        else:
            # x = 0
            bearing_tmp = math.pi / 2
    elif y < 0:
        if x > 0:
            bearing_tmp = -math.atan(-y / x)
        elif x < 0:
            bearing_tmp = math.atan(y / x) - math.pi
        else:
            bearing_tmp = 3 * math.pi
    else:
        # y = 0
        if x > 0:
            bearing_tmp = 0
        elif x < 0:
            bearing_tmp = math.pi
        else:
            bearing_tmp = 0  # "same point"
    azimuth = bearing_tmp * 180 / math.pi
    return "%.3g" % azimuth


class LicenseeList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'rfdjango/licensee_list.html'
    model = Licensee

    def get_queryset(self):
        return Licensee.objects.all().order_by('organization__name', 'organization__area__name')


class TransmitterCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    success_url = '/rfdjango/transmitter/'
    template_name = 'rfdjango/transmitter_form_create_update.html'
    form_class = TransmitterForm
    model = Transmitter

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super(TransmitterCreate, self).form_valid(form)


class TransmitterDetail(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Transmitter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TransmitterUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('rfdjango:transmitter_list_all')
    template_name = 'rfdjango/transmitter_form_create_update.html'
    # fields = transmitter_fields
    form_class = TransmitterForm
    model = Transmitter

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super(TransmitterUpdate, self).form_valid(form)


class TransmitterList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'rfdjango/transmitter_list.html'
    model = Transmitter
    paginate_by = 500

    def get_queryset(self):
        try:
            service = self.kwargs['service']
            return Transmitter.objects.filter(
                organization__countryCode__twoletters="BA",
                licence_type=service,
                licence_state=True
            )
        except:
            return Transmitter.objects.all().order_by('-name')


class FieldMeasurementList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'rfdjango/fieldmeasurement_list.html'
    model = FieldMeasurement

    def get_queryset(self):
        return FieldMeasurement.objects.all().order_by('-date')[:500]


class FieldMeasurementDetail(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'rfdjango/fieldmeasurement_detail.html'
    model = FieldMeasurement


class FieldMeasurementCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    success_url = '/rfdjango/fieldmeas/'
    template_name = 'rfdjango/fieldmeasurement_form_create_update.html'
    form_class = FieldMeasurementForm
    model = FieldMeasurement

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super(FieldMeasurementCreate, self).form_valid(form)


class FieldMeasurementUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    template_name = 'rfdjango/fieldmeasurement_form_create_update.html'
    success_url = '/rfdjango/fieldmeas/'
    form_class = FieldMeasurementForm
    model = FieldMeasurement


class FieldMeasurementDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    template_name = 'rfdjango/fieldmeasurement_delete.html'
    model = FieldMeasurement
    success_url = reverse_lazy('rfdjango:fieldmeasurement_list')
