import datetime
from django.http import (
    HttpResponseRedirect,
    HttpResponse,
    HttpRequest
    )
from django.shortcuts import render, redirect
from django.core import serializers

from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages

from .forms import (
    LoginForm,
    UserForm,
    ProfileForm
)

from rfdjango.models import (
        monitorstanice,
        MapDefinition,
    )


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'index.html',
        context=
        {
            'user': request.user,
            'title': 'Home Page',
            'monitoringStations': serializers.serialize(
                'json',
                monitorstanice.objects.only('naziv', 'latitude', 'longitude').all(),
                fields=('naziv', 'latitude', 'longitude')
            ),
            'mapDefinition': serializers.serialize(
                'json',
                MapDefinition.objects.only('map_lat', 'map_lon', 'map_zoom').filter(name='home_page'),
                fields=('map_lat', 'map_lon', 'map_zoom')
            ),
            'year': datetime.datetime.now().year,
        }
    )


@csrf_protect
def loginreq(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        this_is_the_login_form = request.POST.get('this_is_the_login_form')
        # next = request.GET['next']
        user = authenticate(username=username, password=password)
        if this_is_the_login_form:
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirect to a success page.
                    # return HttpResponse('\"%s\" - You have just logged-in! and next is => %s' % (username, next))
                    # return http.HttpResponseRedirect('%s' % next)
                    return HttpResponseRedirect('/')
                else:
                    # Return a 'disabled account' error message
                    return HttpResponse('User exists but it is administratively inactivated.')
            else:
                # Return an 'invalid login' error message.
                return HttpResponse('Access denied!')
        else:
            return HttpResponse('Go away!')
    form = LoginForm()
    return render(
        request,
        'rfdjango/login.html',
        {
            'Title': 'Log-in Form',
            'message': 'Welcome!',
            'form': form
        }
    )


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('update-profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def logoutreq(request):
    logout(request)
    return HttpResponseRedirect("/")


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'rfdjango/contact.html',
        context=
        {
            'title': 'Contact',
            'error_message': 'Your contact page.',
            'year': datetime.datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'rfdjango/about.html',
        context=
        {
            'title': 'About',
            'message': 'Your application description page.',
            'year': datetime.datetime.now().year,
        }
    )

