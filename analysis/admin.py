from django.contrib import admin
from analysis.models import Composition, Composer, CompositionType, MusicData, MusicXMLScore


admin.site.register(Composition)
admin.site.register(Composer)
admin.site.register(CompositionType)
admin.site.register(MusicData)
admin.site.register(MusicXMLScore)
