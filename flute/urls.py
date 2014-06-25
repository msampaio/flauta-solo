from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'analysis.views.home', name='home'),
    url(r'^login/$', 'analysis.views.login_user', name='login_user'),
    url(r'^range/$', 'analysis.views.show_range', name='range'),
    url(r'^intervals/$', 'analysis.views.show_intervals', name='intervals'),
    url(r'^dashboard/$', 'analysis.views.dashboard', name='dashboard'),
    url(r'^admin/', include(admin.site.urls)),
)
