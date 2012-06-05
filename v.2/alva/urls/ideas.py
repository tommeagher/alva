from django.conf.urls.defaults import *

from alva.models import Idea

idea_info_dict = {
    'queryset': Idea.live.all(),
    'date_field': 'think_date',
}

urlpatterns = patterns('django.views.generic.date_based',
    (r'^$', 'archive_index', idea_info_dict, 'alva_idea_archive_index'),
    (r'^(?P<year>\d{4})/$', 'archive_year', idea_info_dict, 'alva_idea_archive_year'),
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/$', 'archive_month', idea_info_dict, 'alva_idea_archive_month'),
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', 'archive_day', idea_info_dict, 'alva_idea_archive_day'),
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'object_detail', idea_info_dict, 'alva_idea_detail'),
)