from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from analysis.models import MusicData, Composition
from analysis.importmusic import import_musicxml_files


def home(request):
    g1 = MusicData.objects.filter(ambitus__lte=12).count()
    g2 = MusicData.objects.filter(ambitus__gte=13, ambitus__lte=24).count()
    g3 = MusicData.objects.filter(ambitus__gte=25).count()

    args = {'g1': g1, 'g2': g2, 'g3': g3}
    return render(request, "index.html", args)


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


def import_music_data(request):
    if request.POST:
        should_replace_data = request.POST.get('replace-data')
        # FIXME: Now we don't do much
        #import_musicxml_files.delay(should_replace_data)

        return render(request, "dashboard.html", {'importing': True})
    else:
        return HttpResponseRedirect(reverse("import_music_data"))