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
    url(r'^reports/$', 'analysis.views.show_reports', name='reports'),
    url(r'^cluster/all$', 'analysis.views.show_cluster_all', name='cluster_all'),
    url(r'^cluster/duration_ambitus$', 'analysis.views.show_cluster_duration_ambitus', name='cluster_duration_ambitus'),
    url(r'^cluster/intervals_frequency$', 'analysis.views.show_cluster_intervals_frequency', name='cluster_intervals_frequency'),
    url(r'^cluster/durations_frequency$', 'analysis.views.show_cluster_durations_frequency', name='cluster_durations_frequency'),
    url(r'^cluster/contour$', 'analysis.views.show_cluster_contour', name='cluster_contour'),
    url(r'^compositions', 'analysis.views.list_compositions', name='list_compositions'),
    url(r'^composition/(\w+)/$', 'analysis.views.list_composition', name='list_composition'),
    url(r'^composition/(\w+)/intervals/$', 'analysis.views.composition_interval', name='composition_interval'),
    url(r'^composition/(\w+)/durations/$', 'analysis.views.composition_durations', name='composition_durations'),
    url(r'^composition/(\w+)/contour/$', 'analysis.views.composition_contour', name='composition_contour'),
    url(r'^composition/(\w+)/cluster/$', 'analysis.views.composition_cluster', name='composition_cluster'),
    url(r'^dashboard/$', 'analysis.views.dashboard', name='dashboard'),
    url(r'^stats/$', 'analysis.views.stats', name='stats'),
    url(r'^admin/', include(admin.site.urls)),
)
