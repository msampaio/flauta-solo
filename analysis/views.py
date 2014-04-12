from django.shortcuts import render


def home(request):
    args = {}
    return render(request, "index.html", args)
