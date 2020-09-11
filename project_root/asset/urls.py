"""Asset app"""
from django.conf.urls import url
from .views import (
    AssetsList,
    AssetLogList,
    AssetLogDetailView,
    CreateAssetLog,
    AssetLogUpdateView,
    AssetLogDeleteView,
    RFmonSiteList,
    RFmonSiteLogListView,
    RFmonSiteLogDetailView,
    CreateRFmonSiteLog,
    RFmonSiteLogUpdateView,
    RFmonSiteLogDeleteView
)

app_name = 'inventories'

urlpatterns = [
    url(r'^$', AssetsList.as_view(), name='asset_list'),
    url(r'^assetslog/$', AssetLogList.as_view(), name='assetlog_list'),
    url(r'^assetslog/(?P<pk>\d+)$',
        AssetLogDetailView.as_view(), name='assetlog_detail'),
    url(r'^assetlog/new/$', CreateAssetLog.as_view(), name='assetlog_new'),
    url(r'^assetslog/(?P<pk>\d+)/edit/$',
        AssetLogUpdateView.as_view(), name='assetlog_edit'),
    url(r'^assetslog/(?P<pk>\d+)/remove/$',
        AssetLogDeleteView.as_view(), name='assetlog_remove'),

    url(r'^rfmonsite/$', RFmonSiteList.as_view(), name='rfmonsite_list'),
    url(r'^rfmslog/$', RFmonSiteLogListView.as_view(), name='rfmonsitelog_list'),
    url(r'^rfmslog/(?P<pk>\d+)$', RFmonSiteLogDetailView.as_view(),
        name='rfmonsitelog_detail'),
    url(r'^rfmslog/new/$', CreateRFmonSiteLog.as_view(), name='rfmonsitelog_new'),
    url(r'^rfmslog/(?P<pk>\d+)/edit/$',
        RFmonSiteLogUpdateView.as_view(), name='rfmonsitelog_edit'),
    url(r'^rfmslog/(?P<pk>\d+)/remove/$',
        RFmonSiteLogDeleteView.as_view(), name='rfmonsitelog_remove'),
]
