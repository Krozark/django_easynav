# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import patterns#, include, url
from easynav.views import GenericView
from easynav.models import ItemMenu
from easynav.utils import MakePattern

urlpatterns = patterns('',)

for u in ItemMenu.objects.filter(auto_create_page = True).order_by('parent__pk','rank').all():
    urlpatterns += MakePattern(u)
