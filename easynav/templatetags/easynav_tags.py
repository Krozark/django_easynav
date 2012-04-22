#import re

from django.template import Library, Node, VariableDoesNotExist, TemplateSyntaxError
from django.utils.translation import ugettext_lazy as _
from easynav.models import ItemMenu, ItemPage
from django.db.models import Q

register = Library()

######################################## GET NAV ########################################
class makeSubUl(Node):
    def __init__(self, parser):
        self.template_parser = parser

    def render(self, context):
        path=context['request'].path

        parent = None
        try:
            parent = ItemMenu.objects.filter(Q(url=path) | Q(url = path[0:-1])).distinct().exclude(slug='main').get()
        except:
            return ""

        if parent.itemmenu_set.count() == 0:
            return ""

        res ='<h2>%s</h2><ul class="submenu">' % parent.name
        for u in parent.itemmenu_set.filter(is_visible=True).order_by('rank'):
            res+= '<li class="subitem"><a href="%s">%s</a></li>' % (u.url,u.name)
        res+='</ul>'
        return res

class makeUl(Node):
    def __init__(self, parser,slug,prof):
        self.template_parser = parser
        self.slug = slug
        self.prof = int(prof)

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

        
@register.tag(name="getnav")
def getnav(parser, token):

    tokens = token.split_contents()
    fnctl = tokens.pop(0)

    def error():
        raise TemplateSyntaxError, _("%(fonction)s accepts the syntax: {%% %(fontion)s for <easynav_item_slug or name> [with lvl = <x>] %%}\nWith x as a positive number (-1 for all [default])\n If <easynav_item_slug> = \"active\", it the sub nav of the current path that will be display" %{'fonction':fnctl,})
    
    if len(tokens) < 2:
        error()

    
    token = tokens.pop(0)
    if token !='for' :
        error()

    slug = tokens.pop(0)
    if slug == '"active"':
        return makeSubUl(parser)
    prof = 0
    if len(tokens) == 4 :
        token = tokens.pop(0)

        if token != "with":
            error()
        token = tokens.pop(0)

        if token != "lvl":
            error()

        token = tokens.pop(0)
        if token != "=":
            error()

        prof = tokens.pop(0)

    try :
        prof = int(tokens.pop(2))
    except:
        pass
    if prof < 0:
        prof = -1
    elif len(tokens) != 0:
        error()

    return makeUl(parser,slug,prof)


############################### GET CONTENT ###############################
#@register.tag(name="showcontent")
#def showblocks(parser, token):
#    return makeContent(parser)
#
#class makeContent(Node):
#    def __init__(self, parser,slug,prof):
#        self.template_parser = parser
#
#    def render(self, context):
#        path=context['request'].path
#
#        item = ItemMenu.objects.filter(url=path)
#        if item.count()>0:
#            item = item[0]
#        else
#            return ""
#
#        item.itempage_set.order_by('rank')

