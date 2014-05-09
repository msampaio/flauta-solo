from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from analysis.models import MusicData, Composition


def home(request):
    return render(request, "index.html")


def login_user(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, "login_user.html", {'error': True})
        else:
            return render(request, "login_user.html", {'error': True})

    else:
        return render(request, 'login_user.html')


def dashboard(request):
    music_data_count = MusicData.objects.count()
    composition_count = Composition.objects.count()
    args = {'music_data_count': music_data_count,
            'composition_count': composition_count}
    return render(request, "dashboard.html", args)


def show_range(request):
    g1 = MusicData.objects.filter(ambitus__lte=12).count()
    g2 = MusicData.objects.filter(ambitus__gte=13, ambitus__lte=24).count()
    g3 = MusicData.objects.filter(ambitus__gte=25).count()

    args = {'g1': g1, 'g2': g2, 'g3': g3}

    return render(request, 'show_range.html', args)
