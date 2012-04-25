# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

from django.template.context import RequestContext# Context
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from easynav.models import *

class GenericView(TemplateView):
    template_name = "easynav/genericPage.html"

    def get_context_data(self, **kwargs):
        context = super(GenericView, self).get_context_data(**kwargs)

        slug =  kwargs['params'].get('slug',False)
        if not slug:
            slug =  kwargs.get('slug',False)
        if slug:
            content = ItemPage.objects.filter(parent__slug=slug).order_by('rank')
            print content
            context['content_blocks'] = content
        return context
