import json
from django.shortcuts import render, redirect
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpRequest
)
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
)
from django.urls import reverse
from django.db.models import Q
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Basestations, Profile
from .forms import BasestationForm

basestation_fields = [
        'call_sign',
        'address',
        'netid',
        # 'coord_y',
        # 'coord_x',
        'lat_deg',
        'lat_min',
        'lat_sec',
        'lon_deg',
        'lon_min',
        'lon_sec',
        'nominal_power',
        'gain',
        'h_antenna',
        'threshold',
        # 'thresholdrx',
        'bandwidth',
        'bandwidthrx',
        'azimuth',
        'tilt',
        'tilte',
        'antenna_nameh',
        'downlink_cx',
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
        'uplink_cx',
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
        'u_cx16',
        'spacing',
        'category',
        # 'wiencodeh',
        # 'wiencodev',
        # 'erlang',
        # 'call_no',
        # 'delay',
        # 'user',
        # 'til',
        # 'lineoffset',
        # 'precision',
        # 'dateserv',
        # 'datebegin',
        # 'dateend',
        'work_status',
        # 'rpe',
        # 'nfdname',
        # 'type_coord_adm',
        # 'coord_xadm',
        # 'coord_yadm',
        # 'coord_zadm',
        # 'sectorbegin',
        # 'sectorend',
        # 'distsimul',
        # 'modulation',
        # 'fktb',
        # 'aperture',
        # 'radius',
        # 'dynamic',
        # 'diameter',
        # 'xpd',
        # 'rad_step',
        # 'carrier',
        # 'thr10_3',
        # 'thr10_6',
        # 'noisefloor',
        # 'activity',
        # 'pilot',
        # 'paging',
        # 'sync',
        'bit_rate',
        # 'mchips_s',
        # 'discrep',
        # 'peak_pow',
        # 'pulse',
        # 'rd_noise',
        # 'det_pd',
        # 'channel_d',
        # 'plan',
        # 'ics_value',
        # 'heff_vi',
        # 'heff_ge',
        # 'diag_v',
        # 'icst_status',
        # 'polygon',
        # 'ant_fil',
        # 'options',
        'availability',
        # 'stringc',
        # 'addloss',
        'station_id',
        # 'color',
        # 'neighbours',
        'taclac',
        # 'rsi',
        # 'mme',
        # 'saegw',
        # 'pathcfd',
        # 'ci_n0',
        # 'ci_n1',
        # 'rdspi_sid',
        # 'lsn_swtpi',
        # 'tiimain',
        # 'tiisub',
        # 'fffh_trx',
        # 'etsi_class',
        # 'smart',
        # 'arraytx',
        # 'arrayrx',
        # 'mu',
        # 'pdcch',
        # 'pbch',
        # 'pss',
        # 'sss',
        'powermaxw',
        # 'change_date',
        # 'diag_h',
        # 'thr10_8',
        # 'thr10_10',
        # 'string',
        # 'chg_date',
        'pncode',
        # 'operator',
        'technology',
    ]

def deg_min(coords):
    """
    Convert any 4DMS pair to deg.min form.
    That way we are getting BTSs inside of a square of cca 1.8x1.8km
    """
    coord_list = str.split(coords, ' ')
    new_coords = ""
    for coord in coord_list:
        deg_min_list = str.split(coord, '.')
        if len(deg_min_list[1]) == 0:
            deg_min_list[1] = "00"
        elif len(deg_min_list[1]) == 1:
            deg_min_list[1] = f"0{deg_min_list[1]}"
        else:
            deg_min_list[1] = f"{deg_min_list[1][:2]}"
        new_coords = new_coords + f" {deg_min_list[0]}.{deg_min_list[1]}"
    return str.strip(new_coords)


def search_terms_list(terms):
    terms = str.strip(terms)
    term_list = terms.split(' ')
    return term_list


