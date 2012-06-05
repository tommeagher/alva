from django.conf.urls.defaults import *

from alva.models import Category

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', {'queryset': Category.objects.all() }, 'alva_category_list'),
    (r'^(?P<slug>[-\w]+)/$', 'alva.views.category_detail', {}, 'alva_category_detail'),
)