from django import forms
from django.core.urlresolvers import reverse, NoReverseMatch
from django.core.validators import URLValidator
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from easynav import urls as easynav_urls
from easynav.utils import MakePattern

from easynav.models import *


class ItemMenuForm(forms.ModelForm):

    class Meta:
        model = ItemMenu

    def clean_view(self):
        link = self.cleaned_data['view'] or ''
        # It could be a fully-qualified URL -- try that first b/c reverse()
        # chokes on "http://"

        if any([link.startswith(s) for s in ('http://', 'https://')]):
            URLValidator()(link)
            self.url = link
            return self.cleaned_data['view']

        auto = self.cleaned_data['auto_create_page']

        if not auto:
            if link:
                if link[0] == "/": #a defined URL
                    from django.test.client import Client
                    c = Client()
                    try:
                        resp = c.get(link)
                        if resp.status_code == 404:
                            raise forms.ValidationError(_(u'%s is not a local URL (does not exist)' % link))
                        self.url = link
                        return link
                    except:
                        raise forms.ValidationError(_(u'%s is not a local URL (not a valid URL)' % link))

                elif link[0] != '^' : # Not a regex or site-root-relative absolute path
                    try: # named URL or view
                        self.url = reverse(link)
                        return link
                    except NoReverseMatch:
                        raise forms.ValidationError(_('No view find to display the page, and auto_create_page is disable.\nPlease create a view named %s, or enable auto_create_page.' % link))
            raise forms.ValidationError(_('Please supply a valid URL, URL name, or regular expression.'))

        else: #auto
            if link:
                self.url = link
                return link

        self.url = self.cleaned_data['parent'].url +"/"+self.cleaned_data['slug'] 
        return self.cleaned_data['slug']

    def clean(self):
        super(ItemMenuForm, self).clean()

        if 'is_visible' in self.cleaned_data and \
          self.cleaned_data['is_visible'] and \
          'view' in self.cleaned_data and \
          self.cleaned_data['view'].startswith('^'):
            raise forms.ValidationError(_('Menu items with regular expression URLs must be disabled.'))
        return self.cleaned_data

    def save(self, commit=True):
        item = super(ItemMenuForm, self).save(commit=False)
        item.url = self.url
        
        #try to register the new url
        if hasattr(easynav_urls,'urlpatterns'):
            urls = getattr(easynav_urls,'urlpatterns')
            urls += MakePattern(item)

        if commit:
            item.save() 
            pass
        return item



class InlineMenuItemForm(forms.ModelForm):
    #queryset=ItemMenu.objects.all()

    class Meta:
        model = ItemMenu
        fields = ('parent', 'name', 'slug', 'rank', 'is_visible')

class ItemPageForm(forms.ModelForm):
    
    class Meta:
        model = ItemPage

    def clean_parent(self):
        parent = self.cleaned_data['parent']
        if not parent.auto_create_page:
            raise forms.ValidationError(_("generic content are not allow to parent that don't have 'auto_create_page' activated"))
        return parent

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if slug != "":
            return slugify(slug)

        parent = self.cleaned_data['parent']
        rank = self.cleaned_data['rank']

        return slugify("%s-%d" % (parent.slug,rank))
        
