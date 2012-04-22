# -*- coding: utf-8 -*-

from django.contrib import admin
from easynav.forms import *
from easynav.models import *

#################### INLINES ################################
class SubMenuItemInline(admin.TabularInline):
    model = ItemMenu
    extra = 1
    form = ItemMenuForm
    prepopulated_fields = {'slug':('name',)}


class ItemPageInline(admin.TabularInline):
    model = ItemPage
    extra = 1
    form = ItemPageForm


############################################################
class ItemMenuAdmin(admin.ModelAdmin):
    list_display = ('name','slug','rank','view','url','parent','is_visible','auto_create_page','__IsAccessible__')
    list_filter = ('is_visible','auto_create_page')
    prepopulated_fields = {'slug':('name',)}
    form = ItemMenuForm
    inlines = [ItemPageInline,SubMenuItemInline]

    def queryset(self, request):
        return ItemMenu.objects.exclude(pk=1)
admin.site.register(ItemMenu, ItemMenuAdmin)

class ItemPageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','parent','rank','content_type','slug','is_visible',)
    list_filter = ('is_visible','parent')
    form = ItemPageForm
admin.site.register(ItemPage, ItemPageAdmin)
