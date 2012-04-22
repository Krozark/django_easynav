# -*- coding: utf-8 -*-
from easynav.views import GenericView
from django.conf.urls.defaults import patterns,url

def MakePattern(menuItem):
    ur = menuItem.url

    if ur == "/":
        ur=""
    else:
        if ur[0] == "/" and len(ur)>1:
            ur = ur[1:]
        if len(ur)>1 and ur[-1] != "/":
            ur+="/"

    return patterns('',url(
                r'^%s$' % ur,
                GenericView.as_view(),
                kwargs={"slug": menuItem.slug,},
                name="easynav-%s" % menuItem.slug
                ))
