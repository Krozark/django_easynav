from django.db import models
from django.utils.translation import ugettext_lazy as _

ORDER_CHOICES = 20

class ItemMenu(models.Model):
    name = models.CharField(_('Item'),max_length=255)
    rank = models.PositiveIntegerField(_('Rank'),
            default=0,
            choices=[(x, x) for x in range(0, ORDER_CHOICES)],
            help_text = _("The rank of the item in the display nav."))

    slug = models.SlugField(_('Slug'),unique=True,max_length=50)
    parent = models.ForeignKey('self',null=False,blank=False,default=1)

    auto_create_page = models.BooleanField(_('Auto create page'),default=True,
            help_text=_("Register the new url and create new page tha you can edite in the admin"))
    view = models.CharField(_('View'),max_length=255
            ,help_text=_("The view of the page you want to link to, as a python path or the shortened URL name.\nLeave blank to auto create the url by concatenate parent url an slug."),blank=True,null=True)

    is_visible = models.BooleanField(_('Is Visible'),default=True)
    
    #the calculated url
    url = models.CharField(_('Url'),editable=False,max_length=255)

    class Meta:
        ordering = ('parent__pk','rank')
        verbose_name = _("Menu")


    def __IsAccessible__(self):
        if self.is_visible and self.parent != None:
            return self.parent.__IsAccessible__()
        return self.is_visible

    def get_absolute_url(self):
        return self.url

    def __unicode__(self):
        return u'%s' % self.name



#The choices type of the ItemPage
CHOICES = (
    "gblocks.Title",
    "gblocks.Text",
    "gblocks.Image",
    "gblocks.ImageAndLink",
    "gblocks.TitleAndFile",
    "gblocks.TitleTextAndFile",
    "gblocks.TitleAndText",
    "gblocks.TitleTextAndImage",
        )


class ItemPage(models.Model):
    parent = models.ForeignKey(ItemMenu,null=False,blank=False,default=1,limit_choices_to = {'pk__in':ItemMenu.objects.filter(auto_create_page=True).exclude(pk=1)})

    rank = models.PositiveIntegerField(_('Rank'),default=0,
            choices=[(x, x) for x in range(0, ORDER_CHOICES)],
            help_text = _("The rank of the item in the display nav."))

    content_type = models.CharField(_('Model Type'),max_length=255,
            choices =[(x,x.split('.')[1]) for x in CHOICES],
            help_text = _("Content Type of this item"))

    slug = models.SlugField(_('Slug'),unique=True,max_length=50,blank=True,
        help_text= _("If empty, this slug will be generate using the parent slug en rank"))
    
    is_visible = models.BooleanField(_('Is Visible'),default=True)

    class Meta:
        ordering = ('parent__pk',)
        verbose_name = _("Page content")

    def get_absolute_url(self):
        return self.parent.url

    def __unicode__(self):
        return u'%s #%d %s' % (self.parent.name,self.rank,self.content_type)

    
