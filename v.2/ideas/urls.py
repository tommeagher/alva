from django.conf.urls import patterns, url, include
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ideas.views.home', name='home'),
    # url(r'^ideas/', include('ideas.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
#    (r'^weblog/tags/', include('coltrane.urls.tags')),
    (r'^comments/', include('django.contrib.comments.urls')),
#    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', { 'feed_dict': feeds }),
    (r'^$', include('alva.urls.ideas')),
    (r'^categories/', include('alva.urls.categories')),
    (r'', include('django.contrib.flatpages.urls')),
    
)
