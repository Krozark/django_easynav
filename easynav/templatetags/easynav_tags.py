#import re

from django.template import Library, Node, VariableDoesNotExist, TemplateSyntaxError
from django.utils.translation import ugettext_lazy as _
from easynav.models import ItemMenu, ItemPage
from django.db.models import Q

register = Library()

######################################## GET NAV ########################################
    ############ SUBNAV ######################
class makeSubUl(Node):
    def __init__(self,params):
        self.params = params

    def render(self, context):
        path=context['request'].path

        parent = None
        try:
            parent = ItemMenu.objects.filter(Q(url=path) | Q(url = path[0:-1])).distinct().exclude(slug='main').get()
        except:
            return ""

        if parent.itemmenu_set.count() == 0:
            return ""

        res ='<ul class="submenu">'
        for u in parent.itemmenu_set.filter(is_visible=True).order_by('rank'):
            res+= '<li class="subitem"><a href="%s">%s</a></li>' % (u.url,u.name)
        res+='</ul>'
        return res

    ############### Main NAV ##########################
class makeUl(Node):
    def __init__(self,slug,params):
        self.active_nb = params['active_nb']
        self.slug = slug
        self.prof = params['lvl']

    def render(self, context):
        path=context['request'].path
        obj = ItemMenu.objects.filter(Q(url = path) | Q(url = path[0:-1])).distinct().exclude(slug="main").get()
        activs = [obj,]
        
        while True:
            obj = obj.parent
            if obj.slug != "main" :
                activs.append(obj)
            else:
                break


        def makelevel(res,lvl,parent):
            res +='<ul class="menu menu-lvl-%d">\n' % lvl
            for u in parent.itemmenu_set.filter(is_visible=True).order_by('rank'):
                status="inactive"
                if u in activs:
                    status="active"

                res+= '<li class="item item-lvl-%d %s">\n<a href="%s">%s</a>\n' % (lvl,status,u.url,u.name)
                if lvl < self.prof or self.prof == -1:
                    res = makelevel(res,lvl +1 ,u)
                res+='</li>\n'
            res+='</ul>\n'
            return res

        res=""
        try:
            u = ItemMenu.objects.get(slug=self.slug)
            res = makelevel(res,0,u)
        except ItemMenu.DoesNotExist:
            try:
                u = ItemMenu.objects.get(name=self.slug)
                makelevel(res,0,u)
            except ItemMenu.DoesNotExist:
                pass
        return res

    ############### PARSER ############################# 
@register.tag(name="getnav")
def getnav(parser, token):

    tokens = token.split_contents()
    fnctl = tokens.pop(0)

    def error():
        raise TemplateSyntaxError, _("%(fonction)s accepts the syntax: {%% %(fonction)s for <easynav_item_slug or name> [with [lvl=<x>] [parent_active=<y>] ] %%}\nWith x and y as a positive number ( default = -1 )\n If <easynav_item_slug> = \"active\", it the sub nav of the current path that will be display" %{'fonction':fnctl,})
    
    if len(tokens) < 2:
        error()

    
    token = tokens.pop(0)
    if token !='for' :
        error()

    slug = tokens.pop(0)
    params = {
        'lvl': -1,
        'active_nb' : -1,
    }

    if len(tokens) > 1 :
        token = tokens.pop(0)
        if token != "with":
            error()

    while len(token) > 1:
        token = tokens.pop(0).split("=")
        
        if token[0] == "lvl":
            try:
                params['lvl'] = int(token[1])
            except:
                error()
        elif token[0] == "parent_active":
            try:
                params['parent_active'] = int(token[1])
            except:
                error()
        else:
            error()

    if params['lvl'] < 0:
        params['lvl'] = -1

    if slug == '"active"':
        return makeSubUl(params)

    return makeUl(slug,params)