def or_query(terms):
    term_list = search_terms_list(terms)
    q = Q(address__icontains=term_list[0]) | Q(operator__icontains=term_list[0]) | Q(
        call_sign__icontains=term_list[0])
    for term in term_list[1:]:
        q.add(Q(address__icontains=term) | Q(operator__icontains=term)
              | Q(call_sign__icontains=term), q.connector)
    return q


@login_required(login_url='/login/')
def redirect_search(request):
    organization = Profile.objects.get(user=request.user).organization
    terms = request.GET.get('terms', None)
    if terms is None:
        terms = "*ALL*"
    return redirect('base_stations:address-search', terms, organization)


@login_required(login_url='/login/')
def address_search(request, terms, organization):
    bss = Basestations.objects.values(
        'address', 'operator', 'coord_y', 'coord_x').distinct()

    if organization != "ADMIN":
        bss = Basestations.objects.filter(operator=organization).values(
            'address', 'operator', 'coord_y', 'coord_x').distinct()

    if len(terms) < 3:
        return HttpResponse("Your search string is to short. Must be at least 3 chars long!!!")

    if terms != "*ALL*":
        q = or_query(terms)
        bss = bss.filter(q)
    template_name = 'base_stations/address_list_with_search.html'

    page = request.GET.get('page', 1)

    paginator = Paginator(bss, 15)
    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    context = {'title': 'Addresses of sites',
               'objects_list': qs,
               'terms': terms,
               'last_page': paginator.num_pages}
    return render(request, template_name, context)


@login_required(login_url='/login/')
def bts_search(request):
    """
    Generic Search: GET should contain the following:
    terms - the search keywords separated by spaces
    """
    assert isinstance(request, HttpRequest)
    organization = Profile.objects.get(user=request.user).organization
    show_map = request.GET.get('show_map')
    try:
        terms = request.GET.get('terms')
        if len(terms) < 3:
            return HttpResponse("Your search string is to short. Must be at least 3 chars long!!!")
        q = or_query(terms)
    except:
        # Search by coordinates
        coords = request.GET.get('coords')
        if len(coords) < 11:
            return HttpResponse("Your search string is to short. Must be degs and minutes at least included!!!")
        term_list = search_terms_list(deg_min(coords))

        if organization != "ADMIN":
            bss = Basestations.objects.filter(operator=organization).all()
        else:
            bss = Basestations.objects.all()

        q = Q(coord_y__icontains=term_list[0]) & Q(
            coord_x__icontains=term_list[1])
    else:
        if organization != "ADMIN":
            bss = Basestations.objects.filter(operator=organization).all()
        else:
            bss = Basestations.objects.all()

    bss = bss.filter(q)

    template_name = 'base_stations/bts_list.html'
    context = {
        'title': 'BTS found list',
        'site': "#",
        'objects_list': bss
    }

    if int(show_map):
        bts_json_list = []
        # i = 0
        for bts in bss:
            # i += 1
            bts_json_list.append(
                {
                    # "model": "base_stations.basestations",
                    # "pk": i,
                    "fields": {
                        "latitude": bts.lat_decimal(),
                        "longitude": bts.lon_decimal(),
                        "popup": f"<strong>{bts.operator}:{bts.technology}</strong><br>CALL SIGN: {bts.call_sign}<br><ul><li>DL(MHz): {bts.downlinks()}</li><li>UL(MHz): {bts.uplinks()}</li></ul>"
                    }
                }
            )
        template_name = 'base_stations/bts_map.html'
        context = {
            'user': request.user,
            'title': 'BTS Map',
            'baseStations': bts_json_list,
            'mapDefinition': json.dumps(
                [
                    {
                    "fields": {
                        "map_lat": bss[0].lat_decimal(),
                        "map_lon": bss[0].lon_decimal(),
                        "map_zoom": "16"
                    }
                }
                ]
            ),
        }

    return render(request, template_name, context)


class BasestationCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Basestations
    fields = basestation_fields
    success_url = reverse_lazy('base_stations:redirect-search')


class BasestationUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Basestations
    fields = basestation_fields
    success_url = reverse_lazy('base_stations:redirect-search')
    template_name_suffix = '_update_form'

