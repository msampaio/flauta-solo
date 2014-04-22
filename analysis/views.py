import json
from django.core.files.uploadedfile import InMemoryUploadedFile, UploadedFile
from django.http import HttpRequest, HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from analysis.models import MusicData


def home(request):
    g1 = MusicData.objects.filter(ambitus__lte=12).count()
    g2 = MusicData.objects.filter(ambitus__gte=13, ambitus__lte=24).count()
    g3 = MusicData.objects.filter(ambitus__gte=25).count()

    args = {'g1': g1, 'g2': g2, 'g3': g3}
    return render(request, "index.html", args)


def import_musixml_file(filename):
    data = filename.read()


@csrf_exempt
def import_music_data(request):
    if request.method == 'POST':
        if request.FILES:
            uploaded_file = request.FILES['files[]']
            import_musixml_file(uploaded_file)

            data = {'name': uploaded_file.name}
            response_data = json.dumps(data)
            return HttpResponse(response_data, content_type='application/json')
        else:
            return HttpResponseBadRequest('Must have files attached!')
    else:
        return render(request, "upload.html", {})
