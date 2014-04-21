from django.shortcuts import render
from analysis.models import MusicData


def home(request):
    g1 = MusicData.objects.filter(ambitus__lte=12).count()
    g2 = MusicData.objects.filter(ambitus__gte=13, ambitus__lte=24).count()
    g3 = MusicData.objects.filter(ambitus__gte=25).count()

    args = {'g1': g1, 'g2': g2, 'g3': g3}
    return render(request, "index.html", args)
