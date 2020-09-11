# -*- coding: utf-8 -*-

from asset.models import Asset
from asset.models import AssetLog
from asset.models import RFmonSite
from asset.models import RFmonSiteLog

#### CBV ADDITION
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from asset.forms import RFmonSiteLogForm
from asset.forms import AssetLogForm
from django.utils import timezone


class AssetsList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'asset/assets_list.html'
    model = Asset

    def get_queryset(self):
        return Asset.objects.all()


class AssetLogList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'asset/assetlog_list.html'
    model = AssetLog

    def get_queryset(self):
        return AssetLog.objects.all().order_by('-datetime')


class AssetLogDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'asset/assetlog_detail.html'
    model = AssetLog


class CreateAssetLog(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    success_url = reverse_lazy('inventories:assetlog_list')
    template_name = 'asset/assetlog_form_new.html'
    form_class = AssetLogForm
    model = AssetLog

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super(CreateAssetLog, self).form_valid(form)


class AssetLogUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    success_url = reverse_lazy('inventories:assetlog_list')
    template_name = 'asset/assetlog_form_edit.html'
    form_class = AssetLogForm
    model = AssetLog


class AssetLogDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    template_name = 'asset/assetlog_delete.html'
    model = AssetLog
    success_url = reverse_lazy('inventories:assetlog_list')
    
    
class RFmonSiteList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'asset/rfmonsite_list.html'
    model = RFmonSite

    def get_queryset(self):
        return RFmonSite.objects.all()


class RFmonSiteLogListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    # redirect_field_name = 'asset/rfmonsitelog_list.html'
    template_name = 'asset/rfmonsitelog_list.html'
    model = RFmonSiteLog

    def get_queryset(self):
        return RFmonSiteLog.objects.filter(datetime__lte=timezone.now()).order_by('-datetime')


class RFmonSiteLogDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'asset/rfmonsitelog_detail.html'
    model = RFmonSiteLog


class CreateRFmonSiteLog(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    success_url = '/inventory/rfmslog/'
    template_name = 'asset/rfmonsitelog_form_new.html'
    form_class = RFmonSiteLogForm
    model = RFmonSiteLog

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super(CreateRFmonSiteLog, self).form_valid(form)


class RFmonSiteLogUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    template_name = 'asset/rfmonsitelog_form_edit.html'
    success_url = '/inventory/rfmslog/'
    form_class = RFmonSiteLogForm
    model = RFmonSiteLog


class RFmonSiteLogDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    template_name = 'asset/rfmonsitelog_delete.html'
    model = RFmonSiteLog
    success_url = reverse_lazy('inventories:rfmonsitelog_list')
