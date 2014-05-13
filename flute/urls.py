from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'analysis.views.home', name='home'),
    url(r'^login/$', 'analysis.views.login_user', name='login_user'),
    url(r'^d3/$', 'analysis.views.d3', name='d3'),
    url(r'^ajax/range-data/$', 'analysis.views.range_data', name='range_data'),
    url(r'^range/$', 'analysis.views.show_range', name='range'),
    url(r'^dashboard/$', 'analysis.views.dashboard', name='dashboard'),
    url(r'^admin/', include(admin.site.urls)),
)
