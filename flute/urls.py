from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'analysis.views.home', name='home'),
    url(r'^login/$', 'analysis.views.login_user', name='login_user'),
    url(r'^ambitus/$', 'analysis.views.show_ambitus', name='ambitus'),
    url(r'^intervals/$', 'analysis.views.show_intervals', name='intervals'),
    url(r'^durations/$', 'analysis.views.show_durations', name='durations'),
    url(r'^contour/$', 'analysis.views.show_contour', name='contour'),
    url(r'^pure_data/$', 'analysis.views.show_pure_data', name='pure_data'),
    url(r'^cluster/$', 'analysis.views.show_cluster', name='cluster'),
    url(r'^dashboard/$', 'analysis.views.dashboard', name='dashboard'),
    url(r'^stats/$', 'analysis.views.stats', name='stats'),
    url(r'^admin/', include(admin.site.urls)),
)
