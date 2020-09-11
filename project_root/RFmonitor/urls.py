# -*- coding: utf-8 -*-

from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

from django.contrib.auth import views as auth_views

from django.conf.urls import include, url
from django.urls import path

from .views import *


admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),

    # #### RFdjango
    path('', include('rfdjango.urls')),

    # #### RF-DB (Mobile base stations)
    path('bts/', include('base_stations.urls'), name='base_stations'),

    # #### INVENTORY
    path('inventory/', include('asset.urls')),

    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logoutreq, name='logout'),
    path('login/', loginreq, name='login'),
    path('profile/', update_profile, name='update-profile'),

    url(r'^accounts/password/change/$',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change_form.html'
        ),
        name='password_change'),
    url(r'^accounts/password/change/done/$',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html'
        ),
        name='password_change_done'),

    url(r'^$', home),
    url(r'^contact$', contact),
    url(r'^about', about),
    url(r'^media\/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': False}),
]

urlpatterns += staticfiles_urlpatterns()
