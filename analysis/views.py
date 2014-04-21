from django.shortcuts import render
from analysis.models import MusicData


def home(request):
    musicdatas = MusicData.objects.all()
    args = {'musicdatas': musicdatas}
    return render(request, "index.html", args)
