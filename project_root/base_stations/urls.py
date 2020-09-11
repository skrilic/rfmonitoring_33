from django.urls import path
from .views import (
    address_search,
    bts_search,
    redirect_search,
    BasestationCreate,
    BasestationUpdate
    )

app_name = 'base_stations'

urlpatterns = [
        path('redirect_search/', redirect_search, name='redirect-search'),
        path('address/<str:terms>/<str:organization>', address_search, name='address-search'),
        path('address/search/', bts_search, name='bts-search'),
        path('add/', BasestationCreate.as_view(), name='create-basestation'),
        path('edit/<int:pk>', BasestationUpdate.as_view(), name='update-basestation')
    ]
